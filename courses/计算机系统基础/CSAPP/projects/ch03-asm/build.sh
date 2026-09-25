#!/bin/sh
# ch03-asm 构建脚本（gcc）：编译 + 运行 + 反汇编对照
set -e
mkdir -p bin
gcc -Og -std=c99 -Wall -Wextra -c src/funcs.c -o bin/funcs.o
gcc -Og -o bin/funcs bin/funcs.o
echo "== run =="
bin/funcs
echo "== disassemble (objdump -d bin/funcs.o) =="
objdump -d bin/funcs.o | head -80 || true
