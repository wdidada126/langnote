# bazelisk

https://www.zhihu.com/question/350144630/answer/1785938148

实际上现在 bazel 并不需要安装了。 bazelbuild 官方 git 组织提供了更好的使用方式。 在 bazelisk 仓库。个人推荐的使用方式是结合 git submodule 使用。mkdir -p thirdparty tools
git submodule add https://github.com/bazelbuild/bazelisk thirdparty/
cd tools && ln -s ../thirdparty/bazelisk/bazelisk.py .
echo "thirdparty/bazelisk" > .bazelignore
echo "4.0.0" > .bazelversion剩下的就是在使用 bazel 的时候，全部替换为 ./tools/bazelisk.py 就可以了。如 bazel build //... 替换为 ./tools/bazelisk.py build //...bazelisk 脚本会自动搜索 .bazelversion 中的版本，检查当前系统中有无安装 bazel, 并且是否版本匹配。如果不匹配则会从 git release 下载一个合适的版本存储在本地，然后配置好路径。

类似gradle wrapper
maven wrapper

Bzlmod优先：Bazel 8将移除WORKSPACE，建议迁移至MODULE.bazel1。
混合模式：Bazel 7允许同时使用MODULE.bazel和WORKSPACE，但可能冲突。

人工智能框架
PyTorch TensorFlow

https://github.com/pytorch/pytorch
https://github.com/pytorch/pytorch/blob/main/.bazelignore

https://github.com/bazelbuild/bazelisk
Bazelisk 可以：

将Bazel自动更新到最新的LTS或滚动版本。
使用 .bazelversion文件中指定的Bazel版本构建项目。将该文件签入版本控制系统，以确保build的可重现性。
帮助迁移项目以适应不兼容的更改（见上文）
轻松试用候选版本

.bazelversion
文件，就是版本号

```shell
bazelisk build //:main2 --verbose_failures
2025/07/22 14:33:43 Downloading https://releases.bazel.build/5.1.0/release/bazel-5.1.0-windows-x86_64.exe...
Downloading: 44 MB out of 44 MB (100%) 
Extracting Bazel installation...
Starting local Bazel server and connecting to it...
ERROR: D:/develops/git/github/c/testlibevent/WORKSPACE:1:21: fetching new_local_repository rule //external:libevent: java.io.IOException: The repository's path is "/usr/local/Cellar/libevent/2.1.12" (absolute: "/usr/local/Cellar/libevent/2.1.12") but this directory does not exist.
ERROR: D:/develops/git/github/c/testlibevent/BUILD:2:10: //:main2 depends on @libevent//:libevent in repository @libevent which failed to fetch. no such package '@libevent//': The repository's path is "/usr/local/Cellar/libevent/2.1.12" (absolute: "/usr/local/Cellar/libevent/2.1.12") but this directory does not exist.   
ERROR: Analysis of target '//:main2' failed; build aborted: Analysis failed
INFO: Elapsed time: 5.990s
INFO: 0 processes.
FAILED: Build did NOT complete successfully (33 packages loaded, 127 targets configured)
    Fetching @local_config_cc; Restarting.
```

下载的文件bazel-5.1.0-windows-x86_64.exe在
C:\Users\wdidada\AppData\Local\bazelisk\downloads

C:\Users\wdidada\AppData\Local\bazelisk\downloads\sha256\edda0b9e5481931e9162a231a837eb8c8154a5904e93a344f2205e8b96f9b8f2\bin\bazel.exe version
WARNING: Invoking Bazel in batch mode since it is not invoked from within a workspace (below a directory having a WORKSPACE file).
Build label: 5.1.0
Build target: bazel-out/x64_windows-opt/bin/src/main/java/com/google/devtools/build/lib/bazel/BazelServer_deploy.jar
Build time: Thu Mar 24 14:03:32 2022 (1648130612)
Build timestamp: 1648130612
Build timestamp as int: 1648130612


C:\Users\wdidada\AppData\Local\bazelisk\downloads\sha256\a3349d1d9e2327e03344c47244d4832ab14fc78142d050aa5599d85ee26b5f79\bin\bazel.exe version
WARNING: Invoking Bazel in batch mode since it is not invoked from within a workspace (below a directory having a MODULE.bazel file).
OpenJDK 64-Bit Server VM warning: Options -Xverify:none and -noverify were deprecated in JDK 13 and will likely be removed in a future release.
Build label: 8.3.1
Build target: @@//src/main/java/com/google/devtools/build/lib/bazel:BazelServer
Build time: Mon Jun 30 16:26:17 2025 (1751300777)
Build timestamp: 1751300777
Build timestamp as int: 1751300777
