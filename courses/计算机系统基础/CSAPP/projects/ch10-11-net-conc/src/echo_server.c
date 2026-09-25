/*
 * echo_server.c —— 线程版回显服务器骨架（L19 网络 + L20 并发）
 * POSIX: pthreads；Windows: Win32 threads + Winsock2。
 * 每个连接一条线程："逻辑上串行"的服务模型，同步问题被推给 OS 调度。
 * 对照阅读：README 中"事件驱动版"设计（epoll/IOCP 单线程写法）。
 * 用法: echo_server [port]   （默认 8000；Ctrl-C 停止）
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
  #include <winsock2.h>
  #include <ws2tcpip.h>
  typedef SOCKET      sock_t;
  typedef int         sock_len_t;      /* 老 SDK 的 MSVC 没有 socklen_t */
  #define BAD_SOCK    INVALID_SOCKET
  #define closesock(s) closesocket(s)
  /* build.bat 已链接 ws2_32.lib；cl 亦可加 /link ws2_32.lib */
#else
  #include <unistd.h>
  #include <sys/socket.h>
  #include <sys/types.h>
  #include <netinet/in.h>
  #include <netdb.h>
  #include <signal.h>
  #include <pthread.h>
  typedef int         sock_t;
  typedef socklen_t   sock_len_t;
  #define BAD_SOCK    (-1)
  #define closesock(s) close(s)
#endif

#define LISTENQ  1024
#define MAXMSG   4096

/* 把 n 字节全部写出（短写重试，L18/L19） */
static int send_all(sock_t fd, const char *buf, int n)
{
    int sent = 0;
    while (sent < n) {
        int k = (int)send(fd, buf + sent, (size_t)(n - sent), 0);
        if (k <= 0)
            return -1;
        sent += k;
    }
    return sent;
}

/* 一条连接的完整服务过程：recv 一段、echo 一段，直到对端 EOF/出错 */
static void serve_conn(sock_t conn)
{
    for (;;) {
        char buf[MAXMSG];
        int n = (int)recv(conn, buf, sizeof buf, 0);
        if (n == 0)               /* 客户端有序关闭 = EOF */
            break;
        if (n < 0)                /* 出错（含 ECONNRESET/管道断开）*/
            break;
        if (send_all(conn, buf, n) != n)
            break;
    }
    closesock(conn);              /* 必须关，否则 fd 泄漏（L18 三层表）*/
}

#ifdef _WIN32
static DWORD WINAPI worker(LPVOID arg)
{
    serve_conn(*(sock_t *)arg);
    free(arg);
    return 0;
}
#else
static void *worker(void *arg)
{
    serve_conn(*(sock_t *)arg);
    free(arg);
    return NULL;
}
#endif

static sock_t make_listen(const char *port)
{
    struct addrinfo hints, *res0 = NULL, *res;
    int opt = 1;
    sock_t fd = BAD_SOCK;

    memset(&hints, 0, sizeof hints);
    hints.ai_family   = AF_INET;        /* 演示固定 v4；AF_UNSPEC 可同时试 v6 */
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags    = AI_PASSIVE;     /* 通配地址 0.0.0.0 */
    if (getaddrinfo(NULL, port, &hints, &res0) != 0)
        return BAD_SOCK;

    for (res = res0; res != NULL; res = res->ai_next) {
        fd = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
        if (fd == BAD_SOCK)
            continue;
        setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, (const char *)&opt, sizeof opt);
        if (bind(fd, res->ai_addr, (int)res->ai_addrlen) == 0 &&
            listen(fd, LISTENQ) == 0)
            break;                       /* 成功 */
        closesock(fd);
        fd = BAD_SOCK;
    }
    freeaddrinfo(res0);
    return fd;
}

int main(int argc, char **argv)
{
    const char *port = (argc > 1) ? argv[1] : "8000";
    sock_t listenfd;
#ifdef _WIN32
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        fprintf(stderr, "WSAStartup failed\n");
        return 1;
    }
#else
    /* write 到已断开连接默认收到 SIGPIPE 杀死进程 → 转 EPIPE 走错误分支 */
    signal(SIGPIPE, SIG_IGN);
#endif

    listenfd = make_listen(port);
    if (listenfd == BAD_SOCK) {
        fprintf(stderr, "listen on %s failed (端口占用? 试试别的)\n", port);
#ifdef _WIN32
        WSACleanup();
#endif
        return 1;
    }
    printf("echo_server 监听 :%s （线程版，Ctrl-C 结束）\n", port);

    for (;;) {
        struct sockaddr_storage cliaddr;
        socklen_t len = sizeof cliaddr;
        sock_t conn = accept(listenfd, (struct sockaddr *)&cliaddr, &len);
        char host[NI_MAXHOST] = "?";

        if (conn == BAD_SOCK) {
            perror("accept");
            continue;
        }
        getnameinfo((struct sockaddr *)&cliaddr, len, host, sizeof host,
                    NULL, 0, NI_NUMERICHOST);
        printf("[连接] %s\n", host);

        {   /* 每连接一线程：conn 所有权交给 worker */
            sock_t *arg = (sock_t *)malloc(sizeof *arg);
            if (!arg) { closesock(conn); continue; }
            *arg = conn;
#ifdef _WIN32
            { HANDLE h = CreateThread(NULL, 0, worker, arg, 0, NULL);
              if (h) CloseHandle(h); else { free(arg); closesock(conn); } }
#else
            { pthread_t tid;
              pthread_attr_t at; pthread_attr_init(&at);
              pthread_attr_setdetachstate(&at, PTHREAD_CREATE_DETACHED);
              if (pthread_create(&tid, &at, worker, arg) != 0) {
                  free(arg); closesock(conn);
              }
              pthread_attr_destroy(&at); }
#endif
        }
    }
    /* listenfd 永不关闭：进程退出时由 OS 回收（L18 语义） */
#ifdef _WIN32
    WSACleanup();
#endif
    return 0;
}
