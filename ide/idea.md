# IDEA
核心技术是Program Structure Interface数据结构，也叫PSI，相当于一个加强版的AST，适配了各种语言，不但解析了语法，还分析了语义。信息量吊打vscode的LSP

idea 打开java文件
The file size (2.8 MB) exceeds the configured limit (2.56 MB). Code insight features are not available. 
当 IntelliJ IDEA 打开 Java 文件时提示 “The file size (2.8 MB) exceeds the configured limit (2.56 MB). Code insight features are not available.”，是因为 IDEA 对能关联的文件大小做了限制，主要是为了保护内存。默认情况下，IDEA 允许提供代码洞察功能的文件大小限制为 2.5 MB 左右（2500 KB），而你打开的 Java 文件大小为 2.8 MB，超过了这个限制，所以会出现该提示，并且代码洞察功能（如代码补全、跳转定义等）将不可用。

要解决这个问题，可以通过以下步骤修改文件大小限制：
1. 打开 IDEA 的菜单，选择 “Help”（帮助）→“Edit Custom Properties”（编辑自定义属性）。这会打开 `idea.properties` 文件，如果该文件不存在，IDEA 会自动创建。
2. 在 `idea.properties` 文件中，添加或修改 `idea.max.intellisense.file size` 属性的值。例如，将其设置为 `5000` 或更大的值，单位是 KB。如果原来文件中存在 `idea.max.intellisense.file size = 2500` 这样的配置，将 `2500` 修改为你想要的值即可；如果文件中没有该属性，则直接添加 `idea.max.intellisense.file size = 5000`。
3. 保存 `idea.properties` 文件并关闭。
4. 重启 IntelliJ IDEA，使修改后的配置生效。

修改文件大小限制可能会对 IDE 的性能产生影响，尤其是在处理非常大的文件时。因此，在调整这些设置之前，最好先评估一下对系统性能的影响。如果可能的话，尽量保持文件大小合理，或者考虑将大文件拆分成多个较小的文件来管理。


账号：Lindsay_Kaschmitter
密码：kj@b$hRR

按下Ctrl+Alt+L快捷键。IDEA将自动对文件中的代码进行格式化，包括JSON字符串。

big data tools
Big Data Tools是IntelliJ IDEA Ultimate的新插件,是为使用Zeppelin和Spark的数据工程师和其他专业人员所量身定做的一款软件。

## IDEA
多余的import需要删掉，不然代码用sts打开，有warn

idea java 取消import * import 类全路径

https://www.cnblogs.com/leonbond/p/6638200.html

idea取消import_星.png

## debug

watch 变量

可以修改代码，热更新的

升级IDEA会与lombok版本不匹配，会出现这个问题，java 找不到符号

idea，debug断点的时候，选择变量，watch

查看一个类的类图，查看类有哪些方法
在Windows/Linux上，可以按下 Ctrl + Alt + Shift + U 快捷键。


## App Password
If you use non-latest JetBrains products and it isn't prompting you to enter a one-time password, use App Password instead of your regular password for sign in.

947s3bed7v8puusfz4f0xe66h

## 官方文档
https://www.jetbrains.com/zh-cn/opensource/idea/

https://plugins.jetbrains.com/docs/intellij/welcome.html?from=jetbrains.org

https://www.jetbrains.com/help/idea/remote-development-starting-page.html#space_integration

## EasyCode

https://plugins.jetbrains.com/plugin/10954-easycode
基于IntelliJ IDEA开发的代码生成插件，支持自定义任意模板（Java，html，js，xml）。
只要是与数据库相关的代码都可以通过自定义模板来生成。支持数据库类型与java类型映射关系配置。
支持同时生成生成多张表的代码。每张表有独立的配置信息。完全的个性化定义，规则由你设置。

toolbox
https://www.jetbrains.com/toolbox-app/

IDEA 可以同时打开多个maven项目，不用挨个打开
eclipse可以同时打开多个项目

IDEA快捷键 等于号前面的类型可以自动生成

IDEA实现序列化接口Serializable自动生成serialVersionUID
Settings->Editor->inspect->Serialable without id 选上
IDEA  generateAllSetter插件

https://github.com/gejun123456/intellij-generateAllSetMethod

Ctrl Enter

