#!/bin/sh
# ch08-09-ecf-io 构建脚本（gcc）
set -e
mkdir -p bin
gcc -std=c99 -Wall -Wextra -O1 -o bin/mini_shell src/mini_shell.c
gcc -std=c99 -Wall -Wextra -O1 -o bin/cp_like  src/robust_copy.c
echo "built: bin/mini_shell bin/cp_like"
