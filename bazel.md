# bazel

国内大厂使用blade
抖音公司c++技术栈，在腾讯开源blade的基础上改的，可以用最新标准的c++

bazel就是用最新版java写的
bazel 8是Java 21写的，谷歌那帮人是真的牛啊

Build C++
Build Java
Android
iOS

bazel在vcpkg
conan
cargo
xmake

 find ~ -name "bazel"
/home/wdidada/vcpkg/buildtrees/grpc/src/v1.70.1-7044911025.clean/third_party/upb/upb/bazel
/home/wdidada/vcpkg/buildtrees/grpc/src/v1.70.1-7044911025.clean/tools/distrib/python/xds_protos/bazel
/home/wdidada/vcpkg/buildtrees/grpc/src/v1.70.1-7044911025.clean/tools/dockerfile/test/bazel
/home/wdidada/vcpkg/buildtrees/grpc/src/v1.70.1-7044911025.clean/tools/bazel
/home/wdidada/vcpkg/buildtrees/grpc/src/v1.70.1-7044911025.clean/templates/tools/dockerfile/test/bazel
/home/wdidada/vcpkg/buildtrees/grpc/src/v1.70.1-7044911025.clean/bazel
/home/wdidada/vcpkg/buildtrees/grpc/src/v1.70.1-7044911025.clean/test/distrib/bazel
/home/wdidada/vcpkg/buildtrees/grpc/src/v1.70.1-7044911025.clean/test/distrib/bazel/python/tools/bazel
/home/wdidada/vcpkg/buildtrees/grpc/src/v1.70.1-7044911025.clean/test/distrib/bazel/cpp/tools/bazel
/home/wdidada/vcpkg/buildtrees/protobuf/src/v5.29.3-7ac3e413eb.clean/hpb/bazel
/home/wdidada/vcpkg/buildtrees/protobuf/src/v5.29.3-7ac3e413eb.clean/bazel
/home/wdidada/vcpkg/buildtrees/protobuf/src/v5.29.3-7ac3e413eb.clean/upb/bazel
/home/wdidada/vcpkg/buildtrees/utf8-range/src/v5.29.3-03b5e8031c.clean/hpb/bazel
/home/wdidada/vcpkg/buildtrees/utf8-range/src/v5.29.3-03b5e8031c.clean/bazel
/home/wdidada/vcpkg/buildtrees/utf8-range/src/v5.29.3-03b5e8031c.clean/upb/bazel
/home/wdidada/.cache/bazelisk/downloads/sha256/0440ae4581ea5eac5cb36ed0790b1e942778eb81e3ba9bc1326f189427aef0fd/bin/bazel
/home/wdidada/.cache/bazelisk/downloads/sha256/973e213b1e9207ccdd3ea4730c0f92cbef769ec112ac2b84980583220d8db845/bin/bazel
/home/wdidada/.cache/bazel
/home/wdidada/.cache/bazel/_bazel_wdidada/66408b8f62a6061f9d977b9e3d293844/external/rules_cc/third_party/com/github/bazelbuild/bazel
/home/wdidada/.cache/bazel/_bazel_wdidada/install/79570a41fb8272e4808f43403af3b38c/embedded_tools/third_party/grpc/bazel
/home/wdidada/.cache/bazel/_bazel_wdidada/install/cbf972266931ad9fad1857441b832915/embedded_tools/third_party/grpc/bazel
/home/wdidada/.conan2/p/glog67462d74e78d6/s/src/bazel
/home/wdidada/.conan2/p/gflagb709d4ecffc89/s/src/bazel
/home/wdidada/.conan2/p/fmtfd0fc8a6cd618/s/src/support/bazel
/home/wdidada/.conan2/p/b/glog7d156edc2bc5d/b/src/bazel
/home/wdidada/.conan2/p/b/fmtebb950e6d507d/b/src/support/bazel
/home/wdidada/.conan2/p/b/gflag0282a58925f94/b/src/bazel
/home/wdidada/brpc/bazel
/home/wdidada/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/cxx-1.0.153/tools/bazel
/home/wdidada/.xmake/repositories/build-artifacts/packages/b/bazel
/home/wdidada/.xmake/repositories/xmake-repo/packages/b/bazel


bazelisk下载bazel之后
/home/wdidada/.cache/bazelisk/downloads/sha256/0440ae4581ea5eac5cb36ed0790b1e942778eb81e3ba9bc1326f189427aef0fd/bin/bazel
/home/wdidada/.cache/bazelisk/downloads/sha256/973e213b1e9207ccdd3ea4730c0f92cbef769ec112ac2b84980583220d8db845/bin/bazel
/home/wdidada/.cache/bazel
/home/wdidada/.cache/bazel/_bazel_wdidada/66408b8f62a6061f9d977b9e3d293844/external/rules_cc/third_party/com/github/bazelbuild/bazel
/home/wdidada/.cache/bazel/_bazel_wdidada/install/79570a41fb8272e4808f43403af3b38c/embedded_tools/third_party/grpc/bazel
/home/wdidada/.cache/bazel/_bazel_wdidada/install/cbf972266931ad9fad1857441b832915/embedded_tools/third_party/grpc/bazel

