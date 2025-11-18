# Learn LLVM 17
Learn LLVM 17 - Second Edition

https://book.douban.com/subject/36736905/

作者: Kai Nacke / Amy Kwan
出版社: Packt Publishing
副标题: A beginner's guide to learning LLVM compiler tools and core libraries with C++
出版年: 2024-1
页数: 416
装帧: Paperback
ISBN: 9781837631346

https://github.com/edidada/Learn-LLVM-17

构造编译器是一项复杂而迷人的任务。LLVM项目为编译器提供了可重用的组件，LLVM核心库实现了世界级的优化代码生成器，可以为所有主流CPU架构翻译与源语言无关的机器码中间表示，许多编程语言的编译器已经在使用LLVM。
本书将介绍如何实现自己的编译器，以及如何使用LLVM来实现。您将了解编译器的前端如何将源代码转换为抽象语法树，以及如何从中生成中间表示(IR)。此外，还将探索在编译器中添加一个优化管道，可将IR编译为高性能的机器码。
LLVM框架可以通过多种方式进行扩展，读者将了解如何向LLVM添加通道，甚至是一个全新的后端。高级主题，如编译不同的CPU架构和扩展clang和clang静态分析器与自己的插件和检查器也包括在内。本书遵循一种实用的方法，并附有示例源代码，读者可以在自己的项目中应用相应的代码。

作者简介
Kai Nacke是一名专业IT架构师，目前居住在加拿大多伦多。毕业于德国多特蒙德技术大学的计算机科学专业。他关于通用哈希函数的毕业论文，被评为最佳论文。
他在IT行业工作超过20年，在业务和企业应用程序的开发和架构方面有丰富的经验。他在研发一个基于LLVM/Clang的编译器。
几年来，他一直是LDC(基于LLVM的D语言编译器)的维护者。在Packt出版过《D Web Development》一书，他也曾在自由和开源软件开发者欧洲会议(FOSDEM)的LLVM开发者室做过演讲。

随书代码
https://github.com/edidada/Learn-LLVM-17_src


