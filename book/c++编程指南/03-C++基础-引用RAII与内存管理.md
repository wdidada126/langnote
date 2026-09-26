# 03 C++ 基础——引用、RAII 与内存管理的地基九问

> 对应站点板块：主要内容第 3 板块 `/docs/cpp-basic/`（9 篇，实抓 ✅）。
> 9 篇的题目全是"追问式"：引用为什么存在、RAII 的 ScopeExit 妙用、#ifndef 与 #pragma once、
> new[]/delete[] 必须配对吗、四种转型为什么是四种、nullptr 为什么不是 NULL、
> chrono 时间处理、指针 vs 引用、volatile 到底管什么。
> 这是全站的**方法论样本**：每个"理所当然"的基础概念，追问到源码/汇编/标准定义层。

## 核心概念速览（中英对照）

- **引用即别名** — reference as alias：不是对象，不能重绑定、必须初始化、无空引用；`operator[]` 返回引用是它存在的头号理由
- **资源获取即初始化** — RAII：构造函数拿资源、析构函数还资源，异常路径由语言保证回滚
- **作用域退出守卫** — ScopeExit：把"函数尾要做的事"包进析构执行任意 lambda 的 RAII 对象
- **头文件保护** — include guard (`#ifndef`) vs `#pragma once`：宏防重 vs 编译器按文件身份防重，后者更快但非标准
- **数组 cookie** — array new cookie：`new T[n]` 在元素区前方藏个数/字节数，供 `delete[]` 逐个析构
- **RTTI 转型** — dynamic_cast：依赖虚表旁挂的类型信息，向下转型带运行时检查，失败返回 nullptr/抛 bad_cast
- **空指针字面量** — `nullptr` / `std::nullptr_t`：C++98 的 `0` 兼营整数与空指针两职，nullptr 让它辞职
- **三种时钟** — system_clock / steady_clock / high_resolution_clock：墙钟会回拨，计时必须 steady_clock
- **易变而非原子** — volatile：仅禁止编译器优化掉读写，既不保证原子性也不保证线程间可见性

## 动机：基础板块=面试初筛层的镜像

站方在 `summary`（24 陷阱篇）里自陈目标读者"能背八股但说不清为什么"。
本板块 9 篇即针对这个断层：每个概念给"源码级证据"（NULL 的定义、std::move 的实现、
new[] 的头部 4/8 字节）+ "翻车演示"（不配对 delete 的析构次数）。这决定了阅读姿势：
**把站文当"为什么"的答案模板，把标准当"是什么"的裁判**。

## 机制：九问的机制链

### 引用为什么必须存在（`cpp-reference` / `cpp-ref-vs-pointer`）

站文论证：指针=存地址的整数，引用=变量的别名（"王二小有个外号"）。引用能做的指针都能做，
但**用恰当工具做恰如其分的事**：引用把"非空、不可重绑定、始终代表某对象"写进类型，
让 `vector::operator[]`、`std::cout <<` 链式、swap、输出参数这些场景的意图不可违背。
底层两者同构（指针实现），差别全在契约强度——这一句就是"选引用还是指针"的完整答案：
**参数可能为空或要 reseating → 指针（更要用智能指针）；否则引用**。

### RAII 与 ScopeExit（`cpp-raii`）

站文把 RAII 场景列全（内存/文件句柄/锁/网络连接/计时器），然后给进阶一手：
**ScopeExit**——`template<class F> class ScopeExit { F f; ~ScopeExit(){ f(); } }`，
把"任何清理动作"塞进析构。C 版 future（02 章）与 07 章 goto 式错误回滚对比着看：
RAII 的本质是**把资源回滚的编排权从程序员手里收归语言**（逆构造序析构）。
对照 [../现代C++实战30讲/01-堆栈与RAII.md](../现代C++实战30讲/01-堆栈与RAII.md)：秦叙宝用同一思路做了带
`dismiss()` 的版本（可取消的守卫）。

### 头文件保护二选一（`cpp-pragma`）

`#ifndef`：标准、可移植，但要维护唯一宏名，改名/复制粘贴会漏（两个文件同宏名 → 第二份整体消失，
经典事故）；`#pragma once`：一行、按文件身份（inode/路径）判重，多数编译器还有缓存加速，
但**非标准**、网络文件系统同文件双路径时可能失效。站文结论："现代项目默认 #pragma once，
跨极端平台留 #ifndef 双保险"。C++23 modules（05 章）在更高维度消灭这个问题：**不再文本包含，
自然无需防重**。

### new[]/delete[] 配对与 cookie（`cpp-new-delete`，板块招牌篇）

站文的机器级论证：`new T[n]` 需要知道 n 才能逐个析构，所以在元素数组**头部多分配若干字节**
存 cookie（计数或字节数，实现定义）；`delete[]` 向前找 cookie，从后往前调析构再 free。
四种配对推演：
- `new[] + delete[]`：正确，n 次析构；
- `new[] + delete`：delete 当作单对象，只析构 1 个（调一次析构后把指针中存储的奇怪值喂给 free）→ 站文实测**异常终止**；
- `new + delete[]`：没有 cookie，delete[] 向前读到垃圾计数 → **析构不定次数后崩溃**；
- POD 类型（无析构函数）：libstdc++ 对无析构元素不写 cookie，配对错误"碰巧"不死——
  站文点破"不配对也没事"传言的来源，并强调**这是 UB，不是许可**。
本目录实测（见文末）在 g++ 15.2 上直接**看到了 cookie 本尊**。

### 四种转型各管一段（`cpp-cast`）

