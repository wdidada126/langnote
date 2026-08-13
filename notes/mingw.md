# mingw

https://github.com/niXman/mingw-builds-binaries/releases

https://github.com/mmozeiko/build-gcc-mingw/releases
新版本


https://github.com/skeeto/w64devkit/releases/tag/v1.23.0
https://github.com/niXman/mingw-builds-binaries/releases
https://github.com/skeeto/w64devkit/releases

mingw32-make.exe重命名为make.exe

eclipse win支持mingw
https://www.mingw-w64.org/downloads/
https://www.mingw-w64.org/

https://github.com/mingw-w64

https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win64/

MinGW，是Minimalist GNU for Windows的缩写。它是一个可自由使用和自由发布的Windows特定头文件和使用GNU工具集导入库的集合，允许你在GNU/Linux和Windows平台生成本地的Windows程序而不需要第三方C运行时（C Runtime）库。

以下答案截止至 2021/06/01：MinGW: 编译目标仅兼容 32 位应用程序，最新的官方二进制版本为 GCC 9.2.0。(OSDN)MinGW-w64: 衍生自 MinGW 的项目，编译目标兼容 32 位应用程序与64 位应用程序，最新的官方二进制版本为 GCC 8.1.0。(SourceForge)TDM-GCC: 衍生自 MinGW 和 MinGW-w64 的项目，分为 32 位与 64 位两个版本，32 位版本的编译目标仅兼容 32 位应用程序，64位版本的编译目标兼容 32 位应用程序与 64 位应用程序，最新的官方二进制版本为 GCC 10.3.0。以上三个 GCC 编译器的 Windows 发行版均兼容 POSIX 线程标准 。("pthread.h")个人推荐优先选择 TDM-GCC 作为首选 C / C++ 编译器。

https://www.zhihu.com/question/39952667/answer/1133837727

https://github.com/jmeubank/tdm-gcc-src/releases

```powershell
gcc --version
gcc.exe (x86_64-posix-sjlj-rev0, Built by MinGW-W64 project) 8.1.0
Copyright (C) 2018 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

g++ --version
g++.exe (x86_64-posix-sjlj-rev0, Built by MinGW-W64 project) 8.1.0
Copyright (C) 2018 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


PS C:\Users\edidada> g++ --version
g++.exe (GCC) 5.3.0
Copyright (C) 2015 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

PS C:\Users\edidada> gdb --version
GNU gdb (GDB) 7.6.1
Copyright (C) 2013 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "mingw32".
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.


make -h
Usage: make [options] [target] ...
Options:
  -b, -m                      Ignored for compatibility.
  -B, --always-make           Unconditionally make all targets.
  -C DIRECTORY, --directory=DIRECTORY
                              Change to DIRECTORY before doing anything.
  -d                          Print lots of debugging information.
  --debug[=FLAGS]             Print various types of debugging information.
  -e, --environment-overrides
                              Environment variables override makefiles.
  --eval=STRING               Evaluate STRING as a makefile statement.
  -f FILE, --file=FILE, --makefile=FILE
                              Read FILE as a makefile.
  -h, --help                  Print this message and exit.
  -i, --ignore-errors         Ignore errors from recipes.
  -I DIRECTORY, --include-dir=DIRECTORY
                              Search DIRECTORY for included makefiles.
  -j [N], --jobs[=N]          Allow N jobs at once; infinite jobs with no arg.
  -k, --keep-going            Keep going when some targets can't be made.
  -l [N], --load-average[=N], --max-load[=N]
                              Don't start multiple jobs unless load is below N.
  -L, --check-symlink-times   Use the latest mtime between symlinks and target.
  -n, --just-print, --dry-run, --recon
                              Don't actually run any recipe; just print them.
  -o FILE, --old-file=FILE, --assume-old=FILE
                              Consider FILE to be very old and don't remake it.
  -O[TYPE], --output-sync[=TYPE]
                              Synchronize output of parallel jobs by TYPE.
  -p, --print-data-base       Print make's internal database.
  -q, --question              Run no recipe; exit status says if up to date.
  -r, --no-builtin-rules      Disable the built-in implicit rules.
  -R, --no-builtin-variables  Disable the built-in variable settings.
  -s, --silent, --quiet       Don't echo recipes.
  -S, --no-keep-going, --stop
                              Turns off -k.
  -t, --touch                 Touch targets instead of remaking them.
  --trace                     Print tracing information.
  -v, --version               Print the version number of make and exit.
  -w, --print-directory       Print the current directory.
  --no-print-directory        Turn off -w, even if it was turned on implicitly.
  -W FILE, --what-if=FILE, --new-file=FILE, --assume-new=FILE
                              Consider FILE to be infinitely new.
  --warn-undefined-variables  Warn when an undefined variable is referenced.

This program built for x86_64-w64-mingw32
Report bugs to <bug-make@gnu.org>
```


https://www.zhihu.com/question/22137175

对标cl.exe


