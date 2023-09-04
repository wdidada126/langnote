# Understand工具
understand和doxygen。understand擅长基于语法结构浏览代码，doxygen除了基于语法结构外还支持基于注释提供的功能结构浏览代码。如果coder能在注释中利用doxygen提供的group指令描述代码的层次，则doxygen可以根据这些指令在文档中生成相应的链接。另外，doxygen支持的语言相当多，这点比understand强。understand强在生成各种关系图，查询定位准确，支持代码质量分析和统计等doxygen没有或较弱的功能。
除了understand和doxygen以外，ea和visio也能浏览代码，他们强在能自动生成uml图，对于快速浏览类体系结构有帮助。但是在语法分析方面较弱，如果程序中宏定义较多的话，往往会报错，比如qt的代码经常能把ea玩死。
https://blog.csdn.net/eagle11235/article/details/125210975

understand具有以下几个特点：
支持多语言：Ada, C, C++, C#, Java, FORTRAN, Delphi, Jovial, and PL/M ，混合语言的project也支持；
多平台： Windows/Linux/Solaris/HP-UX/IRIX/MAC OS X
代码语法高亮、代码折迭、交叉跳转、书签等基本阅读功能。
可以对整个project的architecture、metrics进行分析并输出报表。
可以对代码生成多种图（butterfly graph、call graph、called by graph、control flow graph、UML class graph等），在图上点击节点可以跳转到对应的源代码位置。
支持Perl API、python，便于扩展。
内置的目录和文件比较器。
支持project的snapshot，并能和自家的TrackBack集成便于监视project的变化。
understand软件有教育版


Source Insight

Source Insight是一个面向项目开发的程序编辑器和代码浏览器，它拥有内置的对C/C++, C#和Java等程序的分析。Source Insight能分析你的源代码并在你工作的同时动态维护它自己的符号数据库，并自动为你显示有用的上下文信息。 Source Insight不仅仅是一个强大的程序编辑器，它还能显示reference trees，class inheritance diagrams和call trees。Source Insight提供了最快速的对源代码的导航和任何程序编辑器的源信

prince2
https://baike.baidu.com/item/PRINCE2/4525398

一直以来，我以为Source Insight的代码分析已经是业界最强、最专业。今天试用了一下Scitools的Understand，导入代码后直接可以生成图形化分析结果，包括模块间调用，函数调用流程等，确实比较震撼。
https://zhuanlan.zhihu.com/p/476563039

*.und 新建项目生成的文件夹

### 两个类的时序图
http://codemx.cn/2016/04/30/Understand01/index.html


SciTools Understand、Source Insight的代码可视化工具？

时序图和调用关系图


https://www.jb51.net/softs/822835.html#downintro2
破解版

淘宝上有购买破解版

Scientific Toolworks Understand是一种静态分析工具，用于维护、测量和分析关键或大型代码库。从指标和图表到依赖分析，用理解掌握您的源代码。

基本指标
* 类数
* 文件数
* 函数数
* 行数
* 空白行数
* 代码行数
* 注释行数
* 非活动行数
* 声明性语句数
* 可执行语句数
* 注释与代码的比率

高级指标(部分列表)
* 圈复杂度
* 结
* 类耦合
* 内聚不足百分比
* 路径计数
* 最大继承
* 基类计数
* 继承的类计数
* 实例方法数
* 每个类的加权方法


自带的例子
https://github.com/TheAlgorithms/Java


生成UML类图、调用树图

默认安装的插件不支持这两种图，需要从官网下载插件。
_//www.scitools.com/perl_scripts/uperl/uml_class.upl
_//www.scitools.com/perl_scripts/uperl/invocation.upl
放到sti/conf/scripts/local目录下。
然后重新运行，执行 project- project graphical views - xxxx可以生成这两种图。


有一款商业化的代码可视化工具sourcetrail。它对于个人使用是免费的，支持Windows、macOS、Linux三大平台。
它支持C/C++与Java，支持CFG流程图，类图，类成员与类之间的调用关系显示效果都还不错，可以试试。