IDEA插件

1. FindBugs-IDEA 2. Maven Helper 3. VisualVM Launcher 4. GenerateAllSetter 5. Rainbow Brackets 6. Translation 7. P3c

java命令行执行程序，增加-D参数
idea run configure ，vm options

idea自动调用所有set开头的方法
安装使用GenerateAllSetter插件
https://blog.csdn.net/dkm123456/article/details/122999227

你可以使用像Soot这样的框架来分析Java字节码并生成控制流图。Soot 是一个用于分析和转换 Java 和 Android 应用程序的框架，它提供了丰富的API来构建和操作控制流图。
其他类似的工具包括JDT（Java Development Tools）和Jimple，它们也可以用来分析 Java 代码并生成控制流图。

Control Flow Graphs  https://plugins.jetbrains.com/plugin/23074-javaflowdiagram/versions#tabs
Call Trees           IDEA看代码必备插件Call Graph
Call-By Trees
Include Tree
Butterfly Graph
Declaration Graphs
Depends On and Depended on By
Everything this file depends on
Data Members
Object References
UML Class Diagram  自带
UML Sequence Diagrams 插件 安装插件 - SequenceDiagram
Overrides
Dependency Graphs
Base and Derived Graphs
Architecture Graphs
Compare – Butterfly Graph
Compare – Control Flow
Project Overview Graphs
Custom Graphs

### 自带的类图
类图不显示方法，可以设置显示方法

Translation插件 中英翻译

understand查看大型项目，生成调用链

idea查看函数调用链
IDEA完整的调用链显示P
idea时序图显示完整方法调用链
安装插件 - SequenceDiagram
https://vanco.github.io/SequencePlugin/
https://plugins.jetbrains.com/plugin/8286-sequence-diagram
选中需要生成调用链的方法，右键，选中“Sequence Diagram”


反向类图 时序图
一、检查UML类图插件是否开启
IDEA默认已经集成了该功能，只是默认没打开，我们要手动打开它，参考下图：
File——Settings——Plugins——UML Support：
https://blog.csdn.net/zj420964597/article/details/87856758

idea所有操作系统版本通用的
idea设置新建类模板

IDEA创建类模板和方法模板（超详细）
https://blog.csdn.net/sdut406/article/details/81750858

### Windows版本IDEA
Java OO
Ctrl - H 查看类继承关系
Ctrl - N 查找类
Alt - 7 查看当前类所有的方法
【CTRL+ALT+T】 将光标定位到这段代码,按快捷键,try catch快捷键

![exception capture](../imgs/20201117214347.png)

### git冲突解决

IDEA解决git冲突
先执行'git add'命令

### MAC版本IDEA查找接口的实现类：
IDEA 风格 ctrl+h
windows

IDEA 区分大小写 查找 CTrl -F
选择“Aa”

Ctrl+f12 查看

https://blog.csdn.net/weixin_36210698/article/details/78564252

https://www.cnblogs.com/exmyth/p/5949192.html

https://blog.csdn.net/qq_35625303/article/details/80346402


IntelliJ IDEA中用快捷键自动创建测试类的默认按键为：

ctrl+shift+t  --> create new test


https://blog.csdn.net/fanrenxiang/article/details/80497977

