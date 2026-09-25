# mini_shell — fork/exec/管道/重定向迷你 shell

对应讲次：**L05（系统调用）**、**L20（IPC/管道）**、并服务于 L01 的 Unix 进程模型。
6.1810 lab-shell 的宿主可移植版：POSIX 用 fork+execvp+dup2+pipe；Windows 用
CreateProcess + 匿名管道 + STARTUPINFO 重定向（同一套语义，两套后端——正好体会
"系统调用接口"在不同内核上的实现自由度）。

## 机制说明

- **解析**：`splitline()` 就地分词，`|` 切段（≤4 段），`<`/`>` 记录重定向文件；
- **内建命令**：`cd`（必须是内建——子进程改不了父进程的 cwd，这是"为什么 fork 之后 chdir 没用"的活教材）、`pwd`、`exit`；
- **管道链**（POSIX）：每相邻两段 `pipe()`；第 i 段 stdout 接到 i+1 段 stdin；
  所有中间 fd 设 `FD_CLOEXEC`，靠 `dup2` 移交——否则第三段永远等不到 EOF / 或泄漏进孙进程
  （这是 lab-shell 的 `wait` 死锁经典坑，README 值得踩一次）；
- **Windows 分支**：`CreatePipe` + `SetHandleInformation` + `STARTF_USESTDHANDLES`，
  父进程交出写端（CloseHandle）语义与 POSIX 一一对应；
- **收尾**：`waitpid` 全部子进程，报退出码。

## 构建与运行

```sh
./build.sh     # → mini_shell（Linux/macOS/MinGW）
```
```bat
build.bat      # → mini_shell.exe（cl，Developer Command Prompt）
```

试玩（先造一个输入文件）：
```
> echo hello world > tmp.txt
> sort < tmp.txt | head        # POSIX
> findstr "pattern" big.txt | sort > out.txt   # Windows
> cd ..
> pwd
> exit
```
对照：lab-shell 还要求 `;` 与后台 `&`——作为练习补上（POSIX 分支只需少一次 waitpid）。
