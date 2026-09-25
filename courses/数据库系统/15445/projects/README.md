# 15-445/645 配套项目（projects）

C++17、仅标准库、每项目一个自洽 `main.cpp`（含断言式测试），借鉴 BusTub 思想但独立实现。**本轮只写不编译**，统一由用户自行构建。

## 构建方式（每个子目录都自带）
- Windows（MSVC，Developer Command Prompt）：`build.bat`（内部 `cl /std:c++17`）
- Linux/macOS：`bash build.sh`（内部 `g++ -std=c++17 -Wall -Wextra`）
- 手动单行：`g++ -std=c++17 main.cpp -o app && ./app`

## 项目总表

| # | 目录 | 对应讲次 | 核心机制 | 语言 |
|---|---|---|---|---|
| 01 | `01-buffer-pool` | L06 | 缓冲池：Clock/second-chance 置换 + `pin_count` + 脏页回写 | C++17 |
| 02 | `02-bplus-tree` | L08 | B+ 树：insert+分裂、叶子兄弟链 range scan | C++17 |
| 03 | `03-record-storage` | L04/L05 | 字节级 slotted page + 单页 heap 表（TID 稳定、墓碑删除） | C++17 |
| 04 | `04-volcano-executor` | L12 | 火山迭代器：SeqScan/Filter/Project/Limit（pipelined） | C++17 |
| 05 | `05-agg-sort` | L10 | 阻塞算子：Sort + HashAgg（SUM/COUNT/AVG/MIN/MAX） | C++17 |
| 06 | `06-mini-sql` | L02/L12/L14 | 子集 SQL 解析器 → AST → 接执行器 | C++17 |
| 07 | `07-wal-recovery` | L19/L20 | WAL + STEAL/NO-FORCE + redo/undo mini-ARIES | C++17 |
| 08 | `08-lock-manager` | L16 | 2PL 锁管理器：S/X 冲突矩阵 + wait-for 图死锁检测 | C++17 |

## 建议做序（沿数据流走一遍）
01（页驻留）→ 02（有序索引）→ 03（页里放什么）→ 04（逐元组执行）→ 05（聚合排序）→ 06（SQL 打通到执行）→ 07（写操作如何扛崩溃）→ 08（并发如何不串台）。

## 组合成"迷你 BusTub"的思路
04/05/06 共用 volcano 算子接口；01+02+03 可合成存储层（缓冲池载页→页内 slotted→B+树索引）；07 给写路径加持久性；08 给并发加正确性。把它们缝起来即覆盖课程 P1–P5 的骨架。

## 说明
- 代码为教学最小实现，未覆盖 B+ 树删除（借/合并）、哈希索引、向量化执行、多版本 GC 等——各 README 的"与讲义的接缝"列出了推荐扩展点。
- 所有测试均为纯断言 harness，输出 `[ ok ]/[FAIL]`，退出码 0 表示全通过。
