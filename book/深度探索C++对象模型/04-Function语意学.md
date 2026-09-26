# 第 4 章 Function 语意学（The Semantics of Function）

> 对应《深度探索C++对象模型》第 4 章：4.1 Member 的各种调用方式（nonstatic / virtual / static）/
> 4.2 Virtual Member Functions（vptr 与 vtable、多重继承下的虚拟函数、虚拟继承下的虚拟函数）/
> 4.3 函数的效能 / 4.4 指向 Member Function 的指针 / 4.5 Inline Functions。
> 阅读地图见 [00-总览与阅读地图.md](00-总览与阅读地图.md)；单文件版见 [../深度探索C++对象模型.md](../深度探索C++对象模型.md)。
> 上一章管"数据怎么躺"，这一章管"函数怎么被叫到、`this` 怎么被喂对"。

## 核心概念速览（中英对照）

- **this 指针** — this pointer：非静态成员函数的隐式首参数；实测 x64 下经 `%rcx` 传入（Microsoft x64 调用约定）。
- **静态成员函数** — static member functions：无 `this`、无 vptr 参与，普通函数 + 类作用域 + 访问权——书中"当回调函数用零开销"的断言今天依旧成立。
- **vptr** — virtual table pointer：对象头部指针；**虚拟调用** = `*(obj)` 取表 + `表[槽]` 取函数 + 间接 call。
- **vtable 槽序** — vcall offset / slot order：cfront 按**字典序**排 vtable（书中反复吐槽的历史包袱）；
  Itanium/MSVC 按**声明序**——槽 0 归第一个虚函数或第一个被重写的虚函数。
- **thunk** — thunk：vtable 槽里存放的"先调 this 再跳真身"的小段代码，多重继承的次基类入口靠它；
  实测符号 `_ZThn16_N7Derived2vfEv`（non-virtual thunk for offset 16）。
- **vcall offset** — 虚调用偏移：虚拟继承下"到 this 调整量"不再是编译期常数，槽里存**偏移的偏移**，
  调用点多两跳（Itanium ABI §2.5.2，文档 ✅）。
- **指向成员函数的指针** — pointer-to-member-function：Itanium 实测 16 字节 {delta, ptr/offset}，
  低位标签区分虚/非虚两条通路。
- **devirtualization** — 去虚化：编译器证明动态类型唯一后把间接 call 换成直调——书中"效能"一节的现代续集。
- **内建展开** — inline expansion：4.5 的告诫（参数多次求值、局部变量命名冲突）是宏思维向函数语义的迁移税。

## 动机：同一个 `p->fly()`，三条完全不同的机器路径

```asm
; 实测 g++ 15.2 -O0 (x86-64)，🔧 t5.cpp 反汇编节选
; drive(): p->g(); p->h();
mov  (%rax), %rax        ; ① 读对象头 8 字节 = vptr
mov  (%rax), %rdx        ; ② 取 vtable 槽 0
call *%rdx               ; ③ 间接调用（虚拟函数 g）
call _ZN1V1hEv           ; ④ 非虚函数 h：编译期直调，零运行时查表
```

非虚：签名改写 + 直调，与 C 函数同价。静态：连 this 都没有。虚：三跳。
把三条路径的指令数、可内联性、可缓存性摆在一起，就是 4.3"函数的效能"的原始论证。

## 机制

### 1. 三种成员函数的调用翻译（4.1）

| 形式 | 编译器改写 | 运行时成本 |
| --- | --- | --- |
| `obj.f(args)`（nonstatic） | `X::f(&obj, args)` | 0（等价 C 函数） |
| `obj.g()`（virtual） | `(*(obj->vptr)[slot])(&obj)` | 1 load + 1 间接 call |
| `X::s()`（static） | `X_s()`，类作用域解析 | 0；可当回调、可放函数指针 |

### 2. vtable 内容与 this 的静态调整（4.2 实测）

