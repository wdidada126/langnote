# 笔记：C++ 符号表分离 —— objcopy 剥离与挂载调试信息

> **来源**：CSDN 博客 [c++ 符号表分离———objcopy(调试信息挂载)](https://blog.csdn.net/cyteven/article/details/13015511)
> **作者**：程序猿BinZoo　**发布时间**：2013-10-25
> **原文标签**：`gdb` `linux` `objcopy` `--only-keep-debug` `--strip-debug`
> **版权**：CC 4.0 BY-SA
> **整理日期**：2026-09-12
> **一句话概括**：用一个"带调试信息编译、剥离前抽走调试段"的流程，让线上部署**体积小、性能高**的二进制，同时保留事后用 gdb 定位 core dump 的能力。

---

## 1. 问题背景

线上服务器跑的是 release 版本程序，突然宕机，用 gdb 看 core 文件：

- 堆栈被破坏（怀疑指针/数组使用不规范），想进一步查看相关变量 → 失败
- 换成 debug 版本 → 可以查到符号信息

对比两者编译选项：

| 版本 | 编译选项 | 调试信息 | 体积 | 效率 |
|---|---|---|---|---|
| release | `-O3` | 无 | 小 | 高 |
| debug | `-g3` | 有 | 大 | 低（未优化） |

**目标**：既要有符号信息（可调试），又要保证运行效率（不影响线上性能）。
**手段**：Linux 的 `objcopy` 可以把可执行文件中的调试信息**剥离成独立文件**，需要时再**挂载**回去。

### 优化级别备忘

`-O0`（无优化）／`-O1`（默认）／`-O2`／`-O3`（优化最高）。

---

## 2. 演示代码

`main.cpp`：

```cpp
#include <iostream>
using std::cout;
using std::endl;

void my_print();

int main(int argc, char *argv[])
{
    my_print();
    cout << "hello!" << endl;
    return 0;
}

void my_print()
{
    int a = 10;
    int b = 20;
    cout << "a=" << a << endl;
    cout << "b=" << b << endl;
}
```

---

## 3. 实验一：对 **不含调试信息** 的 release 版做分离（无效）

编译（release，无 `-g`）：

```bash
g++ -O3 main.cpp -o mainO3
```

执行分离：

```bash
objcopy --only-keep-debug mainO3 mainO3.symbol   # 抽出符号表文件
objcopy --strip-debug      mainO3 mainO3.bin     # 抽出被剥离的可执行文件
```

**观察结果**：

- `mainO3`、`mainO3.bin`、`mainO3.symbol` 三者**文件大小基本相当**
- 用 `readelf -S` 对比三者的**段信息完全一样**
- `mainO3.bin` 可以正常执行，行为与原来一致

**结论**：源文件本来就没有调试信息可剥，所以**这种分离没有任何作用**。

---

## 4. 实验二：对 **带调试信息** 的可执行文件做分离（有效）

编译（带调试信息 + 开优化，`-g3` 与 `-O3` 可共存）：

```bash
g++ -g3 -O3 main.cpp -o maingo
```

同样的分离操作：

```bash
objcopy --only-keep-debug maingo maingo.symbol
objcopy --strip-debug      maingo maingo.bin
```

**观察结果**（用 `readelf -S` 看段）：

| 文件 | 说明 |
|---|---|
| `maingo` | 明显比 `mainO3` 大；段里**含 `.debug_*` 段** |
| `maingo.symbol` | 体量同样很大；**包含全部 debug 段** |
| `maingo.bin` | 很小；段里**已不含任何 debug 段**，剥离成功 |

`maingo.bin` 仍可正常执行。

---

## 5. 实验三：四种情况下 gdb 的调试效果对比

gdb 常用操作：

```bash
gdb                 # 启动
(gdb) file mainO3   # 载入可执行文件
(gdb) b my_print    # 打断点
(gdb) r             # 运行
(gdb) info locals   # 查看局部变量
(gdb) n             # 单步
```

| # | 调试对象 | 结果 |
|---|---|---|
| 1 | `mainO3`（release） | 提示 `(no debugging symbols found)`，看不到符号/局部变量，**无法定位问题** |
| 2 | `maingo`（debug） | 可看到**文件名、行号、每一行代码、局部变量值** |
| 3 | `maingo.bin`（剥离后） | 与 release 一样，什么都看不到 |
| 4 | `maingo.bin` + **挂载符号表** | ✅ 可以看到函数信息与**局部变量值** |
| 5 | 第 4 种 + 源码同目录 | 源码仍看不到，但**局部变量值仍可查** |

第 4 步的挂载方式（原文写法）：

```bash
gdb -s maingo.symbol maingo.bin
# 或在 gdb 内：
(gdb) symbol-file maingo.symbol
```

> 原文的结论："在外网部署优化后的文件不影响效率，同时挂载符号表后可以查看相关信息。"

---

## 6. 标准操作流程（可直接复用）

```bash
# 1) 编译：同时带调试信息与优化
g++ -g3 -O3 main.cpp -o maingo

# 2) 抽取调试信息到独立符号表文件
objcopy --only-keep-debug maingo maingo.symbol

# 3) 从原可执行文件中剥离调试信息
objcopy --strip-debug maingo maingo.bin

# 4) 校验：分离结果是否符合预期
readelf -S maingo.bin | grep debug        # 应无输出
readelf -S maingo.symbol | grep debug     # 应有 .debug_info 等
ls -lh maingo maingo.bin maingo.symbol    # 观察体积差异
```

部署：只上线 `maingo.bin`（体积小、性能不受影响），`maingo.symbol` 另行归档。

出问题时：

```bash
gdb -s maingo.symbol maingo.bin
# 或
gdb maingo.bin
(gdb) symbol-file maingo.symbol
(gdb) bt            # 结合 core： gdb -s sym bin core
```

---

## 7. 要点总结

1. `-O0/-O1/-O2/-O3` 是优化级别，`-O3` 最高；优化与调试信息（`-g`）**可以同时开启**，这是本方案的前提。
2. 对**本身不含调试信息**的二进制做 `--only-keep-debug` / `--strip-debug`，产物大小与段信息几乎不变，**分离毫无意义**。
3. 只有编译时加了 `-g`（原文用 `-g3`），抽出的独立符号表才有价值，剥离后的可执行文件才会显著变小。
4. 剥离后的二进制在 gdb 中会提示 `(no debugging symbols found)`，函数、行号、局部变量全部不可见。
5. 挂载符号表文件后，即使看不到源码，**仍能查到函数信息与局部变量值**。
6. 该方案的核心价值：**线上部署优化后的小体积高性能二进制，同时保留 core dump 的事后定位能力**。

---

## 8. 整理者补充与勘误

- **笔误**：原文第二段的 `g++ -g3 -o3 ...` 应为 `-O3`（大写字母 O 才是优化选项，小写 `-o` 是输出文件）。
- **原文表述矛盾**：实验一里"不含符号表"与"里面有 debug 调试信息"前后不一致。结合实验二可确定：**未加 `-g` 的 release 编译结果不含调试段**，这才是分离无效的原因。
- **`gdb -s` 的说明**：原文写"gdb 启动时通过 `–s` 指定符号表文件"，实际对应启动参数 `-s <symfile>`；更常用的做法是在 gdb 内执行 `symbol-file <symfile>`。
- **更推荐的自动关联方式**：用 `objcopy --add-gnu-debuglink` 把符号表文件名/校验和信息写进可执行文件，gdb 会自动按约定路径查找，省去手动指定：
  ```bash
  objcopy --only-keep-debug maingo maingo.debug
  objcopy --strip-debug      maingo maingo.bin
  objcopy --add-gnu-debuglink=maingo.debug maingo.bin
  # 部署时把 maingo.debug 放到约定目录（如 ./ 、/usr/lib/debug/...）
  ```
- **工程化替代方案**：`strip` / `eu-strip`（elfutils，可保留 build-id）、`gcc -gsplit-dwarf`（`-g` + `.dwo` 文件）、以及发行版普遍采用的 **build-id + debuginfo 包** 机制；现代链接器还可加 `-Wl,--build-id` 配合 `/usr/lib/debug/.build-id/` 目录实现完全自动的符号查找。
- **平台的差异**：本文基于 Linux ELF；Windows 侧对应能力是 PDB（`/Zi` + `/DEBUG`，`link /PDB`、`diasymreader`），macOS 是 dSYM（`dsymutil`）。
- 原文中的若干截图（文件大小对比、`readelf -S` 段信息红框、gdb 输出）在纯文本抓取中未保留，正文以"文件如下""如上红框"等指代，本笔记已按上下文还原其含义。

---

## 9. 原文相关推荐（延伸阅读题目）

- GDB 动态加载符号表实战：剥离与重载调试技巧
- 生成独立的 gcc 调试文件及利用调试文件调试 core 文件
- 使用 objcopy 选择性修改/删除符号表以及其他相关 ELF 段
- 用 objcopy 把调试信息放到单独的文件中
- gdb 与 symbol 符号表文件的调试
- 使用 strip、eu-strip、objcopy 等剥离与导回符号表及调试信息
- Linux 环境 Release 版本的符号表剥离及调试方法
- Linux 下将动态库的调试信息分离
- 程序减肥：strip、eu-strip 及其符号表
- `objcopy(1)` man page
