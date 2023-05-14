# xmake
debian xmake 包做到一半，发现 xmake 依赖的库 tbox libsv 啥的都已经在 debian 仓库里了。
sudo apt install libtbox-dev 可以直接装了



安装
非root用户

- xmake
- xrepo



xrepo自动下载依赖

xmake install xxx -y

[wdidada@10-23-29-39 ~]$ xrepo install  zlib tbox
note: install or modify (m) these packages (pass -y to skip confirm)?
in xmake-repo:
  -> zlib v1.2.12 
  -> tbox v1.6.7 
please input: y (y/n/m)
n
error: packages(zlib, tbox): must be installed!
error: execv(xmake require -j 2 --extra={system=false} zlib tbox) failed(255)
[wdidada@10-23-29-39 ~]$ xrepo install  zlib tbox
note: install or modify (m) these packages (pass -y to skip confirm)?
in xmake-repo:
  -> zlib v1.2.12 
  -> tbox v1.6.7 
please input: y (y/n/m)
m
note: select the following 3rd packages
  1. pacman::zlib -> zlib v1.2.12 
  2. apt::zlib1g-dev -> zlib v1.2.12 
  please input number list: n (1,2,..)
  2
  note: install or modify (m) these packages (pass -y to skip confirm)?
  in xmake-repo:
    -> tbox v1.6.7 
  in apt:
    -> apt::zlib1g-dev latest 
  please input: y (y/n/m)
  y
    => install apt::zlib1g-dev latest .. failed

apt not found!
if you want to get more verbose errors, please see:
  -> /dev/shm/.xmake1000/220419/xrepo/working/build/.packages/a/apt_zlib1g-dev/latest/cache/installdir.failed/logs/install.txt
error: install failed!
error: execv(xmake require -j 2 --extra={system=false} zlib tbox) failed(255)
[wdidada@10-23-29-39 ~]$ xrepo install  zlib tbox
note: install or modify (m) these packages (pass -y to skip confirm)?
in xmake-repo:
  -> zlib v1.2.12 
  -> tbox v1.6.7 
please input: y (y/n/m)
y
  => download https://github.com/tboox/tbox/archive/v1.6.7.tar.gz .. ok
  => download https://github.com/madler/zlib/archive/v1.2.12.tar.gz .. ok
  => install zlib v1.2.12 .. ok              
  => install tbox v1.6.7 .. ok     
[wdidada@10-23-29-39 ~]$ xrepo search grpc
The package names:
[wdidada@10-23-29-39 ~]$ xrepo search poco
The package names:
    poco: 
      -> poco-1.11.1: The POCO C++ Libraries are powerful cross-platform C++ libraries for building network- and internet-based applications that run on desktop, server, mobile, IoT, and embedded systems. (in xmake-repo)
[wdidada@10-23-29-39 ~]$ xrepo install poco
note: install or modify (m) these packages (pass -y to skip confirm)?
in xmake-repo:
  -> poco 1.11.1 
please input: y (y/n/m)
y
  => download https://github.com/pocoproject/poco/archive/refs/tags/poco-1.11.1-release.tar.gz .. ok
  => install poco 1.11.1 .. failed 

CMake Error at XML/CMakeLists.txt:23 (find_package):
  Could not find a package configuration file provided by "EXPAT" with any of
  the following names:
    EXPATConfig.cmake
    expat-config.cmake
  Add the installation prefix of "EXPAT" to CMAKE_PREFIX_PATH or set
  "EXPAT_DIR" to a directory containing one of the above files.  If "EXPAT"
  provides a separate development package or SDK, be sure it has been
  installed.
evtoolset-7/root/usr/bin/c++
-- Check for working CXX compiler: /opt/rh/devtoolset-7/root/usr/bin/c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Checking for C++14 compiler
-- Checking for C++14 compiler - available
if you want to get more verbose errors, please see:
  -> /home/wdidada/.xmake/cache/packages/2204/p/poco/1.11.1/installdir.failed/logs/install.txt
