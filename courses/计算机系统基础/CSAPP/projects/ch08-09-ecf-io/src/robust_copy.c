/*
 * robust_copy.c —— Unix I/O 风格健壮文件复制（L18 / CSAPP Ch.10）
 * 要点：短读/短写重试、EINTR 处理、错误路径完整。
 * POSIX 用 open/read/write；Windows 用 CRT _open/_read/_write（二进制模式）。
 * 用法: cp_like <src> <dst>
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#ifdef _WIN32
#include <io.h>
#include <fcntl.h>
#include <sys/stat.h>
typedef long ssize_win;
#define OPEN(path, flags, mode)        _open((path), (flags), (mode))
#define READ(fd, buf, n)               _read((fd), (buf), (unsigned)(n))
#define WRITE(fd, buf, n)              _write((fd), (buf), (unsigned)(n))
#define CLOSE(fd)                      _close(fd)
#define O_BINARY_F                     O_BINARY
#else
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#define OPEN(path, flags, mode)        open((path), (flags), (mode))
#define READ(fd, buf, n)               read((fd), (buf), (n))
#define WRITE(fd, buf, n)              write((fd), (buf), (n))
#define CLOSE(fd)                      close(fd)
#define O_BINARY_F                     0
#endif

#define BUFSIZE 4096

/* 健壮读：循环直到读满 n 或到 EOF；EINTR 时重试（L15 的技能）。 */
static long rio_readn(int fd, void *usrbuf, size_t n)
{
    size_t nleft = n;
    long nread;
    char *bufp = (char *)usrbuf;

    while (nleft > 0) {
        nread = (long)READ(fd, bufp, nleft);
        if (nread < 0) {
#ifndef _WIN32
            if (errno == EINTR)      /* 被信号打断 → 重试 */
                continue;
#endif
            return -1;
        } else if (nread == 0) {
            break;                   /* EOF */
        }
        nleft -= (size_t)nread;
        bufp += nread;
    }
    return (long)(n - nleft);
}

static long rio_writen(int fd, const void *usrbuf, size_t n)
{
    size_t nleft = n;
    long nwritten;
    const char *bufp = (const char *)usrbuf;

    while (nleft > 0) {
        nwritten = (long)WRITE(fd, bufp, nleft);
        if (nwritten <= 0) {
#ifndef _WIN32
            if (errno == EINTR)
                continue;
#endif
            return -1;               /* 短写<=0 且非 EINTR：错误 */
        }
        nleft -= (size_t)nwritten;
        bufp += nwritten;
    }
    return (long)n;
}

int main(int argc, char **argv)
{
    int fd_src, fd_dst;
    char buf[BUFSIZE];
    long nread, total = 0;
    int flags_ro = O_RDONLY | O_BINARY_F;
    int flags_wo = O_WRONLY | O_CREAT | O_TRUNC | O_BINARY_F;

    if (argc != 3) {
        fprintf(stderr, "usage: %s <src> <dst>\n", argv[0]);
        return 1;
    }
    fd_src = OPEN(argv[1], flags_ro, 0);
    if (fd_src < 0) {
        fprintf(stderr, "open %s: %s\n", argv[1], strerror(errno));
        return 1;
    }
    fd_dst = OPEN(argv[2], flags_wo,
#ifdef _WIN32
                  _S_IWRITE | _S_IREAD
#else
                  S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH
#endif
                 );
    if (fd_dst < 0) {
        fprintf(stderr, "open %s: %s\n", argv[2], strerror(errno));
        CLOSE(fd_src);
        return 1;
    }

    while ((nread = rio_readn(fd_src, buf, sizeof buf)) > 0) {
        if (rio_writen(fd_dst, buf, (size_t)nread) != nread) {
            fprintf(stderr, "write %s failed: %s\n", argv[2], strerror(errno));
            break;
        }
        total += nread;
    }
    if (nread < 0)
        fprintf(stderr, "read %s failed: %s\n", argv[1], strerror(errno));

    CLOSE(fd_src);
    CLOSE(fd_dst);
    printf("copied %ld bytes: %s -> %s\n", total, argv[1], argv[2]);
    return nread < 0 ? 1 : 0;
}
