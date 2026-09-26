# 第 3 章 Data 语意学（The Semantics of Data）

> 对应《深度探索C++对象模型》第 3 章：3.1 Data Member 的绑定 / 3.2 Data Member 的布局 /
> 3.3 Data Member 的存取（static 与 nonstatic）/ 3.4 "继承"与 Data Member（只要继承不要多态、加上多态、
> 多重继承、虚拟继承）/ 3.5 对象成员的效率 / 3.6 指向 Data Members 的指针。
> 阅读地图见 [00-总览与阅读地图.md](00-总览与阅读地图.md)；单文件版见 [../深度探索C++对象模型.md](../深度探索C++对象模型.md)。
> 本章主题：**数据成员为什么、以及如何在布局上"属于"类，却在名字上"属于"作用域。**

## 核心概念速览（中英对照）

- **Data Member 的绑定** — binding of a data member：成员函数体内引用的名字，绑定发生在**成员函数定义处**
  而非类声明处——类中后声明的成员在先前定义的成员函数里不可见（cfront 语意，现代编译器一致）。
- **nonstatic 数据成员** — nonstatic data members：每对象一份；对象内布局由编译器决定（书中常见策略：声明序）。
- **static 数据成员** — static data members：零个字段占用于对象；本质是"带名字修饰的全局变量"。
- **名字修饰** — name mangling：`Empty::s` 实测符号 `_ZN5Empty1sE`（Itanium）/ MSVC 风格 `?s@Empty@@2HA`——
  类作用域在链接期靠修饰名保留。
- **成员偏移量存取** — offset-based access：`this->m` ≙ `*(this + offset)`；实测 `&Virt::a` 的指向成员数据值就是 **8**
  （vptr 占 0–7）。
- **指针成员（pointer-to-member）** — pointer to data member：Itanium 下就是一个字节偏移（实测 8 字节）；
  cfront 曾用"字符串名字 + 运行时查表"（书中语境，⚠️ 现代无人生还）。
- **primary base subobject** — 主基类子对象：多重继承下排在偏移 0、与派生类共享 vptr 的那个非虚基类。
- **vbase offset / vbptr** — 虚基偏移：Itanium 记在**虚表**的 vbase offset 区（实测对象内无偏移字段：`Mid1` 32 = vptr+x+pad+内嵌 VBase）；MSVC 才每对象存 vbptr→vbtable。
- **对象切片** — object slicing：值传递派生类到基类，"切掉"派生部分——3.4 布局知识直接解释其代价与风险。
- **空基类优化** — Empty Base Optimization (EBO)：无状态基类可与派生类首成员重叠（实测 `offsetof(Eb,x)==0`）。

## 动机：数据不关心"类"，类只关心布局

C++ 的数据成员从来不是"封装进对象的过程"——对象里**只有数据**（第 1 章）。本章回答三个更细的问题：
名字如何解析到偏移；继承树如何折叠成一段线性内存；指向成员的指针凭什么这么贵/便宜。

## 机制

### 1. Data Member 的绑定（3.1）

```cpp
class Sandbox {
  int object_a;
  int member_function() { return object_b; }  // ❌ 此时 object_b 尚未声明
  int object_b;
};
```

书中语境：cfront 按"到定义处为止可见"解析；**实测 g++ 15.2 同样拒绝**（类内成员函数体在类完整前解析，
仅两阶段查找救得了模板）。要点：成员函数定义顺序参与名字绑定，成员**声明**顺序参与布局——两件事互相独立。

### 2. 布局策略（3.2）

标准只规定"非静态数据成员按声明顺序分配（对于 standard-layout 类）"，其余留给 ABI：

```text
实测 g++ 15.2 (Itanium x64)              实测 MSVC 14.38 x64（同一份源码）
NonVirt{int a; double b; char c} = 24     24
Virt{int a; 2×virtual}           = 16     16   (vptr@0, a@8 —— 两家一致)
Derived{Virt 基 + int d}         = 16     24   ★ d@12 vs d@16
Multi{NonVirt 基 + Virt 基 + int m} = 48  48   (两家都把含 vptr 的 Virt 提到偏移 0)
```

★ 处的差异是经典 ABI 分歧：**Itanium 允许派生类复用基类尾部填充**（d 填进 Virt 的 12–15 空洞），
MSVC 保守地另起对齐段。同一程序两个编译器 `sizeof` 不同——跨 ABI 传二进制布局必须重编（详见
[08-专题-现代编译器视角Itanium与MSVC.md](08-专题-现代编译器视角Itanium与MSVC.md)）。

### 3. static vs nonstatic 的存取（3.3）

- **static**：对象里没有字段；存取=直接引用修饰过的全局符号。实测 nm：`_ZN5Empty1sE` 落在 **BSS**，
  `sizeof(Empty)==1`。cfront 时代"static 成员函数以普通全局函数调用、零 this 开销"的论证今天完全兑现。
- **nonstatic**：`obj.m` 编译成 `*(obj + 常量偏移)`——与 C 结构体成员访问同价，**封装不产生运行时代码**。
  只有当偏移要经过继承链/vbase 时才升级为动态计算（见 4）。

### 4. 继承如何改变"取一个成员"的成本（3.4）

```text
(a) 只要继承不要多态        (b) 加上多态            (c) 多重继承              (d) 虚拟继承
Base{int m}  Derived{n}     Base 带虚函数            Multi: Virt@0 NonVirt@16   Diamond: Mid1@0 Mid2@16
Derived.m ≙ this+0          Derived 也变多态          m@40                       z@28 VBase@32
一次常量偏移                 多一次 vptr(8) 前置       访问 Base1 系成员恒+0/常数   访问 VBase::v:
                             取址即静态绑定            访问 Base2 系成员恒+16      this + *(vptr + vbase_offset槽)
                                                                    ↑ Itanium:偏移记在虚表→load vptr+查表;MSVC:对象内 vbptr+查 vbtable
```

