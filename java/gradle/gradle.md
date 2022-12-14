# gradle

设置环境变量
- GRADLE_HOME
- GRADLE_USER_HOME


要使用 ANTLR 插件，请在构建脚本中包含以下语句：
示例 40.1. 使用 ANTLR 插件
build.gradle
apply plugin: 'antlr'



gradle命令行

gradle init --dsl kotli


```shell
gradle -h

USAGE: gradle [option...] [task...]

-?, -h, --help            Shows this help message.
-a, --no-rebuild          Do not rebuild project dependencies.
-b, --build-file          Specify the build file.
--build-cache             Enables the Gradle build cache. Gradle will try to reuse outputs from previous builds.
-c, --settings-file       Specify the settings file.
--configure-on-demand     Configure necessary projects only. Gradle will attempt to reduce configuration time for large multi-project builds. [inc
ubating]
--console                 Specifies which type of console output to generate. Values are 'plain', 'auto' (default), 'rich' or 'verbose'.
--continue                Continue task execution after a task failure.
-D, --system-prop         Set system property of the JVM (e.g. -Dmyprop=myvalue).
-d, --debug               Log in debug mode (includes normal stacktrace).
--daemon                  Uses the Gradle Daemon to run the build. Starts the Daemon if not running.
--foreground              Starts the Gradle Daemon in the foreground.
-g, --gradle-user-home    Specifies the gradle user home directory.
-I, --init-script         Specify an initialization script.
-i, --info                Set log level to info.
--include-build           Include the specified build in the composite.
-m, --dry-run             Run the builds with all task actions disabled.
--max-workers             Configure the number of concurrent workers Gradle is allowed to use.
--no-build-cache          Disables the Gradle build cache.
--no-configure-on-demand  Disables the use of configuration on demand. [incubating]
--no-daemon               Do not use the Gradle daemon to run the build. Useful occasionally if you have configured Gradle to always run with the
daemon by default.
--no-parallel             Disables parallel execution to build projects.
--no-scan                 Disables the creation of a build scan. For more information about build scans, please visit https://gradle.com/build-sca
ns.
--offline                 Execute the build without accessing network resources.
-P, --project-prop        Set project property for the build script (e.g. -Pmyprop=myvalue).
-p, --project-dir         Specifies the start directory for Gradle. Defaults to current directory.
--parallel                Build projects in parallel. Gradle will attempt to determine the optimal number of executor threads to use.
--priority                Specifies the scheduling priority for the Gradle daemon and all processes launched by it. Values are 'normal' (default)
or 'low' [incubating]
--profile                 Profile build execution time and generates a report in the <build_dir>/reports/profile directory.
--project-cache-dir       Specify the project-specific cache directory. Defaults to .gradle in the root project directory.
-q, --quiet               Log errors only.
--refresh-dependencies    Refresh the state of dependencies.
--rerun-tasks             Ignore previously cached task results.
-S, --full-stacktrace     Print out the full (very verbose) stacktrace for all exceptions.
-s, --stacktrace          Print out the stacktrace for all exceptions.
--scan                    Creates a build scan. Gradle will emit a warning if the build scan plugin has not been applied. (https://gradle.com/buil
d-scans)
--status                  Shows status of running and recently stopped Gradle Daemon(s).
--stop                    Stops the Gradle Daemon if it is running.
-t, --continuous          Enables continuous build. Gradle does not exit and will re-execute tasks when task file inputs change.
--update-locks            Perform a partial update of the dependency lock, letting passed in module notations change version. [incubating]
-v, --version             Print version info.
-w, --warn                Set log level to warn.
--warning-mode            Specifies which mode of warnings to generate. Values are 'all', 'summary'(default) or 'none'
--write-locks             Persists dependency resolution for locked configurations, ignoring existing locking information if it exists [incubating
]
-x, --exclude-task        Specify a task to be excluded from execution.
```



文档中文翻译
https://github.com/msdx/gradledoc

spring ldap 构建系统用gradle，运行失败

grovvy

gradle配置项，有json字符串格式的
有列表格式的

maven
xml格式的

jcenter关闭了？

https://search.maven.org/

[Gretty插件实现Gradle Web项目热部署](https://segmentfault.com/a/1190000020446597)

gradle -q taskname 执行单个任务

build.gradle文件有多个
pom.xml文件有多个
CmakeLists.txt也有多个



jar包下载的位置
Mac系统默认下载到：/Users/(用户名)/.gradle/caches/modules-2/files-2.1
Windows系统默认下载到：C:\Users\(用户名)\.gradle\caches\modules-2\files-2.1

https://book.douban.com/subject/26649087/

https://book.douban.com/subject/26609447/

gradle组织公司的项目

testgradle github项目

build.gradle 配置文件

ninja.build

meson.build

conanfiles.py
conanfilex.txt

grovvy编程语言，可以操作的内容更多，自定义的能力更强


`gradlew tasks`执行一次

gradlew 
mvnw

wapper包装一层，避免gradle maven版本差异

gradle init --type java-application
gradle init --type java-library

https://www.cnblogs.com/wuchaodzxx/p/7084242.html

gradle init --type pom

Gradle Task


Java工程的任务
Java插件在我们的构建中加入了很多任务，我们这篇教程涉及到的任务如下：

assemble任务会编译程序中的源代码，并打包生成Jar文件，这个任务不执行单元测试。
build任务会执行一个完整的项目构建。
clean任务会删除构建目录。
compileJava任务会编译程序中的源代码。
我们还可以执行以下命令得到一个可运行任务及其描述的完整列表：

gradle tasks


java -cp build/classes/main/ cn.wdidada.easyexceltest.EasyexcelApp
java -jar build/libs/GradleWorkSpace-0.1.jar