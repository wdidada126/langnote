#!/bin/sh
# Stage 01 (MiniC lexer) — build with g++ on Linux / macOS / MSYS2 / WSL.
# Only ONE translation unit: main.cpp pulls the core via relative quoted
# includes ("../common/lexer.h"), which resolve against main.cpp's directory,
# so run this script from THIS directory:  ./build.sh
set -e
g++ -std=c++17 -Wall -Wextra -O2 main.cpp -o minic01
echo "built: ./minic01  ->  ./minic01 ../samples/hello.minic"
