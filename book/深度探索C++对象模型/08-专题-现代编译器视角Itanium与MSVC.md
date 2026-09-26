# 专题 现代编译器视角下的对象模型：Itanium ABI 与 MSVC 实测对照

> 补编章，**不属于原书 7 章**。《深度探索C++对象模型》的参照系是 cfront 与 1996 年主流编译器；
> 本目录各章凡"书中语境"与"现代实现"分叉处，都汇聚到本章做系统性对照。
> 全部实测在两台同机工具链完成：**MinGW g++ 15.2（x86-64，Itanium C++ ABI）** 与
> **MSVC 工具集 14.38.33130 / cl 19.38（VS2022 17.13，x64）**；临时工程置于仓库外
> `D:\develops\tmp\cppsnippets_objectmodel\`，仓库内不留任何 .cpp/.o/.exe。
> 阅读地图见 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 核心概念速览（中英对照）

- **Itanium C++ ABI** — 64 位 POSIX 世界（Linux/macOS/*BSD）事实标准，GCC/Clang 共同实现；
  规范文本 ✅ https://itanium-cxx-abi.github.io/cxx-abi/abi.html（本次核实可达，含 §2.5 vcall offsets、
  §2.6 构造期虚拟表、§2.9.4 RTTI Layout）。
- **MSVC C++ ABI** — Windows 原生工具链布局：文档**不完整公开**，社区整理见
  [vblendpd/MSVC-ABI "64-bit C++ ABI Analysis"](https://github.com/vblendpd/MSVC-ABI)（仓库存在 ✅，内容 ⚠️ 非官方）。
- **名字修饰** — name mangling：`Foo::bar()` → `_ZN3Foo3barEv`（Itanium，Z 前缀式）vs `?bar@Foo@@QEAAXXZ`
  （MSVC，反问号起始式）——**两家二进制永不互操作**的第一道墙。
- **primary base** — 主基类：两家都要挑"继承 vptr 的那个基"，但判据与摆放策略不同（见对照表）。
- **tail padding reuse** — 基类尾部填充复用：Itanium 允许派生成员填进基类子对象的对齐空洞，MSVC 不允许——
  实测同一源码 `sizeof(Derived)` = 16 vs 24。
- **thunk vs 匿名调整码** — Itanium 的 `_ZThn/_ZTv` 符号级 thunk vs MSVC 的 vftable 槽内嵌调整片段
  （obj 级实测：MSVC 目标文件**找不到** thunk 符号，但运行期 this 调整正确）。
- **COL（CompleteObjectLocator）** — MSVC 特有：vftable 前置的类型定位记录，`dynamic_cast`/异常匹配/
  `/RTC` 家族都从它出发；对应 Itanium 的 vtable 头部 offset-to-top + type_info 两字。
- **vbtable vs vbase offset 区** — 虚基记账：MSVC 每带虚基的对象存 vbptr→vbtable（实测符号 `??_8Diamond@@7B...`）；
  Itanium 对象里**不放**偏移字段（实测 `Mid1` 32 = vptr+x+pad+内嵌 VBase 子对象，无任何额外槽），
  "到各虚基的距离"记在**虚表的 vbase offset 区**（✅ 规范 §2.5.2）。两家把账本记在不同地方。

## 动机：把书当"双镜头"读

书里的每一句"通常实现是……"在今天都有两个答案。写跨平台库、读崩溃现场的 this 值、
或者只是想知道"为什么我的对象大 8 字节"，都需要这张对照表。

## 机制：同一份源码，两套布局（全部实测）

### 1. 尺寸与偏移对照（🔧 t1.cpp，两编译器各编译运行）

| 类型 | g++ 15.2 (Itanium x64) | MSVC 14.38 (x64) | 差异解读 |
| --- | --- | --- | --- |
| `NonVirt{int a;double b;char c}` | 24 | 24 | 无机制，两家同 |
| `Virt{int a;虚×2}` | 16（vptr@0，a@8） | 16（a@8） | x64 下两家 vptr 都在偏移 0 |
| `Derived:Virt{int d}` | 16，**d@12** | 24，**d@16** | Itanium 复用基类尾填充；MSVC 不复用 |
| `Multi:NonVirt,Virt{int m}` | 48，Virt@0 NonVirt@16 m@40 | 48，同 | 两家都把"含 vptr 的基"提为主基放 0 位 |
| `Mid1:virtual VBase{int x}` | 32 = vptr+X+pad+内嵌VBase(16)，无对象内偏移字段 | 32（含 vbptr→vbtable） | 记账位置不同：虚表 vs 对象 |
| `Diamond` | 48（z@28，VBase@32） | 56（z@32，VBase@40） | 尾填充不复用逐级放大 |

### 2. 符号与表结构对照（🔧 t1/t3，nm 与 dumpbin）

```text
事项            g++ 15.2 实测符号                 MSVC 14.38 实测符号
默认构造         _ZN4VirtC1Ev / C2Ev              ??0Virt@@QEAA@XZ（无 C1/C2 双份之分）
虚析构三件套      D1(析)/D2(基析)/D0(deleting)      ??1(析) / ??_E(deleting) / ??_G(scalar deleting)
vtable          _ZTV4Virt (R 段)                 ??_7Virt@@6B@
type_info       _ZTI4Virt / _ZTS(名字串)          ??_R0?AVVirt@@@8 + COL（`??_R...` 符号族）
完整对象构造      _ZTC7Diamond0_4Mid1              未见独立同类符号，职责由 COL/vbtable 承担 ⚠️ 未逐符号核实
thunk           _ZThn16_N7Derived2vfEv           obj 中未见对应符号(运行期正确) ⚠️ 同上
虚基记账         虚表 vbase offset 区(对象内无字段)   ??_8Diamond@@7BMid1@@@8 (对象内 vbptr→vbtable)
```

### 3. 调用序列对照（🔧 t2/t5/t9 反汇编）

- 虚拟调用两家同构：`load vptr → load 槽 → call`，`this` 已按静态类型调整完毕；
  MSVC 实测 `setup()` 里 `static_cast` 也是 `add rax,10h` 编译期常量。
- 差异在**次基类入口**：Itanium vtable 槽放 `_ZThn16_...` thunk 地址；
  MSVC 目标函数列表里看不到独立 thunk（实测 /Od obj 仅 4 个函数），调整由编译器生成在
  vftable 引用的代码片段中（其组织方式属未公开细节，⚠️ 依社区文档描述为"thunk 码 + COL 配合"）。
- **构造期**：实测 g++ 在 ctor 开头写 vptr 且虚调用直调本类版本；MSVC 同行为（t9 运行输出一致），
  语意由标准锁定，两家只是表与记账方式不同。

### 4. 成员指针与 RTTI 表示

| 事项 | Itanium（实测） | MSVC |
| --- | --- | --- |
| 指向数据成员 | 8 字节 = 字节偏移（`&Virt::a`→8） | 4/8 字节偏移（单/多继承模型下） ⚠️ 未实测 |
| 指向成员函数 | 16 字节 {delta, 带标签的 ptr/vcall offset} | 16 字节（general 模型）；`/vmb` 等可换小模型 ⚠️ 未实测 |
| dynamic_cast | 调 `__dynamic_cast`（实测 U 符号） | 调内部 `__adjust_pointer`/COL 搜索 ⚠️ 未实测 |
| typeid 名字 | "1A"（mangled，实测） | ".?AVA@@"（修饰名原文，据社区文档 ⚠️） |

## 附录：本目录全部实测的复现配方（🔧）

```bash
# 工具链: MinGW g++ 15.2 (x86-64) 与 VS2022 17.13 的 cl 19.38 (工具集 14.38.33130)
# 临时目录(仓库外): D:\develops\tmp\cppsnippets_objectmodel
g++ -std=gnu++23 t1.cpp -o t1.exe && ./t1.exe      # 尺寸/偏移对照表(§1)
nm t1.exe | grep -E "ZTV|ZTI|ZTS|ZTC|ZThn"          # 符号族对照(§2)
objdump -d --no-show-raw-insn t2.o                  # this 调整与虚调用序列(§3)
g++ -std=gnu++23 t9.cpp -o t9.exe && ./t9.exe       # 次基类虚分派运行期正确性
cl /std:c++latest t1.cpp /Fe:t1msvc.exe             # MSVC 侧: 先 call vcvars64.bat
dumpbin /symbols t1msvc.obj | findstr ??            # MSVC 修饰名族
```

注意两点踩坑记录：① MSVC 的 `vcvars64.bat` 若加 `>nul 2>&1` 静默，在部分机器上会导致
INCLUDE 未注入（本次实测如此），裸调用即正常；② `offsetof` 用于基类子对象是编译扩展，
两家用"全局对象地址差"替代（🔧 t1 手法）。

## 权衡

- **尾填充复用**：省内存（本例 −8B/对象）但布局随编译器版本敏感；MSVC 的保守换来"加成员不重排老成员"
  的稳定性红利——两种哲学没有胜负，只有边界。
- **公开规范 vs 既成事实**：Itanium 有据可查（上表 ✅ 章节号）；MSVC 依赖逆向社区 + 微软零散文档，
  老 MSDN 链接大面积失效（本次核实 `learn.microsoft.com/...vftables...` 等多页 404）——
  写工具/插桩/安全研究时，引用 MSVC 布局结论务必标版本与出处。

## 相邻概念对比

- **cfront（书中主角）**：字符串 vtable、链接期查名、typedef 模拟前向声明——本章任何"两家一致"的
  机制（vptr 头部、声明序槽位）都是对 cfront 的**背离**；读原书时请以本章为现代校准器。
- **Itanium vs ARM EABI 等**：嵌入式侧还有自家 C++ ABI 变体，本章不覆盖 ⚠️。

## 最新演进与工业实践

- **规范维护地**：itanium-cxx-abi 仓库/GitHub Pages 仍在更新（✅ 可达）；
  clang `lib/AST/MicrosoftCXXABI.cpp` 与 `ItaniumCXXABI.cpp` 是两家布局的**可执行定义**
  （✅ llvm/llvm-project）。
- **平台现状**：Windows arm64 仍走 MSVC ABI；macOS/iOS/Linux 全 Itanium；Android NDK=Itanium；
  MinGW-w64 = "Windows 系统 API + Itanium C++ ABI"的杂交体——本目录实测正是这一组合，
  与 msvc 版 Qt/Boost 二进制互不兼容的根源即在本表。
- **工具链锚点**：Clang 的 `-Xclang -ast-dump -fsyntax-only` 与 `-fdump-record-layouts`（配合
  `clang -Xclang -print-record-layouts` 系构建）可直接打印每类偏移决策，读 3.4 时比 objdump 更快。

## 自查清单

1. 给出 `Derived{Virt 基 + int d}` 在两家 x64 的 sizeof，并解释 8 字节差从哪来。
2. 不看笔记：默写 `_ZTV/_ZTI/_ZTS/_ZThn/_ZTC` 各自指向什么，MSVC 对应物是什么。
3. 说明为什么 MinGW 编译的 .lib 不能被 cl 链接（修饰名 + 表头 + 成员指针模型三重不兼容）。

## 交叉链接

- 全目录：[00-总览与阅读地图.md](00-总览与阅读地图.md)；各章：
  [01](01-关于对象.md)｜[02](02-构造函数语意学.md)｜[03](03-Data语意学.md)｜[04](04-Function语意学.md)｜
  [05](05-构造析构拷贝语意学.md)｜[06](06-执行期语意学.md)｜[07](07-站在对象模型的尖端.md)
- 单文件版：[../深度探索C++对象模型.md](../深度探索C++对象模型.md)；系列导航：[../C++系列·总索引.md](../C++系列·总索引.md)
- 延伸阅读：跨 ABI 的库工程视角：[../大规模c++程序设计.md](../大规模c++程序设计.md)、[../C++API设计.md](../C++API设计.md)。
