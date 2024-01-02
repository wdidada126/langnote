# bazel

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


### 安装
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

```shell

```

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