实测（g++ 15.2，🔧 t18 十六进制 dump）：`Mid1` 完整对象 32 字节 = vptr(8)+x(4)+pad(4)+内嵌 VBase 子对象(16)，
**对象里找不出一块"虚基偏移字段"**；`Diamond`（48B）= Mid1 自身(16)+Mid2 自身(12，vptr@16/y@24)+z@28+VBase@32(16)。
"到虚基的距离"在 Itanium 里是**随虚表版本走**的表项（✅ 规范 §2.5.2：vcall offsets → vbase offsets → offset-to-top
→ type_info → 函数槽）。书中 cfront 的虚基表观方案请当作历史语境读 ⚠️；现代两家：
Itanium 用**虚表内数值偏移项**，MSVC 用 **vbptr→vbtable 表**（实测 MSVC 符号 `??_8Diamond@@7B...` 即 vbtable）。

### 5. 指向成员的指针（3.6）

实测（g++ 15.2 x64）：`sizeof(int Virt::*)==8`，值就是字节偏移 8；`sizeof(void(Virt::*)())==16`
（两字：{this 调整量, 函数地址或虚表偏移}，见 [04-Function语意学.md](04-Function语意学.md)）。
书中"指向成员的指针很慢"针对的是 cfront 的字符串查表实现与 MSVC 的多模型表示；
Itanium 时代数据成员指针就是一次加法，成员函数指针是一次"判别 + 间接"。

## 权衡

| 设计点 | 便宜 | 昂贵 |
| --- | --- | --- |
| 声明序布局 | 调试器可重算偏移、热补丁友好 | 重排成员=ABI 破坏 |
| 复用基类尾填充（Itanium） | sizeof 更小（Derived 16 vs 24） | 跨 ABI 布局不一致 |
| 虚基偏移记账（Itanium 进虚表/MSVC 进对象） | 虚基共享正确、菱形可解 | 虚表变长或每对象 +8B，成员访问多两跳 |
| pointer-to-member 用偏移 | 常数开销、可内联 | 无法表达"位域/虚成员"扩展性 |

## 相邻概念对比

- **数据成员 vs 静态数据成员**：前者在对象里、按 this 寻址；后者在 BSS、按符号寻址——`sizeof` 是试金石。
- **多重继承 vs 虚拟继承**：MM 的偏移全是**编译期常量**（每类一张布局）；VI 的虚基位置是**运行期变量**
  （经虚表/vbtable 查偏移）。这就是"虚继承更贵"的全部秘密。
- **对象成员 vs 指针成员**：内含（3.5）=构造析构自动、缓存友好；指针=可延迟、可多态、多一次解引用。

## 最新演进与工业实践

- **standard-layout 保证（C++11）**：满足条件的类与 C struct 布局互操作（`offsetof` 合法化），
  这是"声明序"从惯例升级为契约的部分范围；std C++11 §18.10/§9 语境。
- **`[[no_unique_address]]`（C++20）**：成员版的 EBO，实测把 `Wrap{Empty e; int x}` 从 8 压回 4。
- **跨 DLL 边界的类布局冻结**：Qt/Chromium 等工程要求导出类改布局必须重编所有下游，
  这正是 3.2"布局是 ABI 契约"的当代回响（Pimpl 惯用法即解药，见 [../C++API设计.md](../C++API设计.md)）。
- **clang 实现锚点**：`clang::ItaniumRecordLayoutObj` 与 `MicrosoftRecordLayoutObj`（`lib/AST`、`lib/CodeGen`）
  分别实现两家的 3.2/3.4 策略，源码 ✅ [llvm/llvm-project](https://github.com/llvm/llvm-project)。
- **协程帧（C++20）**：promise/局部变量按"帧布局"堆分配，是"编译器决定数据放哪"这一主题的最新战场
  （对照 [../C++20模板元编程.md](../C++20模板元编程.md) 相关讨论 ⚠️ 具体帧布局未实测）。

## 常见误区与自查

1. ❌"成员函数声明在类里的位置影响数据布局"——不影响；**数据成员**声明序才影响（且两家 ABI 对填充态度不同）。
2. ❌"`sizeof` 含静态成员"——不含（实测 Empty=1，仅占位）。
3. ❌"虚继承只是省内存"——它是用**虚表/vbtable 里的偏移账本**换共享基类的唯一实例。
4. ✅ 自查：画出 `Diamond` 的 48 字节布局，标出两份 vptr、共享 VBase 的位置，并说出"到 VBase 的距离"两家分别记在哪。

## 交叉链接

- 上一：[02-构造函数语意学.md](02-构造函数语意学.md)；下一：[04-Function语意学.md](04-Function语意学.md)
- 虚函数表/ thunk 细节：[04-Function语意学.md](04-Function语意学.md)；构造时偏移量何时写入：[05-构造析构拷贝语意学.md](05-构造析构拷贝语意学.md)
- 总览：[00-总览与阅读地图.md](00-总览与阅读地图.md)；单文件版：[../深度探索C++对象模型.md](../深度探索C++对象模型.md)；
  系列导航：[../C++系列·总索引.md](../C++系列·总索引.md)
- 同主题延伸：SGI STL 的 EBO 应用见 [../STL源码剖析.md](../STL源码剖析.md)；
  布局敏感的性能账目见 [../提高C++性能的编程技术.md](../提高C++性能的编程技术.md)。