[IntelliJ IDEA 设置编码为utf-8编码](https://blog.csdn.net/m0_38132361/article/details/80628203)


[IDEA可以添加jetty tomcat等容器的servlet等jar包](https://blog.csdn.net/u013393958/article/details/78329192)


https://www.iteye.com/blog/baowp-1989575

#### IDEA debug时，可以改变变量的值
条件变量

Mac 回到上一次光标的位置
Alt command 箭头

mac windows下的IDEA快捷键不同
[IDEA Debug模式下改变各类型变量值](https://blog.csdn.net/Peng_Hong_fu/article/details/79994860)

Ctrl P
copy reference 复制类的全路径
[IDEA中右侧出现hidden字样的处理方法](https://blog.csdn.net/budaoweng0609/article/details/87860205)
[IDEA中修改文件的默认打开方式](https://blog.csdn.net/u010814849/article/details/77675532)
[如何在IDEA中高效地使用和查找TODO标签](https://jingyan.baidu.com/article/ff42efa9c25811c19e2202ef.html)
[IDEA maven 无法下载源码](https://blog.csdn.net/weixin_33709590/article/details/92383254)
`mvn dependency:resolve -Dclassifier=sources`

IDEA Spring bean是否存在 提示信息
Windows，IntelliJ IDEA中用快捷键自动创建测类的默认按键为：

ctrl+shift+T  --> create new test
IntelliJ IDEA中用快捷键自动创建测类的默认按键为：

ctrl+shift+t  --> create new test

https://stackoverflow.com/questions/42966889/intellij-IDEA-tells-me-errorjava-compilation-failed-internal-java-compiler-e

https://jingyan.baidu.com/article/29697b9163ac7dab20de3cbf.html

全局搜索  Ctrl Shift F

https://jingyan.baidu.com/article/29697b9163ac7dab20de3cbf.html


### IDEA快捷键

[IntelliJ IDEA中 查看某个类中的所有方法](https://blog.csdn.net/tb9125256/article/details/81416358)

[Intellij IDEA 查找接口实现类的快捷键](https://blog.csdn.net/HeatDeath/article/details/79468782)


- 添加三方jar


### add jar
Project Struct


Modules Dependencies



IDEA新建Maven项目文件结构
src/main/webapp/WEB-INF

添加submodule
mvn install报错

```shell
[INFO] shardingspheretest 0.0.1 ........................... SUCCESS [  1.287 s]
[INFO] sumodule 0.0.1 ..................................... FAILURE [  1.187 s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 2.935 s
[INFO] Finished at: 2019-03-12T22:08:51+08:00
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.springframework.boot:spring-boot-maven-plugin:2.1.3.RELEASE:repackage (repackage) on project sumodule: Execution repackage of goal org.springframework.boot:spring-boot-maven-plugin:2.1.3.RELEASE:repackage
failed: Unable to find main class -> [Help 1]
[ERROR]
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR]
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/PluginExecutionException
[ERROR]
[ERROR] After correcting the problems, you can resume the build with the command
[ERROR]   mvn <goals> -rf :sumodule
```

submodule中添加main方法

一般的编辑器中关闭当前文件快捷键为ctrl+w，而IDEA中默认为Ctrl+F4，用起来很不顺手。

IDEA class diagrm

https://blog.csdn.net/hy_coming/article/details/80741717

在IDEA中添加try/catch的快捷键 
ctrl+alt+t 
选中想被try/catch包围的语句，同时按下ctrl+alt+t， 

IDEA 生成javadoc步骤：

菜单
Tools
GEnerate JavaDoc scope
Output directory，选择一个文件夹
Other command line arguments:`-encoding UTF-8 `
[错误：编码GBK的不可映射字符](https://www.cnblogs.com/lucky-zhangcd/p/8409810.html)

[用IDEA生成javadoc文档](http://www.cnblogs.com/noKing/p/8006298.html)


[IDEA Error:java: Compilation failed: internal java compiler error](https://www.cnblogs.com/comeluder/p/8215317.html)

Intellij IDEA单元测试覆盖率插件JaCoCo的使用

IDEA中maven可以新建submodule，而不是新建Project

知道类名查找类:Ctrl+Shift+Alt+N; 

Ctrl+N按名字搜索类

Ctrl+Shift+N按文件名搜索文件

Ctrl+H 查看类的继承关系

Ctrl+Alt+B

Ctrl G linenumbr:XX
跳转到指定行

IDEA查找类的方法：
Ctrl F12

IDEA中查看某个类中的所有方法
alt + 7 （可以查看类的字段、属性、方法，是否继承等）

[IntelliJ IDEA全局内容搜索和替换](https://blog.csdn.net/gnail_oug/article/details/78281354)

Ctrl+H 查看类继承关系

IDEA Spring项目，配置bean的时候，Java代码可以跳转到xml文件


#### IDEA配置变异

ar
含义





断点 IDEA条件 IDEA选中断点 右键



IDEA mac ctrl o或者Shift Ctrl F

Win ctrl n 查找类

https://www.jianshu.com/p/9812be1f746d


idea断点增加代码

IDEA年付账号
zhou39287513@163.com

565%Wiseism

Lindsay_Kaschmitter
kj@b$hRR

失效日期：
October 17, 2025
