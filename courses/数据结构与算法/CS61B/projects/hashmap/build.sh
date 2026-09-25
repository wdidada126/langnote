#!/usr/bin/env bash
# 项目 hashmap 构建脚本（JDK 17：javac/java，无外部依赖；-encoding UTF-8 因源码含中文注释）
set -e
mkdir -p build
javac -encoding UTF-8 -d build src/cs61b/hashmap/*.java
java -cp build cs61b.hashmap.Main
