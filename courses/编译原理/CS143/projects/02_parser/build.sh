#!/bin/sh
# Stage 02 (MiniC parser + AST dump) — build with g++ (Linux/macOS/MSYS2/WSL).
# Single translation unit; the lexer/AST come in via relative quoted includes
# from ../common/*.h. Run from THIS directory: ./build.sh
set -e
g++ -std=c++17 -Wall -Wextra -O2 main.cpp -o minic02
echo "built: ./minic02  ->  ./minic02 ../samples/hello.minic"