@libevent
外部依赖
libevent
内部依赖

## 语言
Starlark

conan python txt
xmake lua
cmake 自定义 txt

## doc
优势：跨语言
资料少
编译缓存
分布式编译

在Bazel 5中，你可以设置编译缓存（remote caching）来加速构建过程。远程缓存允许你将构建输出存储在一个中央位置，并在后续的构建中重用这些输出，即使是在不同的机器上。这可以显著减少重复构建的时间。

Bazel 支持多种类型的远程缓存服务器，包括自托管的解决方案和云服务提供商的产品。下面是如何设置一个基本的 HTTP/HTTPS 缓存服务器 的步骤。

### 步骤一：选择或配置一个缓存服务器

首先，你需要有一个支持HTTP GET 和 PUT请求的缓存服务器。如果你没有现成的服务器，可以考虑以下选项：

- 使用第三方服务：如 Buildbarn、Remote Build Execution (RBE) 等。
- 自建缓存服务器：
  - 使用 Nginx 或 Apache 配置一个简单的文件服务器。
  - 使用专门的工具如 `bazel-remote`，这是一个专为Bazel设计的高效缓存服务器。

#### 示例：安装并运行 `bazel-remote`

1. 安装 `bazel-remote`（假设你使用的是 Linux 系统）：

```bash
wget https://github.com/buchgr/bazel-remote/releases/download/v2.1.1/bazel-remote-linux-amd64
chmod +x bazel-remote-linux-amd64
sudo mv bazel-remote-linux-amd64 /usr/local/bin/bazel-remote
```

2. 启动 `bazel-remote`：

```bash
bazel-remote --max_size=20 --dir=/path/to/cache/dir
```

这里的 `--max_size=20` 表示缓存的最大大小为 20GB，`--dir` 指定了缓存数据存放的目录。

### 步骤二：配置 Bazel 使用远程缓存

接下来，在你的项目中配置 Bazel 来使用这个缓存服务器。你可以通过 `.bazelrc` 文件或命令行参数来指定远程缓存服务器。

#### 方法一：编辑 `.bazelrc`

在项目的根目录下创建或编辑 `.bazelrc` 文件，添加如下内容：

```rc
# 设置远程缓存服务器的 URL
common --remote_cache=http://localhost:8080

# 如果需要认证，可以加上认证信息
# common --remote_cache=http://user:pass@localhost:8080

# 开启结果摘要上传
common --disk_cache=/path/to/disk/cache

# 可选：强制 Bazel 不要重新计算已经存在于缓存中的动作
common --experimental_guard_against_concurrent_changes

# 如果你的缓存服务器不支持 TLS，确保忽略 SSL 错误
# 注意：仅用于测试环境！生产环境中请确保使用安全连接。
common --incompatible_remote_results_ignore_disk
```

#### 方法二：使用命令行参数

你也可以直接在命令行中指定远程缓存服务器，而无需修改 `.bazelrc` 文件：

```bash
bazel build //... --remote_cache=http://localhost:8080
```

### 步骤三：验证配置是否生效

运行一次构建命令后，检查缓存服务器上的缓存数据是否存在。如果一切正常，你应该能在缓存服务器上看到构建输出被成功上传，并且后续的相同构建会从缓存中读取结果，从而加快速度。

### 注意事项

- 安全性：确保你的缓存服务器是安全的，尤其是在公开网络上时。考虑使用 HTTPS 和适当的访问控制。
- 缓存命中率：为了提高缓存命中率，请确保所有参与构建的机器使用相同的工具链版本（如编译器版本等）。
- 磁盘空间管理：定期清理缓存以防止磁盘空间耗尽。某些缓存服务器提供了自动清理策略。

通过以上步骤，你就可以在 Bazel 5 中成功设置并使用远程缓存服务器了。如果有任何问题或需要进一步的帮助，请随时告诉我！

bazel query --output=build //your:target

## bazel
内置模块
cc_binary()
cc_library()
cc_test()

子文件夹编译

## source code

## version
https://github.com/bazelbuild/bazel/releases

8.3.0
2025.07

8.2.0 
2025.04
8.0.0 
Dec 10, 2024

7.0.0
Dec 12, 2023

6.0.0
Dec 20, 2022

## bazel8.3 local
C:\Users\wdidada\_bazel_wdidada\eicgr3kw\external\libevent+\BUILD.bazel
C:\Users\wdidada\_bazel_wdidada\fcx5eyne\external\catch2+\BUILD.bazel

