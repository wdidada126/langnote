#!/bin/sh
set -e
: "${CC:=cc}"
"$CC" -std=gnu11 -O2 -Wall -Wextra -o mini_shell main.c
echo "run: ./mini_shell"
