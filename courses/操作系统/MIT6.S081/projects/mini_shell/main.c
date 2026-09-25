/* main.c — 迷你 shell：fork/exec/管道/重定向（6.1810 lab-shell 的可移植复刻）
 * POSIX：fork + dup2 + execvp + waitpid；Windows：CreateProcess + 匿名管道/文件句柄。
 * 支持：内建 cd/exit/pwd，`cmd < in > out | cmd2 | cmd3`（每行 ≤4 段管道）。 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/wait.h>
#endif

#define MAXCMD 4
#define MAXARG 16

typedef struct { char *argv[MAXARG]; int argc; } Cmd;

/* 就地分词；"|" 分段，"< f"/"> f" 记录重定向；返回段数或 -1 */
static int splitline(char *line, Cmd *cmds, char *rin, char *rout)
{
    char *tok, *save = 0;
    int n = 0, i;
    rin[0] = rout[0] = 0;
    cmds[0].argc = 0;
#ifdef _WIN32
#define NEXTTOK(sp) strtok(sp, " \t\r\n")
#else
#define NEXTTOK(sp) strtok_r(sp, " \t\r\n", &save)
#endif
    for (tok = NEXTTOK(line); tok; tok = NEXTTOK(0)) {
        if (!strcmp(tok, "|")) {
            if (++n >= MAXCMD) return -1;
            cmds[n].argc = 0;
            continue;
        }
        if (!strcmp(tok, "<") || !strcmp(tok, ">")) {
            char *file = NEXTTOK(0), op = tok[0];
            if (!file) return -1;
            strcpy(op == '<' ? rin : rout, file);
            continue;
        }
        i = cmds[n].argc;
        if (i >= MAXARG - 1) return -1;
        cmds[n].argv[i] = tok;
        cmds[n].argv[i + 1] = 0;
        cmds[n].argc = i + 1;
    }
    if (cmds[0].argc == 0) return 0;
    return n + 1;
}

#ifndef _WIN32
static void cloexec(int fd) { if (fd >= 0) fcntl(fd, F_SETFD, FD_CLOEXEC); }

static void spawn(Cmd *c, int fdin, int fdout, int *pid)
{
    int p = fork();
    if (p == 0) {
        if (fdin >= 0) { dup2(fdin, 0); close(fdin); }
        if (fdout >= 0) { dup2(fdout, 1); close(fdout); }
        execvp(c->argv[0], c->argv);
        fprintf(stderr, "exec %s failed\n", c->argv[0]);
        _exit(127);
    }
    *pid = p;
}

static int run_pipeline(Cmd *cmds, int n, const char *rin, const char *rout)
{
    int infd = -1, outfd = -1, pids[MAXCMD], i, status = 0, from_pipe = -1;
    if (*rin && (infd = open(rin, O_RDONLY)) < 0) { perror(rin); return -1; }
    if (*rout && (outfd = open(rout, O_WRONLY | O_CREAT | O_TRUNC, 0644)) < 0) {
        perror(rout);
        if (infd >= 0) close(infd);
        return -1;
    }
    cloexec(infd); cloexec(outfd);        /* 中间段进程不应继承文件重定向 fd */
    for (i = 0; i < n; i++) {
        int pin[2] = { -1, -1 };
        if (i + 1 < n && pipe(pin) < 0) { perror("pipe"); status = -1; break; }
        if (i + 1 < n) { cloexec(pin[0]); cloexec(pin[1]); } /* 两端经 dup2 传递，勿漏进孙进程 */
        spawn(&cmds[i], infd, (i + 1 < n) ? pin[1] : outfd, &pids[i]);
        if (i + 1 < n) {
            close(pin[1]);               /* 父进程不再持有写端 */
            if (from_pipe >= 0) close(from_pipe); /* 上段读端已移交子进程 */
            from_pipe = infd = pin[0];
        }
    }
    for (i = 0; i < n; i++) {
        int st;
        if (pids[i] <= 0) continue;
        while (waitpid(pids[i], &st, 0) < 0) ;
        status = WEXITSTATUS(st);
    }
    if (infd >= 0 && infd != outfd) close(infd);
    if (outfd >= 0) close(outfd);
    return status;
}
#else /* _WIN32 */
static void build_cmdline(Cmd *c, char *out, size_t cap)
{
    int j;
    size_t used = 0;
    out[0] = 0;
    for (j = 0; j < c->argc; j++) {
        int q = strchr(c->argv[j], ' ') != 0;
        const char *pat = q ? "\"%s%s\"" : "%s%s";
        int need = (int)strlen(c->argv[j]) + 4;
        if (used + (size_t)need >= cap) break;
        used += (size_t)sprintf(out + used, pat, j ? " " : "", c->argv[j]);
    }
}

