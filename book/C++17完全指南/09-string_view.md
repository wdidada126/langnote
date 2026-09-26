# 09 std::string_view——一段别人的内存

> 覆盖原书 **Part IV 第 19 章**（`std::string_view`）。
> 一句话：**`{const char*, size_t}` 加上一整套字符串算法**；它不拥有内存，所以它的全部风险都来自寿命。
> 互链：[../C++17完全指南.md](../C++17完全指南.md)｜[../C++系列·总索引.md](../C++系列·总索引.md)｜[07-std-optional.md](07-std-optional.md)

## 核心概念速览（中英对照）

- **字符串视图** — `std::string_view`：指向他人字符缓冲的 `{data(), size()}` 对，构造/拷贝是两个字的琐事。
- **悬垂视图** — dangling view（lifetime trap）：视图活过它所指向的缓冲；**编译器基本抓不到**（本章实测）。
- **无空终止承诺** — not necessarily null-terminated：`data()` 后面可能有 `\0` 也可能没有；**没有** `c_str()`（实测）。
- **视图内切片** — `substr`/`remove_prefix`：返回的还是视图、零拷贝——这也是它作为解析器原语的全部价值。
- **`data()` 的起点陷阱** — 实测：`sv.substr(1,3).data()` 打印出的是**整个底层缓冲**（直到遇到 `\0`），因为 `data()` 不记得 `size()`。
- **显式转 string** — 视图 → `std::string` 必须显式构造（实测拒绝隐式；反向 `string → string_view` 是隐式的）。
- **`"..."sv` 字面量** — `std::literals::string_view_literals`：`"abc"sv` 直接得视图（长度免 strlen，实测通过）。
- **视图比较** — `==`/`compare`/`find` 全套与非类型模板参数无关；C++20 才有 `starts_with`/`ends_with`（实测档位分界）。

## 动机：`const std::string&` 参数解决不了的三件事

```cpp
// 🔧 老 API 的痛
void log(const std::string& msg);
log("literal");                    // 每调用一次：构造一个临时 std::string（堆分配或非 SSO 拷贝）
log(buf.data());                   // 想截一段：先拷贝进 string 再传
auto token = line.substr(a, b-a);  // 解析器里每个 token 都分配一次
```

`string_view` 的参数版把三件事都变成两个字的传递：`void log(std::string_view msg);` 接字面量、接
`const char*+len`、接切片，**零分配**。它是 C++17 把「借用字符串」标准化，动机与 `08` 的 `byte`
（借用内存的**字节**视角）同源。Abseil 早在 2016 年就以此立论：`absl::string_view` 即其前身。

## 机制与实测证据

### 1. 视图就是 {指针, 长度}（已实测 g++ 15.2 -std=gnu++17）

```cpp
std::string_view sv = "abcdef";
sv.substr(2,3)        // "cde"（实测 %.*s 打印）
sv.data()             // "abcdef" —— 注意：substr 之后 data() 仍指向**完整缓冲**起点
sv.size()             // 6
sv.find('c')          // 2；sv == "abcdef" 为 1（与 const char* 比较合法）
std::string fromView(sv);   // 视图 -> string：显式构造（实测隐式被拒，见 §3）
```

`substr(1,3)` 后按 `%s` 打印实测得到 `bcdef`——**`data()` 不裁剪，`size()` 才是真相**。把它交给任何
`strlen`/`%s`/C API，得到的都是底层原串剩余部分：这是 `string_view` 第 1 号行为陷阱。

