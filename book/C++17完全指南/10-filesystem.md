# 10 std::filesystem——路径是一门语法课，更是一门编码课

> 覆盖原书 **Part IV 第 20 章**（`std::filesystem`）。
> 一句话：把 `stat/opendir/GetFileAttributes` 的祖传胶水代码标准化成 **path（纯语法）+ 状态查询（碰磁盘）+ 目录迭代** 三层，
> 代价是要时刻分清「你在操作字符串还是操作系统」。
> 互链：[../C++17完全指南.md](../C++17完全指南.md)｜[../C++系列·总索引.md](../C++系列·总索引.md)｜[09-string_view.md](09-string_view.md)
> 本章全部实测在 **Windows + g++ 15.2（MinGW-w64, x86_64）** 完成——这正是该库坑最密集的平台。

## 核心概念速览（中英对照）

- **路径（语法对象）** — `std::filesystem::path`：一台「字符串按分隔符切分」的解析器，**不碰磁盘**；`lexically_normal` 之类别名「词法操作」。
- **本机编码** — native encoding：`path` 内部表示。Windows 是 **UTF-16（`wchar_t`）**，POSIX 是 `char`（字节序列）——实测 `value_type` 大小 2、`preferred_separator` 为 `\`。
- **词法 vs 物理** — lexical vs physical resolution：`..` 在 `lexically_normal` 里是纯字符串消去，在 `exists/status` 里交给 OS 解析——**两者的结果可以不一样**（本章实测）。
- **双头错误 API** — exception / `error_code` 两族：每个查询都有抛 `filesystem_error` 版与吞错返回哨兵值版（实测哨兵：`file_size` 失败返回 `UINTMAX_MAX`）。
- **目录迭代** — `directory_iterator` / `directory_recursive_iterator`：流式遍历，递归版可查 `depth()`（实测 0/1/2）。
- **状态** — `file_status`/`status`：文件类型 + 权限位的快照；符号链接另有 `symlink_status`。
- **`u8path`** — C++17 的「窄字符串按 UTF-8 入库」入口：**C++20 起弃用**（实测弃用文案），改用 `char8_t` 构造。
- **路径遍历** — path traversal（CWE-22）：`root / 用户输入` 不是沙箱——实测 `不存在的safe_root/../真实文件` 在 Windows 上**解析成功**。

## 动机：在没有它的年代

C++17 之前标准库连「取文件扩展名」都没有：`std::string` 找 `.`、`stat`/`_stat` 查属性、`opendir`/`FindFirstFile` 遍历目录，
每换一个平台重写一遍——这也是 Boost.Filesystem 长期是「事实标准」的原因。标准化时直接采纳了它的设计
（提案基于 Boost.Filesystem v3 的设计，⚠️ 提案号本次未核，勿乱引编号），所以 API 带着浓重的「文件系统直觉」：
**一切路径都是 `path`，一切失败都有两种姿势**。

## 机制与实测证据

### 1. `path` 是语法对象：拆解与词法操作（已实测 g++ 15.2 -std=gnu++17）

```cpp
fs::path p("C:/Windows/notepad.EXE");
p.root_name()   // "C:"
p.stem()        // "notepad"
p.extension()   // ".EXE" —— 注意比较是大小写敏感的：p.extension() == ".txt" 实测为 0
fs::path q = std::string("dir") + char(92) + "sub/../file.txt"; // 运行时拼出 dir\sub/../file.txt，避开源码 \s 转义坑
q.lexically_normal()  // 实测得 "dir\file.txt"：反斜杠在 Windows 上同样是分隔符，/ 与 \ 可混用
q.parent_path()       // "dir\sub/.."（词法切分，不消 ..）
```

`path` 的构造在 Windows 上按「输入类型」选择解码方式：`wchar_t*` 当 UTF-16、`char*` 当**本机 ANSI 码页**——
这一步与之后的输出共同构成本章的编码雷区（§3）。

### 2. UNC 与分隔符：一个诚实的实现差异

实测（`D:\develops\tmp\cppsnippets_cpp17\b2_pathhex3.cpp`，输入字节 hex 先打印自证无误：
`5c 5c 73 65 72 76 65 72 …` 即 `\\server\share\f.txt`）：

| 表达式 | 本机实测 | 说明 |
| --- | --- | --- |
| `path::value_type` 大小 | 2 | Windows 内部是 `wchar_t`（UTF-16） |
| `preferred_separator` | `'\'`(92) | `generic_string()` 会翻成 `/` |
| `\\server\share\f.txt`.root_name() | **空字符串** ⚠️ | 按标准/Windows 语义应为 `\\server`；libstdc++ 未识别 UNC 主机名 |
| 同上的 filename() | `f.txt` ✅ | 其余分解正常 |

UNC 主机名丢失意味着依赖 `root_name()` 做「本地 vs 网络」判断的代码在 GCC/MinGW 上是错的。跨平台项目要用
MSVC 或 Boost/ghc 复测（本机无法交叉实测 ⚠️）。