作者致谢 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
关于作者 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
关于审稿者 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
前言 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
新版本增加的内容 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
适读人群 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
本书内容 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
编译环境 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
下载示例 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
联系方式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
欢迎评论 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
第一部分 使用 LLVM 构建编译器的基础知识 . . . . . . . . . . . . . . . . . . . . . . . . . 15
第 1 章 安装 LLVM . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16
1.1. 编译与直接安装 LLVM . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16
1.2. 配置环境 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16
1.2.1. Ubuntu . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
1.2.2. Fedora 和 RedHat . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
1.2.3. FreeBSD . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
1.2.4. OS X . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
1.2.5. Windows . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
1.3. 使用代码库源码进行构建 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
1.3.1. 配置 Git . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
1.3.2. 克隆库 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
1.3.3. 创建构建目录 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
1.3.4. 生成构建系统文件 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
1.3.5. 编译和安装 LLVM . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
1.4. 自定义构建 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22
1.4.1. 可定义的 CMake 变量 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23
1.4.2. 使用 LLVM 定义的构建配置变量 . . . . . . . . . . . . . . . . . . . . . . 24
1.5. 总结 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27
第 2 章 编译器的结构 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28
2.1. 编译器的构建块 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28
2.2. 算术表达式语言 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28
2.2.1. 描述程序设计语言语法的形式 . . . . . . . . . . . . . . . . . . . . . . . . 29
2.2.2. 语法如何帮助编译器作者? . . . . . . . . . . . . . . . . . . . . . . . . . . 29
2.3. 词法分析 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
2.3.1. 手写词法分析器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 30
2.4. 语法分析 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 34
2.4.1. 手写解析器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 34
2.4.1.1 解析器的实现 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 35
2.4.1.2 错误处理 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 37
2.4.2. 抽象语法树 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39
2.5. 语义分析 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 41
2.6. 使用 LLVM 后端生成代码 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 43
2.6.1. LLVM IR 的文本表示 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 44
2.6.2. 使用 AST 生成 IR . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 45
2.6.3. 缺失的部分——驱动程序和运行时库 . . . . . . . . . . . . . . . . . . . . 48
2.6.3.1 构建和测试 calc 应用程序 . . . . . . . . . . . . . . . . . . . . . . . . . . 50
2.7. 总结 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 51
第二部分 从源码到机器码 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 52
第 3 章 将源码文件转换为抽象语法树 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 53
3.1. 定义一种编程语言 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 53
3.2. 项目的目录结构 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 56
3.3. 管理编译器的输入文件 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 56
3.4. 处理用户信息 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 57
3.5. 构造词法分析器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 59
3.6. 构建递归下降语法分析器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 62
3.7. 执行语义分析 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 66
3.7.1. 处理名称作用域 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 67
3.7.2. AST使用LLVM风格的RTTI . . . . . . . . . . . . . . . . . . . . . . . . 69
3.7.3. 创建语义分析器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 70
3.8. 总结 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 75
第 4 章 生成IR代码的基础知识 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 76
4.1. AST生成IR . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 76
4.1.1. 理解IR代码 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 76
4.1.2. 了解加载和存储的方法 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 79
4.1.3. 控制流映射到基本块 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 80
4.2. 使用AST编号生成SSA格式的IR代码 . . . . . . . . . . . . . . . . . . . . . . . . 82
4.2.1. 定义数据结构保存值 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 82
4.2.2. 定义保存值的数据结构 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 83
4.2.3. 前块中搜索值 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 83
4.2.4. 优化生成的 phi 指令 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 85
4.2.5. 密封块 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 86
4.2.6. 生成表达式的IR . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 86
4.2.7. 生成函数的IR . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 87
4.2.8. 通过链接和名称修改控制可见性 . . . . . . . . . . . . . . . . . . . . . . . 87
4.2.9. AST描述类型转换为LLVM类型 . . . . . . . . . . . . . . . . . . . . . . 88
4.2.10. 创建 LLVM IR 函数 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 89
4.2.11. 生成函数体 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 90
4.3. 设置模块和驱动程序 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 91
4.3.1. 代码生成器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 91
4.3.2. 初始化目标机型类 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 92
4.3.3. 生成汇编程文本和目标代码 . . . . . . . . . . . . . . . . . . . . . . . . . 94
4.4. 总结 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 97
第 5 章 高级语言结构生成的 IR . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 98
5.1. 环境要求 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 98
5.2. 处理数组、结构体和指针 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 98
5.3. 获得应用程序二进制接口 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 101
5.4. 为类和虚函数创建 IR . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 102
5.4.1. 实现单继承 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 103
5.4.2. 使用接口扩展单继承 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 106
5.4.3. 增加对多重继承的支持 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 107
5.5. 总结 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 108
第 6 章 生成 IR 代码的进阶知识 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 110
6.1. 抛出和捕获异常 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 110
6.1.1. 抛出异常 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 114
6.1.2. 捕捉异常 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 116
6.1.3. 将异常处理代码集成到应用程序中 . . . . . . . . . . . . . . . . . . . . . 118
6.2. 为基于类型的别名分析生成元数据 . . . . . . . . . . . . . . . . . . . . . . . . . . . 119
6.2.1. 理解对元数据的需求 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 119
6.2.2. LLVM 中创建 TBAA 元数据 . . . . . . . . . . . . . . . . . . . . . . . . . 120
6.2.3. tinylang 中添加 TBAA 元数据 . . . . . . . . . . . . . . . . . . . . . . . . 121
6.3. 生成调试元数据 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 125
6.3.1. 理解调试元数据的一般结构 . . . . . . . . . . . . . . . . . . . . . . . . . 125
6.3.2. 跟踪变量及其值 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 128
6.3.3. 添加行号 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 130
6.3.4. 使 tinylang 支持调试 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 130
6.4. 总结 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 136
第 7 章 优化 IR . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 137
7.1. 环境要求 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 137
7.2. LLVM 通道管理器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 137
7.3. 实现一个新的通道 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 138
7.3.1. 将 ppprofiler 作为插件进行开发 . . . . . . . . . . . . . . . . . . . . . . . 138
7.3.2. 将通道添加到 LLVM 源代码树中 . . . . . . . . . . . . . . . . . . . . . . 142
7.4. 使用 ppprofiler . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 145
7.5. 向编译器添加优化管道 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 150
7.5.1. 创建优化流水线 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 151
7.5.2. 扩展通道流水线 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 155
7.6. 总结 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 157
第三部分 LLVM 的进阶 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 158
第 8 章 TableGen语言 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 159
8.1. 环境要求 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 159
8.2. 了解 TableGen 语言 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 159
8.3. 实验 TableGen 语言 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 160
8.3.1. 定义记录和类 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 160
8.3.2. 使用多个类一次创建多个记录 . . . . . . . . . . . . . . . . . . . . . . . . 163
8.3.3. 模拟函数调用 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 164
8.4. 使用 TableGen 文件生成 C++ 代码 . . . . . . . . . . . . . . . . . . . . . . . . . . . 166
8.4.1. 用 TableGen 语言定义数据 . . . . . . . . . . . . . . . . . . . . . . . . . . 167
8.4.2. 实现 TableGen 后端 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 169
8.5. TableGen 的缺点 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 177
8.6. 总结 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 177
第 9 章 JIT 编译 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 179
9.1. 环境要求 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 179
9.2. LLVM 的整体 JIT 的实现和用例 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 179
9.3. 使用 JIT 直接执行 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 180
9.3.1. 探索 lli 工具 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 180
9.4. 用 LLJIT 实现 JIT 编译器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 182
9.4.1. 将 LLJIT 引擎集成到计算器中 . . . . . . . . . . . . . . . . . . . . . . . . 183
9.4.2. 修改代码生成——支持通过 LLJIT 进行 JIT 编译 . . . . . . . . . . . . . . 186
9.4.3. 构建基于 LLJIT 的计算器 . . . . . . . . . . . . . . . . . . . . . . . . . . . 188
9.5. 从头开始构建 JIT 编译器类 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 191
9.5.1. 创建 JIT 编译器类 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 191
9.5.2. 使用新的 JIT 编译器类 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 197
9.6. 总结 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 200
第 10 章 使用 LLVM 工具进行调试 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 201
10.1. 环境要求 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 201
10.2. 用消毒器检测应用程序 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 201
10.2.1. 使用地址消毒器检测内存访问问题 . . . . . . . . . . . . . . . . . . . . . 201
10.2.2. 使用内存消毒器查找未初始化的内存访问 . . . . . . . . . . . . . . . . . 203
10.2.3. 使用线程消毒器发现数据竞争 . . . . . . . . . . . . . . . . . . . . . . . 204
10.3. 使用libFuzzer查找bug . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 206
10.3.1. 限制和替代方案 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 208
10.4. 使用 XRay 进行性能分析 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 208
10.5. 使用 clang 静态分析器检查源代码 . . . . . . . . . . . . . . . . . . . . . . . . . . . 212
10.5.1. 向 clang 静态分析器添加新的检查器 . . . . . . . . . . . . . . . . . . . . 214
10.6. 创建基于 clang 的工具 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 222
10.7. 总结 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 228
第四部分 创建自定义后端 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 229
第 11 章 目标描述 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 230
11.1. 为新后端做准备 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 230
11.2. 将新架构添加到 Triple 类中 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 230
11.3. 扩展 LLVM 中的 ELF 文件格式定义 . . . . . . . . . . . . . . . . . . . . . . . . . 231
11.4. 创建目标描述 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 233
11.4.1. 添加寄存器定义 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 233
11.4.2. 定义指令格式和指令信息 . . . . . . . . . . . . . . . . . . . . . . . . . . 235
11.4.3. 为目标描述创建顶层文件 . . . . . . . . . . . . . . . . . . . . . . . . . . 238
11.5. 为 LLVM 添加 M88k 后端 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 239
11.6. 实现汇编解析器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 242
11.7. 创建反汇编器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 253
11.8. 总结 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 256
第 12 章 指令选择 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 257
12.1. 定义调用约定规则 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 257
12.1.1. 执行调用约定规则 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 258
12.2. 通过 DAG 进行指令选择 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 258
12.2.1. 简化 DAG——处理合法类型和设置操作 . . . . . . . . . . . . . . . . . . 260
12.2.2. 向下转译 DAG——处理形参 . . . . . . . . . . . . . . . . . . . . . . . . 261
12.2.3. 向下转译 DAG——处理返回值 . . . . . . . . . . . . . . . . . . . . . . . 264
12.2.4. 指令选择中实现 DAG 到 DAG 的转换 . . . . . . . . . . . . . . . . . . . 265
12.3. 添加寄存器和指令信息 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 266
12.4. 向下转译空帧 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 269
12.5. 发出机器指令 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 270
12.6. 创建目标机器和子目标 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 272
12.6.1. 实现 M88kSubtarget . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 272
12.6.2. 实现 M88kTargetMachine——定义 . . . . . . . . . . . . . . . . . . . . . 274
12.6.3. 实现 M88kTargetMachine——添加实现 . . . . . . . . . . . . . . . . . . . 275
12.7. 全局指令的选择 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 278
12.7.1. 向下转译参数和返回值 . . . . . . . . . . . . . . . . . . . . . . . . . . . 279
12.7.2. 通用机器指令合法化 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 281
12.7.3. 为操作数选择一个寄存器库 . . . . . . . . . . . . . . . . . . . . . . . . . 282
12.7.4. 翻译通用机器指令 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 284
12.7.5. 运行一个示例 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 284
12.8. 进化后端 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 284
12.9. 总结 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 285
第 13 章 超越指令选择 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 286
13.1. 为 LLVM 添加新机器功能通道 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 286
13.1.1. 实现了 M88k 目标的顶层接口 . . . . . . . . . . . . . . . . . . . . . . . . 286
13.1.2. 为机器函数通道添加 TargetMachine 实现 . . . . . . . . . . . . . . . . . 286
13.1.3. 开发具体的机器功能通道 . . . . . . . . . . . . . . . . . . . . . . . . . . 288
13.1.4. 构建新实现的机器函数通道 . . . . . . . . . . . . . . . . . . . . . . . . . 293
13.1.5. 使用 llc 运行机器功能通道 . . . . . . . . . . . . . . . . . . . . . . . . . 293
13.2. 将新目标集成到 clang 前端 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 294
13.2.1. clang 中实现驱动程序的集成 . . . . . . . . . . . . . . . . . . . . . . . . 294
13.2.2. clang 中实现对 M88k 的 ABI 支持 . . . . . . . . . . . . . . . . . . . . . 300
13.2.3. clang 中实现对 M88k 工具链的支持 . . . . . . . . . . . . . . . . . . . . 301
13.3.4. 构建具有 clang 集成的 M88k 目标 . . . . . . . . . . . . . . . . . . . . . 304
13.3. 针对不同的 CPU 架构 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 305
13.4. 总结 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 308

## 笔记

### chap.3

LLVM 风格的 RTTI
LLVM 风格的 RTTI 是 LLVM 项目中使用的一种轻量级、高性能的运行时类型识别系统，它替代了 C++ 标准的 RTTI。让我详细解释：

1. 为什么 LLVM 不使用标准 RTTI

1.1 标准 RTTI 的问题

// 标准 C++ RTTI
#include <typeinfo>

class Base {
public:
    virtual ~Base() = default;
};

class Derived : public Base {};

void example() {
    Base* obj = new Derived();
    
    // 开销较大的类型检查
    if (typeid(*obj) == typeid(Derived)) {
        // 动态类型转换
        Derived* d = dynamic_cast<Derived*>(obj);
    }
    
    // 产生 typeinfo 结构，增加二进制大小
}


标准 RTTI 的缺点：
• 性能开销：dynamic_cast 和 typeid 有运行时成本

• 二进制膨胀：每个多态类都会生成 typeinfo 结构

• 可移植性问题：不同编译器实现不一致

• 禁用困难：很多嵌入式系统要求禁用 RTTI

1.2 LLVM 的解决方案

LLVM 实现了自己的轻量级 RTTI 系统，核心思想是：使用枚举和静态分派代替动态类型检查。

2. LLVM RTTI 的核心机制

2.1 isa<> 模板

#include "llvm/Support/Casting.h"

class Value {
public:
    // 枚举定义类型
    enum ValueKind {
        InstructionVal,
        BasicBlockVal,
        FunctionVal,
        // ... 其他类型
    };
    
private:
    const ValueKind Kind;
    
public:
    Value(ValueKind K) : Kind(K) {}
    ValueKind getValueID() const { return Kind; }
};

class Instruction : public Value {
public:
    Instruction() : Value(InstructionVal) {}
};

