# CMake


rpmbuild spec CMake 创建项目的rpm 包



https://blog.csdn.net/henry860916/article/details/50443574
https://blog.csdn.net/wudongxu/article/details/6804536



CMake中包含的三个工具（cmake cpack ctest）

cpack

ctest





rpm

deb

包



类比maven

jar 本质是一压缩格式，winrar可以打开

war



aar


=======
cmake module模块
```shell
cmake --help-module-list
AddFileDependencies
AndroidTestUtilities
BundleUtilities
CMakeAddFortranSubdirectory
CMakeBackwardCompatibilityCXX
CMakeDependentOption
CMakeDetermineVSServicePack
CMakeExpandImportedTargets
CMakeFindDependencyMacro
CMakeFindFrameworks
CMakeFindPackageMode
CMakeForceCompiler
CMakeGraphVizOptions
CMakePackageConfigHelpers
CMakeParseArguments
CMakePrintHelpers
CMakePrintSystemInformation
CMakePushCheckState
CMakeVerifyManifest
CPack
CPackArchive
CPackBundle
CPackComponent
CPackCygwin
CPackDMG
CPackDeb
CPackFreeBSD
CPackIFW
CPackIFWConfigureFile
CPackNSIS
CPackNuGet
CPackPackageMaker
CPackProductBuild
CPackRPM
CPackWIX
CSharpUtilities
CTest
CTestCoverageCollectGCOV
CTestScriptMode
CTestUseLaunchers
CheckCCompilerFlag
CheckCSourceCompiles
CheckCSourceRuns
CheckCXXCompilerFlag
CheckCXXSourceCompiles
CheckCXXSourceRuns
CheckCXXSymbolExists
CheckFortranCompilerFlag
CheckFortranFunctionExists
CheckFortranSourceCompiles
CheckFortranSourceRuns
CheckFunctionExists
CheckIPOSupported
CheckIncludeFile
CheckIncludeFileCXX
CheckIncludeFiles
CheckLanguage
CheckLibraryExists
CheckOBJCCompilerFlag
CheckOBJCSourceCompiles
CheckOBJCSourceRuns
CheckOBJCXXCompilerFlag
CheckOBJCXXSourceCompiles
CheckOBJCXXSourceRuns
CheckPIESupported
CheckPrototypeDefinition
CheckStructHasMember
CheckSymbolExists
CheckTypeSize
CheckVariableExists
Dart
DeployQt4
Documentation
ExternalData
ExternalProject
FeatureSummary
FetchContent
FindALSA
FindASPELL
FindAVIFile
FindArmadillo
FindBISON
FindBLAS
FindBZip2
FindBacktrace
FindBoost
FindBullet
FindCABLE
FindCUDA
FindCURL
FindCVS
FindCoin3D
FindCups
FindCurses
FindCxxTest
FindCygwin
FindDCMTK
FindDart
FindDevIL
FindDoxygen
FindEXPAT
FindEnvModules
FindFLEX
FindFLTK
FindFLTK2
FindFontconfig
FindFreetype
FindGCCXML
FindGDAL
FindGIF
FindGLEW
FindGLUT
FindGSL
FindGTK
FindGTK2
FindGTest
FindGettext
FindGit
FindGnuTLS
FindGnuplot
FindHDF5
FindHSPELL
FindHTMLHelp
FindHg
FindICU
FindITK
FindIce
FindIconv
FindIcotool
FindImageMagick
FindIntl
FindJNI
FindJPEG
FindJasper
FindJava
FindKDE3
FindKDE4
FindLAPACK
FindLATEX
FindLTTngUST
FindLibArchive
FindLibLZMA
FindLibXml2
FindLibXslt
FindLibinput
FindLua
FindLua50
FindLua51
FindMFC
FindMPEG
FindMPEG2
FindMPI
FindMatlab
FindMotif
FindODBC
FindOpenACC
FindOpenAL
FindOpenCL
FindOpenGL
FindOpenMP
FindOpenSSL
FindOpenSceneGraph
FindOpenThreads
FindPHP4
FindPNG
FindPackageHandleStandardArgs
FindPackageMessage
FindPatch
FindPerl
FindPerlLibs
FindPhysFS
FindPike
FindPkgConfig
FindPostgreSQL
FindProducer
FindProtobuf
FindPython
FindPython2
FindPython3
FindPythonInterp
FindPythonLibs
FindQt
FindQt3
FindQt4
FindQuickTime
FindRTI
FindRuby
FindSDL
FindSDL_image
FindSDL_mixer
FindSDL_net
FindSDL_sound
FindSDL_ttf
FindSQLite3
FindSWIG
FindSelfPackers
FindSquish
FindSubversion
FindTCL
FindTIFF
FindTclStub
FindTclsh
FindThreads
FindUnixCommands
FindVTK
FindVulkan
FindWget
FindWish
FindX11
FindXCTest
FindXMLRPC
FindXalanC
FindXercesC
FindZLIB
Findosg
FindosgAnimation
FindosgDB
FindosgFX
FindosgGA
FindosgIntrospection
FindosgManipulator
FindosgParticle
FindosgPresentation
FindosgProducer
FindosgQt
FindosgShadow
FindosgSim
FindosgTerrain
FindosgText
FindosgUtil
FindosgViewer
FindosgVolume
FindosgWidget
Findosg_functions
FindwxWidgets
FindwxWindows
FortranCInterface
GNUInstallDirs
GenerateExportHeader
GetPrerequisites
GoogleTest
InstallRequiredSystemLibraries
MacroAddFileDependencies
ProcessorCount
SelectLibraryConfigurations
SquishTestScript
TestBigEndian
TestCXXAcceptsFlag
TestForANSIForScope
TestForANSIStreamHeaders
TestForSSTREAM
TestForSTDNamespace
UseEcos
UseJava
UseJavaClassFilelist
UseJavaSymlinks
UsePkgConfig
UseSWIG
Use_wxWindows
UsewxWidgets
WriteBasicConfigVersionFile
WriteCompilerDetectionHeade
```

