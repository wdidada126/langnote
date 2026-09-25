#!/bin/sh
# ch07-linking 构建脚本（gcc + make 封装；Windows 用 build.bat）
set -e
make clean
make all
make weak_demo || true
echo "==== run ===="
cd bin && ./static_demo && ./order_ok && ./dynload