class Function : public Value {
public:
    Function() : Value(FunctionVal) {}
};

// 使用 isa<> 进行类型检查
Value* V = /* ... */;
if (isa<Instruction>(V)) {
    // V 是指令类型
    Instruction* I = cast<Instruction>(V);
}


2.2 cast<> 和 dyn_cast<>

// 安全转换：如果类型不匹配会断言失败
Instruction* I = cast<Instruction>(V);

// 安全转换：如果类型不匹配返回 nullptr
if (Instruction* I = dyn_cast<Instruction>(V)) {
    // 转换成功，使用 I
    I->someMethod();
}

// 不抛异常的转换
Instruction* I = dyn_cast_or_null<Instruction>(V);
if (I) {
    // 使用 I
}


3. 实现自定义 LLVM 风格 RTTI

3.1 基础实现

// 自定义类层次结构的 LLVM RTTI
class MyBase {
public:
    // 类型枚举
    enum Kind {
        Derived1Kind,
        Derived2Kind,
        Derived3Kind
    };
    
private:
    Kind kind;
    
protected:
    MyBase(Kind K) : kind(K) {}
    
public:
    Kind getKind() const { return kind; }
    
    // 模板方法供 isa<> 使用
    static bool classof(const MyBase* B) {
        return true; // 基类匹配所有派生类
    }
};

class Derived1 : public MyBase {
public:
    Derived1() : MyBase(Derived1Kind) {}
    
    static bool classof(const MyBase* B) {
        return B->getKind() == Derived1Kind;
    }
};

class Derived2 : public MyBase {
public:
    Derived2() : MyBase(Derived2Kind) {}
    
    static bool classof(const MyBase* B) {
        return B->getKind() == Derived2Kind;
    }
};


3.2 复杂继承层次

// 多级继承的 RTTI
class ASTNode {
public:
    enum NodeKind {
        ExprKind,
        StmtKind,
        DeclKind
    };
    
private:
    NodeKind kind;
    
protected:
    ASTNode(NodeKind K) : kind(K) {}
    
public:
    NodeKind getKind() const { return kind; }
    
    static bool classof(const ASTNode* N) {
        return true;
    }
};

class Expr : public ASTNode {
protected:
    Expr(NodeKind K) : ASTNode(K) {}
    
public:
    static bool classof(const ASTNode* N) {
        return N->getKind() >= ExprKind && N->getKind() <= DeclKind;
    }
};

class BinaryExpr : public Expr {
public:
    BinaryExpr() : Expr(ExprKind) {}
    
    static bool classof(const ASTNode* N) {
        return N->getKind() == ExprKind;
    }
};


4. LLVM 中的实际应用

4.1 Value 类层次结构

// LLVM IR 中的 Value 类
class Value {
public:
    enum ValueTy {
        // 指令类型
        InstructionVal,
        BasicBlockVal, 
        FunctionVal,
        
        // 常量类型
        ConstantIntVal,
        ConstantFPVal,
        
        // 其他类型
        ArgumentVal,
        GlobalVariableVal
    };
    
private:
    ValueTy Ty;
    
public:
    Value(ValueTy T) : Ty(T) {}
    ValueTy getValueID() const { return Ty; }
};

// 具体类的实现
class Instruction : public Value {
public:
    // 指令子类型
    enum InstructionOps {
        Add, Sub, Mul, Div, 
        Br, Ret, Call, Load, Store
    };
    
private:
    InstructionOps Opcode;
    
public:
    Instruction(InstructionOps Op) 
        : Value(InstructionVal), Opcode(Op) {}
        
    static bool classof(const Value* V) {
        return V->getValueID() == InstructionVal;
    }
};

class BinaryOperator : public Instruction {
public:
    BinaryOperator(InstructionOps Op) : Instruction(Op) {}
    
    static bool classof(const Instruction* I) {
        InstructionOps Op = I->getOpcode();
        return Op >= Instruction::Add && Op <= Instruction::Div;
    }
    
    static bool classof(const Value* V) {
        return isa<Instruction>(V) && 
               classof(cast<Instruction>(V));
    }
};


4.2 实际使用示例

#include "llvm/IR/Value.h"
#include "llvm/IR/Instruction.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/Casting.h"

void processValue(llvm::Value* V) {
    // 类型检查
    if (llvm::isa<llvm::Instruction>(V)) {
        llvm::Instruction* I = llvm::cast<llvm::Instruction>(V);
        // 处理指令
        
        if (llvm::isa<llvm::BinaryOperator>(I)) {
            llvm::BinaryOperator* BO = llvm::cast<llvm::BinaryOperator>(I);
            // 处理二元操作
        }
    }
    else if (llvm::isa<llvm::Function>(V)) {
        llvm::Function* F = llvm::cast<llvm::Function>(V);
        // 处理函数
    }
    else if (llvm::isa<llvm::BasicBlock>(V)) {
        llvm::BasicBlock* BB = llvm::cast<llvm::BasicBlock>(V);
        // 处理基本块
    }
}


5. 性能优势

5.1 编译时优化

// LLVM RTTI - 编译时可优化
template<typename To, typename From>
bool isa(const From& Val) {
    return To::classof(&Val);
}

// 编译后可能内联为简单的比较
// if (V->getValueID() == InstructionVal)


对比标准 RTTI：
// 标准 RTTI - 运行时开销
if (typeid(*obj) == typeid(Derived)) {
    // 需要运行时类型查询
}


5.2 内存占用比较

标准 RTTI：
• 每个多态类有 typeinfo 结构

• 每个对象有虚函数表指针

LLVM RTTI：
• 只有一个枚举值（通常 1-4 字节）

• 无额外虚函数表开销

6. 在自定义项目中使用

6.1 启用 LLVM 风格 RTTI

# CMakeLists.txt
find_package(LLVM REQUIRED)

# 添加 LLVM 的 Casting 支持
target_link_libraries(your_target LLVMSupport)

# 禁用标准 RTTI（可选）
if(MSVC)
    target_compile_options(your_target PRIVATE /GR-)
else()
    target_compile_options(your_target PRIVATE -fno-rtti)
endif()


6.2 完整示例项目

// my_rtti.h
#pragma once

#include <cassert>

// 简化版的 LLVM 风格 Casting
template<typename To, typename From>
bool isa(const From& Val) {
    return To::classof(&Val);
}

template<typename To, typename From>
To* cast(From* Val) {
    assert(isa<To>(Val) && "cast<> argument not of correct type");
    return static_cast<To*>(Val);
}

template<typename To, typename From>
To* dyn_cast(From* Val) {
    return isa<To>(Val) ? cast<To>(Val) : nullptr;
}

// 基类定义
class MyBase {
public:
    enum Kind {
        DerivedAKind,
        DerivedBKind
    };
    
private:
    Kind kind;
    
protected:
    MyBase(Kind K) : kind(K) {}
    
public:
    Kind getKind() const { return kind; }
    
    virtual ~MyBase() = default;
    
    static bool classof(const MyBase*) {
        return true;
    }
};

// 派生类
class DerivedA : public MyBase {
public:
    DerivedA() : MyBase(DerivedAKind) {}
    
    void methodA() { /* A 特定方法 */ }
    
    static bool classof(const MyBase* B) {
        return B->getKind() == DerivedAKind;
    }
};

class DerivedB : public MyBase {
public:
    DerivedB() : MyBase(DerivedBKind) {}
    
    void methodB() { /* B 特定方法 */ }
    
    static bool classof(const MyBase* B) {
        return B->getKind() == DerivedBKind;
    }
};


6.3 使用示例

#include "my_rtti.h"
#include <iostream>

void process(MyBase* obj) {
    // 使用 LLVM 风格 RTTI
    if (isa<DerivedA>(obj)) {
        DerivedA* a = cast<DerivedA>(obj);
        a->methodA();
        std::cout << "Processing DerivedA\n";
    }
    else if (isa<DerivedB>(obj)) {
        DerivedB* b = cast<DerivedB>(obj);
        b->methodB();
        std::cout << "Processing DerivedB\n";
    }
    
    // 安全转换
    if (DerivedA* a = dyn_cast<DerivedA>(obj)) {
        // 只有在是 DerivedA 时才执行
        a->methodA();
    }
}

int main() {
    DerivedA a;
    DerivedB b;
    
    process(&a);
    process(&b);
    
    return 0;
}


7. 最佳实践

7.1 何时使用 LLVM 风格 RTTI