C:\Users\wdidada\_bazel_wdidada\eicgr3kw\execroot\_main\bazel-out\x64_windows-fastbuild\bin\external\libevent+\event_core.lib

## registry

https://registry.bazel.build/search?q=libevent

### source code
https://github.com/bazelbuild/bazel-central-registry

## xx
车企用conan，互联网公司用bazel
高德，头条用Rust

## version

版本号	发布时间	主要特性
6.4.x	2025 年 3 月	改进对 Starlark 的支持、优化远程缓存性能、增强规则兼容性
6.3.x	2025 年 1 月	改进 macOS 和 Windows 构建体验
6.2.x	2024 年 11 月	增强对 C++23 的支持、改进增量构建性能
6.1.x	2024 年 9 月	引入新的 rules_apple 和 rules_swift 支持
6.0.x	2024 年 7 月	重大更新：移除旧版 Python 规则，全面支持 Starlark 规则系统

常见使用场景对应的推荐版本
场景	推荐版本
Android/iOS 开发	6.4.x
C/C++ 项目	6.4.x
TensorFlow 构建	6.4.x 或根据 TF 文档指定版本
兼容老项目（如 2020 年前）	4.x ~ 5.x
学习/教学用途	6.4.x（最新稳定）或 5.4.x（经典）

版本号	发布时间	主要变化
5.4.x	2024 年初	稳定版，广泛用于 Android/iOS 构建
5.0.x	2023 年中	弃用 Skylark，全面启用 Starlark 名称
4.2.x	2021 年末	增加对 remote execution 和 caching 的更好支持
3.7.x	2020 年	最后一个支持 Python 2 的版本
0.4.5	2017 年初	初期稳定版本，被许多项目采用


bazel version
WARNING: --batch mode is deprecated. Please instead explicitly shut down your Bazel server using the command "bazel shutdown".
Build label: 1.1.0
Build target: bazel-out/darwin-opt/bin/src/main/java/com/google/devtools/build/lib/bazel/BazelServer_deploy.jar
Build time: Mon Oct 21 08:47:13 2019 (1571647633)
Build timestamp: 1571647633
Build timestamp as int: 1571647633

bazel从github下载rule
https://github.com/bazelbuild/rules_cc
https://gitee.com/hui2hui/rules_protobuf

## bzlmod

Bazel 6 新增了 bzlmod ，支持了包的多版本管理，可以解决菱形依赖的问题。已经完全成熟可用了。
https://bazel.build/build/bzlmod
11月18日， 特斯拉Autopilot工程师Romi Phadte和Gabriel Gheorghian在2022BazelCon会议上，作了题为“运行数百万次仿真和构建，大规模开发和评估autopilot”的演讲。
https://m.bilibili.com/video/av390471884

IDEA有bazel插件

Bazel 默认支持多种开发语言，如Java，C++，Javascript, Android

iOS官方构建工具不支持增量编译
使用bazel

https://bazel.google.cn/about/intro?hl=zh-cn

为什么我要使用Bazel？
Bazel可以成倍提高构建速度，因为它只重新编译需要重新编译的文件。类似的，它会跳过没有被改变的测试。
Bazel产出确定的结果。这消除了增量和干净构建，开发机器和持续集成之间的构建结果的差异。
Bazel可以使用同一个工程下的相同的工具来构建不同的客户端和服务器端应用程序。例如，你可以在一次提交里修改一个客户端/服务器协议，然后测试更新后的手机程序和服务器端程序能够正常工作，构建时使用的是同样的工具，利用的都是上面提到的Bazel的特性。
我可以看到例子吗？
是的，一个简单的例子，见：
https://github.com/google/bazel/blob/master/examples/cpp/BUILD

https://github.com/bazelbuild/bazel

Bazel源代码本身提供了更复杂的例子，例如：
https://github.com/google/bazel/blob/master/src/main/java/BUILD
https://github.com/google/bazel/blob/master/src/test/java/BUILD

## bazel6

### 安装
yum install bazel4 -y
类似rvm ruby的工具
bazelisk
https://github.com/bazelbuild/bazelisk

https://github.com/bazelbuild/bazelisk/releases
1.19.0

yum install bazel4 -y

windows上支持java？
官方支持的
ubuntu
使用Bazelisk安装/更新Bazel

### 私有仓库
https://registry.bazel.build/

自己构建仓库
https://github.com/bazelbuild/bazel-central-registry/
#### 私有仓库

自己编译运行
bazel-central-registry
--registry 到自己的地址

### 依赖追踪
使用 Bazel 的查询语言跟踪代码中的依赖项。
https://bazel.google.cn/query/guide?hl=zh-cn


### 核心概念
bcr
bazel center register 中央仓库

Bzlmod 将在未来的 Bazel 版本中取代旧版 WORKSPACE 系统

