#!/bin/sh
# ch04-05-perf 构建脚本（gcc）
# 用 -std=gnu99 而非 -std=c99：glibc 下严格 c99 会隐藏 clock_gettime/struct timespec 等 POSIX 符号
set -e
mkdir -p bin
OPT=${CFLAGS:--O2}
gcc -std=gnu99 -Wall -Wextra $OPT -o bin/matrix src/matrix.c
echo "built with [$OPT]: bin/matrix"
bin/matrix