### 3. 编码：本机 ACP 决定窄字符串的命运（实测）

```cpp
// 🔧 已实测：Active code page 65001（chcp 输出为证）
fs::path zh = L"fs测试目录";                 // 宽字符：UTF-16 入库，万无一失
fs::create_directories(zh);                  // ec=0，exists=1
(fs::path(zh) / L"中文文件.txt");            // 组合
e.path().filename().u8string()               // 读回 hex: e4 b8 ad e6 96 87 …（正确的 UTF-8）
fs::path narrow = "fs窄路径测试";             // UTF-8 字面量直接构造 path
```

窄字符版**在本机也成功了**——因为这台 Windows 的活动码页恰好是 **65001（UTF-8）**，`char*` 被按 UTF-8 解码。
换成简体中文默认的 ACP 936（GBK），同样的源码会把 UTF-8 字节按 GBK 误解码，建出**乱码目录名**。结论：
- 要表达「我手里这段 `char*` 是 UTF-8」，C++17 的正解是 `fs::u8path(s)`；
- C++20 起 `u8path` 弃用（实测 gnu++20 编译告警原文：`is deprecated: use 'path((const char8_t*)&*source)' instead`，
  gnu++17 无告警），改走 `char8_t` 迭代域构造；
- 或最朴素：程序内部统一宽字符/`std::string`+显式转换层。⚠️ 弃用对应的提案号（网传 P1952 在 wg21 为 404）不引。

### 4. 双头 API：抛异常版 vs error_code 版（实测）

```cpp
fs::file_size("no_such_file_xyz");             // 抛 filesystem_error，e.code().message()="No such file or directory"
auto sz = fs::file_size("no_such_file_xyz", ec); // 实测 sz=18446744073709551615（UINTMAX_MAX），ec 置位
```

约定：带 `error_code&` 的重载**不抛**、失败返回哨兵（`-1`/`false`/空）；不带的抛 `filesystem_error`。
遍历/复制这类「允许部分失败」的场景一律用 ec 版并逐条判 `ec`——异常版会把整个任务炸掉。

### 5. 目录遍历（实测）

```cpp
for (fs::recursive_directory_iterator it("rtest"); it != {}; ++it)
    std::printf("%s depth=%zu\n", it->path().c_str(), it.depth());
// 实测：rtest\a depth=0 / rtest\a\b depth=1 / rtest\a\b\c depth=2
```

`directory_entry` 缓存了 `status`，遍历时重复查询属性近乎免费；`disable_recursion_pending()` 可剪枝。
符号链接默认**跟随**（`status`）——想区分要 `symlink_status` 与 `directory_options::follow_directory_symlink`。

### 6. 词法 vs 物理：路径遍历安全实测（CWE-22）

「把用户上传的文件名拼进根目录」的经典防线是 `root / user`。实测它**不是防线**：

```cpp
fs::path joined("safe_root/../SUMMARY.md");   // safe_root 这个目录根本不存在
fs::exists(joined)          // 实测 = 1 ！Windows 的词法归一发生在 OS 层：不存在的 X/../ 照样折叠
joined.lexically_normal()   // "SUMMARY.md" —— safe_root 前缀整个蒸发了
fs::weakly_canonical(joined)// 同样折叠到根外
```

