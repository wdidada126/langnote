#!/bin/sh
set -e
: "${CC:=cc}"
"$CC" -std=c11 -O2 -Wall -Wextra -o pgtbl_demo main.c pgtbl.c
./pgtbl_demo
