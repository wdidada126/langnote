#!/bin/sh
# ch10-11-net-conc 构建脚本（gcc；POSIX 线程/套接字）
# 用 -std=gnu99 而非 -std=c99：glibc 下严格 c99 会隐藏 getaddrinfo/NI_MAXHOST 等 POSIX 符号
set -e
mkdir -p bin
gcc -std=gnu99 -Wall -Wextra -O1 -pthread -o bin/echo_server         src/echo_server.c
gcc -std=gnu99 -Wall -Wextra -O1 -o          bin/echo_client          src/echo_client.c
gcc -std=gnu99 -Wall -Wextra -O1 -pthread -o bin/producer_consumer    src/producer_consumer.c
echo "built: bin/echo_server bin/echo_client bin/producer_consumer"
