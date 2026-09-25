#!/usr/bin/env bash
# Build 01-buffer-pool with g++, C++17. Run from this directory.
set -e
mkdir -p build
g++ -std=c++17 -Wall -Wextra -O2 main.cpp -o build/bufferpool
echo "---- running ----"
./build/bufferpool
