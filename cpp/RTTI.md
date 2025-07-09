# RTTI
rtti

非常好！我们来详细讲解 RTTI（Run-Time Type Information），它是 C++ 中支持运行时类型识别的一套机制，主要用于：

- `typeid` 运算符
- `dynamic_cast`
- 异常处理（如 `catch` 类型匹配）



## 一、什么是 RTTI？

RTTI 全称 Run-Time Type Information（运行时类型信息），是 C++ 提供的一种机制，允许程序在运行时查询对象的类型信息。

### 主要用途

| 特性 | 描述 |
|------|------|
| `typeid` | 获取对象或类型的类型信息 |
| `dynamic_cast` | 在继承体系中进行安全的向下转型 |
| 异常匹配 | 用于 `catch(...)` 的类型匹配 |



## 二、RTTI 和虚函数的关系

RTTI 是通过 虚函数表（vtable） 实现的。每个有虚函数的类都会有一个 vtable，其中包含：

```
[ vtable for ClassName ]
│
├── offset to top
├── typeinfo pointer   ← 指向 RTTI 信息
├── virtual function 1
├── virtual function 2
└── ...
```

所以：

> 只有当一个类有虚函数时，才会有 RTTI 信息。

如果你尝试对一个没有虚函数的类使用 `dynamic_cast` 或 `typeid`，编译器会报错（对于 `dynamic_cast`），或者返回静态类型信息（对于 `typeid`）。



## 三、RTTI 使用示例

### 示例 1：`typeid`

```cpp
#include <iostream>
#include <typeinfo>
using namespace std;

class Animal {
public:
    virtual ~Animal() {}
};

class Dog : public Animal {};

int main() {
    Animal* a = new Dog();
    cout << typeid(*a).name() << endl; // 输出 "4Dog"（具体名称可能因编译器而异）
    delete a;
}
```

输出可能是：
```
4Dog
```

> `typeid(*a)` 返回的是对象的实际运行时类型（即 `Dog`），而不是指针类型 `Animal*`。


### 示例 2：`dynamic_cast`

```cpp
#include <iostream>
using namespace std;

class Animal {
public:
    virtual ~Animal() {}
};

class Dog : public Animal {};
class Cat : public Animal {};

int main() {
    Animal* animal = new Dog();
    Dog* dog = dynamic_cast<Dog*>(animal); // 成功
    if (dog) cout << "It's a Dog!" << endl;

    Cat* cat = dynamic_cast<Cat*>(animal); // 失败
    if (!cat) cout << "Not a Cat." << endl;

    delete animal;
}
```

输出：
```
It's a Dog!
Not a Cat.
```

> `dynamic_cast` 利用了 RTTI 来判断类型是否匹配。


## 四、RTTI 数据结构（底层视角）

RTTI 信息由编译器自动生成，通常包括：

### 1. `type_info` 结构体

C++ 标准库定义了抽象类 `std::type_info`，所有具体的类型信息都继承自它。

例如：

```cpp
const type_info& ti = typeid(obj);
cout << ti.name(); // 输出类型名
```

### 2. 编译器扩展结构

GCC 编译器生成的 RTTI 包括以下结构（位于 `<cxxabi.h>`）：

- `__class_type_info`：普通类类型
- `__si_class_type_info`：单一继承类
- `__vmi_class_type_info`：多重继承类
- `__array_type_info`, `__function_type_info` 等：其他类型

这些结构中包含了：

- 类名
- 继承关系
- 虚基类偏移等信息


## 五、RTTI 如何与 vtable 关联？

在 vtable 中，第二个槽位（offset=8）通常是 RTTI 信息地址。

例如：

```asm
vtable for Dog:
        .quad   0                       ; offset 0: RTTI offset from top
        .quad   typeinfo for Dog        ; offset 8: typeinfo pointer
        .quad   Dog::speak()
        .quad   Dog::~Dog() [complete]
        .quad   Dog::~Dog() [deleting]
```

这意味着：

```cpp
void vptr = *(void*)obj;     // 获取 vptr
void* rtti = vptr[1];            // 第二个槽位是 typeinfo 指针
```


##  六、关闭 RTTI 的影响

你可以通过编译选项 `-fno-rtti` 禁用 RTTI：

```bash
g++ -fno-rtti your_code.cpp
```

此时：

- `typeid` 不能用于多态类型，编译时报错
- `dynamic_cast` 只能用于具有明确转换路径的情况（如向上转型），否则报错
- 代码体积减小，适合嵌入式系统等资源受限环境


## 七、总结：RTTI 关键点

| 内容 | 说明 |
|------|------|
| 定义 | Run-Time Type Information，运行时类型信息 |
| 支持功能 | `typeid`, `dynamic_cast`, 异常类型匹配 |
| 必须条件 | 类必须有虚函数（否则无法启用 RTTI） |
| 底层实现 | 存储在 vtable 中，由编译器管理 |
| 优点 | 支持安全的向下转型、类型识别 |
| 缺点 | 占用额外内存、带来一定性能开销 |
| 控制方式 | `-fno-rtti` 可禁用 RTTI |


## 八、查看 RTTI 信息的方法

### 方法 1：使用 `-fdump-class-hierarchy`

```bash
g++ -fdump-class-hierarchy your_code.cpp
```

你会看到类似这样的内容：

```
typeinfo for Dog:
        .quad   vtable for __cxxabiv1::__si_class_type_info+16
        .quad   typeinfo name for Dog
        .quad   typeinfo for Animal
```

### 方法 2：使用 GDB 查看对象 RTTI

```bash
gdb ./your_program
(gdb) p dog
(gdb) x /8gx &dog
```

可以看到对象起始位置是 vptr，然后可以访问其指向的 vtable 中的 typeinfo。


## 九、相关头文件和 API

| 功能 | 头文件 | 说明 |
|------|--------|------|
| `typeid` | `<typeinfo>` | 获取类型信息 |
| `type_info` | `<typeinfo>` | 类型信息结构 |
| `dynamic_cast` | `<typeinfo>` | 安全类型转换 |
| `__cxxabiv1` 命名空间 | `<cxxabi.h>` | GCC ABI 扩展结构 |