### 2. 悬垂：制造它、观察编译器沉默（本章核心实测）

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17 -O0 与 -Wall -O2 两种档位
std::string_view makeBad() {
    std::string local = "hello-local-buffer-xx";   // SSO：数据在栈上的 local 里
    return local;                                   // 视图随 local 一起作废
}
std::string_view sv = makeBad();
poison();                                           // 用一个满 'Z' 的缓冲区踩烂栈
std::printf("悬垂 view 读到: [%.*s]\n", (int)sv.size(), sv.data());
```

实测结论（原样记录）：
- **-Wall -O2 没有任何警告**（未触发 `-Wdangling-*` 系诊断）；
- 运行输出为**空内容**——栈内存已被复用覆盖，「没崩」只说明 UB 尚未发作；
- **ASan 本机不可用**（`cannot find -lasan`，见 `00` 工具链表）⚠️：无法演示 sanitizer 版捕获，
  读者请在自己的 Linux/macOS 机器上用 `-fsanitize=address` 复测「stack-use-after-return」。

高危模式清单（全部由上面一条原理派生）：函数返回指向局部/临时对象的视图；
`sv = 临时string()`（如 `sv = std::string("tmp") + "x";`）；容器重分配/`erase` 后仍持旧切片；
把视图存进成员却没人保证被指向对象更长命。**参数**用 `string_view` 几乎总是安全，**成员/返回值**用
视图才危险——默认按参数用、按返回慎用。

### 3. 没有 c_str、没有隐式退路（实测负例原文）

```cpp
sv.c_str();                 // error: ... has no member named 'c_str'; did you mean '_M_str'?（GCC 的幽默）
std::string s = sv;         // error: could not convert 'sv' from 'std::string_view' to 'std::string'
std::to_string(sv);         // error: no matching function for call to 'to_string(std::string_view&)'
sv.str();                   // 本机 GCC 15 在 17/20/23 三档均无此成员（老版 GCC 扩展已移除）
f(sv);                      // f(std::string)：需写 f(std::string(sv)) 或 f(sv.data(), sv.size())
```

转换被刻意做成显式是有道理的：`string(sv)` **一定发生拷贝**，标准不想让这笔钱悄悄花出去。
⚠️ 实测到的实现方言：`s += sv`（`std::string += string_view`）在 **gnu++17 档位也能编译**——libstdc++
未把该 C++20 重载藏进特性开关；跨实现项目请仍按 C++20 对待。

### 4. 视图 API 的档位分布（实测）

| 成员 | gnu++17 | gnu++20 |
| --- | --- | --- |
| `substr` / `find` / `compare` / `operator==` | ✅ | ✅ |
| `"abc"sv` 字面量 | ✅ | ✅ |
| `starts_with` / `ends_with` | ❌ `has no member named 'starts_with'`（实测原文） | ✅（实测 `starts=1 ends=1`）⚠️ 提案号未核，勿乱引 |
| 编译期比较（constexpr relational） | ✅（实测 `static_assert("abc" > "abb")` 在 17 通过） | ✅ |

## 权衡

| 决策点 | string_view | const string& | 值拷贝 |
| --- | --- | --- | --- |
| 参数：接一切字符串源 | ✅ 字面量/`char*+n`/`string` 全兼容 | 字面量要构造临时 string | — |
| 解析/切片成本 | O(1)，零分配 | 切片即拷贝 | 全量拷贝 |
| 存储为成员 | ⚠️ 必须自己保证宿主寿命 | 安全（拥有） | 安全 |
| 传给只认 `const char*` 的 C API | ⚠️ 需确认 `\0` 结尾，否则先 `string(sv)` | 可直接 `.c_str()` | 可直接 |
| 递归/多线程借用 | 视图只是引用，锁语义同引用 | 同 | 无共享 |

## 相邻概念对比

- **vs `span`（C++20）**：`string_view` ≈ `span<const char>` + 字符串算法；`span` 不带「`\0` 语义」包袱。
- **vs `const char*`**：带长度 ⇒ 二进制安全（可含 `\0`）、可 `substr`；C 字符串的 `strlen` O(n) 隐式成本消失。
- **vs `07` optional**：两者都是「轻量语义壳」；optional 管**存在性**，view 管**借用**——`optional<string_view>` 同时表达「可能没有，且有的话不拥有」。
- **vs `std::string` 的 SSO**：别用 sizeof 论证视图更快：真正的收益是**免分配**，短字符串路径上两者成本差很小。

## 最新演进与工业实践

**标准之后**
- **C++20**：`starts_with`/`ends_with`（实测见上表）；`operator<=>` 接入后比较代码可删一截。
- **C++23/26**：视图本身趋稳；周边继续演进的是 ranges 组合（`views::transform` 处理 token 流）、
  `std::format` 原生吃 `string_view`（fmt 库早多年）。⚠️ 逐条提案号未核，此处不列。

**工业实践与开源口径**
- **Abseil 的 `absl::string_view`**（`abseil/abseil-cpp`，00 当日实测 ≈18.1k★）：Google 风格指南明确
  「输入参数用 string_view；**不要**用作成员/返回值，除非生命周期显然」——与本章 §2 结论同文。
- **fmt**（`fmtlib/fmt`，00 当日实测 ≈25.8k★）：格式化 API 全量 `string_view` 化（`format_string` 即其变体），
  是「视图做参数」的最大规模活样本。
- **解析器惯用法**：手写 parser 时让每个 token 是视图、`std::string` 只在「要留下」时诞生——
  [../C++API设计.md](../C++API设计.md) 的借用参数一节与此呼应。

## 常见误区（实测）

1. **「`data()` 以 `\0` 结尾」——不保证**：`substr` 后实测打印 `bcdef`；给 C API 前要么 `string(sv)` 要么确认源。
2. **「没有 `c_str()` 是标准偷懒」——反了**：没有 `\0` 承诺自然没有 `c_str()`；GCC 诊断里连私有的 `_M_str` 都替你标好了 ⚠️ 别真去用。
3. **「编译器/静态检查会抓悬垂」——实测没有**：`-Wall -O2` 零警告、零崩溃、读到空内容；ASan 本机又缺位。防线只有「参数用视图、返回/成员用值」。
4. **「`sv.size()-2` 越界会崩」——错**：size_t 下溢得到一个天文数字，`operator[]` 越界是 UB；写 `sv.size() >= 2 && ...` 先行短路。
5. **「string_view 参数能省一切」——小半错**：`string_view` 进函数后要 `std::string` 出来（如存进成员），拷贝只是被推迟，没被消灭。

## 与其他章 / 其他笔记的联系

- ← 本目录 `07`：`optional<string_view>`/`string_view` 返回值的「存在 + 借用」组合语义。
- → 本目录 `10`：`filesystem::path` 与视图/编码的纠缠（Windows 宽字符 ⇒ `path` 不是「一段 char」）。
- → 本目录 `12`：`to_chars`/`from_chars` 用 `{ptr, ec}` 而非视图报告转换——同为「零分配字符串处理」战壕。
- → [../C++标准库/08-特殊容器与字符串.md](../C++标准库/08-特殊容器与字符串.md)：`std::string` 本体（SSO、迭代器失效）是理解视图危险面的前提。
- → [../现代C++实战30讲/07-Unicode与多文字世界.md](../现代C++实战30讲/07-Unicode与多文字世界.md)：视图按「码元」切片对 UTF-8 的破坏。
- → [../Effective_Modern_C++/01-类型推导.md](../Effective_Modern_C++/01-类型推导.md)：`auto` 与视图搭配时的退化陷阱（`auto sv = buf + "x";`）。

## 思考题

1. 把本章 §2 的 `makeBad` 在你的编译器上跑 `-O0`/`-O2`/ASan 三档，把「崩/不崩/报什么」记成表——哪一档给了你最强的证据？为什么？
2. `std::string_view token = line.substr(0, pos);`（`line` 随后被 `line.clear()`）属于哪一类危险？写出两种修复（改持有 / 改顺序），并说明各自的性能含义。
3. 为什么标准故意不提供 `string_view -> string` 的隐式转换、却允许 `string -> string_view` 隐式？用「谁付拷贝钱」的角度写三行答案。
