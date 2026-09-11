# 笔记：查看库文件信息 —— `ar` / `tar` / `nm` 与符号表

> **来源**：CSDN [C/C++ -- Lib库文件nm调试之符号表](https://blog.csdn.net/helloworld20102010/article/details/46345783)
> **作者**：helloworld20102010（转载，原始出处指向 `gugemichael/article/details/8215738`）
> **发布时间**：2015-06-03　**专栏**：linux/c/cpp
> **整理日期**：2026-09-12
> **一句话概括**：`.o/.a/.so` 是三种**不同格式**的文件，要用对应的工具看——**`.a` 用 `ar`（不是 `tar`）**，看**里面有哪些函数/变量、缺什么符号**一律用 `nm`（C++ 记得 `-C` 反解名字修饰）。

---

## 0. 先纠正一个前提：`ar` ≠ `tar`

原文标题写作"利用 **tar**/nm 查看库文件"，这里的 `tar` 是笔误，**应为 `ar`**：

| | `ar` | `tar` |
|---|---|---|
| 归档格式 | **ar 格式**（魔数 `!<arch>\n`） | tar 格式（`ustar`/GNU 等） |
| 常见用途 | **静态库 `.a`**（成员是 `.o`） | 源码包、备份（`.tar`/`.tar.gz`） |
| 能否读对方的归档 | ❌ 一般不能（bsdtar 侧有例外，见 §6） | **GNU tar 读 `.a` 会报 `This does not look like a tar archive`** |
| 列出成员 | `ar t libfoo.a` | `tar -tf pkg.tar.gz` |

> 所以"**查看 `.a` 静态库**"正确姿势是 `ar t` / `ar tv`；`tar` 只在处理 `.tar` 类归档时才用。用户口语里的"tar/nm"实际上对应"**归档内容 + 符号表**"两件事。

**按文件类型选工具**（这张表是本文的骨架）：

| 文件 | 本质 | 看"内容/结构" | 看"符号" |
|---|---|---|---|
| `.o` | ELF **可重定位目标文件** | `file`、`readelf -h/-S` | **`nm`**、`objdump -t` |
| `.a` | **ar 归档**（打包了一堆 `.o`，**无压缩**） | **`ar t`** / `ar tv` | **`nm`**（可直接对归档整体使用） |
| `.so` | ELF **共享对象** | `readelf -d`、`ldd` | `nm -D`、`objdump -T` |
| 可执行文件 | ELF **可执行** | `readelf`、`ldd` | `nm`、`objdump -t` |
| `.tar/.tar.gz` | tar 归档（可含任意文件） | `tar -tvf` | — |

---

## 1. 原文要点：Linux 库文件与它们的生成

### 1.1 库文件的本质

写好 `.h` + `.c/.cpp`，编译成中间产物供他人使用。**生成中间库时不经过链接阶段**：

```bash
gcc -c -o foo.o foo.c        # -c：只编译不链接
```

因此源码里即使调用了 `pthread_create` 这类外部函数，**`gcc -c` 阶段也不需要 `-lpthread`** —— 那时还没到"找符号"的环节。

> 原文此处列的编译阶段顺序混乱（写作"文本解析 → 语法解析 → 此法分析 → 预处理分析"），正确顺序见 [§7 勘误](#7-整理者补充与勘误)。

### 1.2 静态库 vs 动态库

| | 静态库 `.a`（Linux）/ `.lib`（Windows） | 动态库 `.so`（Linux）/ `.dll`（Windows） |
|---|---|---|
| 链接时机 | **编译链接时**并入程序 | **运行时**加载进进程 |
| 是否成为程序一部分 | 是 | 否 |
| 运行时是否依赖外部文件 | 不依赖（不会因缺库而启动失败） | 依赖（库缺失则启动/加载失败） |
| 内存占用 | 每个进程各一份 | **多进程共享**一份 |
| 更新 | 必须重新编译程序 | **直接替换 `.so`** 即可 |
| 可执行文件体积 | 偏大 | 偏小 |

选择依据：一般第三方库两种版本都提供；系统库几乎都是动态库。**注意链接器默认优先找 `.so`**。

### 1.3 生成与使用

```bash
# 1) 编译成 .o（不需要头文件参与）
gcc -c -o foo.o foo.c

# 2) 静态库：ar 打包
ar -r libfoo.a foo.o            # 可加 s 建索引：ar -rsv libfoo.a foo.o

# 3) 动态库：位置无关代码 + 共享
gcc -fPIC -shared -o libfoo.so foo.c

# 4) 使用库（lib 前缀被 -l 隐含；优先匹配 libfoo.so）
gcc -o test test.c -lfoo
```

要点：

- `-fPIC`：生成**位置无关代码**，动态库运行时被加载到任意地址，需要重定位支持。
- `-lfoo` 会去找 `libfoo.so` 或 `libfoo.a`，**优先 `.so`**；只想用静态库时用 `-Wl,-Bstatic -lfoo -Wl,-Bdynamic` 或直接写 `libfoo.a` 全路径。
- **C++ 引 C 库**：头文件里必须加 `extern "C"`，因为 C++ 有重载、**符号名会被修饰（mangling）**，不声明就找不到 C 的那个同名符号。
- 动态库查找路径：`/lib`、`/usr/lib` 等预定义目录；自定义目录改 `/etc/ld.so.conf` 后执行 **`ldconfig`** 刷新缓存（或运行期用 `LD_LIBRARY_PATH`）。

---

## 2. 原文核心：用 `nm` 看符号表

### 2.1 被测代码

```cpp
#include <stdio.h>
int g1;
int g2 = 0;
static int g3;
static int g4 = 0;
const int g5 = 0;
static const int g6 = 0;

int main(int argc, char *argv[])
{
    static int st = 0;
    int t1;
    int t2 = 0;
    const int t3 = 0;
    printf("printf-function");
    return 0;
}

void foo1() {}
static void foo2() {}
```

```cpp
// 文件 2
void overload(int i) {}
// 文件 3
void overload(float i) {}
```

用 `g++ -c` 编出 `.o` 后，`nm a.o`（原文输出，节选）：

```
0000000000000000 t
0000000000000000 d
0000000000000000 b
0000000000000000 r
0000000000000000 r
0000000000000000 n
0000000000000000 n

0000000000000000 B g1
0000000000000004 B g2
0000000000000008 b g3
000000000000000c b g4
000000000000001c r g5
0000000000000020 r g6
                 U __gxx_personality_v0
0000000000000000 T main
0000000000000000 a nm.cpp
                 U printf
000000000000003e T _Z4foo1v
0000000000000044 t _Z4foo2v
0000000000000054 T _Z8overloadf
000000000000004a T _Z8overloadi
0000000000000010 b _ZZ4mainE2st
```

### 2.2 输出三列的含义

| 列 | 含义 |
|---|---|
| 第 1 列 | **符号地址/值**（十六进制）；`U`（未定义）行该列留空 |
| 第 2 列 | **符号类型**（大写=全局/外部，小写=局部 static） |
| 第 3 列 | **符号名**（C++ 下是修饰后的名字） |

### 2.3 原文给出的符号类型表（+ 本篇补齐）

| 类型 | 含义 | 原文举例 |
|---|---|---|
| `B` / `b` | **BSS 段**（未初始化/零初始化）数据；(小写为局部 static) | `g1`、`g2`（`B`）；`g3`、`g4`（`b`） |
| `D` / `d` | **已初始化数据段**（`.data`）；**小写为局部 static** | 原文示例中未出现有名字的 `d` |
| `R` / `r` | **只读数据**（`.rodata`，如 `const` 变量） | `g5`、`g6` |
| `T` / `t` | **代码段（.text）中的符号**；**小写一般是 static 函数** | `main`、`foo1`（`T`）；`foo2`（`t`） |
| `U` | **本文件未定义、需由外部提供的引用** | `printf`、`__gxx_personality_v0` |
| `N` / `n` | **调试/非分配段中的符号**（`N` 为调试符号；小写 `n` 常见于 `.debug_*`、`.comment` 等**非分配段**） | 原文输出中两个裸 `n` |
| `A` / `a` | **绝对符号**（值不会因重定位改变）；**`a nm.cpp` 是文件名符号（STT_FILE）** | `a nm.cpp` |
| `C` | **Common 符号**（未初始化的暂定定义，多个 `.o` 可合并） | — |
| `W` / `w` | **弱符号**（`__attribute__((weak))`） | — |
| `V` / `v` | **弱对象符号** | — |
| `I` / `i` | **间接引用符号**；`i` 在 ELF 下表示 **IFUNC**（运行期解析的函数） | — |
| `G` / `g` / `S` / `s` | **small data/bss**（小对象优化段） | — |
| `?` | 未知类型 | — |

> 完整列表见 `man nm`；**大小写之别**是本表最要紧的规律：**大写 = 全局/外部可见，小写 = 本文件局部（static）**（`u`/`v`/`w` 是特例）。

### 2.4 原文几个值得记的"读表"结论

1. **地址递增反映同类数据在段内的排布顺序**：`g1@0, g2@4, g3@8, g4@0xc`，`st@0x10`（都在 `.bss` 里继续排）。
2. **`int g2 = 0;` 仍然是 `B`（BSS）而不是 `D`（.data）** —— 因为**零初始化**会被放进 `.bss`，只有**非零初值**才占用 `.data` 空间。
3. **自动变量（`t1/t2/t3`）在符号表里根本没有条目** —— 它们生活在栈上，只有调试信息才会描述；只有 **static 局部变量 `st`** 有符号（`_ZZ4mainE2st`）。
4. **`U` 行就是"待链接的外部依赖"**：`printf` 来自 libc，`__gxx_personality_v0` 来自 C++ 异常处理运行时。

### 2.5 `nm` 最实用的一点：C++ 名字修饰（name mangling）

`g++` 编译后函数名带前后缀：**前缀表示所属类/命名空间，后缀表示参数类型缩写**。

| 原始声明 | 修饰后符号 | 解读 |
|---|---|---|
| `void foo1()` | `_Z4foo1v` | `4foo1` = 长度 4 的名字 `foo1`；`v` = `void`（无参） |
| `static void foo2()` | `_Z4foo2v` | 同上，且是小写 `t`（局部） |
| `void overload(int)` | `_Z8overloadi` | `i` = `int` |
| `void overload(float)` | `_Z8overloadf` | `f` = `float` |
| `main` 内的 `static int st` | `_ZZ4mainE2st` | `_ZZ` 表示"函数内的 static 局部符号" |
| 类成员 | `_ZN6Widget4drawEv` | `N...E` 包裹类名 |

**原文的金句**：符号表里**没有返回值的信息**，所以"仅返回值不同"的函数根本无法区分 —— 这正是**"返回值不同不能构成重载"的根本原因**。

反解（demangle）：

```bash
nm -C a.o                 # 直接打印可读名
nm a.o | c++filt          # 或管道交给 c++filt
```

---

## 3. 常用命令速查

### 3.1 `ar` —— 操作静态库（`.a`）

```bash
ar t  libfoo.a            # 列出成员（.o 文件名）
ar tv libfoo.a            # 列出成员 + 大小/时间/权限
ar x  libfoo.a            # 解包到当前目录
ar p  libfoo.a foo.o > f.o  # 把某个成员打印到 stdout
ar r  libfoo.a foo.o      # 添加/替换成员（同名的会被替换）
ar d  libfoo.a foo.o      # 删除成员
ar rs libfoo.a            # 建立/刷新符号索引（也可用 ranlib）
```

**注意**：

- `.a` 是**归档**不是**压缩**包，成员原样存放，所以"打成 .a 体积不变"。
- `.a` **不能打进 `.a`**（成员应是 `.o`）。
- 修改归档后**必须确保符号索引存在**（`s` 修饰符或 `ranlib`），否则链接器可能报找不到符号。

### 3.2 `tar` —— 操作 tar 归档

```bash
tar -tf  pkg.tar.gz       # 列出内容
tar -tvf pkg.tar.gz       # 详细列表（权限/属主/大小/时间）
tar -xzf pkg.tar.gz       # 解包
tar -czf pkg.tar.gz dir/  # 打包 + gzip
```

> 再次强调：`.a` 不要用 `tar`。

### 3.3 `nm` —— 看符号表（核心工具）

```bash
nm a.o                     # 基本用法
nm -C a.o                  # 反解 C++ 名字修饰
nm -D libfoo.so            # 只看动态符号表（.so 的导出符号就在这里）
nm -A libfoo.a             # 显示每个符号属于哪个成员/文件
nm -u a.o                  # 只看未定义（U）符号 → 谁在"欠账"
nm --defined-only libfoo.a # 只看已定义 → 库里到底提供了什么
nm -S a.o                  # 连符号大小一起显示
nm --size-sort a.o         # 按大小排序（找"最占地的函数"）
nm -n a.o                  # 按地址排序（默认按名字排序）
nm -l a.o                  # 附上源码行号（需 -g 编译）
nm libfoo.a > a.txt        # 输出重定向到大文件，便于 grep
```

### 3.4 其他配套工具

| 工具 | 用途 |
|---|---|
| `file xxx` | 一眼看出是 ELF 可执行/共享对象/ar 归档 |
| `readelf -h/-S/-s/-d` | ELF 头、段表、符号表、动态段（比 `nm` 更底层更全） |
| `objdump -t` / `-T` | 符号表 / 动态符号表 |
| `objdump -d` / `-dr` | 反汇编（`-r` 带重定位） |
| `strings libfoo.so` | 提取可打印字符串，找版本号/错误信息线索 |
| `ldd ./test` | 看可执行文件运行时依赖哪些 `.so` |
| `c++filt _Z8overloadi` | 单独反解一个修饰名 |
| `size libfoo.a` | 看 text/data/bss 各段大小 |
| `strip` / `objcopy --strip-debug` | 剥离符号/调试信息（见 `objcopy-symbol-separation-notes.md`） |

---

## 4. 实战：定位 `undefined reference`

链接错误的本质是"**某个 `U` 符号在所有地方都找不到定义**"，用 `nm` 顺着走一遍即可：

```bash
# 1) 我到底缺哪个符号？（注意 C++ 要先反解出可读名）
nm -C -u build/a.o

# 2) 我链接的这个库里有没有它？
nm -C --defined-only libfoo.a | grep -i foo

# 3) 动态库是否把它导出了？（.so 要看 -D！）
nm -D -C libfoo.so | grep -i foo

# 4) 名字对不上？看是不是 C/C++ 混编少了 extern "C"
nm -C libfoo.a | grep foo          # 若看到 _Z3foov 而你在 C 里写 foo → 就是这个问题

# 5) 让链接器直接告诉你
gcc -Wl,--trace-symbol=foo -o test test.o -lfoo
gcc -Wl,-y,foo ...                 # -y 同义
```

**常见四类原因**：

| 现象 | 原因 |
|---|---|
| 库里根本没这个符号 | 源文件没参与编译 / 库是旧版本 |
| 库里有但名字不同（`_Z3foov`） | C/C++ 混编未加 `extern "C"` |
| 库里有且名字对，仍报错 | **静态库链接顺序**问题（`-lfoo` 要放在引用它的 `.o` 之后）；或只 `.so` 而运行期路径不对 |
| 同一符号报 multiple definition | 头文件里定义了全局变量/非 inline 函数；或 `C` 型 common 符号冲突 |

---

## 5. `nm` 输出解读小结（一张表记住）

| 你看到的 | 说明 |
|---|---|
| `U xxx` | 依赖外部提供，**这行是链接错误的元凶候选** |
| `T xxx` | 本文件定义的函数（全局可见） |
| `t xxx` | 本文件定义的 static 函数（外部不可见） |
| `B xxx` / `D xxx` | 全局变量（`B` 在 bss，`D` 在 data） |
| `b xxx` / `d xxx` | static 全局变量 |
| `R xxx` / `r xxx` | `const` 只读数据 |
| 只有 `t/d/b/r/n` 而**没有名字** | **段符号（STT_SECTION）**，标识 `.text/.data/.bss/.rodata/其他段` 的起点 |
| `a nm.cpp` | **文件名符号（STT_FILE）**，绝对符号 |
| `_Z...` | C++ 修饰名，用 `nm -C` 或 `c++filt` 反解 |

---

## 6. 补充：`tar` 到底能不能看 `.a`？

- **GNU tar**：不能。`tar -tf libfoo.a` 会失败（`This does not look like a tar archive`），因为它是 **ar 格式**而不是 tar 格式。
- **BSD tar / bsdtar**（macOS、Windows 10+ 自带，基于 **libarchive**）：libarchive 本身支持 `ar` 格式，所以在这类系统上 `tar -tf libfoo.a` **可能**能列出来。
- **但不要依赖这一点**：跨平台脚本、CI 里一律用 **`ar t`**；想看"库里有哪些符号"则用 `nm`。

---

## 7. 整理者补充与勘误

| # | 原文 | 更正/补充 |
|---|---|---|
| 1 | 标题"利用 **tar**/nm 查看库文件" | 应为 **`ar`/`nm`**；`.a` 是 ar 归档，`tar` 不适用（§0、§6） |
| 2 | "文本解析 → 语法解析 → 此法分析 → 预处理分析" | 正确顺序：**预处理（宏/头文件展开）→ 词法分析（扫描）→ 语法分析 → 语义分析 → 中间代码与优化 → 目标代码生成 → 汇编 → 链接**；"此法分析"是"词法分析"的笔误 |
| 3 | "**.a 就是 .o 的压缩包**" | 是**归档（archive）**而非压缩：成员原样存放，因此打包不减小体积；`ar` 额外写入**符号索引**供链接器快速查找 |
| 4 | `ar -r libfoo.a foo.o` | 建议写成 `ar -rsv` 或随后 `ranlib libfoo.a`，确保符号索引存在（部分实现会自动建立，但显式写更保险） |
| 5 | "多进程共" | 应为"多进程**共享**"（漏字） |
| 6 | "`externc "C"`" | 应为 **`extern "C"`** |
| 7 | 符号类型表只解释了 7 种，`d`/`n`/`a` 在输出中出现却未说明 | 已补齐：`d`=局部已初始化数据、`n`=非分配段（调试/辅助段）中的局部符号、`A/a`=绝对符号（`a nm.cpp` 即文件名符号）；并补充 `C/W/V/I` 等（§2.3） |
| 8 | 未解释输出里几个"只有类型没有名字"的行 | 那是**段符号（STT_SECTION）**，每个段一个，值为 0 表示段内偏移起点（§5） |
| 9 | "`int g2 = 0;` 出现在 `B`" | 正确但没说原因：**零初始化仍归 `.bss`**，只有非零初值才占 `.data`；`const` 变量归 `.rodata`（`R/r`） |
| 10 | 未提 `nm` 的排序行为 | 默认**按符号名**排序，`-n` 才是**按地址**排序（原文输出呈按段/地址排列，疑为 `nm -n` 或经整理） |
| 11 | 未提静态库链接顺序 | 静态库按命令行**从左到右**顺序解析，`-lfoo` 必须在引用它的目标文件**之后**，否则报 undefined reference |
| 12 | 未提 `.so` 要用 `nm -D` | 共享库的导出符号在**动态符号表**里，`nm` 默认只读 `.symtab`；对 strip 过的 `.so` 往往必须 `nm -D` |

---

## 8. 一句话总结

**"看库文件"其实分两件事**：**看容器**用 `ar t`（`.a`）/ `tar -tf`（`.tar`）/ `readelf`（`.so`）；**看符号**用 `nm -C`（谁定义了 `T/t`、谁欠账 `U`、C++ 名字怎么修饰）—— 这两招配合 `ldd`/`objdump`，足以定位绝大多数链接期的 `undefined reference`。
