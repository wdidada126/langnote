# 讲 11｜Unicode：进入多文字支持的世界

> **一句话**：C++ 的 `char` 是**字节**而不是字符——这条三十年前的设计决定，让「字符串」在标准库里始终是字节序列；理解这一点，就理解了一半多文字支持的全部麻烦。

---

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 字符集 / 编码 / 码点 | 三者的区别 | 平时说的「Unicode」通常指「码点集合 + 一种编码」 |
| `char` 是字节 | `std::string` 的语义 | 长度是字节数；`++it` 可能落在半个字符中间 |
| `wchar_t` 的陷阱 | 大小与编码由实现定义 | Linux 上是 4 字节 UTF-32，Windows 上是 2 字节 UTF-16：别写跨平台代码依赖它 |
| `char16_t` / `char32_t` / `char8_t` | 显式编码单元的字符集类型 | 明确写清每个字面量的编码，避免「看起来都是字符串」的混乱 |
| 字面量前缀对照 | `""/u8""`/`u""`/`U""`/`L""` | 项目里应统一一条规则，最好只用 UTF-8 |
| 遍历与截断 | 按字节切分会破坏多字节字符 | 需要「字符」语义时使用专门的文本处理库 |
| 大小写、规范化与排序 | NFC/NFD、locale 相关规则 | 直接比较字节串对非 ASCII 输入基本无意义 |
| 🔧 现代补充 | `char8_t`（C++20）、`u8""` 的类型变化、`std::string_view` 与编码 | 2026 年的结论：**内部一律 UTF-8，`char8_t` 只出现在边界** |

---

## 核心精讲

> 以下均为**教学示意，不参与构建**。

### 1. 先分清三个词

| 名词 | 含义 | 例子 |
| --- | --- | --- |
| 字符集（Character Set） | 有哪些字符 | Unicode：码位从 0 到 0x10FFFF |
| 编码（Encoding） | 码点如何变成字节 | UTF-8、UTF-16、UTF-32、GBK |
| 码点（Code Point） | 字符在字符集里的编号 | `U+4E2D` 是「中」 |

> 所谓「Unicode 字符串」在 C++ 里从来不是一个标准类型；`<string>` 装的是 `char` 的序列，也就是**字节序列**。

### 2. C++ 的字符类型全景

```cpp
// 教学示意：各字符类型的存在意义（不参与构建）
char        a = u8"中文";    // C++11 起 u8 是 const char[]；C++20 起应写成 char8_t
char16_t    b = u"中文";     // UTF-16 编码单元
char32_t    c = U"中文";     // UTF-32 编码单元
wchar_t     d = L"中文";     // 实现定义：Linux 4 字节 / Windows 2 字节
```

| 类型 | 底层 | 典型用途 |
| --- | --- | --- |
| `char` | 字节（有符号性由实现定义） | 文件、网络、UTF-8 存储 |
| `char8_t`（C++20） | 无符号字节 | 明确表示「这是 UTF-8 数据」 |
| `char16_t` | 16 位 | UTF-16 数据 |
| `char32_t` | 32 位 | UTF-32 数据 |
| `wchar_t` | 由实现定义 | 与 OS API 交互（Windows 的 Unicode 路径） |

> **`wchar_t` 的历史包袱**：它本意是「宽字符」，但各平台给了不同的宽度与编码，导致「同一个 `L"文"` 在两个平台上的字节完全不同」。跨平台项目里应当**避免**在接口中使用 `wchar_t`。

### 3. 按字节遍历中文会发生什么

```cpp
// 教学示意：字节级操作的典型后果（不参与构建）
std::string s = "中文abc";                 // UTF-8 下「中」占 3 字节
s.substr(0, 1);                            // 切出一个不完整的字符（乱码）
std::string::size_type n = s.length();    // 返回字节数，不是字符数

// 若非要用字节切片，至少保证切在字符边界上
bool is_continuation(unsigned char c) { return (c & 0xC0) == 0x80; }
```

UTF-8 的两个关键性质值得记住：**多字节序列的首字节值总是小于 0x80 之后的连续字节**，且**ASCII 是 UTF-8 的子集**。因此「按字节比较」对纯 ASCII 是对的，对混合文本就不成立。