• 性能敏感的代码

• 需要禁用标准 RTTI 的环境

• 大型类层次结构

• 编译器/工具链开发

7.2 设计指南

1. 枚举值规划：合理规划类型枚举，考虑扩展性
2. classof 方法：正确实现类关系判断
3. 错误处理：使用 cast<> 时确保类型正确
4. 继承层次：对于复杂继承，实现多级 classof

7.3 调试技巧

// 添加调试支持
class MyBase {
public:
    const char* getKindName() const {
        switch (getKind()) {
        case DerivedAKind: return "DerivedA";
        case DerivedBKind: return "DerivedB";
        default: return "Unknown";
        }
    }
    
    void dump() const {
        std::cout << "Object kind: " << getKindName() << "\n";
    }
};


总结
LLVM 风格 RTTI 的核心优势：
• 高性能：编译时优化，运行时开销小
• 可控性：完全掌控类型系统行为
• 可移植性：不依赖编译器特定的 RTTI 实现
• 二进制大小：减少代码膨胀

适用场景：
• 高性能计算库
• 编译器基础设施
• 嵌入式系统（禁用 RTTI 时）
• 大型项目需要精细控制类型系统时

这种设计模式体现了 LLVM 项目对性能和可控性的极致追求，是值得学习的高级 C++ 设计技术。

好的，我来详细解释 AST 编号 和 SSA 格式的 IR 代码 这两个概念，以及它们之间的关系。

1. AST 编号（抽象语法树编号）

1.1 什么是 AST 编号？

AST 编号是为抽象语法树节点分配的唯一标识符，用于在编译过程中跟踪和管理节点。

1.2 AST 编号示例

