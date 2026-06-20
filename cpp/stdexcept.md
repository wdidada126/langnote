# stdexcept

#include <stdexcept>  

<stdexcept>头文件是C++标准库中的一个重要组成部分，它定义了一系列标准异常类，这些异常类用于表示C++程序在运行时的各种错误情况。以下是根据<stdexcept>头文件中的API列表，对这些异常类的简要介绍：

1. std::exception
基类：所有<stdexcept>中定义的异常类的基类。
成员函数：virtual const char* what() const noexcept;，用于返回描述异常原因的C风格字符串。
2. 逻辑错误（Logic Errors）
逻辑错误类继承自std::logic_error，表示程序逻辑上的错误，这类错误在程序执行前理论上应该是可以检测到的。

std::logic_error
基类：std::exception
用途：作为所有逻辑错误的基类。
std::invalid_argument
用途：表示传递给函数的参数无效。
std::domain_error
用途：表示参数值不在函数的有效域内。
std::length_error
用途：表示尝试创建一个超出其最大可能长度的对象。
std::out_of_range
用途：表示使用了超出有效范围的值，如访问vector的元素时使用了无效的索引。
3. 运行时错误（Runtime Errors）
运行时错误类继承自std::runtime_error，表示程序在执行过程中检测到的错误。

std::runtime_error
基类：std::exception
用途：作为所有运行时错误的基类。
std::range_error
用途：表示结果超出了允许的范围，如数学运算的结果太大，无法表示。
std::overflow_error
用途：表示算术运算的结果超出了可表示的最大值。
std::underflow_error
用途：表示算术运算的结果低于可表示的最小值（尽管这在标准浮点数表示中不常见）。
4. 特殊异常
std::bad_alloc
用途：表示内存分配失败，如使用new运算符时无法分配足够的内存。
std::bad_cast
用途：表示类型转换失败，如dynamic_cast操作中的类型不匹配。
std::bad_exception
用途：表示未捕获的异常，如在throw语句中抛出了一个未定义的异常（这个类的使用相对较少，因为C++标准库通常不会抛出此类异常）。
总结
<stdexcept>头文件提供的异常类为C++程序提供了丰富的错误表示机制，使得程序能够更精确地报告和处理各种异常情况。通过继承这些异常类并适当地使用它们，开发者可以编写出更加健壮和易于维护的C++代码。

请注意，以上信息基于C++标准库的一般描述，并且可能会随着C++标准的更新而有所变化。然而，<stdexcept>头文件中的这些异常类在C++标准库中已经存在多年，并且在各种C++编译器和环境中都得到了广泛的支持。

