#!/bin/sh
set -e
: "${CC:=cc}"
"$CC" -std=gnu11 -O2 -Wall -Wextra -pthread -o lock_demo main.c
./lock_demo