// 源代码：int result = (a + b) * c;
// 对应的 AST 结构：

     [=] (Node #5)
     /          \
 [result] #1   [*] #4
               /     \
             [+] #2  [c] #6
            /    \
         [a] #0  [b] #3

// AST 节点编号：
// #0: 变量 a
// #1: 变量 result  
// #2: 加法运算 a + b
// #3: 变量 b
// #4: 乘法运算 (a+b) * c
// #5: 赋值运算 result = ...
// #6: 变量 c


1.3 AST 编号的实现

class ASTNode {
private:
    static int nextId;
    int nodeId;
    NodeType type;
    std::string value;
    std::vector<ASTNode*> children;
    
public:
    ASTNode(NodeType t, const std::string& val = "") 
        : nodeId(nextId++), type(t), value(val) {}
    
    int getId() const { return nodeId; }
    NodeType getType() const { return type; }
    void addChild(ASTNode* child) { children.push_back(child); }
    
    // 递归打印 AST（带编号）
    void print(int indent = 0) const {
        std::cout << std::string(indent, ' ') 
                  << "#" << nodeId << " " << getTypeName() 
                  << " '" << value << "'\n";
        for (auto child : children) {
            child->print(indent + 2);
        }
    }
};

int ASTNode::nextId = 0;


2. SSA 格式的 IR 代码

2.1 什么是 SSA（Static Single Assignment）？

SSA 是一种中间表示形式，其中每个变量只被赋值一次。

2.2 传统代码 vs SSA 形式对比

// 传统代码（非 SSA）
int x = 1;
if (condition) {
    x = x + 1;  // x 被多次赋值
} else {
    x = x - 1;
}
int y = x * 2;

// SSA 形式
int x1 = 1;
if (condition) {
    int x2 = x1 + 1;  // 新变量 x2
} else {
    int x3 = x1 - 1;  // 新变量 x3
}
int x4 = φ(x2, x3);  // φ 函数合并不同路径的值
int y1 = x4 * 2;


2.3 SSA IR 示例（LLVM IR）

; SSA 形式的 LLVM IR
define i32 @example(i32 %a, i32 %b, i1 %condition) {
entry:
  %x1 = add i32 %a, %b        ; x1 = a + b
  br i1 %condition, label %then, label %else

then:
  %x2 = mul i32 %x1, 2        ; x2 = x1 * 2 (新变量)
  br label %merge

else:
  %x3 = add i32 %x1, 1        ; x3 = x1 + 1 (新变量)
  br label %merge

merge:
  %x4 = phi i32 [%x2, %then], [%x3, %else]  ; φ 函数
  ret i32 %x4
}


3. 从 AST 编号到 SSA IR 的转换

3.1 转换过程


源代码 → AST（带编号） → SSA IR


3.2 具体转换示例

// 源代码：z = (a + b) * c

// 1. 生成 AST 编号
     [=] #3
     /    \
   [z] #0 [*] #2
          /     \
        [+] #1  [c] #4
       /    \
     [a] #5 [b] #6

// 2. 转换为 SSA IR
; 使用虚拟寄存器（%0, %1, %2...）对应 AST 编号
define i32 @main() {
  %a = alloca i32, align 4     ; #5: 变量 a
  %b = alloca i32, align 4     ; #6: 变量 b  
  %c = alloca i32, align 4     ; #4: 变量 c
  %z = alloca i32, align 4     ; #0: 变量 z
  
  ; 加载值
  %a_val = load i32, i32* %a   ; a 的值
  %b_val = load i32, i32* %b   ; b 的值
  %c_val = load i32, i32* %c   ; c 的值
  
  ; AST 节点 #1: a + b
  %1 = add i32 %a_val, %b_val
  
  ; AST 节点 #2: (a+b) * c  
  %2 = mul i32 %1, %c_val
  
  ; AST 节点 #3: z = 结果
  store i32 %2, i32* %z
  
  ret i32 0
}


4. 完整的 AST 到 SSA IR 转换器

4.1 AST 节点定义

enum class NodeType {
    VARIABLE, NUMBER, BINARY_OP, ASSIGNMENT
};

class ASTNode {
public:
    int id;
    NodeType type;
    std::string value;
    ASTNode* left;
    ASTNode* right;
    
    ASTNode(int id, NodeType t, const std::string& val = "") 
        : id(id), type(t), value(val), left(nullptr), right(nullptr) {}
};

class SSAGenerator {
private:
    int tempCounter;
    std::map<int, std::string> varMap;  // AST id -> SSA 变量名
    
public:
    SSAGenerator() : tempCounter(0) {}
    
    std::string generateTemp() {
        return "%t" + std::to_string(tempCounter++);
    }
    
    // 递归生成 SSA IR
    std::string generateIR(ASTNode* node) {
        if (!node) return "";
        
        switch (node->type) {
            case NodeType::VARIABLE:
                return handleVariable(node);
            case NodeType::NUMBER:
                return handleNumber(node);
            case NodeType::BINARY_OP:
                return handleBinaryOp(node);
            case NodeType::ASSIGNMENT:
                return handleAssignment(node);
            default:
                return "";
        }
    }
    
private:
    std::string handleVariable(ASTNode* node) {
        std::string varName = "%" + node->value;
        varMap[node->id] = varName;
        return varName;
    }
    
    std::string handleNumber(ASTNode* node) {
        std::string temp = generateTemp();
        varMap[node->id] = temp;
        return temp + " = " + node->value;
    }
    
    std::string handleBinaryOp(ASTNode* node) {
        std::string leftIR = generateIR(node->left);
        std::string rightIR = generateIR(node->right);
        
        std::string temp = generateTemp();
        varMap[node->id] = temp;
        
        std::string op;
        if (node->value == "+") op = "add";
        else if (node->value == "*") op = "mul";
        else if (node->value == "-") op = "sub";
        
        return temp + " = " + op + " i32 " + varMap[node->left->id] + 
               ", " + varMap[node->right->id];
    }
    
    std::string handleAssignment(ASTNode* node) {
        std::string rightIR = generateIR(node->right);
        return "store i32 " + varMap[node->right->id] + 
               ", i32* " + varMap[node->left->id];
    }
};


4.2 转换示例

// 构建 AST：x = (a + b) * 3
ASTNode* a = new ASTNode(1, NodeType::VARIABLE, "a");
ASTNode* b = new ASTNode(2, NodeType::VARIABLE, "b");  
ASTNode* three = new ASTNode(3, NodeType::NUMBER, "3");
ASTNode* add = new ASTNode(4, NodeType::BINARY_OP, "+");
add->left = a;
add->right = b;
ASTNode* mul = new ASTNode(5, NodeType::BINARY_OP, "*");  
mul->left = add;
mul->right = three;
ASTNode* x = new ASTNode(6, NodeType::VARIABLE, "x");
ASTNode* assign = new ASTNode(7, NodeType::ASSIGNMENT, "=");
assign->left = x;
assign->right = mul;

// 生成 SSA IR
SSAGenerator generator;
std::string ir = generator.generateIR(assign);


生成的 IR：
; 生成的 SSA IR
%a = alloca i32
%b = alloca i32  
%x = alloca i32
%t0 = 3
%t1 = add i32 %a, %b    ; #4: a + b
%t2 = mul i32 %t1, %t0  ; #5: (a+b) * 3
store i32 %t2, i32* %x  ; #7: x = 结果


5. 控制流的 SSA 生成（带 φ 函数）

5.1 复杂控制流示例

// 源代码
if (a > b) {
    x = a + b;
} else {
    x = a - b;
}
y = x * 2;

// AST 结构（简化）：
//     [if] #0
//    /     |    \
// [>] #1 [then] #2 [else] #3
//               |         |
//            [=] #4    [=] #5
//            /   \     /   \
//          [x] #6[+] #7 [x] #8[-] #9


5.2 生成带 φ 函数的 SSA IR

; 生成的 SSA IR
define i32 @control_flow(i32 %a, i32 %b) {
entry:
  %cmp = icmp sgt i32 %a, %b    ; #1: a > b
  br i1 %cmp, label %then, label %else

then:
  %x_then = add i32 %a, %b      ; #7: x = a + b (then 分支)
  br label %merge

else:  
  %x_else = sub i32 %a, %b      ; #9: x = a - b (else 分支)
  br label %merge

merge:
  %x = phi i32 [%x_then, %then], [%x_else, %else]  ; φ 函数
  %y = mul i32 %x, 2            ; y = x * 2
  ret i32 %y
}


6. AST 编号在 SSA 生成中的作用

6.1 编号的重要性

1. 唯一标识：每个 AST 节点有唯一 ID
2. 值跟踪：通过编号跟踪值的定义和使用
3. 优化基础：为后续优化提供基础结构
4. 调试支持：便于调试和错误定位
6.2 编号策略

class IRGenerator {
private:
    int nextTempId;
    std::map<int, Value*> valueMap;  // AST id -> LLVM Value*
    
public:
    // 为每个 AST 节点生成唯一的虚拟寄存器
    Value* getOrCreateValue(ASTNode* node, IRBuilder<>& builder) {
        if (valueMap.find(node->id) != valueMap.end()) {
            return valueMap[node->id];
        }
        
        Value* val = generateValue(node, builder);
        valueMap[node->id] = val;
        return val;
    }
    
    Value* generateValue(ASTNode* node, IRBuilder<>& builder) {
        switch (node->type) {
            case NodeType::NUMBER:
                return builder.getInt32(std::stoi(node->value));
            case NodeType::BINARY_OP:
                return generateBinaryOp(node, builder);
            // ... 其他类型
        }
    }
};


7. 实际编译器中的实现
7.1 使用 LLVM API 的实现
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/LLVMContext.h"

class ASTToSSAConverter {
private:
    llvm::LLVMContext& context;
    llvm::IRBuilder<>& builder;
    std::map<int, llvm::Value*> valueMap;
    
public:
    ASTToSSAConverter(llvm::LLVMContext& ctx, llvm::IRBuilder<>& b) 
        : context(ctx), builder(b) {}
    
    // 转换入口点
    llvm::Value* convert(ASTNode* root) {
        return generateValue(root);
    }
    
private:
    llvm::Value* generateValue(ASTNode* node) {
        if (!node) return nullptr;
        
        // 检查是否已生成
        if (valueMap.find(node->id) != valueMap.end()) {
            return valueMap[node->id];
        }
        
        llvm::Value* result = nullptr;
        switch (node->type) {
            case NodeType::VARIABLE:
                result = generateVariable(node);
                break;
            case NodeType::BINARY_OP:
                result = generateBinaryOp(node);
                break;
            case NodeType::ASSIGNMENT:
                result = generateAssignment(node);
                break;
        }
        
        valueMap[node->id] = result;
        return result;
    }
    
    llvm::Value* generateBinaryOp(ASTNode* node) {
        llvm::Value* lhs = generateValue(node->left);
        llvm::Value* rhs = generateValue(node->right);
        
        if (node->value == "+") {
            return builder.CreateAdd(lhs, rhs, "addtmp");
        } else if (node->value == "*") {
            return builder.CreateMul(lhs, rhs, "multmp");
        }
        // ... 其他操作符
        return nullptr;
    }
};


总结
AST 编号的作用：
• 唯一标识 AST 节点
• 跟踪数据流
• 支持调试和优化
• 映射到 SSA 虚拟寄存器

SSA IR 的优势：
• 简化数据流分析
• 启用更多优化
• 清晰的 def-use 关系
• 标准化的中间表示

转换流程：


源代码 → 词法分析 → 语法分析 → AST（带编号）→ SSA IR生成 → 优化 → 目标代码


这种转换是现代编译器（如 Clang/LLVM）的核心技术，能够生成高效且可优化的代码。

M88k 后端 是 LLVM 中针对 Motorola 88000 系列处理器的代码生成器。让我详细解释这个后端的技术细节、架构和实现。

1. M88k 架构概述

1.1 Motorola 88000 特性

// M88k 架构关键特性
class M88kArchitecture {
public:
    // RISC 架构
    static const bool IsRISC = true;
    
    // 32位架构
    static const int PointerSize = 32;
    
    // 大端字节序
    static const Endianness ByteOrder = BigEndian;
    
    // 寄存器特性
    static const int NumGPRegisters = 32;   // 32个通用寄存器
    static const int NumFPRegisters = 32;   // 32个浮点寄存器
    
    // 特殊寄存器
    enum SpecialRegisters {
        R0 = 0,        // 硬编码零寄存器
        R1 = 1,        // 汇编临时寄存器
        R31 = 31       // 栈指针/链接寄存器
    };
};


1.2 指令集特征

; 典型的 M88k 指令示例
add %r2, %r3, %r4      ; R2 = R3 + R4
ld %r2, 0(%r1)         ; 加载内存
st %r2, 4(%r1)         ; 存储到内存
br label                ; 无条件跳转
bb0 %r2, label         ; 位测试分支
fadd.d %f2, %f3, %f4   ; 双精度浮点加法


2. LLVM M88k 后端结构

2.1 后端文件结构


llvm/lib/Target/M88k/
├── M88kTargetMachine.cpp     # 目标机器定义
├── M88kISelDAGToDAG.cpp      # DAG 到 DAG 指令选择
├── M88kISelLowering.cpp      #  lowering 逻辑
├── M88kInstrInfo.cpp         # 指令信息
├── M88kRegisterInfo.cpp      # 寄存器信息
├── M88kFrameLowering.cpp     # 栈帧处理
├── M88kMCInstLower.cpp       # MCInst  lowering
├── M88kAsmPrinter.cpp        # 汇编输出
├── M88kTargetObjectFile.cpp  # 目标文件格式
└── M88k.td                   # TableGen 定义


2.2 TableGen 目标描述

// M88k.td - 目标描述文件
def M88k : Target {
    let InstructionSet = M88kInstrInfo;
    let AssemblyParsers = [M88kAsmParser];
    let AssemblyPrinters = [M88kAsmPrinter];
    let Disassemblers = [M88kDisassembler];
}

// 寄存器定义
class M88kReg<string n> : Register<n> {
    let Namespace = "M88k";
}

def R0 : M88kReg<"r0">, DwarfRegNum<0>;
def R1 : M88kReg<"r1">, DwarfRegNum<1>;
// ... 其他寄存器
def R31 : M88kReg<"r31">, DwarfRegNum<31>;

// 寄存器类
def GR32 : RegisterClass<"M88k", [i32], 32,
    [R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10,
     R11, R12, R13, R14, R15, R16, R17, R18, R19, R20,
     R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31]>;


3. 指令选择与 Lowering

3.1 指令选择模式

// 在 M88kInstrInfo.td 中的模式匹配
def : Pat<(add i32:$lhs, i32:$rhs), (ADD $lhs, $rhs)>;
def : Pat<(sub i32:$lhs, i32:$rhs), (SUB $lhs, $rhs)>;
def : Pat<(mul i32:$lhs, i32:$rhs), (MUL $lhs, $rhs)>;

// 带常数的模式
def : Pat<(add i32:$lhs, (i32 42)), (ADD $lhs, 42)>;

// 内存操作
def : Pat<(load i32:$addr), (LD $addr)>;
def : Pat<(store i32:$val, i32:$addr), (ST $val, $addr)>;


3.2 Lowering 逻辑

// M88kISelLowering.cpp
M88kTargetLowering::M88kTargetLowering(const TargetMachine &TM,
                                       const M88kSubtarget &STI)
    : TargetLowering(TM) {
    
    // 设置操作默认 lowering
    setOperationAction(ISD::ADD, MVT::i32, Legal);
    setOperationAction(ISD::SUB, MVT::i32, Legal);
    setOperationAction(ISD::MUL, MVT::i32, Legal);
    
    // 浮点操作
    setOperationAction(ISD::FADD, MVT::f64, Legal);
    setOperationAction(ISD::FSUB, MVT::f64, Legal);
    setOperationAction(ISD::FMUL, MVT::f64, Legal);
    
    // 需要自定义 lowering 的操作
    setOperationAction(ISD::BRCOND, MVT::Other, Custom);
    setOperationAction(ISD::SELECT, MVT::i32, Custom);
    
    // 设置寄存器类
    addRegisterClass(MVT::i32, &M88k::GR32RegClass);
    addRegisterClass(MVT::f64, &M88k::FP64RegClass);
}


4. 调用约定与栈帧处理

4.1 M88k 调用约定

// M88kCallingConv.cpp
class M88kCC : public CallingConv {
public:
    static bool CC_M88k(unsigned ValNo, MVT ValVT, MVT LocVT,
                       CCValAssign::LocInfo LocInfo,
                       ISD::ArgFlagsTy ArgFlags, CCState &State) {
        // 前6个参数在寄存器中
        if (ValNo < 6) {
            State.addLoc(CCValAssign::getReg(ValNo, ValVT, 
                           getRegForArg(ValNo), LocVT, LocInfo));
            return false;
        }
        
        // 其余参数在栈上
        unsigned Offset = (ValNo - 6) * 4;
        State.addLoc(CCValAssign::getMem(ValNo, ValVT, Offset, LocVT, LocInfo));
        return false;
    }
    
private:
    static unsigned getRegForArg(unsigned ArgNo) {
        static const unsigned ArgRegs[] = { M88k::R2, M88k::R3, M88k::R4,
                                           M88k::R5, M88k::R6, M88k::R7 };
        return ArgRegs[ArgNo];
    }
};


4.2 栈帧处理

// M88kFrameLowering.cpp
void M88kFrameLowering::emitPrologue(MachineFunction &MF,
                                    MachineBasicBlock &MBB) const {
    MachineFrameInfo &MFI = MF.getFrameInfo();
    MachineBasicBlock::iterator MBBI = MBB.begin();
    DebugLoc DL;
    
    // 计算栈帧大小
    uint64_t StackSize = MFI.getStackSize();
    
    // 生成栈调整指令
    if (StackSize > 0) {
        BuildMI(MBB, MBBI, DL, TII.get(M88k::SUBri))
            .addReg(M88k::R31)
            .addReg(M88k::R31)
            .addImm(StackSize)
            .setMIFlag(MachineInstr::FrameSetup);
    }
}

void M88kFrameLowering::emitEpilogue(MachineFunction &MF,
                                    MachineBasicBlock &MBB) const {
    // 恢复栈指针
    uint64_t StackSize = MF.getFrameInfo().getStackSize();
    if (StackSize > 0) {
        BuildMI(MBB, MBB.getFirstTerminator(), DL, TII.get(M88k::ADDri))
            .addReg(M88k::R31)
            .addReg(M88k::R31)
            .addImm(StackSize);
    }
}


5. 汇编器与反汇编器

5.1 指令编码

// M88kInstrInfo.cpp
unsigned M88kInstrInfo::getInstSizeInBytes(const MachineInstr &MI) const {
    // M88k 指令固定为4字节
    return 4;
}

// 指令编码格式
struct M88kInstructionFormat {
    unsigned opcode : 6;    // 操作码
    unsigned r1 : 5;        // 源寄存器1
    unsigned r2 : 5;        // 源寄存器2
    unsigned r3 : 5;        // 目标寄存器
    unsigned unused : 11;    // 未使用/立即数
};


5.2 汇编输出

// M88kAsmPrinter.cpp
void M88kAsmPrinter::emitInstruction(const MachineInstr *MI) {
    M88kMCInstLower Lower(MF->getContext(), *this);
    MCInst TmpInst;
    Lower.lower(MI, TmpInst);
    EmitToStreamer(*OutStreamer, TmpInst);
}

// 自定义指令打印
void M88kAsmPrinter::printOperand(const MachineInstr *MI, int OpNum,
                                  raw_ostream &O) {
    const MachineOperand &MO = MI->getOperand(OpNum);
    switch (MO.getType()) {
    case MachineOperand::MO_Register:
        O << M88kInstPrinter::getRegisterName(MO.getReg());
        break;
    case MachineOperand::MO_Immediate:
        O << MO.getImm();
        break;
    case MachineOperand::MO_MachineBasicBlock:
        O << *MO.getMBB()->getSymbol();
        break;
    }
}


6. 目标机器配置

6.1 TargetMachine 实现

// M88kTargetMachine.cpp
M88kTargetMachine::M88kTargetMachine(const Target &T, const Triple &TT,
                                     StringRef CPU, StringRef FS,
                                     const TargetOptions &Options,
                                     Optional<Reloc::Model> RM,
                                     Optional<CodeModel::Model> CM,
                                     CodeGenOpt::Level OL, bool JIT)
    : LLVMTargetMachine(T, "e-m:e-p:32:32", TT, CPU, FS, Options,
                        RM.getValueOr(Reloc::Static),
                        CM.getValueOr(CodeModel::Small), OL),
      TLOF(std::make_unique<M88kTargetObjectFile>()),
      Subtarget(TT, CPU, FS, *this) {
    
    initAsmInfo();
}

// 目标机器注册
extern "C" void LLVMInitializeM88kTarget() {
    RegisterTargetMachine<M88kTargetMachine> X(getTheM88kTarget());
    RegisterMCAsmInfo<M88kMCAsmInfo> Y(getTheM88kTarget());
}


6.2 子目标特性

// M88kSubtarget.cpp
M88kSubtarget::M88kSubtarget(const Triple &TT, StringRef CPU,
                            StringRef FS, M88kTargetMachine &TM)
    : M88kGenSubtargetInfo(TT, CPU, FS),
      TargetTriple(TT),
      InstrInfo(initializeSubtargetDependencies(CPU, FS)),
      TLInfo(TM, *this),
      FrameLowering(*this) {
    
    // 解析特性字符串
    ParseSubtargetFeatures(CPU, FS);
    
    // 设置默认 CPU
    if (CPU.empty()) {
        CPU = "mc88100";  // 默认 MC88100
    }
}


7. 代码生成流程

7.1 编译流程示例

# 使用 M88k 后端编译
clang -target m88k-unknown-elf -mcpu=mc88100 -O2 test.c -S -o test.s

# 生成的汇编代码
    .text
    .globl main
    .type main,@function
main:
    sub %r31, %r31, 16     ; 分配栈空间
    st %r2, 0(%r31)        ; 保存寄存器
    add %r2, %r0, 42       ; R2 = 42
    ld %r3, 0(%r31)        ; 恢复寄存器
    add %r31, %r31, 16     ; 释放栈空间
    jmp %r1                ; 返回


7.2 支持的文件格式

// M88kTargetObjectFile.cpp
class M88kTargetObjectFile : public TargetLoweringObjectFileELF {
public:
    M88kTargetObjectFile() {
        // M88k 使用 ELF 格式
        PLTRelativeVariantKind = MCSymbolRefExpr::VK_PLT;
    }
    
    MCSection *getSectionForConstant(const DataLayout &DL,
                                    SectionKind Kind,
                                    const Constant *C) const override {
        // 常量数据段
        return getDataSection();
    }
};


8. 测试与验证

8.1 LLVM 测试基础设施

; test.ll - LLVM IR 测试文件
define i32 @test_add(i32 %a, i32 %b) {
entry:
    %sum = add i32 %a, %b
    ret i32 %sum
}

; 运行测试
llc -mtriple=m88k-unknown-elf test.ll -o test.s

; 验证生成的代码
; CHECK: add %r2, %r2, %r3


8.2 后端测试用例

// M88k 后端单元测试
TEST(M88kInstrInfoTest, TestADDInstruction) {
    LLVMContext Context;
    std::unique_ptr<M88kTargetMachine> TM = createM88kTargetMachine();
    
    // 创建测试函数
    Function *F = createTestFunction(Context, "test_add");
    
    // 指令选择测试
    SelectionDAG DAG(*TM, F);
    SDValue Add = DAG.getNode(ISD::ADD, MVT::i32, 
                             DAG.getRegister(M88k::R2, MVT::i32),
                             DAG.getRegister(M88k::R3, MVT::i32));
    
    // 验证选择了正确的指令
    ASSERT_EQ(Add->getOpcode(), M88k::ADD);
}


9. 交叉编译支持

9.1 工具链配置

# CMake 交叉编译配置
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR m88k)

