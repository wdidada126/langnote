# cpack

## 例子
antlr4的cpp runtime

## some
GitHub mypersonal cmaketest 仓库

打包一个 两个rpm包



cpack 打包so .h 文件
https://note.qidong.name/2019/11/cmake-cpack-deb/
源码
https://github.com/edidada/cmake-cpack-demo

https://blog.csdn.net/weixin_30477293/article/details/94942747
https://blog.csdn.net/mango9126/article/details/52289485
https://zhuanlan.zhihu.com/p/267803605
https://www.jianshu.com/p/b4529e15c34d

CMake菜谱（CMake Cookbook中文版）
https://www.bookstack.cn/read/CMake-Cookbook/content-chapter11-11.1-chinese.md

yum install rpm-build -y


在cmake build debug文件夹下面
cpack -G RPM --verbose

对应仓库地址https://github.com/edidada/cmaketest.git 

```shell
cpack -G RPM --verbose
CPack: Enable Verbose
CPack Verbose: Read CPack config file: 
CPack Verbose: Read CPack configuration file: /root/cmaketest/cmake-build-debug/CPackConfig.cmake
CPack Verbose: Specified generator: RPM
CPack Verbose: Use generator: cmCPackRPMGenerator
CPack Verbose: For project: mylib1name
CPack: Create package using RPM
CPack Verbose: Read description file: /root/cmake-3.16.6-Linux-x86_64/share/cmake-3.16/Templates/CPack.GenericDescription.txt
CPack Verbose: [RPM] requested component grouping = ONE_PER_GROUP
CPack Verbose: Remove toplevel directory: /root/cmaketest/cmake-build-debug/_CPack_Packages/Linux/RPM
CPack: Install projects
CPack: - Run preinstall target for: cmaketest
CPack: - Install project: cmaketest []
CPack Verbose: Install configuration: "Debug"
CPack: Create package
CPack Verbose: Package files to: /root/cmaketest/cmake-build-debug/_CPack_Packages/Linux/RPM/mylib1name-1.0.0-Linux.rpm
CPack Verbose: Packaging all groups in one package...(CPACK_COMPONENTS_ALL_[GROUPS_]IN_ONE_PACKAGE is set)
CPackRPM:Warning: CPACK_SET_DESTDIR is set (=ON) while requesting a relocatable package (CPACK_RPM_PACKAGE_RELOCATABLE is set): this is not supported, the package won't be relocatable.
CPackRPM: Will use GENERATED spec file: /root/cmaketest/cmake-build-debug/_CPack_Packages/Linux/RPM/SPECS/mylib1name.spec
CPack Verbose: Copying final package(s) [1]:
CPack: - package: /root/cmaketest/cmake-build-debug/mylib1name-1.0.0-Linux.rpm generated.
```



Cpack 打包 二进制 库文件



https://blog.csdn.net/qq_29493353/article/details/90205415

Linux下可以用tar.gz、rpm、zip等格式。



mac

```shell
cpack --help
Usage

  cpack [options]

Options
  -G <generators>              = Override/define CPACK_GENERATOR
  -C <Configuration>           = Specify the project configuration
  -D <var>=<value>             = Set a CPack variable.
  --config <configFile>        = Specify the config file.
  --verbose,-V                 = Enable verbose output
  --trace                      = Put underlying cmake scripts in trace mode.
  --trace-expand               = Put underlying cmake scripts in expanded
                                 trace mode.
  --debug                      = Enable debug output (for CPack developers)
  -P <packageName>             = Override/define CPACK_PACKAGE_NAME
  -R <packageVersion>          = Override/define CPACK_PACKAGE_VERSION
  -B <packageDirectory>        = Override/define CPACK_PACKAGE_DIRECTORY
  --vendor <vendorName>        = Override/define CPACK_PACKAGE_VENDOR
  --help,-help,-usage,-h,-H,/? = Print usage information and exit.
  --version,-version,/V [<f>]  = Print version number and exit.
  --help-full [<f>]            = Print all help manuals and exit.
  --help-manual <man> [<f>]    = Print one help manual and exit.
  --help-manual-list [<f>]     = List help manuals available and exit.
  --help-command <cmd> [<f>]   = Print help for one command and exit.
  --help-command-list [<f>]    = List commands with help available and exit.
  --help-commands [<f>]        = Print cmake-commands manual and exit.
  --help-module <mod> [<f>]    = Print help for one module and exit.
  --help-module-list [<f>]     = List modules with help available and exit.
  --help-modules [<f>]         = Print cmake-modules manual and exit.
  --help-policy <cmp> [<f>]    = Print help for one policy and exit.
  --help-policy-list [<f>]     = List policies with help available and exit.
  --help-policies [<f>]        = Print cmake-policies manual and exit.
  --help-property <prop> [<f>] = Print help for one property and exit.
  --help-property-list [<f>]   = List properties with help available and
                                 exit.
  --help-properties [<f>]      = Print cmake-properties manual and exit.
  --help-variable var [<f>]    = Print help for one variable and exit.
  --help-variable-list [<f>]   = List variables with help available and exit.
  --help-variables [<f>]       = Print cmake-variables manual and exit.

Generators
  7Z                           = 7-Zip file format
  Bundle                       = Mac OSX bundle
  DragNDrop                    = Mac OSX Drag And Drop
  External                     = CPack External packages
  IFW                          = Qt Installer Framework
  NSIS                         = Null Soft Installer
  NSIS64                       = Null Soft Installer (64-bit)
  NuGet                        = NuGet packages
  OSXX11                       = Mac OSX X11 bundle
  PackageMaker                 = Mac OSX Package Maker installer
  STGZ                         = Self extracting Tar GZip compression
  TBZ2                         = Tar BZip2 compression
  TGZ                          = Tar GZip compression
  TXZ                          = Tar XZ compression
  TZ                           = Tar Compress compression
  ZIP                          = ZIP file format
  productbuild                 = Mac OSX pkg
```





