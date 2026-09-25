#!/usr/bin/env bash
# p1 build (g++, C++17)
set -e
mkdir -p bin
g++ -std=c++17 -O2 -Wall -Wextra -o bin/p1 src/main.cpp
echo "OK -> ./bin/p1"
