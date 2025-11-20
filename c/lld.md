# lld

不是lldb

sudo apt install -y lld
LLD 是 LLVM 项目自带的现代化链接器（linker），全称 LLVM Linker，目标是彻底取代古老的 GNU BFD 和 GNU Gold。

简单来说：lld 就是又快又好用的新世代链接器。

### 一、和传统链接器对比（一句话看懂）

| 链接器       | 速度          | 内存占用      | 并行能力      | 是否默认支持 Windows | 维护状态       |
|--------------|---------------|---------------|---------------|----------------------|----------------|
| GNU ld (BFD) | 极慢          | 吃内存如喝水  | 几乎无并行    | 不支持               | 还在维护但很老 |
| GNU gold     | 快一些        | 仍较高        | 有一定并行    | 不支持               | 半放弃状态     |
| lld      | 极快（常10倍+） | 内存极省      | 高度并行      | 原生完美支持         | 活跃开发中     |
| mold         | 比 lld 还快   | 低            | 极强并行      | 支持但非重点         | 第三方新星     |

实测数据（编译 LLVM/Clang 自身）：
- GNU ld：约 80~120秒
- lld：约812秒
- mold：约35秒

### 二、lld 的三大杀手级优点

1. 极致快
   - 多线程并行链接，核心越多越快
   - 大项目（如 Chrome、LLVM、Rust）链接时间经常从几分钟降到几秒

2. 支持所有主流平台，且是“开箱即用”
   - Linux（ELF）
   - Windows（PE/COFF，原生产生 .exe 和 .dll）
   - macOS（Mach-O）
   - WebAssembly（wasm-ld）

3. 和 Clang 无缝集成
   ```bash
   clang -fuse-ld=lld main.cpp -o main   # 只要 lld 装了，这条命令在 Linux/Windows/macOS 都直接生效
   ```

### 三、在不同系统上怎么装

| 系统                 | 安装命令                                      |
|----------------------|-----------------------------------------------|
| Ubuntu/Debian        | `sudo apt install lld` 或 `sudo apt install lld-18` |
| Fedora               | `sudo dnf install lld`                        |
| Arch Linux           | `sudo pacman -S lld`                          |
| macOS（Homebrew）    | `brew install llvm`（会顺带装 lld）           |
| Windows              | 装 LLVM 官方发布版、Scoop、Chocolatey、MSYS2 都行<br>或者直接用 Visual Studio 2022 17.5+ 自带 lld |

### 四、日常使用方式

```bash
# 最常用：让 clang/clang++ 自动用 lld
clang++ -fuse-ld=lld a.cpp b.cpp -o myprogram

# 直接调用 lld（类似 ld）
ld.lld a.o b.o -o myprogram

# Windows 下生成 exe（完美支持）
cl.exe /fuse-ld:lld hello.cpp
# 或者
clang-cl hello.cpp -fuse-ld=lld
```

### 五、总结一句话

lld = 快 + 省内存 + 跨平台 + 积极维护 = 2025 年之后所有 C/C++ 项目都应该默认使用的链接器。

现在大厂（Google、Meta、Apple、Microsoft）、大语言（Rust、Zig、Swift）、大项目（LLVM、Chrome、Firefox）全都默认用 lld 或者 mold，基本没人再用老的 GNU ld 了。

所以看到 `-fuse-ld=lld` 报错的时候，别犹豫，赶紧装上 lld，链接速度立刻起飞！