centos 7



```shell
cpack --help
cpack version 2.8.12.2
Usage

  cpack -G <generator> [options]

Options
  -G <generator>              = Use the specified generator to generate
                                package.
  -C <Configuration>          = Specify the project configuration
  -D <var>=<value>            = Set a CPack variable.
  --config <config file>      = Specify the config file.
  --verbose,-V                = enable verbose output
  --debug                     = enable debug output (for CPack developers)
  -P <package name>           = override/define CPACK_PACKAGE_NAME
  -R <package version>        = override/define CPACK_PACKAGE_VERSION
  -B <package directory>      = override/define CPACK_PACKAGE_DIRECTORY
  --vendor <vendor name>      = override/define CPACK_PACKAGE_VENDOR
  --help-command cmd [file]   = Print help for a single command and exit.
  --help-command-list [file]  = List available commands and exit.
  --help-commands [file]      = Print help for all commands and exit.
  --help-variable var [file]  = Print help for a single variable and exit.
  --help-variable-list [file] = List documented variables and exit.
  --help-variables [file]     = Print help for all variables and exit.
  --copyright [file]          = Print the CMake copyright and exit.
  --help,-help,-usage,-h,-H,/?= Print usage information and exit.
  --help-full [file]          = Print full help and exit.
  --help-html [file]          = Print full help in HTML format.
  --help-man [file]           = Print full help as a UNIX man page and exit.
  --version,-version,/V [file]= Show program name/version banner and exit.

Generators
  DEB                         = Debian packages
  NSIS                        = Null Soft Installer
  NSIS64                      = Null Soft Installer (64-bit)
  RPM                         = RPM packages
  STGZ                        = Self extracting Tar GZip compression
  TBZ2                        = Tar BZip2 compression
  TGZ                         = Tar GZip compression
  TZ                          = Tar Compress compression
  ZIP                         = ZIP file format
```

ln -s /root/cmake-3.16.6-Linux-x86_64/bin/cpack /usr/bin/cpack


cpack入门

`cpack -G RPM --verbose`

执行 cmake 命令后, 你会发现当前目录下面多了两个文件 **CPackConfig.cmake** 和 **CPackSourceConfig.cmake**。 编译完成后，执行 `cpack -G RPM` 就可将文件打包成 rpm 包，当前目录下会生成一个 **_CPack_Packages** 目录和一个以 .rpm 为后缀名的文件 **example-1.0.0-Linux.rpm**，**example-1.0.0-Linux.rpm** 就是我们想要的安装包文件。
CPack 是根据用户的配置生成_CPack_Packages/Linux/RPM/SPECS/example.spec 文件，然后让 rpm-build 用。
https://zhuanlan.zhihu.com/p/141956373
用到的配置变量是以 CPACK_RPM_XXX 为前缀。最终通过 **rpm-build** 这个工具去打包，所以需要安装 **rpm-build** 这个工具，可以通过 `sudo yum install -y rpm-build` 安装。
```shell
# 设置生成的安装包名字
set(CPACK_PACKAGE_NAME "example")
# 设置支持指定安装目录的控制为 ON                                   
set(CPACK_SET_DESTDIR ON)
# 设置安装到的目录路径
set(CPACK_INSTALL_PREFIX "/home/vesoft/install")   
# 这是生成的安装的版本号信息                       
set(CPACK_PACKAGE_VERSION "1.0.0") 
# 设置 group 名字                                     
set(CPACK_RPM_PACKAGE_GROUP "vesoft")      
# 设置 vendor 名字                             
set(CPACK_PACKAGE_VENDOR "vesoft")    
# 设置 license 信息                                  
set(CPACK_RPM_PACKAGE_LICENSE "Apache 2.0 + Common Clause 1.0")
include(CPack)
```



