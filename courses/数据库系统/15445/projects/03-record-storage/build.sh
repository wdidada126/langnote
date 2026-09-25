#!/usr/bin/env bash
set -e
mkdir -p build
g++ -std=c++17 -Wall -Wextra -O2 main.cpp -o build/recordstore
echo "---- running ----"
./build/recordstore
