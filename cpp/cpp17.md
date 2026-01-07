# cpp17

cpp date库，cmake文件有定义 CMAKE_CXX_STANDARD 17。时区api，cpp 11 未定义符号，cpp 17 link成功
set( CMAKE_CXX_STANDARD 17 CACHE STRING "The C++ standard whose features are requested." )

网友：c++17 filesystem超级好用
记忆已更新
std::fstream 是 C++ 标准库中的一个类模板，定义在 <fstream> 头文件中。它提供了对文件的输入输出操作功能。std::fstream 结合了 std::ifstream（输入文件流）和 std::ofstream（输出文件流）的功能，允许你同时从文件中读取数据并向文件中写入数据。
基本概念
std::ifstream: 用于只读方式打开文件，继承自 std::istream。
std::ofstream: 用于只写方式打开文件，继承自 std::ostream。
std::fstream: 既可以用于读取也可以用于写入，继承自 std::iostream。
常用构造函数
std::fstream(): 默认构造函数，不打开任何文件。
std::fstream(const char* filename, std::ios::openmode mode = std::ios::in | std::ios::out): 打开名为 filename 的文件，使用指定的模式 mode。
常用的文件打开模式（std::ios::openmode）
std::ios::in: 打开文件用于读取。
std::ios::out: 打开文件用于写入。
std::ios::binary: 以二进制模式打开文件。
std::ios::app: 以追加模式打开文件。写入的所有数据将附加到文件末尾。
std::ios::ate: 文件打开后定位到文件末尾。
std::ios::trunc: 如果文件存在，打开文件时清空文件内容。
C++17 新特性
虽然 C++17 没有对 std::fstream 本身做出直接的更改，但 C++17 引入了 std::filesystem，这使得处理文件路径和文件操作变得更方便。你可以将 std::filesystem::path 直接传递给 std::fstream，以更安全、跨平台的方式处理文件路径。