# sqlite_orm

https://github.com/edidada/sqlite_orm

mac电脑编译不了qlite_orm项目的example
设置c++标准17，编译成功
set(CMAKE_CXX_STANDARD 11)  # 设置为 C++11 标准
找不到sqlite_orm库

是head only

struct
java代码里面只有get set的类，是不是在c++里面都是struct，不是class？

int main() {
    using namespace sqlite_orm;

函数里面引用namespace

在 C++ 中，你可以在函数的定义中引用命名空间。有两种常见的方法可以实现这一点：

1. 使用 `using` 声明：可以在函数的定义中使用 `using` 声明来引用命名空间中的特定成员。例如：
```cpp
#include <iostream>

namespace MyNamespace {
    void MyFunction() {
        std::cout << "Hello from MyNamespace!" << std::endl;
    }
}

void AnotherFunction() {
    using namespace MyNamespace;
    MyFunction();  // 在函数中直接使用 MyFunction()
}

int main() {
    AnotherFunction();
    return 0;
}
```
在上述示例中，`AnotherFunction()` 函数中使用了 `using namespace MyNamespace;`，这样就可以直接在函数中使用 `MyFunction()`，而无需显式地指定命名空间。

2. 使用限定符：另一种方法是在函数中使用命名空间限定符来引用命名空间中的特定成员。例如：
```cpp
#include <iostream>

namespace MyNamespace {
    void MyFunction() {
        std::cout << "Hello from MyNamespace!" << std::endl;
    }
}

void AnotherFunction() {
    MyNamespace::MyFunction();  // 使用命名空间限定符调用 MyFunction()
}

int main() {
    AnotherFunction();
    return 0;
}
```
在上述示例中，`AnotherFunction()` 函数使用了 `MyNamespace::MyFunction()` 的限定符形式来调用函数。

无论是使用 `using` 声明还是限定符形式，都可以在函数内部引用命名空间中的成员。你可以根据个人喜好和代码的可读性选择适合的方法。请注意，如果在函数中引用了命名空间，应确保引用的命名空间成员在函数内是可见的，或者在函数之前进行适当的声明和定义。

在 C++ 中，通常建议将 `using namespace` 语句放在文件的开头，在所有函数定义之前。这是因为 `using namespace` 语句会将整个命名空间的成员引入当前作用域，可能会导致命名冲突或歧义。

然而，如果你只想在特定的函数中使用命名空间，你可以在函数的作用域内使用 `using namespace`。这种方法会限制命名空间的引入范围，减少潜在的冲突。

以下是一个示例：

```cpp
#include <iostream>

namespace MyNamespace {
    void MyFunction() {
        std::cout << "Hello from MyNamespace!" << std::endl;
    }
}

void AnotherFunction() {
    using namespace MyNamespace;
    MyFunction();  // 在函数中直接使用 MyFunction()
}

int main() {
    AnotherFunction();
    return 0;
}
```

在上述示例中，`using namespace MyNamespace;` 语句被放置在 `AnotherFunction()` 函数中，而不是整个文件的开头。这样可以确保 `MyNamespace` 的成员只在 `AnotherFunction()` 函数内可见，而不会对其他函数产生影响。

需要注意的是，尽管可以在函数内使用 `using namespace`，但这样做可能会增加代码的可读性和维护性方面的挑战。如果可能，最好将 `using namespace` 放在文件的开头，并在全局范围内使用限定符来引用命名空间的成员，以避免潜在的命名冲突。

`std::move` 是 C++ 中的一个函数模板，用于实现移动语义。它位于 `<utility>` 头文件中，并用于将左值转换为右值引用，从而允许移动语义的使用。

移动语义是一种优化技术，可以避免不必要的对象复制，提高程序的性能。通过使用移动语义，可以将资源（如动态分配的内存或打开的文件句柄）从一个对象转移到另一个对象，而无需进行深层次的复制。

`std::move` 的使用方式如下：

```cpp
#include <utility>

Type dest = std::move(source);
```

在上述代码中，`std::move` 将 `source` 转换为右值引用，并将其作为参数传递给 `dest`。这样做可以告诉编译器，我们希望使用移动语义来将资源从 `source` 移动到 `dest`，而不进行深层次的复制。

请注意，使用 `std::move` 只是告诉编译器采用移动语义，而不会自动执行实际的移动操作。你需要确保目标类型支持移动构造函数或移动赋值操作符，以便实际执行资源的移动。通常情况下，标准库中的类型已经实现了适当的移动操作，但自定义类型可能需要手动实现移动操作。

使用 `std::move` 时需要小心，确保你不会在移动后继续使用被移动的对象，以避免悬空引用或未定义的行为。一般来说，在移动对象后，你应该将其置于有效但无定义的状态，或者重新赋值给其他对象。

总结一下，`std::move` 是用于实现移动语义的函数模板，用于将左值转换为右值引用。它允许使用移动语义来高效地转移资源，避免不必要的复制操作。在使用 `std::move` 时，请确保目标类型支持移动操作，并小心处理被移动对象的后续使用。
std::forward

std::tuple<>