set(CMAKE_C_COMPILER clang)
set(CMAKE_C_COMPILER_TARGET m88k-unknown-elf)
set(CMAKE_C_FLAGS "-mcpu=mc88100 -mbig-endian")

set(CMAKE_CXX_COMPILER clang++)
set(CMAKE_CXX_COMPILER_TARGET m88k-unknown-elf)
set(CMAKE_CXX_FLAGS "-mcpu=mc88100 -mbig-endian")

# 禁用测试和文档
set(CMAKE_CROSSCOMPILING TRUE)


9.2 链接器脚本

/* m88k.ld - 链接器脚本 */
ENTRY(_start)

MEMORY {
    ROM (rx) : ORIGIN = 0x00000000, LENGTH = 1M
    RAM (rwx) : ORIGIN = 0x10000000, LENGTH = 4M
}

SECTIONS {
    .text : {
        *(.text .text.*)
    } > ROM
    
    .data : {
        *(.data .data.*)
    } > RAM AT > ROM
    
    .bss : {
        *(.bss .bss.*)
    } > RAM
}


10. 现状与维护

10.1 当前状态

• 实验性后端：M88k 后端在 LLVM 中处于实验状态

• 维护状态：由于 M88k 架构已不再广泛使用，维护相对较少

• 功能完整性：支持基本指令集，但可能缺少某些优化

