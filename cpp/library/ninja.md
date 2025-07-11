# ninja

choco install ninja -y
支持windows mac linux

ceph使用ninja

yum install cmake -y
yum install ninja-build -y

Arch: pacman -S ninja
Debian/Ubuntu: apt-get install ninja-build
Fedora: dnf install ninja-build
Gentoo: emerge dev-util/ninja
Opensuse: zypper in ninja
Alpine: apk add ninja
Void: xbps-install -S ninja

类似于make，编译速度快

cmake生成build.ninja

chrome source code

# 官方主页
[The Ninja build system]( https://ninja-build.org/manual.html)

vs支持cmake，就是用ninja这个generator

Clion不支持ninja?

ninja类似make
build.ninja这个文件
make使用makefile

 [使用 Ninja 代替 make](https://blog.csdn.net/rankun1/article/details/80420301)

yum install cmake -y
yum install ninja-build -y

类似于make，编译速度快

cmake生成build.ninja

chrome source code

ninja -c build

[The Ninja build system]( https://ninja-build.org/manual.html)

vs支持cmake，就是用ninja这个generator

clion不支持ninja?cmake支持ninja

ninja类似make
build.ninja这个文件
make使用makefile

[使用 Ninja 代替 make](https://blog.csdn.net/rankun1/article/details/80420301)

当直接执行 ninja 命令是，它会在当前目录下默认寻找 build.ninja 文件来进行编译。
ninja 的语法格式是：

ninja [options] TARGETs
上述 options 如果没有则可以省略。比如，直接执行 ./ninja ninja_test 将会生成可执行文件 ninja_test，然后再执行 ninja_test 就可以看到测试结果。

克隆Ninja的Github仓库：
git clone https://github.com/ninja-build/ninja.git
进入克隆的仓库目录：
cd ninja
运行配置脚本：
./configure.py --bootstrap
将Ninja复制到系统路径中：
cp ./ninja /usr/bin
检查安装版本：
ninja --version



git clone -b v1.11.1 https://github.com/ninja-build/ninja.git
cd ninja
cmake -Bbuild-cmake
cmake --build build-cmake
./build-cmake/ninja --version

## github上有编译好的二进制

## mac ninja
ibqodeMacBook-Pro:~ ibqo$ ninja --version
1.10.2
ibqodeMacBook-Pro:~ ibqo$ brew info ninja
==> ninja: stable 1.11.1 (bottled), HEAD
Small build system for use with gyp or CMake
https://ninja-build.org/
/usr/local/Cellar/ninja/1.10.2_1 (10 files, 402.3KB) *
  Poured from bottle on 2022-04-17 at 11:28:23
From: https://github.com/Homebrew/homebrew-core/blob/HEAD/Formula/ninja.rb
License: Apache-2.0
==> Dependencies
Build: python@3.11 ✘
==> Options
--HEAD
	Install HEAD version
==> Caveats
Bash completion has been installed to:
  /usr/local/etc/bash_completion.d

Emacs Lisp files have been installed to:
  /usr/local/share/emacs/site-lisp/ninja