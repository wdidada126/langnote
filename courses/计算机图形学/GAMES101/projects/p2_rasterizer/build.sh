#!/usr/bin/env bash
# p2 build (g++, C++17)
set -e
mkdir -p bin
g++ -std=c++17 -O2 -Wall -Wextra -o bin/p2 src/main.cpp
echo "OK -> ./bin/p2"