10.2 使用限制

# 需要启用实验性后端
cmake -DLLVM_EXPERIMENTAL_TARGETS_TO_BUILD="M88k" ..

# 编译时可能需要的选项
clang -target m88k-unknown-elf -mcpu=generic -msoft-float test.c


总结

M88k 后端的关键特点：
• RISC 架构：简单的指令选择模式
• 大端字节序：影响数据布局和访问
• 固定长度指令：所有指令4字节
• 丰富的寄存器集：32个通用寄存器 + 32个浮点寄存器

主要组件：
1. TargetMachine：目标机器配置
2. ISelLowering：IR lowering 逻辑
3. RegisterInfo：寄存器分配
4. FrameLowering：栈帧管理
5. AsmPrinter：汇编输出

虽然 M88k 架构现已不常见，但其后端实现展示了 LLVM 如何支持传统 RISC 架构，为嵌入式系统和历史软件提供编译支持。

libFuzzer 是 LLVM 生态系统中的一个进程内、覆盖率引导的模糊测试引擎。让我详细解释它的工作原理、使用方法和最佳实践。

1. libFuzzer 核心概念

1.1 什么是 libFuzzer？

// libFuzzer 是一个库，链接到被测试代码中
#include <stdint.h>
#include <stddef.h>

// 用户必须实现的模糊测试目标函数
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    // 使用 Data 和 Size 测试目标代码
    // 返回 0 表示成功，非 0 表示失败
    return 0;
}


1.2 关键特性

• 进程内模糊测试：与目标代码在同一进程运行

• 覆盖率引导：使用代码覆盖率优化测试用例

• 无外部依赖：只需链接 libFuzzer 库

• 快速迭代：每秒可执行数千次测试

2. 基本使用方法

2.1 最简单的模糊测试目标

// simple_fuzzer.cpp
#include <stdint.h>
#include <stddef.h>

// 被测试的函数
bool CheckMagicBytes(const uint8_t *Data, size_t Size) {
    return Size >= 3 && Data[0] == 'F' && Data[1] == 'U' && Data[2] == 'Z';
}

// libFuzzer 入口点
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    CheckMagicBytes(Data, Size);
    return 0;  // 总是返回 0，libFuzzer 处理崩溃
}


2.2 编译和运行

# 使用 clang 编译（自动链接 libFuzzer）
clang -fsanitize=fuzzer simple_fuzzer.cpp -o simple_fuzzer

# 运行模糊测试
./simple_fuzzer

# 使用语料库目录
./simple_fuzzer corpus_dir

# 设置最大长度
./simple_fuzzer -max_len=100 corpus_dir


3. 高级功能和使用模式

3.1 使用 Sanitizers 增强检测

// 使用 AddressSanitizer 检测内存错误
clang -fsanitize=fuzzer,address fuzzer.cpp -o fuzzer_asan

// 使用 UndefinedBehaviorSanitizer
clang -fsanitize=fuzzer,undefined fuzzer.cpp -o fuzzer_ubsan

// 使用 MemorySanitizer
clang -fsanitize=fuzzer,memory fuzzer.cpp -o fuzzer_msan

// 组合使用多个 Sanitizer
clang -fsanitize=fuzzer,address,undefined fuzzer.cpp -o fuzzer_full


3.2 自定义初始化函数

#include <stdint.h>
#include <stddef.h>

// 全局状态初始化（只执行一次）
extern "C" int LLVMFuzzerInitialize(int *argc, char ***argv) {
    // 初始化全局资源
    // 解析命令行参数
    return 0;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    // 使用 Data 进行测试
    return 0;
}


4. 实际应用示例

4.1 解析器模糊测试

// json_fuzzer.cpp
#include <stdint.h>
#include <stddef.h>
#include <string>

// 假设的 JSON 解析器（被测试代码）
class SimpleJsonParser {
public:
    bool Parse(const std::string& json) {
        // 简化的解析逻辑
        if (json.empty()) return false;
        if (json[0] != '{') return false;
        if (json.back() != '}') return false;
        
        // 这里可能有漏洞的解析逻辑
        for (size_t i = 0; i < json.size(); i++) {
            if (json[i] == '\0') {
                // 潜在的空字符问题
                return false;
            }
        }
        return true;
    }
};

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    if (Size < 2) return 0;  // 忽略太小的输入
    
    SimpleJsonParser parser;
    std::string input(reinterpret_cast<const char*>(Data), Size);
    
    // 测试解析器
    parser.Parse(input);
    
    return 0;
}


4.2 图像解码器模糊测试

// image_fuzzer.cpp
#include <stdint.h>
#include <stddef.h>
#include <vector>

// 简化的图像解码器接口
class ImageDecoder {
public:
    bool Decode(const uint8_t* data, size_t size) {
        if (size < 8) return false;
        
        // 检查魔数
        if (data[0] != 0x89 || data[1] != 'P' || data[2] != 'N' || data[3] != 'G')
            return false;
            
        // 模拟解码过程（可能有漏洞的代码）
        uint32_t width = (data[4] << 24) | (data[5] << 16) | (data[6] << 8) | data[7];
        uint32_t height = (data[8] << 24) | (data[9] << 16) | (data[10] << 8) | data[11];
        
        // 检查合理的图像尺寸
        if (width > 10000 || height > 10000) return false;
        if (width == 0 || height == 0) return false;
        
        // 模拟内存分配（可能触发溢出）
        std::vector<uint8_t> pixels(width * height * 4);
        
        // 解码逻辑...
        return true;
    }
};

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    ImageDecoder decoder;
    decoder.Decode(Data, Size);
    return 0;
}


5. libFuzzer 选项和配置

5.1 常用命令行选项

# 基本选项
./fuzzer -help  # 显示所有选项

# 执行控制
./fuzzer -max_len=1024      # 最大输入长度
./fuzzer -runs=1000000      # 执行次数
./fuzzer -timeout=10         # 单次测试超时（秒）
./fuzzer -max_total_time=300 # 总运行时间（秒）

# 覆盖率引导
./fuzzer -use_value_profile=1  # 使用值分析
./fuzzer -shrink=1            # 尝试缩小输入

# 字典和种子
./fuzzer -dict=my_dict.txt   # 使用字典
./fuzzer -seed=123456        # 随机种子