```text
struct Base1{int b1; virtual vf;}  Base2{int b2; virtual vf;}
struct Derived : Base1, Base2 { void vf() override; }
Derived 对象: [Base1 子对象 0-15][Base2 子对象 16-31][d 32-35][pad]
  vtable#1 (@Base1 vptr): [Derived::vf]                ; 主基类直连真身
  vtable#2 (@Base2 vptr): [_ZThn16_N7Derived2vfEv]     ; thunk: sub this,16; jmp Derived::vf
实测 nm(t3.o): _ZN7Derived2vfEv 与 _ZThn16_N7Derived2vfEv 两个符号并列
实测反汇编 setup()(t2): static_cast<Base2*>(d) 编译成 add $0x10,%rax —— 编译期常量调整
```

cfront 语境差异：书中"vtable 按函数名字典序排列、派生类槽位可能整表重排"是 **cfront 的实现规定**；
现代 Itanium/MSVC 按声明序 + 追加序，指针比较与偏移都友好得多。读第 4 章时凡遇"槽位不可预期"都应先想是不是这段历史。

### 3. 虚拟继承下的虚调用（4.2 末）

虚基类子对象位置每对象可变 ⇒ this 调整量不能在 thunk 里写死。
Itanium 方案（✅ ABI 文档 §2.5.2）：vtable 该槽存指向 **vcall offset 表项**的负偏移（表项就在函数槽下方的
vcall offsets 区），调用序列变成：
`load vptr → load 槽 → 按 vptr+负偏移再 load "this 调整量" → 调整 this → call`。
书中用 cfront 的 vtable-vbase 混合表讲这事，现代对应物即上述四级指针追踪——**比 MI 慢，比 MI 灵活**。

### 4. 指向成员函数的指针（4.4）

实测（g++ 15.2 x64，🔧 t6）：

```text
sizeof(void (Virt::*)()) == 16          ; {long delta; long ptr}
非虚 &Virt::g: 原始字节 = (函数地址, 0)   ; delta=0，直接 call
虚   &Virt::f: 原始字节 = (1, 0)          ; ptr 槽存 vcall offset(带最低位标签)，调用时查 vtable
```

书中文脉：cfront 用"字符串表 + 运行时查名字"实现 PMF，代价巨大；AT&T 曾设计"槽 0 存类描述符"方案。
Itanium 的两词表示是第三条路——比 cfront 快几个数量级，但仍是**开放世界**（跨 DSO 比较无定义）。
MSVC 更折腾：单继承/多继承/虚继承三套成员指针模型（`/vmb /vmg /vmm` 家族）⚠️ 本机 cl 未逐一实测。

### 5. Inline（4.5）

书中两条告诫 + 一条本质：
- 参数被宏式展开会**重复求值**（`inline int max(a,b){return a>b?a:b;}` 遇 `max(i++,j)` 变味——
  这恰恰是函数语义优于宏之处：实测 gcc 对带副作用参数按引用语义求值一次）；
- 函数体内声明的"局部变量"在 cfront 靠名字 mangling 避免冲突，现代直接放栈帧，问题消失；
- 本质：inline 是**编译期符号可见性**问题，不是行号归属问题（跨 TU 需 LTO 或头文件可见）。

## 权衡

- 虚调用三跳 vs 函数指针直调：多一层 vptr 但换来可扩展性；vtable 本身可被 patch（mock/拦截框架利用这点，
  也利用它的脆弱——见"演进"）。
- thunk 让 vtable 槽类型统一（都是函数指针），代价是间接跳一次；vcall offset 让虚基可移动，
  代价是把编译期常量变成两次运行期 load。**MI 便宜 VI 贵**在函数侧同样成立。
- PMF 的 16 字节 + 判别分支 vs "把虚函数表索引进对象头"的 table-driven 假想模型（第 1 章）。

## 相邻概念对比

- **虚函数 vs std::function/type erasure**：前者表在编译期生成、对象头记账；后者表在堆上、
  构造时生成——同样的分派语义，不同的布局归属。