```shell
cmake --help-module FindSQLite3
FindSQLite3
-----------

Find the SQLite libraries, v3

IMPORTED targets
^^^^^^^^^^^^^^^^

This module defines the following ``IMPORTED`` target:

``SQLite::SQLite3``

Result variables
^^^^^^^^^^^^^^^^

This module will set the following variables if found:

``SQLite3_INCLUDE_DIRS``
  where to find sqlite3.h, etc.
``SQLite3_LIBRARIES``
  the libraries to link against to use SQLite3.
``SQLite3_VERSION``
  version of the SQLite3 library found
``SQLite3_FOUND``
  TRUE if found
```

cmake find_package()
https://blog.csdn.net/haluoluo211/article/details/80559341

.cmake文件

E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-linux-dbg\cmake_install.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\CMakeFiles\Export\share\protobuf\protobuf-targets.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\CMakeFiles\Export\share\protobuf\protobuf-targets-debug.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\share\protobuf\protobuf-targets.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\share\protobuf\protobuf-config-version.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\share\protobuf\protobuf-options.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\share\protobuf\protobuf-module.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\share\protobuf\protobuf-config.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\CMakeFiles\3.14.0\CMakeSystem.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\CMakeFiles\3.14.0\CMakeCXXCompiler.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\CMakeFiles\3.14.0\CMakeCCompiler.cmake
E:\$RECYCLE.BIN\S-1-5-21-1699714220-3637226014-2084147787-123785\$R0NDEFH\buildtrees\protobuf\x64-osx-dbg\cmake_install.cmake
>>>>>>> 6faa5abd105d9ac215af4c26599be94f269ae80a



add_test(NAME uuid_generator COMMAND uuid_generator)

理论上只需要find_package()就可以引入一个三方库
没有最佳实践
没有资金支持


在 gRPC 的 CMakeLists.txt 文件中，c-ares 的 find_package 模式为 CONFIG（find_package(c-ares CONFIG) ），关于 find_package() 模式的解释如下：
find_package()包括module模式和config模式。
在module模式下，CMake搜索所有名为Find<package>.cmake的文件，这些文件的路径由变量由安装CMake时指定的CMAKE_MODULE_PATH变量指定。如果查找到了该文件，它会被CMake读取并被处理。如果没有找到文件，则进入config模式。
Config 模式，继续搜索<Name>config.cmake 或<low-case-name>config.cmake文件，这两个文件是安装库自动安装的。



- cpack

- ctest



