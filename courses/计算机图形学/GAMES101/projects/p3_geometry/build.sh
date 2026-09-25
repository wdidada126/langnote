#!/usr/bin/env bash
# p3 build (g++, C++17)
set -e
mkdir -p bin
g++ -std=c++17 -O2 -Wall -Wextra -o bin/p3 src/main.cpp
echo "OK -> ./bin/p3"