C 一个语法 `(T)x` 包打天下，把"意图"压扁了。C++ 按意图拆四份：
`static_cast`=显式化的安全隐式转换（含向下转型但**不检查**）；`dynamic_cast`=带 RTTI 检查的
向下转型（前提：多态类型）；`const_cast`=唯一能扔 const 的手术刀（对真 const 对象写它是 UB）；
`reinterpret_cast`=指针/整数间的位模式重解释，跨平台边界的专用通道。
站文立场与 Core Guidelines 一致：**禁 C 式转型，理由是可 grep、可审、窄化即报警**。

### nullptr 的考古学（`cpp-nullptr`）

证据链：C 里 `NULL=((void*)0)`，C++ 里 NULL 是整数 `0`——因为 C++ 不允许 `void*` 隐式转 T*，
`(void*)0` 根本没法给指针赋值。而"0 既可以是整数也可以是空指针常量"的双面性制造了
`f(0)` vs `f((void*)0)` 重载歧义（经典 `void f(int)/void f(char*)` 例）。
C++11 用 `std::nullptr_t` 的常量 `nullptr` 接管空指针职务，让 0 只当 0。
这一篇是站内少数**直接引标准原文**（C++03 4.10 措辞）的文章。

### chrono 三时钟（`cpp-date`）

`duration<Rep, ratio>` + `time_point<Clock>` + Clock 三件套；核心警告一句话：
**system_clock 会因 NTP/手改而回拨，测时长用 steady_clock**；
high_resolution_clock 只是"最快的那个"，实现上常常=另两个之一的别名。
`time_since_epoch()`、`duration_cast` 的整型截断语义一并讲清。

### volatile 的三条边界（`cpp-volatile`）

站文逐条钉死：volatile 只承诺"**每次访问都真访内存**"（防循环优化/防折叠），
(1) 不保证原子——`volatile int x; x++` 在多线程下照丢更新；
(2) 不保证顺序/可见性——它不参与 happens-before（那是 06 章 atomic 的领域）；
(3) 它的合法用户是**内存映射外设/信号处理函数里的共享量**。
"volatile 当同步用"是中文八股重灾区，这篇是全站的纠偏样本之一。

## 最新演进与工业实践

- **cookie 位置与 ABI**：Itanium ABI 把数组 cookie 定为"分配返回地址之前的 vector cookie"，
  含虚析构/自定义 operator delete[] 时才必写——站文的"4 字节"说法是 32 位时代的遗留，
  64 位 GCC 实测是 8 字节计数+对齐（见文末实测）。
- **`#pragma once` 现状**：所有主流编译器支持且被 C++23 modules 时代大量弃用中；
  Bazel/大型仓惯例仍 guard（对工具链兼容性最好）。
- **chrono**：C++20 加了 `std::chrono::calendar`（year_month_day 等，补了站文只讲 duration 的空白）；
  C++20 `std::chrono::clock_cast` 至今未定稿（⚠️ 勿在面试吹）。
- **工业对应物**：ScopeExit 家族——folly::ScopeGuard、absl::Cleanup、**C++26 已收编 std::at_exit
  （P2589R1，wg21.link/P2589 实测 302 ✅）**：站文手搓版 5 年后成了标准件，这就是训练营知识库的天花板
  与标准流程的距离。dynamic_cast 的性能敏感路径用 abseil 的 `AsPtr` 风格 tag 或
  LLVM RTTI 替代；内存映射设备场景 MSVC 用 `volatile` + `_mm_sfence`，对应 Linux `readl/writel`。
- **训练营属性→真实使用频率**：引用 vs 指针、RAII、include guard 是**每天**的工程决策（高频）；
  cookie 机制、NULL 考古是**面试高频、现场零次**（知道一次就好，不必背）；
  chrono 三时钟在音视频/监控代码里是事故源头级重要（时间戳回拨打崩排序/日志乱序）。

## 实测样例（已实测 g++ 15.2）

复现 `cpp-new-delete` 的核心断言——窥探 `new T[n]` 的 cookie 与逆序析构：

```cpp
#include <cstdio>
#include <cstring>
struct C { int x; ~C(){ printf("~C %d\n", x); } };
int main(){
  C* a = new C[3]{ {1},{2},{3} };
  unsigned long long raw[4];
  memcpy(raw, (char*)a - 32, 32);   // 窥探数组头部（教学性 UB，gcc 会警告）
  printf("words before array: %llu %llu %llu %llu\n", raw[0], raw[1], raw[2], raw[3]);
  delete[] a;
}
```

```
$ g++ -O2 s03.cpp && ./s03        # 编译期另有 -Wstringop-overread 警告，本体即教材
words before array: 0 0 864753835102781372 3
~C 3
~C 2
~C 1
```

解读：返回指针前第 8 字节处就是计数 **3**（那个大数是堆基址/元数据残影），
`delete[]` 按 3→2→1 **逆序**析构——站文"头部藏长度、倒着拆"的模型在 64 位 MinGW 上成立；
编译器对窥探行为的警告恰好佐证"这是 UB 级侦查，不是可依赖的 ABI"。

## 导航

- 返回：[00-总览与阅读地图](00-总览与阅读地图.md) · 单文件登记：[../c++编程指南.md](../c++编程指南.md) · [../C++系列·总索引.md](../C++系列·总索引.md)
- 上一章：[02-C语言基础与内存模型](02-C语言基础与内存模型.md) · 下一章：[04-C++进阶-移动转发与泛型设施](04-C++进阶-移动转发与泛型设施.md)
- 对读：[../Effective_Modern_C++.md](../Effective_Modern_C++.md)（条款 1–22 覆盖本板块全部主题的权威版）；
  [../C++标准库/02-通用工具与智能指针.md](../C++标准库/02-通用工具与智能指针.md)
