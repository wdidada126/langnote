/*
 * echo_client.c —— 回显客户端（L19 / CSAPP 11.4）
 * POSIX 与 Windows(Winsock2) 双平台。用 getaddrinfo 处理地址/端口。
 * 用法: echo_client <host> <port> [message...]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
  #include <winsock2.h>
  #include <ws2tcpip.h>
  typedef SOCKET   sock_t;
  #define BAD_SOCK INVALID_SOCKET
  #define closesock(s) closesocket(s)
#else
  #include <unistd.h>
  #include <sys/socket.h>
  #include <netinet/in.h>
  #include <netdb.h>
  #include <signal.h>
  typedef int      sock_t;
  #define BAD_SOCK (-1)
  #define closesock(s) close(s)
#endif

#define MAXMSG 4096

/* 打开到 host:port 的 TCP 连接（CSAPP open_clientfd 的等价实现） */
static sock_t open_clientfd(const char *host, const char *port)
{
    struct addrinfo hints, *res0 = NULL, *res;
    sock_t fd = BAD_SOCK;

    memset(&hints, 0, sizeof hints);
    hints.ai_family   = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    if (getaddrinfo(host, port, &hints, &res0) != 0)
        return BAD_SOCK;
    for (res = res0; res != NULL; res = res->ai_next) {
        fd = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
        if (fd == BAD_SOCK)
            continue;
        if (connect(fd, res->ai_addr, (int)res->ai_addrlen) == 0)
            break;                      /* 成功 */
        closesock(fd);
        fd = BAD_SOCK;
    }
    freeaddrinfo(res0);
    return fd;
}

int main(int argc, char **argv)
{
    const char *host, *port;
    char msg[MAXMSG] = "ping from 15-213\n";
    char buf[MAXMSG];
    sock_t fd;
    int n, i;

#ifdef _WIN32
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) return 1;
#endif
    if (argc < 3) {
        fprintf(stderr, "usage: %s <host> <port> [msg...]\n", argv[0]);
        return 1;
    }
    host = argv[1];
    port = argv[2];
    if (argc > 3) {
        msg[0] = '\0';
        for (i = 3; i < argc; i++) {
            strncat(msg, argv[i], sizeof msg - strlen(msg) - 2);
            strncat(msg, " ", sizeof msg - strlen(msg) - 2);
        }
        strncat(msg, "\n", sizeof msg - strlen(msg) - 1);
    }

    fd = open_clientfd(host, port);
    if (fd == BAD_SOCK) {
        fprintf(stderr, "无法连接 %s:%s（服务器没起？）\n", host, port);
#ifdef _WIN32
        WSACleanup();
#endif
        return 1;
    }

    if (send(fd, msg, (int)strlen(msg), 0) < 0) {
        fprintf(stderr, "send failed\n");
    } else {
        /* 读回显直到 EOF 或读满（无行协议，演示裸字节流） */
        while ((n = (int)recv(fd, buf, sizeof buf - 1, 0)) > 0) {
            buf[n] = '\0';
            printf("echo< %s", buf);
        }
    }
    closesock(fd);
#ifdef _WIN32
    WSACleanup();
#endif
    return 0;
}
