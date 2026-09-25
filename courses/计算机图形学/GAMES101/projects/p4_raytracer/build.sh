#!/usr/bin/env bash
# p4 build (g++, C++17)
set -e
mkdir -p bin
g++ -std=c++17 -O2 -Wall -Wextra -o bin/p4 src/main.cpp
echo "OK -> ./bin/p4"
