# tbb

使用Intel TBB实现可串行化冲突
首先，你需要安装Intel TBB库。如果你还没有安装，可以通过以下方式安装：

- 在Linux上，你可以使用包管理器安装，比如`apt-get`：
```bash
sudo apt-get install libtbb-dev
```

- 在Windows上，你可以从Intel官网下载安装包。
接下来，是示例代码：

```cpp
#include <iostream>
#include <vector>
#include <tbb/tbb.h>

// 共享资源
int shared_resource = 0;

// 一个线程执行的函数
void increment(int thread_id) {
    tbb::mutex::scoped_lock lock(mtx);  // 锁定互斥锁
    
    // 访问和修改共享资源
    std::cout << "Thread " << thread_id << " is incrementing the shared resource." << std::endl;
    shared_resource++;
    std::cout << "Shared resource after increment: " << shared_resource << std::endl;
}

int main() {
    const int num_threads = 10;
    std::vector<std::thread> threads;

    // 使用tbb::parallel_for并行执行线程
    tbb::parallel_for(0, num_threads, [](int i) {
        increment(i);
    });

    std::cout << "Final value of shared resource: " << shared_resource << std::endl;
    return 0;
}
```

### 代码解释：

1. 共享资源：`shared_resource`是所有线程访问和修改的共享变量。
2. TBB库：包括头文件`tbb/tbb.h`来使用TBB库中的功能。
3. 互斥锁：使用`tbb::mutex`来保护共享资源的访问。
4. 线程函数：`increment`函数在访问和修改共享资源前锁定互斥锁。
5. 主函数：
    - 使用`tbb::parallel_for`并行执行线程，避免了手动管理线程的创建和同步。
    - 打印最终的共享资源值。
TBB库提供了更高层次的抽象，使并行编程更加简洁和高效。通过使用`tbb::parallel_for`，我们可以轻松地并行执行多个线程，并保证线程安全。

conan支持tbb
https://github.com/oneapi-src/oneTBB

c++写的

c关键字
NULL

win c
__declspec

`__declspec` 是 Microsoft Visual C++ 编译器中的一个特定关键字，用于指定特定的存储类属性或属性修饰符。它允许程序员定义函数或变量的属性，例如它们的导出或导入、对齐方式等。

以下是一些常见的 `__declspec` 使用方式：

### 1. `__declspec(dllexport)` 和 `__declspec(dllimport)`
用于导出或导入 DLL 中的符号。

- **`__declspec(dllexport)`**:
  - 当你编写一个 DLL 并希望导出函数或变量以供其他程序使用时，使用 `__declspec(dllexport)`。
  - 例如，在 DLL 中导出一个函数：
    ```c
    __declspec(dllexport) void myFunction();
    ```

- **`__declspec(dllimport)`**:
  - 当你使用另一个 DLL 中导出的函数或变量时，使用 `__declspec(dllimport)`。
  - 例如，从 DLL 导入一个函数：
    ```c
    __declspec(dllimport) void myFunction();
    ```

### 2. `__declspec(align(#))`
用于指定变量或结构的内存对齐。

- 例如，指定一个结构体的对齐方式为 16 字节：
  ```c
  __declspec(align(16)) struct MyStruct {
      int a;
      double b;
  };
  ```

### 3. `__declspec(naked)`
用于定义一个不包含函数前置和后置代码（如栈帧设置和恢复）的函数。通常用于编写内联汇编代码。

- 例如，定义一个裸函数：
  ```c
  __declspec(naked) void myNakedFunction() {
      __asm {
          // 内联汇编代码
      }
  }
  ```

### 4. `__declspec(thread)`
用于声明线程本地存储（Thread Local Storage, TLS）变量。每个线程都会有该变量的独立副本。

- 例如，声明一个线程本地存储的变量：
  ```c
  __declspec(thread) int threadLocalVar;
  ```

### 5. `__declspec(property(get=GetX, put=PutX))`
用于为类成员定义属性，可以指定 `get` 和 `set` 访问器函数。

- 例如，定义一个属性：
  ```c
  class MyClass {
  private:
      int x;
  public:
      __declspec(property(get = GetX, put = PutX)) int MyProperty;
      int GetX() { return x; }
      void PutX(int value) { x = value; }
  };
  ```

### 6. `__declspec(selectany)`
用于声明一个变量为弱符号，如果在多个模块中定义了相同的符号，链接器会选择一个进行使用。

- 例如，定义一个弱符号：
  ```c
  __declspec(selectany) int myVariable = 10;
  ```

### 总结：
`__declspec` 是一个非常强大的关键字，用于控制符号的导入、导出、内存对齐、线程本地存储等。在编写跨平台代码时，通常会使用宏来封装这些特定于编译器的关键字，以保持代码的可移植性。