5.2 性能优化选项

# 性能调优
./fuzzer -jobs=4            # 并行运行（需要独立模式）
./fuzzer -workers=4          # worker 进程数
./fuzzer -reload=1          # 定期重载语料库
./fuzzer -reduce_inputs=1   # 减少输入大小

# 内存限制
./fuzzer -rss_limit_mb=2048 # 内存限制
./fuzzer -malloc_limit_mb=1024 # 分配限制


6. 高级技巧和模式

6.1 使用字典文件

# dictionary.txt
# 为特定格式提供关键字
kw1="important_keyword"
kw2="\x00\x01\x02\x03"  # 二进制数据
kw3="{\"key\":\"value\"}"

./fuzzer -dict=dictionary.txt corpus_dir


6.2 自定义数据生成

// custom_fuzzer.cpp
#include <stdint.h>
#include <stddef.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    // 自定义输入验证
    if (Size < 4) return 0;
    
    // 提取字段
    uint32_t type = *reinterpret_cast<const uint32_t*>(Data);
    const uint8_t* payload = Data + 4;
    size_t payload_size = Size - 4;
    
    // 根据类型分派测试
    switch (type % 3) {
        case 0: TestParser(payload, payload_size); break;
        case 1: TestEncoder(payload, payload_size); break;
        case 2: TestDecoder(payload, payload_size); break;
    }
    
    return 0;
}


6.3 持久性模糊测试模式

// persistent_fuzzer.cpp
#include <stdint.h>
#include <stddef.h>

class TestTarget {
    // 昂贵的初始化
    void Initialize() { /* ... */ }
    
public:
    TestTarget() { Initialize(); }
    
    void Test(const uint8_t* data, size_t size) {
        // 测试逻辑
    }
};

// 全局实例（避免重复初始化）
static TestTarget* target = nullptr;

extern "C" int LLVMFuzzerInitialize(int *argc, char ***argv) {
    target = new TestTarget();
    return 0;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    if (target) {
        target->Test(Data, Size);
    }
    return 0;
}


7. 集成测试和持续模糊测试

7.1 与构建系统集成

# CMakeLists.txt
if(LIBFUZZER_SUPPORTED)
    add_executable(my_fuzzer fuzzer.cpp)
    target_compile_options(my_fuzzer PRIVATE -fsanitize=fuzzer,address)
    target_link_options(my_fuzzer PRIVATE -fsanitize=fuzzer,address)
endif()


7.2 自动化测试脚本

#!/bin/bash
# run_fuzzer.sh

set -e

# 编译模糊测试器
clang -fsanitize=fuzzer,address,undefined -g -O1 fuzzer.cpp -o fuzzer

# 创建语料库目录
mkdir -p corpus

# 添加种子文件
echo "test input" > corpus/seed1
echo "another test" > corpus/seed2

# 运行模糊测试
./fuzzer -max_total_time=600 \
         -rss_limit_mb=2048 \
         -max_len=1024 \
         corpus

# 检查是否发现崩溃
if ls crash-* 2>/dev/null; then
    echo "Found crashes!"
    exit 1
else
    echo "No crashes found"
    exit 0
fi


8. 调试和崩溃分析

8.1 调试符号和崩溃分析

# 带调试信息编译
clang -fsanitize=fuzzer,address -g -O1 fuzzer.cpp -o fuzzer_debug

# 重现崩溃
./fuzzer_debug crash-123456abcdef

# 使用 GDB 调试
gdb --args ./fuzzer_debug crash-123456abcdef


8.2 自动化崩溃分析

// crash_analyzer.cpp
#include <iostream>
#include <fstream>
#include <vector>

void AnalyzeCrash(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    std::vector<uint8_t> data((std::istreambuf_iterator<char>(file)),
                             std::istreambuf_iterator<char>());
    
    std::cout << "Crash file: " << filename << std::endl;
    std::cout << "Size: " << data.size() << " bytes" << std::endl;
    
    // 分析崩溃输入的特征
    if (data.size() > 0) {
        std::cout << "First bytes:";
        for (size_t i = 0; i < std::min(data.size(), size_t(16)); i++) {
            printf(" %02x", data[i]);
        }
        std::cout << std::endl;
    }
}

int main(int argc, char** argv) {
    for (int i = 1; i < argc; i++) {
        AnalyzeCrash(argv[i]);
    }
    return 0;
}


9. 实际项目集成案例

9.1 开源项目集成示例

许多知名项目使用 libFuzzer：

OpenSSL:
// openssl_fuzzer.cpp
#include <openssl/ssl.h>
#include <stdint.h>
#include <stddef.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    SSL_CTX* ctx = SSL_CTX_new(TLS_method());
    SSL* ssl = SSL_new(ctx);
    
    // 测试 SSL 解析
    BIO* bio = BIO_new_mem_buf(Data, Size);
    SSL_set_bio(ssl, bio, bio);
    
    SSL_accept(ssl);  // 可能触发漏洞
    
    SSL_free(ssl);
    SSL_CTX_free(ctx);
    return 0;
}


SQLite:
// sqlite_fuzzer.cpp  
#include <sqlite3.h>
#include <stdint.h>
#include <stddef.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    sqlite3* db = nullptr;
    if (sqlite3_open(":memory:", &db) == SQLITE_OK) {
        char* errmsg = nullptr;
        std::string sql(reinterpret_cast<const char*>(Data), Size);
        
        // 执行 SQL 语句（可能触发解析器漏洞）
        sqlite3_exec(db, sql.c_str(), nullptr, nullptr, &errmsg);
        
        if (errmsg) sqlite3_free(errmsg);
        sqlite3_close(db);
    }
    return 0;
}


10. 最佳实践和注意事项

10.1 最佳实践

1. 从小语料库开始：提供有意义的种子文件
2. 使用 Sanitizers：结合 ASan、UBSan 等增强检测
3. 设置合理的超时：避免挂起测试
4. 内存限制：防止内存耗尽
5. 定期更新语料库：合并新的测试用例

10.2 常见问题解决

# 处理内存不足
./fuzzer -rss_limit_mb=1024

# 处理超时
./fuzzer -timeout=5

# 处理缓慢的初始化
使用持久性模糊测试模式

# 处理非确定性行为
设置固定的随机种子：-seed=123


10.3 性能优化技巧

// 优化技巧示例
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    // 快速拒绝明显无效的输入
    if (Size < minimum_required_size) return 0;
    if (Size > maximum_reasonable_size) return 0;
    
    // 检查魔数或签名
    if (!CheckHeader(Data, Size)) return 0;
    
    // 进行实际测试
    return TestFunction(Data, Size);
}


总结

libFuzzer 的核心优势：
•  高性能：进程内执行，快速迭代
•  智能引导：覆盖率引导优化测试用例
•  易于集成：只需实现一个函数
•  强大生态：与 Sanitizers 完美集成

适用场景：
• 解析器、解码器测试
• 协议实现验证  
• 文件格式处理代码
• 任何有复杂输入的代码

关键成功因素：
1. 好的种子语料库
2. 合适的 Sanitizers 组合
3. 合理的资源限制
4. 持续的运行和监控

libFuzzer是现代软件安全测试的重要工具，能够有效发现内存损坏、未定义行为等严重漏洞。

TableGen 是 LLVM 的领域特定语言 (DSL)，用于声明式描述目标机器信息。
核心概念
1. 目的
• 描述硬件架构信息（寄存器、指令、调度等）
• 生成 C++ 代码和文档
• 减少手写重复代码
2. 基本语法

// 定义记录（类）
class Instruction {
    string Name;
    int Size = 4;
}

// 实例化记录
def ADD : Instruction {
    let Name = "ADD";
    let Size = 4;
}


3. 关键组件
• 记录 (Records)：主要数据结构
• 类 (Classes)：可重用的模板
• 字段 (Fields)：记录的属性
• 多态 (Multiclass)：一次生成多个记录
4. 典型应用

// 定义寄存器
class Register<string n> {
    string Name = n;
}

def R0 : Register<"r0">;
def R1 : Register<"r1">;

// 定义指令模式
def ADD : Instruction {
    let Opcode = 0b0001;
    let Operands = (ins R0, R1, R2);
}

5. 工作流程

.tablegen 文件 → TableGen 工具 → 生成的 C++ 代码 → LLVM 编译器

本质：用声明式语言描述硬件，自动生成编译器需要的底层代码。


