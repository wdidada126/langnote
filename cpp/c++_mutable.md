# c++_mutable
mutable c++关键字

mutable 是 C++ 中的一个关键字，它用于修饰类的非静态数据成员。当你在类的成员变量前加上 mutable 关键字时，这个成员即使在类的 const 成员函数中也可以被修改。mutable 的主要作用是允许在 const 成员函数内部修改类的某些特定成员，而无需将整个函数声明为非 const。

这在某些情况下非常有用，比如你需要在一个 const 成员函数内更新一个用于缓存或记录状态的成员变量，但又不想破坏类的 const 正确性。

下面是一个简单的例子来说明 mutable 的用法：

```cpp
#include <iostream>  
#include <string>  
  
class MyClass {  
public:  
    MyClass(std::string value) : value_(value), accessCount_(0) {}  
  
    void setValue(const std::string& newValue) const {  
        // 这里尝试修改value_会编译错误，因为value_不是mutable的  
        // value_ = newValue; // 错误  
  
        // 但我们可以修改mutable成员  
        ++accessCount_; // 正确  
    }  
  
    // 假设这个函数用于获取value_的副本，但同时记录它被访问了多少次  
    std::string getValue() const {  
        ++accessCount_; // 允许在const函数中修改mutable成员  
        return value_;  
    }  
  
    // 一个非const成员函数，用于展示如何修改所有成员  
    void changeValue(const std::string& newValue) {  
        value_ = newValue;  
        ++accessCount_;  
    }  
  
private:  
    std::string value_; // 非mutable成员  
    mutable int accessCount_; // mutable成员  
};  
  
int main() {  
    MyClass obj("Initial");  
    obj.getValue(); // 访问并更新accessCount_  
    obj.getValue(); // 再次访问并更新accessCount_  
  
    // 尝试修改value_，需要非const成员函数  
    obj.changeValue("Changed");  
  
    std::cout << "Value: " << obj.value_ << ", Accessed " << obj.accessCount_ << " times." << std::endl;  
  
    return 0;  
}
```

在这个例子中，accessCount_ 是一个 mutable 成员，它可以在 const 成员函数中被修改。而 value_ 则不是 mutable 的，因此它不能在 const 成员函数中被修改。注意，mutable 成员通常用于缓存、计数器等场景，它们不直接影响对象的状态（即不影响对象在逻辑上是否相等），但可能需要根据访问情况更新。