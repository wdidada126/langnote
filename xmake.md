# xmake
## repo
https://github.com/xmake-io/xmake-repo
https://github.com/xmake-io/xmake-repo/blob/dev/packages/d/drogon/xmake.lua

drogon_xmake.lua

### vs conan2
python/txt
lua

设置cpu架构 arch
x86
64
arm
arm64
mips

os
linux
win
mac
android
iOS

cppstd
11 14 17 20

库编译选项
conan 2
option

xmake

## clion xmake插件
中国朋友可以加QQ群交流及反馈BUG: 343118190
## dd
xmake.lua

-- add_requires("tbox 1.7.5")
add_requires("tbox 1.7.1", {debug = true})

上面是release的
下面是debug的

## config

### 设置debug，不是release
xmake config -m debug

 xmake g --pkg_searchdirs=C:\Users\edida\Downloads
configure
{
    network = public
    pkg_searchdirs = C:\Users\edida\Downloads
    project = .
    theme = default
    proxy_pac = pac.lua
    yes = true
}


## library
xmake下载三方库源代码保存位置
C:\Users\edida\AppData\Local\.xmake\cache\packages\2407\t\tbox\v1.7.5\v1.7.5.tar.gz

## tbox

/Users/ibqo/.xmake/packages/t/tbox/v1.7.1/296ac87121a0440f8173e5059fc57b1e/lib/cmake

ibqodeMacBook-Pro:tbox ibqo$ ls
algorithm       container       hash            math            object          prefix.h        string          utils
charset         coroutine       libc            memory          platform        regex           tbox.config.h   xml
config.h        database        libm            network         prefix          stream          tbox.h          zip
ibqodeMacBook-Pro:tbox ibqo$ pwd
/Users/ibqo/.xmake/packages/t/tbox/v1.7.1/296ac87121a0440f8173e5059fc57b1e/include/tbox
ibqodeMacBook-Pro:tbox ibqo$ 


```cmake
target_include_directories(ctestttbox SYSTEM PRIVATE
    C:/Users/edida/AppData/Local/.xmake/packages/t/tbox/v1.7.5/a41dba6299f84517b895d362c0e33963/include
)

target_link_directories(ctestttbox PRIVATE
    C:/Users/edida/AppData/Local/.xmake/packages/t/tbox/v1.7.5/a41dba6299f84517b895d362c0e33963/lib
)
```

## xmake.lua转换成CMakeLists.txt

xmake project -k cmake -y

## 版本
2025.06 3

## xrepo

C:\Users\edida\AppData\Local\.xmake\repositories\xmake-repo

xmake l find_package pthread

issue提在github上，matainer不怎么看gitee上的问题

brpc muduo添加进xmake
提交pr
https://github.com/xmake-io/xmake-repo/pull/2887

https://github.com/xmake-io/xmake-repo/tree/dev/packages/m/muduo/xmake.lua

专注于跨平台c开发解决方案（QQ技术交流群：343118190）
https://t.me/tbooxorg
https://twitter.com/waruqi

编写.lua文件

xmake 从零开始创建一个 hello world 单文件真的是我见过最快的，从这点来说它就很适合学校教学

xmake类似maven，定义文件
xmake.lua
pom.xml
然后再下载xmake . 
mvn package
会下载库文件，找不到库文件会报错

xrepo install  zlib tbox -y可以下载库文件到本地

强制编译
xmake -P . -y

搜索库
xrepo search grpc

xmake search_libs <库名>

