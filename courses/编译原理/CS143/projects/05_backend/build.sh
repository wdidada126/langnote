#!/bin/sh
# Stage 05 (MiniC three-address VM) — build with g++.
# New this stage: interp.h. Run from THIS directory: ./build.sh
set -e
g++ -std=c++17 -Wall -Wextra -O2 main.cpp -o minic05
echo "built: ./minic05  ->  ./minic05 ../samples/hello.minic"
