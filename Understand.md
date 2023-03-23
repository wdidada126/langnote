# Understand工具


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

