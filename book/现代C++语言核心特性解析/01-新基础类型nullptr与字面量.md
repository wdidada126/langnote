# 01 新基础类型、nullptr 与字面量优化

> 对应原书 **第1章 新基础类型（C++11～C++20）· 第23章 指针字面量nullptr（C++11）· 第29章 字面量优化（C++11～C++17）**
> 导航：[系列索引](../C++系列·总索引.md) ｜ [单文件笔记](../现代C++语言核心特性解析.md) ｜ [00 总览](00-总览与阅读地图.md)

## 核心概念速览（中英对照）

- **长长整型** — long long int：C++11 纳入语言标准的至少 64 位整型
- **新字符类型** — char16_t / char32_t：与 UTF-16/UTF-32 代码单元绑定的独立字符类型
- **UTF-8 字符类型** — char8_t：C++20 为 u8 字面量专设的新类型（破坏性变更）
- **空指针字面量** — nullptr（std::nullptr_t）：不再是"整数 0"的类型安全空指针
- **十六进制浮点字面量** — hexadecimal floating literal：0x1.8p1，尾数十六进制、指数以 2 为底
- **二进制整数字面量** — binary integer literal：0b1010
- **数字分隔符** — digit separator：1'000'000 中的单引号，仅提升可读性
- **原生字符串字面量** — raw string literal：R"( ... )"，反斜杠不再被转义吃掉
- **用户自定义字面量** — user-defined literal (UDL)：100_km、"s"sv 等以 `_xxx` 后缀扩展字面量
- **字符串前缀** — string literal prefixes：u8/u/U/L 与字符类型矩阵

## 动机

C++98 的"基础类型面"有三处历史欠账：① 整型最宽只到 long（Windows ILP32 上仍 32 位，
Linux LP64 上 64 位——同一份代码两种命运）；② 字面量与转义规则耦合，正则/路径字符串
`"C:\\dir\\new"` 必须双倍反斜杠，整数常量 1000000 位数数不清；③ `0` 作空指针导致
`f(int)` 与 `f(int*)` 重载歧义、模板实参推导把空指针推成 `int`。char16_t/char32_t 则
是 Unicode 生态倒逼：`wchar_t` 的宽度由实现决定（Windows 2、Linux 4），标准库又缺
UTF-16/32 一等公民载体。

## 机制（编译器视角）

- `long long` 进标准时**只加类型不加库**：`<cstdint>` 的 `int64_t` 是别名，`long long`
  是语言保证（`>=64` 位）。GCC 对两者生成完全相同的 64 位运算指令。
- `char8_t` 的实现是"新类型 + 字面量类型改写"：C++20 起 `u8"x"` 的类型从 `const char[]`
  变为 `const char8_t[]`——这是**源码不兼容变更**（模板按 `char` 特化的接口收不到 u8 串）。
  MinGW 实测下见 🔧 样例。
- `nullptr` 不是宏也不是 `0`：`std::nullptr_t` 是独立类型，任何指针可隐式自它构造；
  编译器在重载决议里给 `nullptr → T*` 完全匹配、`nullptr → int` **不可转换**。
- 字面量优化几乎全是**词法层（lexer）**改动：`'` 分隔符、`0b`、十六进制浮点、R"()" 都在
  preprocessing token 阶段变形，不产生任何代码差异——`0x1.8p1` 与 `3.0` 编译后是同一个
  `double` 常量（实测打印 `hexfloat=3.000`）。
- UDL 则是**语法层**：`operator""_km` 把 `100_km` 变成函数调用；标准库用它在 `<chrono>`
  （`12h`）、`<string>`（`"sv"`）、`<complex>`（`1i`）里造出类型化字面量。

## 权衡

- `char8_t` 换来类型正确性，代价是存量代码 `const char* p = u8"x";` 直接编译失败；
  C++20 委员会投票引入（P0482R6），GCC 11 起默认跟进。想要旧行为只能靠 `-fno-char8_t`
  一类开关（MSVC 提供 `/Zc:char8_t-`；GCC 的开关形态 ⚠️ 未在本机验证）。
- `wchar_t` 保留不删：Windows API（UTF-16）依赖它，跨平台库的通行做法是
  `char16_t`+`std::u16string` 或干脆全线 UTF-8 `char`。
- `long long` 与 `int64_t`：要"至少 64 位"用前者，要"恰好 64 位且可移植布局"（序列化/ABI）
  用后者。

## 相邻概念对比

