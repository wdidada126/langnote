/*
 * mini_shell.c —— Shell Lab 骨架（L15 / CSAPP Ch.8）
 * 前台/后台作业、Ctrl-C/Ctrl-Z 语义、SIGCHLD 收割竞态的正确姿势。
 * 仅 POSIX 平台有完整语义；Windows 下退化为"顺序执行"并给出说明。
 */
#ifndef _WIN32

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <errno.h>

#define MAXLINE 1024
#define MAXARGS 64

static volatile sig_atomic_t child_done = 0;   /* L15: 唯一安全跨界的类型 */

static void sigchld_handler(int sig)
{
    (void)sig;
    /* 信号可能合并 → 一次收割所有已终止子进程（Shell Lab 头号坑） */
    while (waitpid(-1, NULL, WNOHANG) > 0)
        ;
    child_done = 1;
}

static void sigint_handler(int sig)  { (void)sig; printf("\n[shell] 前台进程收到 SIGINT，shell 不受影响\n"); }
static void sigtstp_handler(int sig) { (void)sig; printf("\n[shell] 收到 SIGTSTP（骨架略过作业表）\n"); }

struct job {
    pid_t pid;
    char  cmd[MAXLINE];
    int   fg;                       /* 1=前台 0=后台 */
};

static struct job jobs[MAXARGS];
static int next_slot = 0;

static void reap_finished(void)
{
    int i;
    for (i = 0; i < MAXARGS; i++) {
        if (jobs[i].pid > 0) {
            int status;
            pid_t r = waitpid(jobs[i].pid, &status, WNOHANG);
            if (r == jobs[i].pid) {
                printf("[shell] job %d (%s) 结束, status=0x%x\n",
                       i, jobs[i].cmd, status);
                jobs[i].pid = 0;
            }
        }
    }
}

static int parse_line(char *line, char **argv)
{
    int argc = 0;
    char *tok = strtok(line, " \t\n");
    while (tok && argc < MAXARGS - 1) {
        argv[argc++] = tok;
        tok = strtok(NULL, " \t\n");
    }
    argv[argc] = NULL;
    return argc;
}

int main(void)
{
    struct sigaction sa;
    char cmdline[MAXLINE];
    char jobname[MAXLINE];
    char *argv[MAXARGS];

    memset(&sa, 0, sizeof sa);
    sa.sa_handler = sigchld_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART;                 /* 别让 read/fgets 频繁 EINTR */
    sigaction(SIGCHLD, &sa, NULL);

    signal(SIGINT, sigint_handler);           /* Ctrl-C 默认杀 shell → 必须处理 */
    signal(SIGTSTP, sigtstp_handler);

    printf("mini_shell 骨架启动 (POSIX)。输入 exit 退出，命令尾加 & 转后台\n");
    for (;;) {
        reap_finished();
        printf("15-213> ");
        fflush(stdout);
        if (!fgets(cmdline, sizeof cmdline, stdin))
            break;
        if (cmdline[0] == '\n')
            continue;

        strncpy(jobname, cmdline, MAXLINE - 1);   /* strtok 会就地改写 cmdline */
        jobname[MAXLINE - 1] = '\0';
        int argc = parse_line(cmdline, argv);
        if (argc == 0) continue;

        if (strcmp(argv[0], "exit") == 0) break;
        if (strcmp(argv[0], "cd") == 0 && argv[1]) {
            if (chdir(argv[1]) != 0) perror("cd");
            continue;
        }

        int bg = 0;
        if (argc >= 1 && argv[argc - 1][0] == '&' && argv[argc - 1][1] == '\0') {
            bg = 1; argv[--argc] = NULL;
        }

        pid_t pid = fork();                   /* L14 */
        if (pid < 0) { perror("fork"); continue; }
        if (pid == 0) {                       /* child */
            signal(SIGINT, SIG_DFL);          /* 把默认行为还给子进程 */
            signal(SIGTSTP, SIG_DFL);
            signal(SIGCHLD, SIG_DFL);
            setpgid(0, 0);                    /* 独立进程组：Ctrl-C 只打前台组 */
            execvp(argv[0], argv);            /* L14 */
            perror(argv[0]);
            exit(1);
        }
        int slot = next_slot++ % MAXARGS;
        jobs[slot].pid = pid;
        jobs[slot].fg = !bg;
        strncpy(jobs[slot].cmd, jobname, MAXLINE - 1);
        jobs[slot].cmd[MAXLINE - 1] = '\0';

        if (!bg) {
            /* 前台：阻塞式等待（骨架版。生产级用 sigsuspend+标志位，见 L15） */
            int status;
            while (waitpid(pid, &status, 0) < 0)
                if (errno != EINTR) break;
        } else {
            printf("[%d] %s & (后台)\n", (int)pid, argv[0]);
        }
    }
    return 0;
}

#else /* _WIN32 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    printf("mini_shell 骨架（Windows 简化版：仅顺序执行，无作业控制）\n");
    printf("进程创建用 CreateProcess / system；信号语义请转 POSIX 平台体验 L15\n");
    char line[512];
    for (;;) {
        printf("15-213> "); fflush(stdout);
        if (!fgets(line, sizeof line, stdin)) break;
        line[strcspn(line, "\n")] = '\0';
        if (strcmp(line, "exit") == 0) break;
        if (line[0]) {
            int rc = system(line);            /* 阻塞式，等价 cmd.exe 行为 */
            if (rc != 0) printf("(exit code %d)\n", rc);
        }
    }
    return 0;
}

#endif