https://blog.csdn.net/wlhwaii/article/details/88026673



[add thread pthread](https://www.zhihu.com/question/37189523)



CMake

参考mysql项目源码，同一个cmake项目，可以有多个可执行文件

cpp不支持module

CmakeList.txt也可以有多个
maven pom.xml也可以有多个





cmake入门

核心观点：**Learning by Doing.** 

边做边学，由浅入深，以问题驱动自己去做。比如

1.如何使用CMake创建一个可执行程序

2.如何创建一个动态库／静态库，如何配合第三方库

3.如何支持不同平台不同编译器以及其参数，如何用CMake组织多层目录的项目

4.如何自定义CMake Target

5.如何使用CMake调用外部工具等等。

学习也不用想着100%都知道了才能开始做，这对于CMake这样的工具是更加不可取的做法。无论如何，推荐一个材料叫CMake实践，搜索这个名字"CMake实践 PDF"就会出来相应的pdf。

而CMake的好处在于什么呢？一个巨大的好处就在于你不用去折腾平台了，Windows你需要创建Visual Studio项目文件，还是如何？Linux创建Makefile？OS X创建Xcode项目文件？编译选项呢？实际上大部分你的配置都会是一样的，使用CMake会给你很好的项目维护性，也会降低你的维护成本。

抽象

定义cmakefile.txt



 `CMAKE_INSTALL_PREFIX`  

https://packages.ubuntu.com/eoan/all/rapidjson-dev/filelist 



```
/usr/lib/cmake/RapidJSON/RapidJSONConfig.cmake
/usr/lib/cmake/RapidJSON/RapidJSONConfigVersion.cmake
```



cmake修改文件 复制文件 获取git信息

 https://blog.csdn.net/qq_38410730/article/details/103741579 



find_package
是寻找
packageConfig.cmake
cpacage_config.cmake

[cmake_root not set module not speic](https://blog.csdn.net/lichen18848950451/article/details/79912265)



cmake可以多模块编译

gn

xmake支持cuda



参考moduo的cmakelists.txt

leveldb



[muduo](https://github.com/chenshuo/muduo/blob/master/CMakeLists.txt)





 list(APPEND CXX_FLAGS "-Wno-null-dereference") 



`**CMD#51: list** `列表操作命令。

```
  　　list(LENGTH <list> <output variable>)
  　　list(GET <list> <element index> [<element index> ...] <output variable>)
  　　list(APPEND <list> <element> [<element> ...])
  　　list(FIND <list> <value> <output variable>)
  　　list(INSERT <list> <element_index> <element> [<element> ...])
  　　list(REMOVE_ITEM <list> <value> [<value> ...])
  　　list(REMOVE_AT <list> <index> [<index> ...])
  　　list(REMOVE_DUPLICATES <list>)
  　　list(REVERSE <list>)
  　　list(SORT <list>)
```

　　使用LENGTH选项时，该命令会返回给定list的长度。

　　使用GET选项时，该命令返回list中所有被index索引的元素构成的list。

　　使用APPEND选项时，该命令将会在该list之后追加若干元素。

　　使用FIND选项时，该命令将返回list中指定的元素的索引；若果未找到，返回-1。

　　使用INSERT选项时，该命令将在list中指定的位置插入若干元素。

　　使用REMOVE_AT和REMOVE_ITEM选项将会从list中删除一些元素。它们之间的区别是：REMOVE_ITEM删除的是指定的项，而REMOVE_AT删除的是在指定索引处的项。

　　使用REMOVE_DUPLICATES选项时，该命令将删除list中的重复项。

　　使用REVERSE选项时，该命令将把list的内容就地前后倒换。

　　使用SORT选项时，该命令将按字母序对list总的内容就地排序。

　　注意：在CMake中，一个list是一个由封号;分割的一组字符串。使用set命令可以创建一个list。例如，set(var a b c d e)命令将会创建一个list：a;b;c;d;e；而set(var "a b c d e")命令创建的只是一个字符串，或者说是只有一个项的list。

　　当使用指定索引的命令格式时，如果<element index>是大于等于0的数，<element index>是从list第一个项开始的序号，list的第一项的索引是0。如果<element index>小于等于-1，这个索引是从结尾开始的逆向索引，其中-1表示的是list的最后一项。当使用负数索引时，注意它们不是从0开始！-0与0等价，它指向list的第一个成员。



[CMake 手册详解](https://blog.csdn.net/jiayizhenzhenyijia/article/details/98851886)



 find_package(CURL) 

if(CURL_FOUND)
  message(STATUS "found curl")
endif()


find_path(CARES_INCLUDE_DIR ares.h)
find_library(CARES_LIBRARY NAMES cares)


if(CARES_INCLUDE_DIR AND CARES_LIBRARY)
  message(STATUS "found cares")
endif()


[caffe的CMakeList.txt注释](https://blog.csdn.net/fuzi2012/article/details/72454532/)



 CMAKE_BUILD_TYPE 



[cmake 常用变量、常用环境变量、常用语法总结](https://blog.csdn.net/bytxl/article/details/50634868)



# cmake:环境变量(environment variable)读写和if判断



[cmake语法-STREQUAL](https://blog.csdn.net/10km/article/details/51769633)



# cmake语法-STREQUAL

 **STREQUAL** 用于比较字符串，相同返回 **true** 。 



### option

 option(MUDUO_BUILD_EXAMPLES "Build Muduo examples" ON) 



[CMake----if与option使用小记](https://www.cnblogs.com/rickyk/p/3872568.html)





- [cmaketest](https://github.com/edidada/cmaketest)
- 



cmake .."-DCMAKE_TOOLCHAIN_FILE=D:\vcpkg-master\vcpkg\scripts\buildsystems\vcpkg.cmake" -G"Visual Studio 14"

https://blog.csdn.net/kasteluo/article/details/81384746


cmake --check-system-vars

cmake 库有多个，顺序是？

CmakeLists.txt 
.cmake文件 作用

[cmake手册 私人撰写](https://chenxiaowei.gitbook.io/cmake-cookbook/4.0-chinese/4.4-chinese)

# README

.a 可以用压缩工具打开

.so库文件如何设置

https://blog.csdn.net/ktigerhero3

[大型项目CMakeLIsts.txt的编写规范](https://blog.csdn.net/dongfang1984/article/details/55105537)

[多目录工程的CmakeLists.txt编写](https://blog.csdn.net/ktigerhero3/article/details/70313350)

### cmake
生成makefile ninja.build之类的文件
Generator支持多种
不同操作系统支持的generator不同


[cmakelists.txt+添加子文件夹的cmakelists.txt](https://blog.csdn.net/u012258999/article/details/87161613)

```shell script
project(mainproject VERSION 1.0.0 LANGUAGES C CXX)
```
cmake是版本2.8时报错


```shell script
/home/edidada/cmake-3.14.7-Linux-x86_64/bin/cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=/usr/bin/gcc -DCMAKE_CXX_COMPILER=/usr/bin/g++ -G "CodeBlocks - Unix Makefiles" /home/edidada/CLionProjects/cmaketest
CMake Warning (dev) at anotherproject/CMakeLists.txt:2 (project):
  Policy CMP0048 is not set: project() command manages VERSION variables.
  Run "cmake --help-policy CMP0048" for policy details.  Use the cmake_policy
  command to set the policy and suppress this warning.

  The following variable(s) would be set to empty:

    PROJECT_VERSION
    PROJECT_VERSION_MAJOR
    PROJECT_VERSION_MINOR
    PROJECT_VERSION_PATCH
This warning is for project developers.  Use -Wno-dev to suppress it.

-- Configuring done
-- Generating done
-- Build files have been written to: /home/edidada/CLionProjects/cmaketest/cmake-build-debug

[Finished]

```

一种是用了的，设置cmake的版本为3.8
一种是`cmake_policy(SET CMP0048 NEW)`


[cmake 添加头文件目录，链接动态、静态库](https://www.cnblogs.com/binbinjx/p/5626916.html)

maven中也可以设置java版本
cmake中可以设置gcc g++版本

[cmake中使用c++11](https://blog.csdn.net/sohu_2011/article/details/51276884)


不添加c++11直接运行报错

```shell script
====================[ Build | stdarray | Debug ]================================
/home/edidada/cmake-3.14.7-Linux-x86_64/bin/cmake --build /home/edidada/CLionProjects/testc11/cmake-build-debug --target stdarray -- -j 2
Scanning dependencies of target stdarray
[ 50%] Building CXX object CMakeFiles/stdarray.dir/stdarray.cpp.o
In file included from /usr/include/c++/5/array:35:0,
                 from /home/edidada/CLionProjects/testc11/stdarray.cpp:5:
/usr/include/c++/5/bits/c++0x_warning.h:32:2: error: #error This file requires compiler and library support for the ISO C++ 2011 standard. This support must be enabled with the -std=c++11 or -std=gnu++11 compiler options.
 #error This file requires compiler and library support \
  ^
/home/edidada/CLionProjects/testc11/stdarray.cpp: In function ‘int main()’:
/home/edidada/CLionProjects/testc11/stdarray.cpp:10:5: error: ‘array’ is not a member of ‘std’
     std::array<int, 3> a1{ {1,2,3} };  // double-braces required
     ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:10:16: error: expected primary-expression before ‘int’
     std::array<int, 3> a1{ {1,2,3} };  // double-braces required
                ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:11:5: error: ‘array’ is not a member of ‘std’
     std::array<int, 3> a2 = {1, 2, 3}; // except after =
     ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:11:16: error: expected primary-expression before ‘int’
     std::array<int, 3> a2 = {1, 2, 3}; // except after =
                ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:12:5: error: ‘array’ is not a member of ‘std’
     std::array<std::string, 2> a3 = { {std::string("a"), "b"} };
     ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:12:27: error: expected primary-expression before ‘,’ token
     std::array<std::string, 2> a3 = { {std::string("a"), "b"} };
                           ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:12:32: error: ‘a3’ was not declared in this scope
     std::array<std::string, 2> a3 = { {std::string("a"), "b"} };
                                ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:12:63: warning: extended initializer lists only available with -std=c++11 or -std=gnu++11
     std::array<std::string, 2> a3 = { {std::string("a"), "b"} };
                                                               ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:15:15: error: ‘a1’ was not declared in this scope
     std::sort(a1.begin(), a1.end());
               ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:16:23: error: ‘a2’ was not declared in this scope
     std::reverse_copy(a2.begin(), a2.end(), 
                       ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:22:15: error: ISO C++ forbids declaration of ‘s’ with no type [-fpermissive]
     for(auto& s: a3)
               ^
/home/edidada/CLionProjects/testc11/stdarray.cpp:22:18: warning: range-based ‘for’ loops only available with -std=c++11 or -std=gnu++11
     for(auto& s: a3)
                  ^
make[3]: *** [CMakeFiles/stdarray.dir/stdarray.cpp.o] Error 1
make[2]: *** [CMakeFiles/stdarray.dir/all] Error 2
make[1]: *** [CMakeFiles/stdarray.dir/rule] Error 2
make: *** [stdarray] Error 2
```



```

"D:\Program Files\CMake\bin\cmake.exe" ..  -A x64 -DCMAKE_TOOLCHAIN_FILE="D:\vcpkg\scripts\buildsystems\vcpkg.cmake"
-- Building for: Visual Studio 16 2019
-- The C compiler identification is MSVC 19.23.28106.4
-- The CXX compiler identification is MSVC 19.23.28106.4
-- Check for working C compiler: C:/Program Files (x86)/Microsoft Visual Studio/2019/BuildTools/VC/Tools/MSVC/14.23.28105/bin/Hostx64/x64/cl.exe
-- Check for working C compiler: C:/Program Files (x86)/Microsoft Visual Studio/2019/BuildTools/VC/Tools/MSVC/14.23.28105/bin/Hostx64/x64/cl.exe -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done
-- Check for working CXX compiler: C:/Program Files (x86)/Microsoft Visual Studio/2019/BuildTools/VC/Tools/MSVC/14.23.28105/bin/Hostx64/x64/cl.exe
-- Check for working CXX compiler: C:/Program Files (x86)/Microsoft Visual Studio/2019/BuildTools/VC/Tools/MSVC/14.23.28105/bin/Hostx64/x64/cl.exe -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Found ZLIB: optimized;D:/vcpkg/installed/x64-windows/lib/zlib.lib;debug;D:/vcpkg/installed/x64-windows/debug/lib/zlibd.lib (found version "1.2.11")
-- Found OpenSSL: D:/vcpkg/installed/x64-windows/debug/lib/libeay32.lib (found version "1.0.2s")
CMake Error at D:/vcpkg/scripts/buildsystems/vcpkg.cmake:263 (_find_package):
  Found package configuration file:

    D:/vcpkg/installed/x64-windows/share/poco/PocoConfig.cmake

  but it set Poco_FOUND to FALSE so package "Poco" is considered to be NOT
  FOUND.  Reason given by package:

  The Poco package requires at least one component

Call Stack (most recent call first):
  CMakeLists.txt:31 (find_package)


-- Configuring incomplete, errors occurred!
See also "D:/visual studio 2015/Projects/CMakeWindowsCppRestSdk/cmmm/CMakeFiles/CMakeOutput.log".

D:\visual studio 2015\Projects\CMakeWindowsCppRestSdk\cmmm>subl D:/vcpkg/installed/x64-windows/share/poco/PocoConfig.cmake

```




-A x64
设置64bit架构
默认是32bit

https://blog.csdn.net/linuxheik/article/details/74626996

CMakeWindowsCppRestSdk项目

cpprestsdk没例子
cpp-netlib
Poco
这两个报错


```
# CMake 最低版本号要求
cmake_minimum_required (VERSION 2.8)
# 项目信息
project (Demo3)
# 查找当前目录下的所有源文件
# 并将名称保存到 DIR_SRCS 变量
aux_source_directory(. DIR_SRCS)
# 添加头文件路径
include_directories("${PROJECT_SOURCE_DIR}/math")
# 添加 math 子目录
add_subdirectory(math)
# 指定生成目标
add_executable(Demo main.c)
# 添加链接库
target_link_libraries(Demo MathFunctions)

```


```

add_library(archive archive.cpp zip.cpp lzma.cpp)
add_executable(zipapp zipapp.cpp)
target_link_libraries(zipapp archive)

```

- SHARED
- STATIC
- MODULE
- OBJECT


https://www.kancloud.cn/itfanr/cmake-practice/82989

1，CMAKE_BINARY_DIR PROJECT_BINARY_DIR _BINARY_DIR

这三个变量指代的内容是一致的，如果是in source 编译，指得就是工程顶层目录，如果是out-of-source 编译，指的是工程编译发生的目录。PROJECT_BINARY_DIR 跟其他指令稍有区别，现在，你可以理解为他们是一致的。


cmake-build-debug

vs支持cmake

参考mysql项目源码，同一个cmake项目，可以有多个可执行文件

CmakeList.txt也可以有多个

多module

add_subdirectory

[CMake多模块的构建方式](http://www.leadroyal.cn/?p=781)

需要看文档和实践

module

maven pom.xml也可以有多个

https://docs.microsoft.com//cpp/build/cmake-projects-in-visual-studio?view=vs-2019



多看官方文档



生成makefile文件的

跨平台



Clion支持

`include(TestBigEndian)`
TestBigEndian.cmake

[find_package与CMake如何查找链接库详解](https://blog.csdn.net/bytxl/article/details/50637277)

cmake有哪些内置的模块?

https://github.com/Kitware/CMake/tree/master/Modules

FindZLIB.cmake
Findosg.cmake
TestBigEndian.cmake
CheckIncludeFile.cmake
CheckLibraryExists.cmake

`check_library_exists`

[c++ - 使用CMAKE，如何使用CHECK_LIBRARY_EXISTS检查C++库](https://www.ojit.com/article/1713263)





cmake target_link_libraries private public



add_library STATIC SHARED



cmake添加变量

```
cmake -DOPENSSL_ROOT_DIR=/usr/include/openssl -DOPENSSL_LIBRARIES=/usr/local/ssl/lib
```



## 

[cmake 安装和测试](https://www.hahack.com/codes/cmake/)



定制安装规则
首先先在 math/CMakeLists.txt 文件里添加下面两行：


###### 指定 MathFunctions 库的安装路径
install (TARGETS MathFunctions DESTINATION bin)
install (FILES MathFunctions.h DESTINATION include)
指明 MathFunctions 库的安装路径。之后同样修改根目录的 CMakeLists 文件，在末尾添加下面几行：

###### 指定安装路径
install (TARGETS Demo DESTINATION bin)
install (FILES "${PROJECT_BINARY_DIR}/config.h"
         DESTINATION include)
通过上面的定制，生成的 Demo 文件和 MathFunctions 函数库 libMathFunctions.o 文件将会被复制到 /usr/local/bin 中，而 MathFunctions.h 和生成的 config.h 文件则会被复制到 /usr/local/include 中。我们可以验证一下（顺带一提的是，这里的 /usr/local/ 是默认安装到的根目录，可以通过修改 CMAKE_INSTALL_PREFIX 变量的值来指定这些文件应该拷贝到哪个根目录）：


[ehome@xman Demo5]$ sudo make install
[ 50%] Built target MathFunctions
[100%] Built target Demo
Install the project...
-- Install configuration: ""
-- Installing: /usr/local/bin/Demo
-- Installing: /usr/local/include/config.h
-- Installing: /usr/local/bin/libMathFunctions.a
-- Up-to-date: /usr/local/include/MathFunctions.h
[ehome@xman Demo5]$ ls /usr/local/bin
Demo  libMathFunctions.a
[ehome@xman Demo5]$ ls /usr/local/include
config.h  MathFunctions.h
为工程添加测试
添加测试同样很简单。CMake 提供了一个称为 CTest 的测试工具。我们要做的只是在项目根目录的 CMakeLists 文件中调用一系列的 add_test 命令。


###### 启用测试
enable_testing()

###### 测试程序是否成功运行
add_test (test_run Demo 5 2)

###### 测试帮助信息是否可以正常提示
add_test (test_usage Demo)
set_tests_properties (test_usage
  PROPERTIES PASS_REGULAR_EXPRESSION "Usage: .* base exponent")

###### 测试 5 的平方
add_test (test_5_2 Demo 5 2)

set_tests_properties (test_5_2
 PROPERTIES PASS_REGULAR_EXPRESSION "is 25")

###### 测试 10 的 5 次方
add_test (test_10_5 Demo 10 5)

set_tests_properties (test_10_5
 PROPERTIES PASS_REGULAR_EXPRESSION "is 100000")

###### 测试 2 的 10 次方
add_test (test_2_10 Demo 2 10)

set_tests_properties (test_2_10
 PROPERTIES PASS_REGULAR_EXPRESSION "is 1024")
上面的代码包含了四个测试。第一个测试 test_run 用来测试程序是否成功运行并返回 0 值。剩下的三个测试分别用来测试 5 的 平方、10 的 5 次方、2 的 10 次方是否都能得到正确的结果。其中 PASS_REGULAR_EXPRESSION 用来测试输出是否包含后面跟着的字符串。

让我们看看测试的结果：


[ehome@xman Demo5]$ make test
Running tests...
Test project /home/ehome/Documents/programming/C/power/Demo5
    Start 1: test_run
1/4 Test #1: test_run .........................   Passed    0.00 sec
    Start 2: test_5_2
2/4 Test #2: test_5_2 .........................   Passed    0.00 sec
    Start 3: test_10_5
3/4 Test #3: test_10_5 ........................   Passed    0.00 sec
    Start 4: test_2_10
4/4 Test #4: test_2_10 ........................   Passed    0.00 sec

100% tests passed, 0 tests failed out of 4

Total Test time (real) =   0.01 sec
如果要测试更多的输入数据，像上面那样一个个写测试用例未免太繁琐。这时可以通过编写宏来实现：

###### 定义一个宏，用来简化测试工作
macro (do_test arg1 arg2 result)
  add_test (test_${arg1}_${arg2} Demo ${arg1} ${arg2})
  set_tests_properties (test_${arg1}_${arg2}
    PROPERTIES PASS_REGULAR_EXPRESSION ${result})
endmacro (do_test)

# 使用该宏进行一系列的数据测试
do_test (5 2 "is 25")
do_test (10 5 "is 100000")
do_test (2 10 "is 1024")
关于 CTest 的更详细的用法可以通过 man 1 ctest 参考 CTest 的文档。

支持 gdb
让 CMake 支持 gdb 的设置也很容易，只需要指定 Debug 模式下开启 -g 选项：

set(CMAKE_BUILD_TYPE "Debug")
set(CMAKE_CXX_FLAGS_DEBUG "$ENV{CXXFLAGS} -O0 -Wall -g -ggdb")
set(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -O3 -Wall")
之后可以直接对生成的程序使用 gdb 来调试。