x86_64-8.1.0-release-posix-sjlj-rt_v6-rev0

## MSYS2 与 pacman：Windows 上的 Arch 风格包管理（截至 2026-08）

MSYS2 是 Windows 上提供 POSIX shell、GNU 工具和 MinGW-w64/LLVM 原生工具链的发行环境。它使用从 Arch Linux 移植并针对 Windows/Cygwin 调整过的 `pacman` 管理二进制包；因此 `pacman` 的角色大致相当于 Debian/Ubuntu 中的 `apt`，但包格式、仓库、命令选项和环境模型都不同。

不要把 **MSYS2** 写成 `mxys2`。也不要把 MSYS2 当作 WSL：MSYS2 工具运行在 Windows 上，MSYS shell 通过兼容层提供类 Unix 体验，而 UCRT64/MinGW/Clang 环境生成的是 Windows 原生可执行文件和 DLL。

### 与 apt 的快速对照

| 目的 | Debian/Ubuntu | MSYS2 / pacman | 说明 |
| --- | --- | --- | --- |
| 更新软件源并完整升级 | `apt update && apt upgrade` | `pacman -Suy` | MSYS2 是 rolling release，只支持完整升级，不要长期只刷新索引。 |
| 安装包 | `apt install git` | `pacman -S git` | 会解析并安装依赖。 |
| 搜索远端包 | `apt search keyword` | `pacman -Ss keyword` | 搜索已安装包用 `pacman -Qs keyword`。 |
| 查看已安装包信息 | `apt show pkg` / `dpkg -s pkg` | `pacman -Qi pkg` | 远端仓库信息用 `pacman -Si pkg`。 |
| 删除包 | `apt remove pkg` | `pacman -R pkg` | 删除依赖前先理解反向依赖；常见的递归清理是 `-Rns`，不可盲用。 |
| 查文件归属 | `dpkg -S /path/file` | `pacman -Qo /full/path/file` | 路径、大小写和 Windows 的 `.exe` 后缀必须准确。 |
| 查哪个远端包提供文件 | `apt-file search file` | `pacman -Fy` 后执行 `pacman -F file` | `-Fy` 会更新文件数据库。 |
| 清理下载缓存 | `apt clean` | `paccache -r` | pacman 缓存默认在 `/var/cache/pacman/pkg/`。 |

`pacman -Syu` 与 `pacman -Suy` 在选项组合上等价；本文沿用 MSYS2 文档的 `pacman -Suy` 写法。`-S` 表示同步仓库，`-y` 刷新仓库数据库，`-u` 升级已安装包，`-R` 删除，`-Q` 查询本地数据库，`-F` 查询仓库中的文件清单。

### 首次安装与日常更新

安装 MSYS2 后，先打开 **MSYS** 终端完成基础升级。更新核心组件时终端可能会被 pacman 主动关闭；重新打开后再执行一次，直到没有待升级包：

```bash
pacman -Suy
# 若 pacman 提示关闭所有 MSYS2 进程，确认后重新打开终端，再执行一次 pacman -Suy
```

不要把 `pacman -Sy some-package` 当作日常“只安装一个包”的命令。它可能使本地仓库索引变新而已安装依赖仍旧，形成 partial upgrade。正确做法是先完整升级，再安装所需包：

```bash
pacman -Suy
pacman -S git make cmake ninja
```

长期未更新后若出现 PGP 签名或 keyring 错误，先按 MSYS2 官方更新文档处理：

```bash
pacman-key --refresh-keys
# 若仍因缺少新的维护者 key 失败：
pacman -Sy msys2-keyring
pacman -Suy
```

不要为图省事在未知状态下使用 `--overwrite '*'`、删除 pacman 数据库或从网上复制镜像配置。文件冲突先用 `pacman -Qo <冲突文件>` 查归属，确认手工安装或其他工具覆盖了哪个文件后再最小化处理。

### 先选环境，再安装工具链

MSYS2 不止一个“软件仓库”。当前 shell 的 `MSYSTEM`、PATH 前缀、C 运行时、编译器和包名前缀共同决定目标环境。一个项目必须从编译到链接尽量保持同一环境；尤其不能混用 UCRT 与 MSVCRT 构建的静态库、对象文件，或跨 DLL 传递 `FILE*`、C++ STL 对象等 CRT 所有权对象。

| 环境 | 路径前缀 | 默认工具链 / C 运行时 | 建议用途 |
| --- | --- | --- | --- |
| MSYS | `/usr` | GCC / Cygwin 兼容层 | bash、pacman、Autotools、Git 等 Unix 风格工具；不作为发布原生 Windows 程序的默认目标。 |
| UCRT64 | `/ucrt64` | GCC / UCRT | 64 位 Windows 原生开发的默认选择；与现代 MSVC/UCRT 兼容性较好。 |
| CLANG64 | `/clang64` | LLVM/Clang + LLD / UCRT | 希望使用 Clang、libc++、sanitizer 或 LLD 的 64 位原生开发。 |
| CLANGARM64 | `/clangarm64` | LLVM/Clang / UCRT | Windows on ARM 的原生目标。 |
| MINGW64 | `/mingw64` | GCC / MSVCRT | 历史 64 位环境；MSYS2 已在 2026-03 宣布弃用，新的项目不要再以它为默认。 |
| MINGW32 / CLANG32 | `/mingw32`、`/clang32` | 32 位目标 | 32 位环境已处于淘汰阶段，仅为维护遗留需求使用。 |

