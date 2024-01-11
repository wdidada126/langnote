# gradle

G:\gradle\cache\caches\modules-2\files-2.1
## 依赖版本管理
    testCompile group: 'junit', name: 'junit', version: '4.+'

    版本号支持通配符
    maven支持通配符吗？
    npm是支持的

局部变量
https://dongchuan.gitbooks.io/gradle-user-guide-/content/writing_build_scripts/local_variables.html

## slack
https://gradle-community.slack.com/

gradle init --type pom
`gradle init --type pom`命令行的作用是初始化一个Gradle项目，并将项目类型设置为POM（Project Object Model）。
执行`gradle init --type pom`命令行后，会在当前目录下生成一个名为`build.gradle`的Gradle构建脚本文件和一个名为`settings.gradle`的Gradle设置文件。同时，还会在项目根目录下生成一个`src`源代码文件夹。这些文件是Gradle项目的基础结构，用于定义项目的构建规则和依赖管理等。

maven可以打包成jar包，gradle如何打包成jar包
mvn可以使用antlr生成.java文件，gradle如何打包
mvn可以调用本地的protoc命令行文件，gradle如何组织

## 竞品
apt
dnf
yum
ant
maven

## gradle版本和windows版本关系
Gradle 8.4 需要的 Java 版本是 JDK 11。

$env:JAVA_HOME = "D:\Java\jdk-11.0.4"

## 使用gradle的开源项目
https://github.com/elastic/elasticsearch
spring

## 仓库
gradle可以使用maven的库仓库
mavenLocal() 使用本地仓库

## 插件
antlr
java
eclipse
idea
spring-boot
war 网页应用
protoc
https://github.com/google/protobuf-gradle-plugin

### android plugin
https://developer.android.com/build/releases/gradle-plugin?hl=zh-cn

### java插件
https://docs.gradle.org/7.3/userguide/java_plugin.html
https://docs.gradle.org/current/userguide/java_plugin.html

src/sourceSet/java
src/sourceSet/resources
Java 插件引入了资源设置 (Source Set) 的概念, 资源设置就是一组被编译和执行在一起的源文件. 这些源文件可能包含 Java 的源文件以及一些资源文件. 其他的插件可能还会在资源设置中包含 Groovy 和 Scala 的源文件. 资源设置有一个与之关联的关于编译的 classpath 和有关运行的 classpath.

资源设置的用法之一就是将源文件归档到描述它们目的的各个逻辑组, 举个例子, 你可以使用一个资源设置来定义一个集成测试套件 也可以使用另外的资源设来定义你项目的 API 和实现类.

Java 插件定义了两个标准资源设置, 分别称为main和test, main资源设置中包含最终面向客户的代码, 也就是编译和集成为一个 Jar 文件. test资源设置包括了测试阶段的代码, 也就是使用 JUnit 或者 TestNG 编译和执行的代码. 它们可以是单元测试, 集成测试, 验收测试或者任何对你有用的测试集.
https://dongchuan.gitbooks.io/gradle-user-guide-/content/the_java_plugin/java_plugin_source_sets.html

java 插件-任务
compileJava
processResources
https://dongchuan.gitbooks.io/gradle-user-guide-/content/the_java_plugin/java_plugin_tasks.html

Gradle 默认在 src/main/java 目录下寻找到你的正式（生产）源码, 在 src/test/java 目录下寻找到你的测试源码, 并在src/main/resources目录下寻找到你准备打包进jar的资源文件。测试代码会被加入到环境变量中设置的目录里运行。所有的输出文件都会被创建在构建目录里, 生成的JAR文件会被存放在 build/libs 目录下.


查看gradle插件是否存在？
https://plugins.gradle.org/plugin/com.gradle.build-scan/3.2.2

网页上显示 https://plugins.gradle.org/plugin/com.gradle.build-scan/3.2.2

gradle如何解决依赖冲突

```grovvy
task checkDependencyConflict {
    doLast {
        configurations.compile.allDependencies.each { dep ->
            println "Checking dependency: ${dep.name} - ${dep.version}"
            configurations.compile.incoming.resolutionResult.allDependencies.each { incoming ->
                if (dep.name.equals(incoming.name) && dep.version != incoming.version) {
                    println "Dependency conflict detected: ${dep.name} - ${dep.version} and ${incoming.version}"
                }
            }
        }
    }
}
```

Gradle可以使用dependencyInsight任务来检查jar包依赖是否存在冲突。该任务可以列出指定依赖的所有版本以及它们之间的依赖关系，并标识出依赖冲突的地方。

以下是使用dependencyInsight任务检查依赖冲突的示例：
gradle dependencyInsight --dependency commons-collections

gradle dependencies 打印jar包依赖
Gradle自带了很多任务，以下是一些常见的任务：
1. `build`：构建项目，包括编译、测试、打包等操作。
2. `clean`：清除项目构建产物和临时文件。
3. `assemble`：打包项目，生成可分发的应用程序或库。
4. `check`：运行所有测试任务，检查项目的正确性和稳定性。
5. `test`：运行所有测试用例。
6. `install`：将项目构建产物安装到本地Maven或Ivy仓库。
7. `dependencies`：列出所有的依赖关系。
8. `tasks`：列出所有可用的任务。
9. `help`：显示Gradle帮助信息。