### bazelrc

### windows最佳实践
自 2020 年 1 月 15 日起，不要从 bash 运行 Bazel，要么是通过 MSYS2 shell、Git Bash、Cygwin 或任何其他 Bash 变体运行。


C:\Users\edida\_bazel_edida\install\643682887d9f8f9c0037a92d6b552571


----                 -------------         ------ ----
d-----        2023/12/25      9:19                embedded_tools
d-----        2023/12/25      9:19                platforms
d-----        2023/12/25      9:19                rules_java
-a----        2033/12/22      9:19      121624003 A-server.jar
-a----        2033/12/22      9:19              5 build-label.txt
-a----        2033/12/22      9:19          92160 build-runfiles.exe
-a----        2033/12/22      9:19           9728 cpu_profiler.dll
-a----        2033/12/22      9:19             32 install_base_key
-a----        2033/12/22      9:19           9216 linux-sandbox.exe
-a----        2033/12/22      9:19          12288 process-wrapper.exe
-a----        2033/12/22      9:19            698 xcode-locator

windows上支持java？

sudo apt install apt-transport-https curl gnupg -y
curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg
sudo mv bazel-archive-keyring.gpg /usr/share/keyrings
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
sudo apt update && sudo apt install bazel

embedded_tools
d-----        2023/12/25      9:19                jdk
d-----        2023/12/25      9:19                src
d-----        2023/12/25      9:19                third_party
d-----        2023/12/25      9:19                tools
-a----        2033/12/22      9:19           2010 MODULE.bazel
-a----        2033/12/22      9:19             32 WORKSPACE


platforms
d-----        2023/12/25      9:19                cpu
d-----        2023/12/25      9:19                os
-a----        2033/12/22      9:19            977 BUILD
-a----        2033/12/22      9:19             30 WORKSPACE


## bazel java引入依赖BUILD文件写法

java_library(
    name = "your_library_name",
    srcs = glob(["src/main/java//*.java"]),
    deps = [
        "//path/to/dependency1:dependency1_jar",
        "//path/to/dependency2:dependency2_jar",
        # ...
    ],
)


bazel.exe -h  
WARNING: Invoking Bazel in batch mode since it is not invoked from within a workspace (below a directory having a MODULE.bazel file).
OpenJDK 64-Bit Server VM warning: Options -Xverify:none and -noverify were deprecated in JDK 13 and will likely be removed in a future release.
                                                           [bazel release 8.3.1]
Usage: bazel <command> <options> ...

Available commands:
  analyze-profile     Analyzes build profile data.
  aquery              Analyzes the given targets and queries the action graph.
  build               Builds the specified targets.
  canonicalize-flags  Canonicalizes a list of bazel options.
  clean               Removes output files and optionally stops the server.
  coverage            Generates code coverage report for specified test targets.
  cquery              Loads, analyzes, and queries the specified targets w/ configurations.
  dump                Dumps the internal state of the bazel server process.
  fetch               Fetches external repositories that are prerequisites to the targets.
  help                Prints help for commands, or the index.
  info                Displays runtime info about the bazel server.
  license             Prints the license of this software.
  mobile-install      Installs targets to mobile devices.
  mod                 Queries the Bzlmod external dependency graph
  print_action        Prints the command line args for compiling a file.
  query               Executes a dependency graph query.
  run                 Runs the specified target.
  shutdown            Stops the bazel server.
  sync                Syncs all repositories specified in the workspace file
  test                Builds and runs the specified test targets.
  vendor              Fetches external repositories into a folder specified by the flag --vendor_dir.
  version             Prints version information for bazel.

Getting more help:
  bazel help <command>
                   Prints help and options for <command>.
  bazel help startup_options
                   Options for the JVM hosting bazel.
  bazel help target-syntax
                   Explains the syntax for specifying targets.
  bazel help info-keys
                   Displays a list of keys used by the info command.


bazel build //:hello
Starting local Bazel server (8.3.1) and connecting to it...
Loading: 0 packages loaded
    Fetching repository @@protobuf+; starting 16s
    Fetching repository @@rules_python+; starting 16s
    Fetching repository @@rules_shell+; starting 16s
    Fetching https://github.com/protocolbuffers/protobuf/releases/download/v29.0/protobuf-29.0.zip; 151.2 KiB (1.4%) 13s
    Fetching https://github.com/bazelbuild/rules_python/releases/download/0.40.0/rules_python-0.40.0.tar.gz; 119.3 KiB (14.0%) 13s
    Fetching https://github.com/bazelbuild/rules_shell/releases/download/v0.2.0/rules_shell-v0.2.0.tar.gz; 13.5 KiB (97.9%) 9s
    Fetching repository @@bazel_skylib+; starting
    Fetching repository @@rules_cc+; starting ... (9 fetches)