error: execv(/usr/bin/curl -SL -A "Xmake/2.8.5+20231218 (Linux;5.15.133.1-microsoft-standard-WSL2) curl/7.81.0" https://github.com/protocolbuffers/protobuf/releases/download/v3.19.4/protobuf-cpp-3.19.4.zip -o protobuf-cpp-3.19.4.zip) failed(28)
  => download https://github.com/protocolbuffers/protobuf/releases/download/v3.19.4/protobuf-cpp-3.19.4.zip .. failed

we can also download these packages manually:
  - https://github.com/protocolbuffers/protobuf/releases/download/v3.19.4/protobuf-cpp-3.19.4.zip
to the local search directories:
  - protobuf-cpp-3.19.4.zip
and we can run `xmake g --pkg_searchdirs=/xxx` to set the search directories.

Xmake ~= Make/Ninja + CMake/Meson + Vcpkg/Conan + distcc + ccache

debian xmake 包做到一半，发现 xmake 依赖的库 tbox libsv 啥的都已经在 debian 仓库里了。
```shell
sudo apt install libtbox-dev -y
```

可以直接装了

安装
非root用户

二进制工具
- xmake
- xrepo

xrepo自动下载依赖，类似maven

xmake install xxx -y
```
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
```

例子
https://gitee.com/edidada/great-project

source ~/.xmake/profile


https://gitee.com/tboox/xmake


Supported package repositories
```
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
```
入门教程
https://www.lanqiao.cn/courses/2764
https://zhuanlan.zhihu.com/p/412503965


```
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
```
[Xmake和C/C++包管理](https://tboox.org/cn/2022/03/12/xmake-and-package-management/)

集成一个内置依赖包只需要几行配置：
```
add_requires("zlib 1.2.11")
target("test")
    add_files("src/*.c")
    add_packages("zlib")
```
集成一个 vcpkg 包，仅仅只需要加上对应的包管理器命名空间，集成方式完全相同：

add_requires("vcpkg::zlib 1.2.11")
target("test")
    add_files("src/*.c")
    add_packages("vcpkg::zlib")
集成一个 conan 包，或者 conda, homebrew, pacman, apt, clib 等第三方包，也只需要改成 conan::zlib 就行了，用户可以随意切换包源。

另外，Xmake 会自动帮你调用 vcpkg/conan install 安装命令去安装依赖包，然后集成它们，不需要用户做任何其他事情，仅仅只需要执行 xmake 一键编译。

目前 Xmake 支持的包源有以下这些：
```
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
```
通过 Xmake 和 xmake-idea 插件，我们可以很方便的在 Clion/Intellji IDEA 中跨平台开发 C/C++ 程序。由于目前插件本身还不支持调试，但是我们在 Clion 中还是可以借助生成 CMakeLists.txt 来变相支持断点调试，Intelligense。

```
xmake project -k cmakelists
```
测试生效

Installed:
  autoconf.noarch 0:2.69-11.el7            automake.noarch 0:1.13.4-3.el7       bison.x86_64 0:3.0.4-2.el7               cscope.x86_64 0:15.8-10.el7            
  ctags.x86_64 0:5.8-13.el7                diffstat.x86_64 0:1.57-4.el7         doxygen.x86_64 1:1.8.5-4.el7             elfutils.x86_64 0:0.176-5.el7          
  gcc-gfortran.x86_64 0:4.8.5-44.el7       indent.x86_64 0:2.2.11-13.el7        intltool.noarch 0:0.50.2-7.el7           libtool.x86_64 0:2.4.2-22.el7_3        
  patchutils.x86_64 0:0.3.3-5.el7_9        rcs.x86_64 0:5.9.0-7.el7             rpm-build.x86_64 0:4.11.3-48.el7_9       rpm-sign.x86_64 0:4.11.3-48.el7_9      
  subversion.x86_64 0:1.7.14-16.el7        swig.x86_64 0:2.0.10-5.el7           systemtap.x86_64 0:4.0-13.el7           

Dependency Installed:
  apr.x86_64 0:1.4.8-7.el7                                apr-util.x86_64 0:1.5.2-6.el7_9.1                    boost-date-time.x86_64 0:1.53.0-28.el7            
  boost-system.x86_64 0:1.53.0-28.el7                     boost-thread.x86_64 0:1.53.0-28.el7                  dyninst.x86_64 0:9.3.1-3.el7                      
  efivar-libs.x86_64 0:36-12.el7                          emacs-filesystem.noarch 1:24.3-23.el7_9.1            gdb.x86_64 0:7.6.1-120.el7                        
  gettext-common-devel.noarch 0:0.19.8.1-3.el7            gettext-devel.x86_64 0:0.19.8.1-3.el7                gnutls.x86_64 0:3.3.29-9.el7_6                    
  libdwarf.x86_64 0:20130207-4.el7                        libgfortran.x86_64 0:4.8.5-44.el7                    libmodman.x86_64 0:2.0.1-8.el7                    
  libproxy.x86_64 0:0.4.11-11.el7                         libquadmath.x86_64 0:4.8.5-44.el7                    libquadmath-devel.x86_64 0:4.8.5-44.el7           
  mokutil.x86_64 0:15-8.el7                               neon.x86_64 0:0.30.0-4.el7                           nettle.x86_64 0:2.7.1-9.el7_9                     
  pakchois.x86_64 0:0.4-10.el7                            perl-Data-Dumper.x86_64 0:2.145-3.el7                perl-Test-Harness.noarch 0:3.28-3.el7             
  perl-Thread-Queue.noarch 0:3.02-2.el7                   perl-XML-Parser.x86_64 0:2.41-10.el7                 subversion-libs.x86_64 0:1.7.14-16.el7            
  systemtap-client.x86_64 0:4.0-13.el7                    systemtap-devel.x86_64 0:4.0-13.el7                  systemtap-runtime.x86_64 0:4.0-13.el7 