除了上述常用任务，还有一些其他的任务，例如：
1. `init`：生成一个初始的Gradle构建文件。
2. `wrapper`：生成Gradle Wrapper脚本，用于在没有安装Gradle的机器上执行Gradle构建。
3. `eclipse`：生成Eclipse项目文件。
4. `idea`：生成IntelliJ IDEA项目文件。
5. `publish`：将项目构建产物发布到指定的Maven或Ivy仓库。

需要注意的是，不同的插件可能会定义自己的任务，因此可以通过查看插件文档或使用`tasks`任务来了解所有可用的任务。

总的来说，Gradle自带了很多任务，可以通过这些任务来构建、测试和打包项目，以及管理依赖关系和发布构建产物等。

https://gradle.org/

要设置环境变量GRADLE_HOME和GRADLE_USER_HOME，可以按照以下步骤在Windows上进行操作：

打开Windows操作系统的环境变量设置：
在开始菜单中搜索"环境变量"，然后点击"编辑系统环境变量"；
或者在"此电脑"上右键点击，选择"属性"，然后点击"高级系统设置"，在弹出的窗口中点击"环境变量"按钮。
在"系统属性"窗口的"高级"选项卡中，点击"环境变量"按钮。
在"环境变量"窗口中，可以编辑或添加新的系统环境变量。
对于GRADLE_HOME，在"变量名"中输入GRADLE_HOME，在"变量值"中输入Gradle的安装目录路径。例如，如果Gradle安装在C:\gradle\gradle-6.7，那么将GRADLE_HOME设置为这个路径。
对于GRADLE_USER_HOME，在"变量名"中输入GRADLE_USER_HOME，在"变量值"中输入你想要设置为用户主目录的路径。例如，可以将其设置为C:\Users\YourUsername\.gradle。
点击"确定"保存更改。

现在，你已经成功设置了环境变量GRADLE_HOME和GRADLE_USER_HOME。可以在命令行窗口中使用这些环境变量，例如运行Gradle命令时将使用这些路径。

设置环境变量
- GRADLE_HOME
- GRADLE_USER_HOME

G:\gradle

gradle -v

------------------------------------------------------------
Gradle 5.1.1
------------------------------------------------------------

Build time:   2019-01-10 23:05:02 UTC
Revision:     3c9abb645fb83932c44e8610642393ad62116807

Kotlin DSL:   1.1.1
Kotlin:       1.3.11
Groovy:       2.5.4
Ant:          Apache Ant(TM) version 1.9.13 compiled on July 10 2018
JVM:          1.8.0_231 (Oracle Corporation 25.231-b11)
OS:           Windows 10 10.0 amd64


GRADLE_USER_HOME/cache是Gradle用户目录下的缓存文件夹，用于存储Gradle的本地缓存文件。在这个文件夹中，Gradle会保存已经下载的依赖项和其他构建过程中生成的临时文件。
具体来说，GRADLE_USER_HOME/cache文件夹包含以下子文件夹：
caches/modules-2: 该文件夹包含所有已下载的依赖项的jar包和其他文件。Gradle会按照依赖关系和版本号的组合来组织该文件夹中的目录结构。
caches/transforms-2: 该文件夹包含由Gradle执行的所有转换操作生成的临时文件。例如，当Gradle将Java源代码编译成字节码时，会生成相应的.class文件，并将其保存在该文件夹中。
caches/file-changes-2: 该文件夹包含Gradle对文件系统中的文件进行监视时生成的临时文件。例如，当Gradle监视项目中的源代码文件时，会生成相应的元数据文件，并将其保存在该文件夹中。
通过将GRADLE_USER_HOME/cache文件夹设置为共享文件夹，可以让多个Gradle项目共享本地缓存文件，从而提高构建效率。需要注意的是，如果多个项目使用相同的依赖项和版本号，Gradle会重复使用缓存中的文件，从而避免重复下载和构建相同的文件。
需要注意的是，GRADLE_USER_HOME/cache文件夹是Gradle 6.0及更高版本中的新特性。在旧版本的Gradle中，缓存文件夹位于GRADLE_USER_HOME/.gradle/caches文件夹中。

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

gradle组织公司的项目

testgradle github项目
https://github.com/edidada/testcomplexgradle
https://github.com/edidada/testgradle
https://github.com/edidada/protocExampleProject
构建产物在build/文件夹下

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

### spring是gradle组织的，如何发布jar包到本电脑上的maven仓库？

参考gradle实战 这本书

gradle 发布 maven 仓库

## gradle不同版本大陆快速下载 版本

gradle安装包国内下载以及maven仓库配置以及其他注意点-CSDN博客.mhtml

https://mirrors.cloud.tencent.com/gradle/

8.5, released on 29 Nov 2023
v8.4 Oct 04, 2023

v7.6.3 Oct 04, 2023

v7.0 Apr 09, 2021

v6.0 Nov 08, 2019

v5.0 Nov 26, 2018
