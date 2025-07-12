# 深度探索C++对象模型

[深度探索C++对象模型](https://book.douban.com/subject/10427315/)

ISBN: 9787121149528
出版年: 2012-1-1

微信读书 电子版

作者Lippman参与设计了全世界第一套C++编译程序cfront，这本书就是一位伟大的C++编译程序设计者向你阐述他如何处理各种explicit（明确出现于C++程序代码中）和implicit（隐藏于程序代码背后）的C++语意。
本书专注于C++面向对象程序设计的底层机制，包括结构式语意、临时性对象的生成、封装、继承，以及虚拟——虚拟函数和虚拟继承。这本书让你知道：一旦你能够了解底层实现模型，你的程序代码将获得多么大的效率。Lippman澄清了那些关于C++额外负荷与复杂度的各种错误信息和迷思，但也指出其中某些成本和利益交换确实存在。他阐述了各式各样的实现模型，指出它们的进化之道及其本质因素。书中涵盖了C++对象模型的语意暗示，并指出这个模型是如何影响你的程序的。
对于C++底层机制感兴趣的读者，这必然是一本让你大呼过瘾的绝妙好书。

本立道生（侯捷 译序） III
前言（Stanley B. Lippman） XIII
第0章 导读（译者的话） XXV
第1章 关于对象（Object Lessons） 1
加上封装后的布局成本（Layout Costs for Adding Encapsulation） 5
1.1　C++对象模式（The C++ Object Model） 6
简单对象模型（A Simple Object Model） 7
表格驱动对象模型（A Table-driven Object Model） 8
C++对象模型（The C++ Object Model） 9
对象模型如何影响程序（How the Object Model Effects Programs） 13
1.2 关键词所带来的差异（A Keyword Distinction） 15
关键词的困扰 16
策略性正确的struct（The Politically Correct Struct） 19
1.3 对象的差异（An Object Distinction） 22
指针的类型（The Type of a Pointer） 28
加上多态之后（Adding Polymorphism） 29
第2章 构造函数语意学（The Semantics of Constructors） 37
2.1 Default Constructor的构造操作 39
“带有Default Constructor”的Member Class Object 41
“带有Default Constructor”的Base Class 44
“带有一个Virtual Function”的Class 44
“带有一个Virtual Base Class”的Class 46
总结 47
2.2 Copy Constructor的构造操作 48
Default Memberwise Initialization 49
Bitwise Copy Semantics（位逐次拷贝） 51
不要Bitwise Copy Semantics！ 53
重新设定Virtual Table的指针 54
处理Virtual Base Class Subobject 57
2.3 程序转化语意学（Program Transformation Semantics） 60
显式的初始化操作（Explicit Initialization） 61
参数的初始化（Argument Initialization） 62
返回值的初始化（Return Value Initialization） 63
在使用者层面做优化（Optimization at the User Level） 65
在编译器层面做优化（Optimization at the Compiler Level） 66
Copy Constructor：要还是不要？ 72
摘要 74
2.4 成员们的初始化队伍（Member Initialization List） 74
第3章 Data语意学（The Semantics of Data） 83
3.1 Data Member的绑定（The Binding of a Data Member） 88
3.2 Data Member的布局（Data Member Layout） 92
3.3 Data Member的存取 94
Static Data Members 95
Nonstatic Data Members 97
3.4 “继承”与Data Member 99
只要继承不要多态（Inheritance without Polymorphism） 100
加上多态（Adding Polymorphism） 107
多重继承（Multiple Inheritance） 112
虚拟继承（Virtual Inheritance） 116
3.5 对象成员的效率（Object Member Efficiency） 124
3.6 指向Data Members的指针（Pointer to Data Members） 129
“指向Members的指针”的效率问题 134
第4章 Function语意学（The Semantics of Function） 139
4.1 Member的各种调用方式 140
Nonstatic Member Functions（非静态成员函数） 141
Virtual Member Functions（虚拟成员函数） 147
Static Member Functions（静态成员函数） 148
4.2 Virtual Member Functions（虚拟成员函数） 152
多重继承下的Virtual Functions 159
虚拟继承下的Virtual Functions 168
4.3 函数的效能 170
4.4 指向Member Function的指针（Pointer-to-Member Functions） 174
支持“指向Virtual Member Functions”的指针 176
在多重继承之下，指向Member Functions的指针 178
“指向Member Functions之指针”的效率 180
4.5 Inline Functions 182
形式参数（Formal Arguments） 185
局部变量（Local Variables） 186
第5章 构造、析构、拷贝语意学（Semantics of Construction, Destruction, and Copy） 191
纯虚函数的存在（Presence of a Pure Virtual Function） 193
虚拟规格的存在（Presence of a Virtual Specification） 194
虚拟规格中const的存在 195
重新考虑class的声明 195
5.1 “无继承”情况下的对象构造 196
抽象数据类型（Abstract Data Type） 198
为继承做准备 202
5.2 继承体系下的对象构造 206
虚拟继承（Virtual Inheritance） 210
vptr初始化语意学（The Semantics of the vptr Initialization） 213
5.3 对象复制语意学（Object Copy Semantics） 219
5.4 对象的效能（Object Efficiency） 225
5.5 析构语意学（Semantics of Destruction） 231
第6章 执行期语意学（Runtime Semantics） 237
6.1 对象的构造和析构（Object Construction and Destruction） 240
全局对象（Global Objects） 242
局部静态对象（Local Static Objects） 247
对象数组（Array of Objects） 250
Default Constructors和数组 252
6.2 new和delete运算符 254
针对数组的new语意 257
Placement Operator new的语意 263
6.3 临时性对象（Temporary Objects） 267
临时性对象的迷思（神话、传说） 275
第7章 站在对象模型的尖端（On the Cusp of the Object Model） 279
7.1 Template 280
Template的“实例化”行为（Template Instantiation） 281
Template的错误报告（Error Reporting within a Template） 285
Template中的名称决议法（Name Resolution within a Template） 289
Member Function的实例化行为（Member Function Instantiation） 292
7.2 异常处理（Exception Handling） 297
Exception Handling快速检阅 298
对Exception Handling的支持 303
7.3 执行期类型识别（Runtime Type Identification，RTTI） 308
Type-Safe Downcast（保证安全的向下转换操作） 310
Type-Safe Dynamic Cast（保证安全的动态转换） 311
References并不是Pointers 313
Typeid运算符 314
7.4 效率有了，弹性呢？ 318
动态共享函数库（Dynamic Shared Libraries） 318
共享内存（Shared Memory） 318


## 第1章 关于对象（Object Lessons）
## 第2章 构造函数语意学（The Semantics of Constructors）
## 第3章 Data语意学（The Semantics of Data）
## 第4章 Function语意学（The Semantics of Function）
## 第5章 构造、析构、拷贝语意学（Semantics of Construction, Destruction, and Copy）
## 第6章 执行期语意学（Runtime Semantics）
## 第7章 站在对象模型的尖端（On the Cusp of the Object Model）
