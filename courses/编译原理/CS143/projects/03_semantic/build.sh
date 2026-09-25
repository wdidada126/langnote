#!/bin/sh
# Stage 03 (MiniC semantic analysis) — build with g++.
# The checking logic is in ../common/checker.h (new this stage).
# Run from THIS directory: ./build.sh
set -e
g++ -std=c++17 -Wall -Wextra -O2 main.cpp -o minic03
echo "built: ./minic03  ->  ./minic03 ../samples/bad.minic"