- **重载决议 vs 虚分派**：重载看**静态类型**编译期定，虚分派看**动态类型**运行期定；
  `base->f(1)` 与 `base->f(1.0)` 可能落进同一个 vtable 槽的**不同函数**（先重载后虚）。
- **this 调整（static_cast）vs this 调整（dynamic_cast）**：前者编译期 `add 0x10`（实测 t2），
  后者进 `__dynamic_cast` 运行时（见 [07-站在对象模型的尖端.md](07-站在对象模型的尖端.md)）。

## 最新演进与工业实践

- **`override`/`final`（C++11）**：把"签名没对上→静默失配"变成编译错误——书中 4.2 多个段落吐槽的
  正是这一 cfront 时代大坑的解药。
- **去虚化三件套**：Clang/GCC 在 LTO+PGO 下做 devirtualization（`-fprofile-generate` 采样后单态调用直调）；
  LLVM 文档见 [llvm.org/docs/](https://llvm.org/docs/)（✅ 站点可达）。这是 4.3 "函数的效能"的当代答案：
  先证明唯一实现，再消灭间接。
- **vtable 破坏型测试的边界**：GoogleMock 的 `MOCK_METHOD` 只能 mock **虚**函数，且"不得在构造/析构期调用 mock 方法"
  ——因为此刻 vptr 还指向半生不熟的表（与本节机制同源，见 [05-构造析构拷贝语意学.md](05-构造析构拷贝语意学.md)）；
  仓库 ✅ [google/googletest](https://github.com/google/googletest)。
- **C++23 `[[assume]]` 与契约式**：不直接改写 vtable，但给"编译器证明调用目标唯一"提供了新的假设注入口；
  主流实现（clang `[[assume]]`）已落地 ⚠️ 与虚分派的交互未见 g++ 15.2 实测，不作断言。
- **函数语义的静态化**：concepts（C++20）+ 模板把"运行时多态"大量替换为"编译期多态"，vtable 三跳归零
  ——对照 [../C++20模板元编程.md](../C++20模板元编程.md) 与 [../C++语言的设计与演化.md](../C++语言的设计与演化.md)。

## 常见误区与自查

1. ❌"虚函数比非虚慢在函数本身"——慢在三跳取址 + 间接 call 打断预测/内联，函数体一样快。
2. ❌"vtable 属于对象"——属于**类**；对象只持有指过去的那根 vptr（每类一份、多继承次基各一份）。
3. ❌"成员函数指针 = 普通函数指针"——Itanium 下 16≠8 字节，且带虚/非虚标签分支（实测 t6）。
4. ✅ 自查：写出 thunk 存在的原因，并说明虚拟继承下为什么 thunk 不够用了。

## 交叉链接

- 上一：[03-Data语意学.md](03-Data语意学.md)；下一：[05-构造析构拷贝语意学.md](05-构造析构拷贝语意学.md)
- vptr 何时被谁设置：[05-构造析构拷贝语意学.md](05-构造析构拷贝语意学.md)
- RTTI 与 dynamic_cast 的成本对照：[07-站在对象模型的尖端.md](07-站在对象模型的尖端.md)
- Itanium ABI 官方文本（vcall offsets §2.5.2、构造期 vtable §2.6）：✅ https://itanium-cxx-abi.github.io/cxx-abi/abi.html
- 总览：[00-总览与阅读地图.md](00-总览与阅读地图.md)；单文件版：[../深度探索C++对象模型.md](../深度探索C++对象模型.md)；
  系列导航：[../C++系列·总索引.md](../C++系列·总索引.md)
- 延伸阅读：性能视角见 [../提高C++性能的编程技术.md](../提高C++性能的编程技术.md)；
  `override/final` 条目见 [../Effective_Modern_C++.md](../Effective_Modern_C++.md)；
  旧版 PMF 惯用法见 [../More%20Effective%20C++.md](../More%20Effective%20C++.md)。
