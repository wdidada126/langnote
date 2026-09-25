# alloc — first-fit → buddy 迷你内存分配器

对应讲次：**L04（va：ulib.c malloc）**、**L19（物理内存分配：kalloc/buddy/slab）**。

## 机制说明

| 组件 | 内核原型 | 这里实现的 |
| --- | --- | --- |
| `firstfit.c` | xv6 `user/ulib.c malloc`、CSAPP 9.9 | 块头+按地址有序空闲链，first-fit 查找，双向合并；统计 `search_steps`（碎片代价） |
| `buddy.c` | Linux `mm/page_alloc.c` | 以 unit(64B) 为粒度的伙伴系统：order 桶、劈半(split)/合并(merge)、内部碎片统计 |
| `main.c` | — | ①确定性混合负载 + 存活区间互不重叠校验（模拟"分配器正确性测试"）②交错释放（棋盘空洞）实验：first-fit 与 buddy 都申请不到 32KB，但 buddy 在其余块也释放后一路 merge 自愈；棋盘场景正说明内核为何还需 slab/对象分桶 ③吞吐基准 |

要点（与讲义对应）：
- first-fit 的外碎片：**空闲总量够但找不到连续空间**——frag_demo 直接演示；
- buddy 缓解外碎片（伙伴可合并、且全空时自愈），但引入 **~25% 内部碎片**（2 的幂凑整）——report 里 `internal-frag` 即此；
- 这正是内核"页帧分配器（buddy）+ 对象分配器（slab）"两层结构的动机。

## 构建与运行

Linux/macOS/MinGW：
```sh
./build.sh        # gcc/cc 编译为 ./alloc_demo 并运行
```
Windows（Developer Command Prompt，含 cl）：
```bat
build.bat         # cl /W3 /O2 编译为 alloc_demo.exe 并运行
```
纯 C11，无 OS 依赖（静态数组模拟堆），MSVC 与 gcc/clang 均可编译。

## 扩展练习
- 给 first-fit 加"下次查找从上次断点继续"（Linux 的 `last_check_pos`），观察 search_steps 变化；
- 把 buddy 的 unit 从 64B 改成 4KB 即得"页帧分配器"；再加一层 size-class 空闲链就是最小 slab；
- 与 `kalloc.c` 对比：xv6 用单条 LIFO 链，无合并——写个 workload 证明它何时失败。
