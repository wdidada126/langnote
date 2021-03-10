#!/bin/bash

#install the glibc
function installGlibc(){
set -e

cd ../../glibcoffline/glibc-2.14
chmod -R a+x glibc-2.14
cd glibc-2.14

if [ ! -d build]; then
mkdir build
fi

cd build/
mkdir -p /data/xxx/lib/glibc-2.14
../configure --prefix=/data/xxx/lib/glibc-2.14
make -j4
make install
export LD_LIBRARY_PATH=/data/xxx/lib/glibc-2.14/lib:$LD_LIBRARY_PATH
echo $LD_LIBRARY_PATH
cd /lib64
ll libc.so.6
ll /data/xxx/lib/glibc-2.14/lib/libc-2.14.so
cp /data/xxx/lib/glibc-2.14/lib/libc-2.14.so /lib64/
unlink /lib64/libc.so.6
ln -s libc-2.14.so /lib64/libc.so.6
ll libc.so.6
strings /lib64/libc.so.6 |grep GLIBC_
}

installGlibc