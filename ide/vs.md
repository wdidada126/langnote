# visual studio


MSVC 没有完整支持 20 年前的 C99 标准。你看下是否适合吧。MSVC 实现的标准 C 功能有：完整的 C94 （ C89 + 后续宽字符支持）不完整的 C99 语核（缺复合字面量、非常量长度数组、 T [static N] 函数参数等）少数 C11 中标准化的扩展（如匿名 struct/union 成员）C99 标准库包含于 C++ 的 C11 标准库部分（有少量缺失）与 C11 标准略有区别的 _s 系列函数基本上还是不要把 MSVC 当成用 C 开发的东西了。如果需要 VS 的话可以考虑 Visual Studio + Clang 。

vla
https://en.wikipedia.org/wiki/Variable-length_array


visual studio linux c++ 开发