不确定时选择 **UCRT64**，通过 `ucrt64.exe` 或 `msys2_shell.cmd -ucrt64` 打开；在该环境中确认：

```bash
echo "$MSYSTEM"       # 预期 UCRT64
echo "$MINGW_PREFIX"  # 预期 /ucrt64
which gcc
gcc --version
```

包名也带有环境含义。MSYS 包通常没有 MinGW 前缀，例如 `git`、`bash`；UCRT64 的原生库/工具常以 `mingw-w64-ucrt-x86_64-` 开头；CLANG64 使用 `mingw-w64-clang-x86_64-`。不要在 UCRT64 项目中安装无前缀的 `/usr` 库来替代原生依赖。

```bash
# 在 UCRT64 shell 中安装常用原生 C/C++ 工具与依赖
pacman -S mingw-w64-ucrt-x86_64-toolchain \
          mingw-w64-ucrt-x86_64-cmake \
          mingw-w64-ucrt-x86_64-ninja \
          mingw-w64-ucrt-x86_64-pkgconf

# 查找正确的环境前缀包，而不是猜包名
pacman -Ss '^mingw-w64-ucrt-x86_64-.*(fmt|boost|openssl)'
```

### 常用查询、依赖与维护命令

```bash
# 搜索仓库、搜索本地已安装、查看包信息
pacman -Ss openssl
pacman -Qs openssl
pacman -Si mingw-w64-ucrt-x86_64-openssl
pacman -Qi mingw-w64-ucrt-x86_64-openssl

# 查看显式安装包、孤儿依赖、依赖树和文件归属
pacman -Qe
pacman -Qdt
pactree mingw-w64-ucrt-x86_64-openssl
pacman -Qo /ucrt64/bin/libssl-3-x64.dll

# 查询仓库提供某文件的包
pacman -Fy
pacman -F pkg-config.exe

# 清理旧缓存；处理 pacnew/pacsave 配置文件
paccache -r
pacdiff
```

`pacman -Qm` 可以找出本地安装、但当前不再由仓库维护的包。`pacdiff` 用于合并升级遗留的 `.pacnew` 和 `.pacsave`，不要直接删除这些文件后再排查“为什么全局配置没升级”。包管理数据库只记录 pacman 安装的文件；`make install`、手动解压、`npm -g` 等写入同一前缀都可能造成文件冲突，因此开发项目应尽量装到项目隔离目录或虚拟环境中。

### MSYS2 特有的实践边界

1. 在 **MSYS** shell 做系统更新和安装通用 Unix 工具，在 **UCRT64/CLANG64** shell 构建目标程序。pacman 可见多个仓库，不代表任何 shell 都应混用它们的二进制。
2. `pacman` 是系统级包管理器，不替代语言级隔离：Python 用 venv/uv，Node.js 用项目 lockfile，Rust 用 Cargo，Java 用 Maven/Gradle。不要用 pacman 全局安装来绕过项目依赖锁定。
3. MSYS2 镜像默认会选择合适镜像。受限企业网络应固定允许的 `repo.msys2.org`，并在 `/etc/pacman.d/mirrorlist.msys`、`mirrorlist.mingw` 中配置，不要依赖会跳转到任意镜像的地址。
4. CI 中应从干净的 MSYS2 环境执行完整升级后再装依赖；同时固定构建脚本的 `MSYSTEM=UCRT64`（或明确的其他目标），并打印 `gcc --version`、`cmake --version` 和 PATH，避免本机与 CI 混入不同 CRT。
5. 安装或删除时仔细读确认列表。MSYS2 的 pacman 在询问删除包时默认回答 `yes`，与 Arch Linux pacman 的默认行为不同；自动化里的 `--noconfirm` 应只用于可重复的受控环境。

### 参考资料

- MSYS2：包管理和 pacman 基础：<https://www.msys2.org/docs/package-management/>
- MSYS2：完整升级、keyring、缓存与 pacnew/pacsave：<https://www.msys2.org/docs/updating/>
- MSYS2：UCRT64、CLANG64、MINGW64 及 CRT 兼容性：<https://www.msys2.org/docs/environments/>
- MSYS2：环境对应的包名前缀：<https://www.msys2.org/docs/package-naming/>
- MSYS2：镜像与企业网络配置：<https://www.msys2.org/docs/mirrors/>
- MSYS2：与 Arch pacman 的行为差异：<https://www.msys2.org/docs/pacman/>