static int run_pipeline(Cmd *cmds, int n, const char *rin, const char *rout)
{
    SECURITY_ATTRIBUTES sa;
    STARTUPINFOA si;
    PROCESS_INFORMATION pi[MAXCMD];
    HANDLE hIn = 0, hOut = 0, curIn = 0, prevRead = 0;
    int i, status = 0;
    char cmdline[512];
    sa.nLength = sizeof sa; sa.bInheritHandle = TRUE; sa.lpSecurityDescriptor = 0;
    memset(pi, 0, sizeof pi);
    if (*rin && (hIn = CreateFileA(rin, GENERIC_READ, FILE_SHARE_READ, &sa,
                                   OPEN_EXISTING, 0, 0)) == INVALID_HANDLE_VALUE) {
        printf("open %s failed\n", rin); return -1;
    }
    if (*rout && (hOut = CreateFileA(rout, GENERIC_WRITE, 0, &sa,
                                     CREATE_ALWAYS, 0, 0)) == INVALID_HANDLE_VALUE) {
        printf("create %s failed\n", rout);
        if (hIn) CloseHandle(hIn);
        return -1;
    }
    curIn = hIn;
    for (i = 0; i < n; i++) {
        HANDLE wr = hOut, rd = 0;
        if (i + 1 < n) {
            HANDLE pipeR, pipeW;
            if (!CreatePipe(&pipeR, &pipeW, &sa, 0)) { status = -1; break; }
            SetHandleInformation(pipeR, HANDLE_FLAG_INHERIT, 0); /* 只有下一段继承读端 */
            wr = pipeW;
            rd = pipeR;
        }
        memset(&si, 0, sizeof si);
        si.cb = sizeof si;
        si.dwFlags = STARTF_USESTDHANDLES;
        si.hStdInput = curIn ? curIn : GetStdHandle(STD_INPUT_HANDLE);
        si.hStdOutput = wr ? wr : GetStdHandle(STD_OUTPUT_HANDLE);
        si.hStdError = GetStdHandle(STD_ERROR_HANDLE);
        build_cmdline(&cmds[i], cmdline, sizeof cmdline);
        if (!CreateProcessA(0, cmdline, 0, 0, TRUE, 0, 0, 0, &si, &pi[i])) {
            printf("spawn %s failed (err %lu)\n", cmds[i].argv[0], GetLastError());
            status = -1;
            if (wr && wr != hOut) CloseHandle(wr);
            if (rd) CloseHandle(rd);
            break;
        }
        /* 父进程立刻交出写端，下一段的读端留作 curIn */
        if (wr && wr != hOut) CloseHandle(wr);
        if (prevRead) CloseHandle(prevRead);
        prevRead = rd;
        if (rd) curIn = rd;
    }
    for (i = 0; i < n; i++) {
        DWORD code = 0;
        if (!pi[i].hProcess) break;
        WaitForSingleObject(pi[i].hProcess, INFINITE);
        GetExitCodeProcess(pi[i].hProcess, &code);
        status = (int)code;
        CloseHandle(pi[i].hProcess);
        CloseHandle(pi[i].hThread);
    }
    if (prevRead) CloseHandle(prevRead);
    if (hIn) CloseHandle(hIn);
    if (hOut) CloseHandle(hOut);
    return status;
}
#endif

static int is_single_builtin(Cmd *cmds, int n)
{
    return n == 1 && cmds[0].argc > 0 &&
           (!strcmp(cmds[0].argv[0], "cd") || !strcmp(cmds[0].argv[0], "exit") ||
            !strcmp(cmds[0].argv[0], "pwd"));
}

int main(void)
{
    char line[256];
    printf("mini_shell — 6.1810 L05/L20 lab-shell (POSIX + Win32). 'exit' quits.\n");
    for (;;) {
        Cmd cmds[MAXCMD];
        char rin[128], rout[128];
        int n, quit = 0;
        printf("> ");
        fflush(stdout);
        if (!fgets(line, sizeof line, stdin)) break;
        n = splitline(line, cmds, rin, rout);
        if (n < 0) { printf("parse error\n"); continue; }
        if (n == 0) continue;
        if (is_single_builtin(cmds, n)) {
            if (!strcmp(cmds[0].argv[0], "exit")) quit = 1;
            else if (!strcmp(cmds[0].argv[0], "cd")) {
                if (cmds[0].argc < 2) { printf("usage: cd DIR\n"); continue; }
#ifdef _WIN32
                if (!SetCurrentDirectoryA(cmds[0].argv[1])) printf("cd failed\n");
#else
                if (chdir(cmds[0].argv[1]) != 0) perror("cd");
#endif
            } else {
                char buf[256] = "";
#ifdef _WIN32
                GetCurrentDirectoryA(sizeof buf, buf);
#else
                if (!getcwd(buf, sizeof buf)) buf[0] = 0;
#endif
                printf("%s\n", buf);
            }
            if (quit) break;
            continue;
        }
        run_pipeline(cmds, n, rin, rout);
    }
    return 0;
}
