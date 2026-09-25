#!/bin/sh
# Stage 04 (MiniC IR generator) — build with g++.
# New this stage: icode.h (three-address IR + IRGen). Run from THIS directory.
set -e
g++ -std=c++17 -Wall -Wextra -O2 main.cpp -o minic04
echo "built: ./minic04  ->  ./minic04 ../samples/hello.minic"
