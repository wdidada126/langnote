#!/bin/sh
set -e
: "${CC:=cc}"
"$CC" -std=c11 -O2 -Wall -Wextra -o minifs_demo main.c minifs.c
./minifs_demo