| | 旧世界 (C++98) | C++11 | C++20 |
| --- | --- | --- | --- |
| 64 位整型 | 平台扩展 `__int64` | `long long` | 不变 |
| 空指针 | `0`/`NULL`（宏展开为整数） | `nullptr` | 不变 |
| UTF-8 载体 | `char` + UTF-8 编码约定 | 同左 | `char8_t`（新类型） |
| UTF-16/32 | `wchar_t`（宽度不定） | `char16_t`/`char32_t` | 不变 |
| 可读性 | `1000000`、`0.09375` | `1'000'000`、`0b1010`、`0x1.8p-4`、R"()" | 不变 |

## 🔧 实测样例（已实测 g++ 15.2，-std=gnu++20）

```cpp
#include <cstdio>
#include <cstring>
#include <string>
#include <type_traits>
int main(){
  printf("sizeof char=%zu wchar_t=%zu char16_t=%zu char32_t=%zu char8_t=%zu\n",
     sizeof(char),sizeof(wchar_t),sizeof(char16_t),sizeof(char32_t),sizeof(char8_t));
  std::u16string u=u"中文"; std::u8string u8=u8"中文";
  printf("u16 units=%zu u8 bytes=%zu\n", u.size(), u8.size());
  printf("sep=%lld hexfloat=%.3f bin=%d\n", 1'000'000LL, 0x1.8p1, 0b1010);
  static_assert(std::is_same_v<decltype(nullptr), std::nullptr_t>);
  int* p=nullptr; printf("null eq %d\n", p==nullptr);
}
```

实测输出（Windows/MinGW）：

```text
sizeof char=1 wchar_t=2 char16_t=2 char32_t=4 char8_t=1
u16 units=2 u8 bytes=6
sep=1000000 hexfloat=3.000 bin=10
null eq 1
```

两个编译器视角结论：**本机 wchar_t=2**——Windows 平台 UTF-16 布局，Linux(LP64) 上是 4，
"用 wchar_t 做跨平台 Unicode"从 sizeof 层就不成立；`u8"中文"` 从"2 个字符单元"变成
**6 字节**（libstdc++ 的 `std::u8string` 本质 `basic_string<char8_t>`），字符数≠字节数的
陷阱第一次被类型显式暴露。

## 最新演进与工业实践

- **std::print（C++23，P2093R14，wg21.link 实测 302）**：`std::print("{} {:X}\n", v, 255)`
  以 {fmt} 语法替代 printf，字面量格式串在编译期检查——字面量话题在"输出侧"的续集。
  ⚠️ 本机 MinGW g++ 15.2 的 `<print>` 编译可过但**链接缺符号 `std::__open_terminal`**
  （实测 ld 报错），与库内《C++语言程序设计5》笔记记录的同一工具链缺陷互证：支持矩阵
  必须区分"编译器前端/标准库/链接运行时"三层。
- **UTF-8 与 char8_t 的行业逆流**：大量代码库（含 Google/Chromium 系）选择"字节流 + UTF-8
  约定"而绕开 char8_t；abseil 提供 `absl::string_view` + `absl::Cord` 承载 UTF-8，不引入
  新字符类型。工业实践的主流是 **`char` + 显式编码文档**，char8_t 采用度低（谨慎判断，
  依据：abseil/GSL 均未提供 char8_t 设施——Glob/API 可查）。
- **`std::start_lifetime_as`（C++20，P0593R6，实测 302）**：把"原始字节缓冲 reinterpret 成
  对象"合法化，是"字面量→字节→对象"链条的库侧补丁；⚠️ 本机 libstdc++ 15 **未实现**
  （实测 error: 'start_lifetime_as' is not a member of 'std'），MSVC 17.x 已提供——三件套
  支持矩阵差异的活例。
- **GSL**：`gsl::narrow`/`narrow_cast` 针对整型字面量/转换的缩窄检查，与第 6 文件的
  列表初始化禁缩窄形成"语言+库"双保险。
- C++26 方向：与基础类型直接相关的大提案未检索到；二进制字面量/分隔符早已进入 MISRA、
  Google Style 等编码规范的推荐位（原生字符串用于测试基线数据是工业常态）。

## 互链

- 编码与字符串库纵深：[../现代C++实战30讲/07-Unicode与多文字世界.md](../现代C++实战30讲/07-Unicode与多文字世界.md)
- 变体/任意类型承载（与字符串类型选型相关）：[../C++新经典_设计模式/00-总览与阅读地图.md](../C++新经典_设计模式/00-总览与阅读地图.md)
- 类型安全总论：[../Effective_Modern_C++/00-总览与阅读地图.md](../Effective_Modern_C++/00-总览与阅读地图.md)
- 下一站：字面量之外"用类型表达意图"见 [03-类型占位符与推导.md](03-类型占位符与推导.md)；
  列表初始化的缩窄话题见 [06-初始化家族与聚合类型.md](06-初始化家族与聚合类型.md)。
