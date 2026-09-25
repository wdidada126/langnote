#!/bin/sh
# build.sh — alloc demo (gcc/clang/cc)
set -e
: "${CC:=cc}"
"$CC" -std=c11 -O2 -Wall -Wextra -o alloc_demo main.c firstfit.c buddy.c
./alloc_demo
