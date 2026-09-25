#!/bin/sh
# ch08-09-ecf-io 构建脚本（gcc）
# 用 -std=gnu99 而非 -std=c99：glibc 下严格 c99 会隐藏 sigaction/SA_RESTART 等 POSIX 符号
set -e
mkdir -p bin
gcc -std=gnu99 -Wall -Wextra -O1 -o bin/mini_shell src/mini_shell.c
gcc -std=gnu99 -Wall -Wextra -O1 -o bin/cp_like  src/robust_copy.c
echo "built: bin/mini_shell bin/cp_like"
