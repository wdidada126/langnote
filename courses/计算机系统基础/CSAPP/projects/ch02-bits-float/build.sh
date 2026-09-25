#!/bin/sh
# ch02-bits-float 构建脚本（gcc / POSIX shell）
set -e
mkdir -p bin
gcc -std=c99 -Wall -Wextra -O1 -o bin/bits_test src/bits.c src/main.c
echo "built: bin/bits_test"
bin/bits_test
