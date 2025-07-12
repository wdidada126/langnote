# bazel

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
使用 Bazelisk 安装 / 更新 Bazel


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
    srcs = glob(["src/main/java/**/*.java"]),
    deps = [
        "//path/to/dependency1:dependency1_jar",
        "//path/to/dependency2:dependency2_jar",
        # ...
    ],
)
