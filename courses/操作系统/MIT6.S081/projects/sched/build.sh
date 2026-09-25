#!/bin/sh
set -e
: "${CC:=cc}"
"$CC" -std=c11 -O2 -Wall -Wextra -o sched_demo main.c
./sched_demo
