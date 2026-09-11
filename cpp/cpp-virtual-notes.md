# 笔记：C++ `virtual` 详解（虚函数 / 纯虚函数 / 虚析构 / 虚继承）

> **来源**：CSDN [C++ Virtual详解](https://blog.csdn.net/ring0hx/article/details/1605254)
> **作者**：悦峰（ring0hx）　**发布时间**：2007-05-11
> **标签**：`c++` `iostream` `float` `class` `query`　**版权**：CC 4.0 BY-SA
> **整理日期**：2026-09-12
> **一句话概括**：`virtual` 让**父类声明接口、子类提供实现**，通过**基类指针/引用**调用时按**对象真实类型**动态分派（多态）；此外 `virtual` 还用于**纯虚函数（抽象类）**、**虚析构**与**虚继承**。

---

## 0. 先回答核心问题：虚拟函数的"父类声明、子类实现"

| 场景 | 父类写法 | 子类义务 | 语义 |
|---|---|---|---|
| **虚函数（有默认实现）** | `virtual void print() { ... }` | 可选覆写（覆写时 `virtual` 可省，但仍具虚性） | 父类给出通用实现，子类按需替换 |
| **纯虚函数（无实现）** | `virtual ostream& print(ostream& = cout) const = 0;` | **必须实现**，否则子类也是抽象类 | 只定义接口契约，父类不可实例化 |

**调用规则的关键**：只有**通过基类指针或引用**间接指向派生类对象时，多态才起作用。用派生类指针/对象本身调用时，走的是普通静态绑定。

---

## 1. 引言：虚函数与多态

```cpp
class Base {
public:
    Base() {}
public:
    virtual void print() { cout << "Base"; }
};

class Derived : public Base {
public:
    Derived() {}
public:
    void print() { cout << "Derived"; }      // 覆写基类虚函数
};

int main() {
    Base *point = new Derived();
    point->print();                          // 输出：Derived（动态分派）
}
```

`point` 的静态类型是 `Base*`，实际对象是 `Derived`，因为 `print` 是虚函数，调用被动态分派到 `Derived::print` —— 这就是运行时多态。

---

## 2. 覆写（override）与重载（overload）的区别

| 对比项 | 覆写 / 覆盖 | 重载 |
|---|---|---|
| 所在类 | 必须在**有继承关系的不同类**中 | 必须在**同一个类**中 |
| 函数签名 | 函数名、参数、返回值**必须相同** | 函数名相同，**参数必须不同** |
| `virtual` | **必须**加（基类侧） | **无关**，加不加都行 |

**为什么不能用返回值区分重载**：调用时程序可能根本不关心返回值，编译器无法从调用点判断调用的是哪一个函数。

---

## 3. 关于"C++ 隐藏规则"的争论（原文最有价值的一节）

原文引用了林锐《高质量C++/C 编程指南》(2001) 总结的"隐藏规则"，然后**明确反驳**其结论，例证代码：

```cpp
#include <iostream.h>      // 原文为旧式头文件，现代写法是 <iostream>

class Base {
public:
    virtual void f(float x) { cout << "Base::f(float) " << x << endl; }
    void g(float x)         { cout << "Base::g(float) " << x << endl; }
    void h(float x)         { cout << "Base::h(float) " << x << endl; }
};

class Derived : public Base {
public:
    virtual void f(float x) { cout << "Derived::f(float) " << x << endl; }
    void g(int x)           { cout << "Derived::g(int) " << x << endl; }   // 参数不同！
    void h(float x)         { cout << "Derived::h(float) " << x << endl; }
};

void main(void) {             // 现代写法：int main()
    Derived d;
    Base *pb = &d;
    Derived *pd = &d;

    // Good : behavior depends solely on type of the object
    pb->f(3.14f);   // Derived::f(float) 3.14
    pd->f(3.14f);   // Derived::f(float) 3.14

    // Bad : behavior depends on type of the pointer
    pb->g(3.14f);   // Base::g(float) 3.14
    pd->g(3.14f);   // Derived::g(int) 3   (surprise!)

    // Bad : behavior depends on type of the pointer
    pb->h(3.14f);   // Base::h(float) 3.14 (surprise!)
    pd->h(3.14f);   // Derived::h(float) 3.14
}
```

### 原文的结论

- 决定调用结果的**不是指针指向的地址，而是指针的静态类型**。
- `pd`（派生类指针）的所有调用都只是调用自己的函数，与多态无关 → 全部输出 `Derived::` 属正常。
- `pb`（基类指针）只有 `f` 是 `virtual`，按多态调用 `Derived::f`；`g`/`h` 非虚，走静态绑定调用 `Base::g` / `Base::h`。
- 因此原文认为："**没有所谓的隐藏规则**"，并引《C++ Primer》3rd：**只有在通过基类指针或引用间接指向派生类子类型时，多态性才会起作用。**

### 整理者补充：这段反驳"对了一半"，需要打个补丁

1. **原文对现象的归因是正确的**：调用结果由**静态类型**（名字查找的起点）+ **是否虚函数**（绑定方式）共同决定，而不是对象地址。
2. **但"名称隐藏（name hiding）"在现代 C++ 中确实是一条真实的标准规则**，原文的说法过于绝对：
   - 派生类中**只要声明了同名函数** `g`，基类的**所有同名重载版本都会被隐藏**（无论参数是否不同、无论是否 virtual、无论是否同签名）。
   - 上面 `pd->g(3.14f)` 之所以输出 `Derived::g(int)` 而非 `Base::g(float)`，正是**名称隐藏**造成的：名字查找在 `Derived` 中就停止，先找到 `Derived::g`，再做重载解析（参数 `double → int` 隐式转换）。
   - 因此林锐描述的**现象是对的**，只是把"通过基类指针时调用哪个版本"也一并归因于隐藏规则，才是他的错误之处。
3. **标准做法**：想恢复被隐藏的基类重载，用 `using` 引入声明：

```cpp
class Derived : public Base {
public:
    using Base::g;          // 让 Base::g 参与 Derived 作用域的重载解析
    void g(int x) { ... }
};
// 之后 pd->g(3.14f) 会调用 Base::g(float)，pd->g(3) 调用 Derived::g(int)
```

4. **实用建议（C++11 起）**：覆写时一律加 `override`，让隐藏/签名不匹配的错误在**编译期**暴露：

```cpp
class Derived : public Base {
public:
    void f(float x) override { ... }   // ✅ 确实覆写了
    void g(int x) override { ... }     // ❌ 编译错误：Base 中无此签名，纯属新函数
};
```

---

## 4. 纯虚函数与抽象类

```cpp
class Query {
public:
    // 声明纯虚拟函数
    virtual ostream& print( ostream&=cout ) const = 0;
    // ...
};
```

- 语法：函数声明后紧跟 `= 0`。
- 包含（或继承）一个或多个纯虚函数的类被识别为**抽象基类**，**不能创建独立对象**（编译期错误）；通过虚拟机制调用纯虚函数同样错误。
- 派生类**必须实现全部纯虚函数**才能被实例化，否则它自身仍是抽象类。

```cpp
// 正确: NameQuery 是 Query 的派生类
Query *pq = new NameQuery( "Nostromo" );

// 错误: new 表达式分配 Query 对象
Query *pq2 = new Query();      // 抽象类不能实例化
```

> 补充：纯虚函数**可以带函数体**（在类外定义），此时它仍使类抽象，但可为派生类提供可复用的默认实现：`void Base::print() { ... }`。析构函数也可以是纯虚的，但**必须提供定义**，否则派生类析构时会链接失败。

---

## 5. 虚析构函数

**规则：只要一个类可能被用作基类（会被 `delete` 基类指针），析构函数就应声明为 `virtual`。**

- 基类析构**非虚**时：`delete` 一个基类指针（实际指向派生类对象）→ **只调用基类析构函数**，派生类析构不执行 → 派生类中的资源泄漏。
- 基类析构**为虚**时：析构函数在继承树上**自底向上依次调用**：最底层派生类 → 一层层向上，直到该指针声明的类型。

```cpp
class Base {
public:
    virtual ~Base() {}          // 关键
};
```

> 补充：更彻底的做法是把基类析构声明为 **public + virtual**，或 **protected + 非 virtual**（表示不允许通过基类指针删除）。

---

## 6. 虚继承（virtual inheritance）

`virtual` 不只用于函数，还用于继承：`virtual public` / `public virtual`（**关键字顺序无所谓**）。

### 6.1 默认继承 = "按值组合"

```cpp
class Bear : public ZooAnimal { ... };       // Bear 对象内嵌一个 ZooAnimal 子对象
class PolarBear : public Bear { ... };       // 层层内嵌，单继承下最紧凑高效
```

### 6.2 多继承下的"菱形"问题

标准库的 `iostream` 就是典型例子：

```cpp
class iostream : public istream, public ostream { ... };
```

`istream` 和 `ostream` 都从抽象类 `ios` 派生 → 默认情况下 `iostream` 对象里**含有两个 `ios` 子对象**。带来四个问题：

1. **存储浪费**：只需要一个 `ios` 实例，却存了两份副本。
2. **构造重复**：`ios` 的构造函数被调用两次。
3. **二义性**：任何未加限定的 `ios` 成员访问都编译报错——到底访问哪个实例？
4. **一致性无法保证**：若 `ostream` 与 `istream` 对各自 `ios` 子对象的初始化略有不同，无法通过 `iostream` 保证这一对 `ios` 值一致。

### 6.3 解决方案：虚拟继承 = "按引用组合"

```cpp
// 这里关键字 public 和 virtual 的顺序不重要
class Bear    : public virtual ZooAnimal { ... };
class Raccoon : virtual public ZooAnimal { ... };
```

- 虚拟继承下，**无论该基类在派生层次中出现多少次，只继承一个共享的基类子对象**，称为**虚拟基类**。
- 对子对象及其非静态成员的访问是**间接**进行的，从而能把多个虚拟基类子对象合并成派生类中的**一个共享实例**，提供了必要的灵活性。
- 虚拟派生**不是基类本身的显式特性**，而是它与派生类之间的关系。
- 即使基类是虚拟的，**仍然可以通过该基类类型的指针或引用操纵派生类对象**。

### 6.4 现代写法与代价

- 菱形继承中的**最派生类**负责初始化虚拟基类（中间类对虚拟基类的初始化被忽略）。
- 代价：对象需额外的 **vbase/vtt 指针**记录虚拟基类偏移，访问虚拟基类成员要**多一次间接寻址**，构造/析构顺序也更复杂。
- 工程建议：能用**组合 + 接口（纯虚基类）+ `unique_ptr`** 就不要用多继承；虚继承基本只在必须共享同一基类子对象的少见场景才用。

---

## 7. 关键结论速览

1. **虚函数 + 基类指针/引用 = 运行时多态**；决定调用版本的是"静态类型做名字查找 + 虚函数做动态绑定"。
2. **只有通过基类指针或引用间接指向派生类子类型时，多态才起作用**（《C++ Primer》3rd）。
3. **覆写 vs 重载**三点差异：不同类 vs 同类；签名相同 vs 参数不同；必须 `virtual` vs 与 `virtual` 无关。
4. **纯虚函数 `= 0`** → 抽象基类不可实例化，派生类必须实现。
5. **基类析构应为 `virtual`**，否则 `delete` 基类指针不会调用派生类析构，可能内存泄漏。
6. **虚继承**用于解决多继承下基类子对象重复（`iostream` 菱形），用"按引用组合"共享唯一虚拟基类子对象。
7. 原文结论：**不存在所谓"隐藏规则"**（整理者按：现象归因正确，但"名称隐藏"在现代 C++ 中确有其事，见 §3.2）。

---

## 8. 整理者补充与勘误

### 8.1 原文代码的时代痕迹（现代编译需修正）

- `#include <iostream.h>` → `#include <iostream>` + `using namespace std;`（或写全 `std::cout`）。
- `void main(void)` → `int main()`。
- 原文 `cout` 未加 `std::` 前缀、依赖旧式头文件把名字注入全局命名空间。

### 8.2 遗漏的关键机制：vtable / vptr

原文只提到"参见 *Inside the C++ Object Model*"，未展开实现原理，简要补上：

- 每个**含虚函数的类**有一张**虚函数表（vtable）**，编译器在**构造期**把对象的 **vptr** 指向它。
- 通过基类指针调用 `p->print()` → 读 `vptr` → 按固定**槽位下标**取函数地址 → 间接调用。这就是"动态绑定"，槽位下标在**编译期**就已确定，所以不是字符串查找。
- `sizeof(对象)` 会多出一个指针（vptr = 1 个机器字）；空基类优化也可能被 vptr 破坏。
- 多重继承下对象可能有**多个 vptr**，并需要 **thunk** 做 `this` 指针调整；虚继承再加 vtordisp/vbase 等偏移信息。
- vptr 在**构造函数里被逐层设置**，因此：**构造/析构期间调用虚函数不会分派到派生类**（此时对象的动态类型还是当前层）。

### 8.3 常见坑

| 坑 | 说明 |
|---|---|
| **构造函数/析构函数不能是虚函数** | 对象尚未/已不再完整，vptr 语义不存在；但虚析构本身例外（可声明，且必须有定义） |
| **析构期间调用虚函数** | 同上，只分派到当前层版本，容易误以为会走派生类逻辑 |
| **默认参数是静态绑定的** | `virtual void f(int x = 10)`，通过基类指针调用时用的仍是**基类的默认值 10**，与被调用的函数体可能不匹配（经典陷阱） |
| **`override` 写错签名** | C++11 前会静默变成"新函数 + 名称隐藏"，日志/行为诡异；一律加 `override`/`final` |
| **在构造/析构中调用纯虚函数** | 直接是**未定义行为**（运行时崩溃） |
| **虚函数并非万能** | 需明确"是否真的需要运行期多态"；确定不覆写就**不要**加 `virtual`（省 vptr、允许内联与值语义） |
| **值语义与切片（slicing）** | `Base b = derivedObj;` 只拷贝基类子对象；多态必须用指针/引用 |
| **性能** | 虚调用无法（通过指针时）内联、可能有分支预测失败；热点路径可用 CRTP / 模板做**编译期多态**替代 |

### 8.4 与相关特性的关系

- `final`（C++11）：禁止继续覆写，或禁止被继承；`override`：编译期校验覆写。
- `dynamic_cast` / `typeid` 依赖 RTTI，需要类**含虚函数**（有 vptr）才可用；`dynamic_cast` 到引用失败会抛 `std::bad_cast`。
- 纯虚接口 + `unique_ptr<Interface>` 是现代 C++ 中"父类声明、子类实现"的推荐形态（比裸 `new`/`delete` 安全）。
- 与之相对的概念：**名称隐藏（name hiding）**、**`using` 引入声明**、**ADL**；以及 Java/C# 中"所有非 static/private 方法默认虚"的设计差异（C++ 需显式 `virtual`）。

---

## 9. 原文引用与延伸阅读

- *Inside the C++ Object Model*（Stanley B. Lippman, Addison Wesley, 1996）——虚机制实现原理。
- *C++ Primer* 3rd Edition——"只有在通过基类指针或引用间接指向派生类子类型时多态性才会起作用"。
- 林锐《高质量C++/C 编程指南》(2001)——原文引用了其"隐藏规则"并加以反驳。
- 页面底部相关推荐文题目：《10. C++关键字 virtual 用法》《C++基础之关键字——virtual 详解》《详解 C++ 中的 virtual》《C++ 中 virtual 详解》《【C++】类中 virtual 详解》等。
