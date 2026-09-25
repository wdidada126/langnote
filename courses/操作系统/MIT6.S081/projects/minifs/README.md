# minifs — 单用户迷你文件系统（含 redo 日志与崩溃模拟）

对应讲次：**L06（文件系统）**、**L07/L09（日志与崩溃一致性）**、**L08（fs+ 设计空间）**、**L14（性能优化/批提交）**。

## 机制说明（与 xv6 的对应关系）

| 概念 | xv6 原型 | 本实现 |
| --- | --- | --- |
| 磁盘 | QEMU virtio 盘 | `Mfs.disk[256×512B]` 内存数组 |
| 缓冲缓存 | `bio.c: bread/bwrite + LRU` | `bread` + 16 槽缓存（满了先 commit） |
| 块/inode 位图 | `fs.c: balloc/ialloc` | 同一块内的两组位图（块位图 + 字节 40 起 inode 位图） |
| inode | 12 直接 + 1 间接 | 8 直接块（单文件 4KiB；**留作练习：加间接块**） |
| 目录 | `(name,inum)` 数组 | 16B 条目，32 项/块 |
| 路径解析 | `namei/nameip` | 单一 `namei`：返回 inum / (父,末段名) |
| 写前日志 | `log.c: log_write/commit/write_head` | `log_write` 快照 + 三段式 commit：日志区→日志头→回写目标块 |
| 崩溃恢复 | `log.recover` 重放 | `fs_mount` 检测日志头 → redo-all 重放（幂等） |
| 崩溃模拟 | lab-fs 的随机 kill | `fs_set_crash_at(op)`：第 n 次"物理写"后 abort，`fs_mount` 假装重启 |

### 演示了什么（main.c 四个实验）
1. **基本**：mkdir/create/write/read/ls/unlink；
2. **崩溃时机 A**（日志头已落盘、目标块回写一半）→ 重放补齐，数据完好——redo 的正确性证明现场；
3. **崩溃时机 B**（日志写一半、头没落盘）→ 事务整体作废，文件 0 字节——"要么全有要么全无"；
4. **批提交**（fssched 思路）：batch=8 把 8 个事务合成一次 commit，物理写与 commit 数对比——
   日志开销大头是"每事务两次头写+屏障"，批处理直接摊薄。

## 构建与运行

```sh
./build.sh    # → minifs_demo
```
```bat
build.bat     # → minifs_demo.exe（cl，Developer Command Prompt）
```
纯 C11、无系统调用依赖（连文件 IO 都没有——磁盘在内存里）。

## 已知简化（刻意留给练习）
- 无间接块/无引用计数（unlink 立即释放，即使 fd 还开着——对照 xv6 `iput` 语义）；
- 单用户无锁（xv6 的 `ilock` 双锁协议因此不可见）；
- 日志容量 19 块 = 最大事务（xv6 同样的 `LOGNBUF` 约束）；
- 无 free 块延迟回收（unlink 后块位图在事务内清掉）。
