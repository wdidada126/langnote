#!/bin/sh
# Stage 06 (MiniC optimizer) — build with g++.
# New this stage: opt.h. Run from THIS directory: ./build.sh
set -e
g++ -std=c++17 -Wall -Wextra -O2 main.cpp -o minic06
echo "built: ./minic06  ->  ./minic06 ../samples/dead.minic"