error: install failed!
error: execv(xmake require -j 2 --extra={system=false} poco) failed(255




例子
https://gitee.com/edidada/great-project

source ~/.xmake/profile


https://gitee.com/tboox/xmake


Supported package repositories

Official package repository xmake-repo (tbox >1.6.1)
Official package manager Xrepo
User-built repositories
Conan (conan::openssl/1.1.1g)
Conda (conda::libpng 1.3.67)
Vcpkg (vcpkg:ffmpeg)
Homebrew/Linuxbrew (brew::pcre2/libpcre2-8)
Pacman on archlinux/msys2 (pacman::libcurl)
Apt on ubuntu/debian (apt::zlib1g-dev)
Clib (clib::clibs/bytes@0.0.4)
Dub (dub::log 0.4.3)
Portage on Gentoo/Linux (portage::libhandy)
Nimble for nimlang (nimble::zip >1.3)

入门教程
https://www.lanqiao.cn/courses/2764
https://zhuanlan.zhihu.com/p/412503965



add_rules("mode.debug", "mode.release")

target("great-project")
    set_kind("binary")
    add_files("src/*.cpp")


-- If you want to known more usage about xmake, please see https://xmake.io
--
-- ## FAQ
--
-- You can enter the project directory firstly before building project.
--
--   $ cd projectdir
--
-- 1. How to build project?
--
--   $ xmake
--
-- 2. How to configure project?
--
--   $ xmake f -p [macosx|linux|iphoneos ..] -a [x86_64|i386|arm64 ..] -m [debug|release]
--
-- 3. Where is the build output directory?
--
--   The default output directory is `./build` and you can configure the output directory.
--
--   $ xmake f -o outputdir
--   $ xmake
--
-- 4. How to run and debug target after building project?
--
--   $ xmake run [targetname]
--   $ xmake run -d [targetname]
--
-- 5. How to install target to the system directory or other output directory?
--
--   $ xmake install
--   $ xmake install -o installdir
--
-- 6. Add some frequently-used compilation flags in xmake.lua
--
-- @code
--    -- add debug and release modes
--    add_rules("mode.debug", "mode.release")
--
--    -- add macro defination
--    add_defines("NDEBUG", "_GNU_SOURCE=1")
--
--    -- set warning all as error
--    set_warnings("all", "error")
--
--    -- set language: c99, c++11
--    set_languages("c99", "c++11")
--
--    -- set optimization: none, faster, fastest, smallest
--    set_optimize("fastest")
--
--    -- add include search directories
--    add_includedirs("/usr/include", "/usr/local/include")
--
--    -- add link libraries and search directories
--    add_links("tbox")
--    add_linkdirs("/usr/local/lib", "/usr/lib")
--
--    -- add system link libraries
--    add_syslinks("z", "pthread")
--
--    -- add compilation and link flags
--    add_cxflags("-stdnolib", "-fno-strict-aliasing")
--    add_ldflags("-L/usr/local/lib", "-lpthread", {force = true})
--
-- @endcode
--

[Xmake和C/C++包管理](https://tboox.org/cn/2022/03/12/xmake-and-package-management/)

集成一个内置依赖包只需要几行配置：

add_requires("zlib 1.2.11")
target("test")
    add_files("src/*.c")
    add_packages("zlib")
集成一个 vcpkg 包，仅仅只需要加上对应的包管理器命名空间，集成方式完全相同：

add_requires("vcpkg::zlib 1.2.11")
target("test")
    add_files("src/*.c")
    add_packages("vcpkg::zlib")
集成一个 conan 包，或者 conda, homebrew, pacman, apt, clib 等第三方包，也只需要改成 conan::zlib 就行了，用户可以随意切换包源。

另外，Xmake 会自动帮你调用 vcpkg/conan install 安装命令去安装依赖包，然后集成它们，不需要用户做任何其他事情，仅仅只需要执行 xmake 一键编译。

目前 Xmake 支持的包源有以下这些：

Official package repository xmake-repo (tbox >1.6.1)
Official package manager Xrepo
User-built repositories
Conan (conan::openssl/1.1.1g)
Conda (conda::libpng 1.3.67)
Vcpkg (vcpkg:ffmpeg)
Homebrew/Linuxbrew (brew::pcre2/libpcre2-8)
Pacman on archlinux/msys2 (pacman::libcurl)
Apt on ubuntu/debian (apt::zlib1g-dev)
Clib (clib::clibs/bytes@0.0.4)
Dub (dub::log 0.4.3)
Portage on Gentoo/Linux (portage::libhandy)
Nimble for nimlang (nimble::zip >1.3)
Cargo for rust (cargo::base64 0.13.0)



通过 Xmake 和 xmake-idea 插件，我们可以很方便的在 Clion/Intellji IDEA 中跨平台开发 C/C++ 程序。由于目前插件本身还不支持调试，但是我们在 Clion 中还是可以借助生成 CMakeLists.txt 来变相支持断点调试，Intelligense。