### 4. 输入 / 输出的边界

```cpp
// 教学示意：与 API 打交道时的编码边界（不参与构建）
void write_utf8(std::ostream& os, std::u8string_view s) {   // C++20：char8_t 版本
    os << reinterpret_cast<const char*>(s.data());          // 只在边界做一次转换
}
void win32_path(std::wstring_view w) {
    // Windows 上 CreateFileW 接受 UTF-16；进入这条路径前必须明确 W 后缀的含义
}
```

工程建议：

1. **程序内部统一 UTF-8**（与 Linux、Web、JSON 生态一致）；
2. **只在与系统 API / 其他编码的库交互时转换**，且转换点集中、有测试；
3. **`u8""` 的类型在 C++20 变成了 `char8_t`**：这既提高了精确性，也意味着老代码中 ` reinterpret_cast` 的情形会变多（见下图的一行示例，此处仅作示意说明，不要照抄）。

### 5. 大小写、规范化与「字符串相等」

```cpp
// 教学示意：为什么字节比较不够（不参与构建）
// "é" 既可以是 U+00E9，也可以是 "e" + U+0301（组合字符）
// 它们的字节表示不同，但它们「看起来是同一个字」

// 需要语义相等时，先做 Unicode 规范化（NFC/NFD），再用规则比较
```

- **大小写映射有例外**：德语 ß 的大写是 SS，土耳其语的 i/I 规则受语言影响；
- **排序依赖 locale**：`std::locale` + `std::collate` 才给出符合语言的顺序，但它们的实现质量因平台而异；
- **`<locale>` 中的 `std::codecvt` 相关模板自 C++17 起被弃用**，新代码建议用 ICU 或专门的转换库。

### 6. 编码选择的现实

| 场景 | 建议 |
| --- | --- |
| 源码文件、内部字符串、JSON、网络协议 | UTF-8 |
| Windows GUI 与 Win32 Unicode API | UTF-16（`wchar_t` / `LPWSTR`） |
| 需要「一个字符一个整数」的算法（如字形处理） | UTF-32 或按需解码 |
| 需要完整 Unicode 支持（排序、规范化、双向文本、正则） | ICU |

---

## 版本演进

| 版本 | 变化 |
| --- | --- |
| C++98 | `char`、`wchar_t`；`std::locale` 与 facet 体系 |
| C++11 | `char16_t`/`char32_t`、`u8/u/U/L` 前缀、`std::u16string`/`u32string` |
| C++17 | `std::string_view`；`std::codecvt` 相关模板**弃用** |
| C++20 | **`char8_t`**；`u8""` 得到 `char8_t` 数组；`std::u8string_view`；`std::format` 支持这些类型 |
| C++23 | 更多编码互操作与 `std::print` 的文本输出路径；`std::format` 的错误处理更完整 |
| C++26 | 文本处理设施的进一步整固（方向性与 grapheme 簇支持仍在推进） |

---

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| *The Unicode Standard*（最新版） | **Unicode Consortium / Addison-Wesley** | 字符、码点、规范化、大小写映射的唯一权威 |
| **UTS #1** *Unicode Character Database* | Unicode Technical Standard | 字符属性表（也是多数库的数据来源） |
| **UTS #15** *Unicode Normalization Forms* | Unicode Technical Standard | NFC / NFD / NFKC / NFKD 的定义 |
| **UTS #18** *Unicode Regular Expressions* | Unicode Technical Standard | 正则引擎该怎样对待码点与 grapheme |
| **P0424** *char8_t: A type to represent a UTF-8 code unit* | **WG21 提案** | `char8_t` 入标准的提案来源 |
| ISO/IEC 14882 第 6.5 章（字符集类型）与 `<locale>` | C++ 标准 | `char`/`wchar_t`/`char16_t`/`char32_t` 与 locale facet 的正式规定 |

---

## 近年研究与工业界开源实践（2015–2026）

