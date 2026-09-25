#!/bin/sh
# ch04-05-perf 构建脚本（gcc）
set -e
mkdir -p bin
OPT=${CFLAGS:--O2}
gcc -std=c99 -Wall -Wextra $OPT -o bin/matrix src/matrix.c
echo "built with [$OPT]: bin/matrix"
bin/matrix