而 `safe_root/../../../windows/win.ini` 实测 `exists=0`——不是因为被拦下，而是从当前目录往上**层数不够**
（落在 `D:\develops\windows\win.ini`，一个不存在的位置）。两条合起来的教训：`..` 折叠既可能救你也可能害你，
**唯一可靠的防线是 canonical 之后校验前缀**：`fs::weakly_canonical(root / user)` 以 `root` 为前缀才放行，
并按分隔符边界比较（防 `root_evil` 冒充 `root`）。参见 MITRE 官方条目
[CWE-22: Improper Limitation of a Pathname to a Restricted Directory](https://cwe.mitre.org/data/definitions/22.html)（链接已核可达）。

## 权衡

| 决策点 | `std::filesystem` | Boost.Filesystem / ghc::filesystem | 手搓平台 API |
| --- | --- | --- | --- |
| 依赖 | 零依赖（但见下方 MinGW 陷阱） | Boost 重 / ghc 单文件 | 零 |
| C++11/14 项目可用 | ❌ | ✅（Boost 同 API 命名空间可切） | ✅ |
| Windows UNC/长路径等边角 | 实测有缺口（§2）⚠️ | Boost 相对更久经考验（未实测 ⚠️） | 自己负责 |
| 异常控制 | 双 API 任选 | 同 + `boost::system::error_code` | 自理 |

**MinGW 实测陷阱**：链接 `std::filesystem` 后直接运行可能崩在老 DLL 上（PATH 上的旧版 `libstdc++-6.dll`，
见 `00` 工具链表）——本章所有测试都用 `-static` 重编后通过。

## 相邻概念对比

- **vs `09` string_view**：`path` 拥有存储且**按平台解码**；视图借裸字节。`path` 存成员的寿命问题不存在，
  寿命问题转移到了「编码假设」上。
- **vs `std::error_code`（`12` 的 charconv 同款）**：filesystem 是标准库把「ec 双 API」风格推向极致的样本。
- **vs POSIX `<filesystem>` 直觉**：POSIX 没有「本机编码」概念（字节即真相）；Windows 的 UTF-16 内部表示
  是本章一半的坑源。

## 最新演进与工业实践

**标准之后**
- **C++20**：`u8path` 弃用（实测告警原文见 §3）；`path` 增加 `char8_t` 支持；比较运算符改用 `lexically_normal` 语义（⚠️ 提案号未核）。
- **C++23/26**：`filesystem` 本体趋于稳定，无重大改动（未逐条核对提案 ⚠️）。
- **MSVC/Windows 长路径**：`\\?\` 前缀路径实测行为未经本章验证 ⚠️，需要 260 字符以上路径时优先测你的编译器。

**工业实践与开源口径**
- **ghc::filesystem**（[ghc/filesystem](https://github.com/ghc/filesystem)，单文件 header-only 的 C++17 语义实现，
  供 C++11/14 项目平移使用；**星数当日未取到** ⚠️）：与标准同 API，切换命名空间即可，是「先上 C++11 再等 C++17」的常见过渡层。
- **Boost.Filesystem**：`std::filesystem` 的娘家，API 高度同源；老项目迁移成本主要在命名空间与错误类型。
- **服务端文件上传**：几乎所有语言的安全指南都要求 §6 的 canonical+前缀校验流程；把校验做成一个工具函数而不是信任 `path` 运算。

## 常见误区（实测）

1. **「`lexically_normal`/`operator/` 会帮我拦住 `..`」——不会**：纯词法折叠后 `safe_root` 整个消失（实测 normal 得 `SUMMARY.md`），且不保证物理存在性。
2. **「`exists(root / userInput)` 为真就说明文件在 root 里」——大错**：实测 `safe_root/../SUMMARY.md` 存在，指向的却是根外文件。
3. **「窄字符路径哪里都能用」——取决于 ACP**：本机 65001 下侥幸成功；ACP 936 下同一程序建出乱码目录。跨平台代码用 `u8path`/宽字符（§3）。
4. **「`file_size` 失败一定抛异常」——还有 ec 版**：ec 版失败**返回 `UINTMAX_MAX`**（实测），只查返回值不查 `ec` 会把哨兵当天文数字文件大小。
5. **「扩展名比较不区分大小写」——区分**：`.EXE` 与 `.exe` 在 `path::extension()` 比较中不相等（实测），自己 `lcase` 或用 `iequal`。
6. **「GCC 的 Windows `path` 完全兼容 Win32 语义」——UNC 实测翻车**：`root_name()` 为空（§2）；拿它做网络盘判断前先在目标工具链上复测。

## 与其他章 / 其他笔记的联系

- ← 本目录 `09`：`string_view`→`path` 转换、编码与 `\0` 语义的对照；`path` 是「拥有+解码」，视图是「借用+裸字节」。
- ← 本目录 `03`（保证的拷贝消除）：`fs::path` 链式 `operator/` 的返回值成本正由 CTAD/Copy elision 那批特性改善。
- → 本目录 `12`：`error_code`/`from_chars` 的「零分配报错」风格与本章双 API 一脉相承。
- → [../C++标准库/08-特殊容器与字符串.md](../C++标准库/08-特殊容器与字符串.md)：`std::string` 编码无关的字节语义是理解 ACP 问题的前提。
- → [../现代C++实战30讲/07-Unicode与多文字世界.md](../现代C++实战30讲/07-Unicode与多文字世界.md)：UTF-8/UTF-16/ACP 全景在这篇；`path` 是它在文件系统的投影。
- → [../C++API设计/01-API简介与通用问题.md](../C++API设计/01-API简介与通用问题.md)：「每个函数给异常版+ec版」是错误处理 API 设计的标准教材。

## 思考题

1. 写出一个 `safeJoin(root, userInput)`：要求对 `../../`、绝对路径、盘符、`\?\` 四类输入都拒绝或折叠回根内。你的实现先折叠再比较，还是先验证再折叠？各漏哪种攻击？
2. 用 `std::filesystem` 实现 `du`（递归统计目录大小），要求：符号链接不跟随、无权限的子目录只警告不中断。为什么这两个要求合在一起必须用 `error_code` 版 API？
3. 在 ACP 936 的机器（或改 `chcp 936`）上重跑 §3 的窄路径实验，记录实际创建的目录名字节；再用 `u8path` 重跑一遍对比。解释两次「解码」分别发生在哪一层。