- **UTF-8 成为默认内部编码**：跨语言生态（Python、Go、Rust、Web）一致，C++ 项目也在向内网 UTF-8 收敛，`wchar_t` 只在 Windows API 边界出现。
- **ICU 仍是完整 Unicode 支持的现实选择**：大小写、规范化、日历、双向文本、collation 都依赖它；但体积与初始化成本限制了在嵌入式场景的使用。
- **编译期检查的 Unicode 字符串**：`std::format`/`std::print`（P2093）与 `consteval` 让「非法 UTF-8 字面量」更早暴露。
- **文件名与路径**：POSIX 把文件名当作任意字节，Windows 用 UTF-16；跨平台代码必须明确「路径是字节串还是宽字符串」。
- 🔧 **`char8_t` 落地后的一次性清理**：C++20 之后的老代码在 `u8""` 上的类型会变，用 `std::u8string_view` 与显式 `reinterpret_cast` 边界转换是 2026 年的推荐写法。
- 🔧 **grapheme 簇仍未进标准**：emoji、组合文字的「用户可见字符」处理依然是 ICU 与第三方库的领地；标准库里最接近的是 `std::wbuffer_convert`（已弃用）。

| 仓库 | star | 说明 |
| --- | --- | --- |
| `unicode-org/icu` | **3.6k★** | Unicode 与 locale 的完整实现，讲 11 的答案是它 |
| `fmtlib/fmt` | **25.8k★** | 支持 `u8/u/U` 字符类型与编译期 UTF-8 校验的格式化 |
| `nlohmann/json` | **50.7k★** | 事实上的 JSON 标准库，UTF-8 边界处理的常见参照 |
| `microsoft/STL` | **11.2k★** | 标准库 locale 与字符类型实现 |
| UTF-8 解码库（多个仓库名已变更） | **star 未核验** | 手写 UTF-8 解码（首字节 + 连续字节校验）在教学上完全够用 |

---

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「`std::string::size()` 返回字符数」 | 返回**字节数**；多字符对的 length 与字符数无关 |
| 2 | 「`wchar_t` 在所有平台都一样」 | 宽度与编码由实现定义；不要在同一份代码里跨 Windows/Linux 依赖它的语义 |
| 3 | 「用 UTF-16 存数据更省空间」 | 取决于文本；中文 UTF-8 只用 3 字节，UTF-16 也用 3–4 字节，而 ASCII 场景下 UTF-8 更省 |
| 4 | 「BOM 是必要的」 | UTF-8 的 BOM（EF BB BF）会污染字符串首字节；编辑器默认「无 BOM UTF-8」 |
| 5 | 「大写转换可以按字符表查表」 | 有语言规则（ß→SS）与特殊例外（希腊语终音Sigma） |
| 6 | 🔧 本讲把 `char8_t` 当作 C++20 的细枝末节 | 它其实是**编码语义的显式化**：2026 年的建议是 `char8_t` 用于「UTF-8 字节」类型标注，`char` 只用于「不透明的字节」（网络包、内存映射） |
| 7 | 🔧 本讲未给「UTF-8 字符串」一个可用的类型 | 实践中用 `std::u8string` / `std::u8string_view`，或在项目里定义一个 `using utf8 = std::basic_string<char8_t>;` 并把边界转换集中到一两个函数 |
| 8 | 🔧 缺少 grapheme 簇的现实提醒 | 一个 emoji 可能由多个码点组成；「用户看到的一个字符」≠「一个码点」≠「一个 `char`」 |
| 9 | 🔧 未提 `<codecvt>` 的弃用后果 | 依赖 `std::wstring_convert` 的老代码在 C++20 之后仍是「已弃用但未移除」，新项目应直接上 ICU |

---

## 与其他章 / 其他书的联系

- **`06-迭代器与新for和易用性改进.md`**：多字节字符的遍历问题本质上也是「迭代器所指单元大小」的问题。
- **`04-容器汇编上下.md`**：`std::string` 是容器的特例，需要单独一节讨论它的编码语义。
- **`05-异常与错误处理的现代化.md`**：转换失败（非法 UTF-8）应当作为可预期错误上报。
- **`13-数字计算与Boost.md`**：Boost.Locale 是使用 ICU 的一条常见路径。
- **`book/软件架构设计/03-语言.md`**：语言层面的文本模型差异属于「跨平台一致性」问题的一部分。
- **Unicode 官方站点与 UTS 文档**：本章实验数据的最终依据（utcc.unicode.org / unicode.org/reports）。
