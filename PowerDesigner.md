# PowerDesigner
windows电脑 sap PowerDesigner

## odbc
使用ODBC连接MySQL数据库是一个相对复杂的过程，因为ODBC是专为Windows操作系统设计的

## sap PowerDesigner vs sybase PowerDesigner
SAP PowerDesigner和Sybase PowerDesigner都是数据建模工具，用于设计和优化数据库结构。它们都支持多种数据库系统，包括Oracle、Microsoft SQL Server、IBM DB2等。

然而，SAP PowerDesigner是由SAP公司开发的，而Sybase PowerDesigner是由Sybase公司开发的。因此，它们在功能和界面上可能存在一些差异。

以下是它们的一些主要区别：
1. 厂商支持：SAP PowerDesigner由SAP公司提供支持，而Sybase PowerDesigner则由Sybase公司提供支持。这意味着如果您遇到问题或需要帮助，您可能需要联系不同的技术支持团队。
2. 价格：SAP PowerDesigner和Sybase PowerDesigner的价格可能有所不同。具体价格取决于您购买的版本和许可类型。
3. 功能：虽然两者都具有类似的功能，但在某些方面可能会有所不同。例如，SAP PowerDesigner可能具有一些特定于SAP应用程序的功能，而Sybase PowerDesigner可能具有一些特定于Sybase应用程序的功能。
4. 兼容性：由于它们是针对不同的数据库系统进行设计的，因此它们可能在与某些数据库系统的兼容性方面存在差异。例如，SAP PowerDesigner可能更好地支持Oracle数据库，而Sybase PowerDesigner可能更好地支持Sybase数据库。
总之，选择SAP PowerDesigner还是Sybase PowerDesigner取决于您的具体需求和偏好。建议您根据自己的情况仔细比较两者的功能、价格和支持等因素，并选择最适合您的工具。


sap 2023最新版本
16.7 SP01

https://www.sap.com/products/technology-platform/powerdesigner-data-modeling-tools.html#get-started

https://www.sybase.com/products/modeling-data-analysis/powerdesigner
Sybase
pdlegacyshell16.exe

可以设计表之间依赖关系

join

可以追踪表设计的变化

可以根据现有数据库导出表er图

32bit jdk

windows 破解版导出sql文件有问题

PowerDesigner 创建表格及导出SQL语句
https://blog.csdn.net/weixin_42179326/article/details/80399400

PowerDesigner 16 32bit
http://www.xue51.com/soft/10174.html

百度网盘 提取码
提取码：04o0

32位的可以安装并激活
64位的不可以
https://www.onlinedown.net/soft/577763.htm

## PowerDesigner模块
PowerDesigner包含六大模块：
1. 用于数据发现的[ProcessAnalyst]模块
2. 用于双层，交互式的数据库设计和构造的[ataArchitect]模块
3. 用于物理建模和应用对象及数据敏感组件的生成的[AppModeler]模块
4. 用于高级的团队开发，信息的共享和模型的管理的[MetaWorks]模块　
5. 用于数据仓库的设计和实现的[WarehouseArchitect]模块　　
6. 用于以只读的、图形化方式访问整个企业的模型信息的[Viewer]模块
以上6大模块共同构成了一套完整的集成化企业级建模解决方案。

数据库表修改后，能够直接映射到数据库表吗？

PowerDesigner如何将设计的表更新到数据库中
https://blog.csdn.net/weixin_34034261/article/details/94033219
这样，你就完成了表的更新。但是，注意这种方法的缺点，这种更新是需要先删除掉表，再创建，如果你有重要数据，请先备份，不然后悔莫及。

工具栏不见了
调色板(Palette)快捷工具栏不见了
PowerDesigner快捷工具栏 palette不见了，怎么重新打开，找回来呢
上网搜索了一下“powerdesigner图形工具栏”,找到了找回PowerDesigner工具栏palette的方法
Tools（工具栏）
customsize toolbars（自定义工具栏）
palette(调色板)勾选
https://blog.csdn.net/gulijiang2008/article/details/7836151?locationNum=1

## sap powerdesigner导入表结构

PowerDesigner导入SQL脚本_51CTO博客_powerdesigner导入sql文件.mhtml

java 8 32位
https://blog.csdn.net/aoeace/article/details/102545337

## sap powerdesigner新建带箭头的外键
toolbox 选择Physical Diagram，Reference，拖拽到画布上

D:\git\github\langnote\imgs\pd_toolbox.png


## 待解决的问题
搜索table，知道哪些表在项目上，哪些表不在
pk fk标志

