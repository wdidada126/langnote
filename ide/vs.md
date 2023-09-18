# visual studio
Vs code团队负责人：Erich Gamma . JUnit 作者之一，《设计模式》作者之一， Eclipse 架构师。2011 加入微软，在瑞士苏黎世组建团队开发基于 web 技术的编辑器，也就是后来的 monaco-editor。VSCode 开发团队从 10 来个人开始，早期成员大多有 Eclipse 开发团队的背景。

VS可以连接远程服务器调试，还要啥Clion啊

测试了下，远程服务器新安装库，在本地vs上提示找不到头文件

使用VS编写Linux程序，可以将VS连接到Linux上，却出现了VS IDE中找不到
#include <sys/socket.h>这类系统头文件的情况，可以将Linux中 /usr/include/ 目录 手动拷贝到windows的
C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\VC\Linux\include\usr\ 位置

https://blog.csdn.net/weixin_43327696/article/details/106463764

D:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\VC\Linux\include\usr\include


vs配置头文件和库目录
https://blog.csdn.net/y24283648/article/details/109517407


https://blog.csdn.net/weixin_44144762/article/details/127467173

MSVC 没有完整支持 20 年前的 C99 标准。你看下是否适合吧。MSVC 实现的标准 C 功能有：完整的 C94 （ C89 + 后续宽字符支持）不完整的 C99 语核（缺复合字面量、非常量长度数组、 T [static N] 函数参数等）少数 C11 中标准化的扩展（如匿名 struct/union 成员）C99 标准库包含于 C++ 的 C11 标准库部分（有少量缺失）与 C11 标准略有区别的 _s 系列函数基本上还是不要把 MSVC 当成用 C 开发的东西了。如果需要 VS 的话可以考虑 Visual Studio + Clang 。

vla
https://en.wikipedia.org/wiki/Variable-length_array


visual studio linux c++ 开发

个人使用的话，推荐微软Visual Studio 2022社区版，安装时把C++ 跨平台开发相关选项勾上，会自动安装MSVC、Clang和GCC三种编译器，开发Windows应用时使用MSVC，开发Linux/安卓/iOS平台应用时视情况选择Clang或GCC。

测试可用：
Visual Studio 2022 Professional
TD244-P4NB7-YQ6XK-Y8MMM-YWV2J
Visual Studio 2022 Enterprise
VHF9H-NXBBB-638P6-6JHCY-88JWH

clang-tools:可视化C ++中的继承关系的工具

VS2019怎么设置启动项?
在解决方案管理器中，右键点击项目，然后在弹出菜单中选择“设为启动项目”。
