#!/bin/sh
# ch10-11-net-conc 构建脚本（gcc；POSIX 线程/套接字）
set -e
mkdir -p bin
gcc -std=c99 -Wall -Wextra -O1 -pthread -o bin/echo_server         src/echo_server.c
gcc -std=c99 -Wall -Wextra -O1 -o          bin/echo_client          src/echo_client.c
gcc -std=c99 -Wall -Wextra -O1 -pthread -o bin/producer_consumer    src/producer_consumer.c
echo "built: bin/echo_server bin/echo_client bin/producer_consumer"
