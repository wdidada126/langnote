# pgtbl — 两级页表 + TLB + 缺页 + CoW 模拟器

对应讲次：**L04（虚拟地址机制）**、**L10（换页与缺页）**、**L11（写时复制 fork）**。

## 机制说明

| 组件 | xv6 原型 | 这里实现的 |
| --- | --- | --- |
| 两级页表（10/10/12） | `kernel/vm.c: walk()/mappages()`（RISC-V 是 9/9/9/12 三级） | `pgtbl.c: pte_slot/pt_map/pt_walk`，页表本身放在 `ram[]` 帧里 |
| TLB（16 项直接映射） | 硬件 + `sfence.vma` 协议 | `tlb_translate` 先查表后 walk，命中率统计；`g_flush_on_map=0` 演示"忘刷→读到陈旧物理页" |
| 缺页处理 | lab: pgtbl/mmap 的 `usertrap` 缺页分支；xv6-mm `uvmfault` | demand paging：首次触碰分配帧、清零、建映射、重放翻译 |
| CoW fork | lab-cow `duppage/uvmfault` | `proc_fork_cow`：可写页双方降只读+`PTE_C`、帧引用计数++；写缺页时按计数决定复制/转正 |

演示内容（`main.c`）：
1. 顺序触碰 40 页：40 次缺页、页内连写命中 TLB；
2. "sfence 忘没忘"对照实验：同 VA 换底层帧，不刷 TLB 读到旧值；
3. 父子共享页 → 子写触发复制 → 父读到旧值、子读到新副本 + 统计 cow-copy。

## 构建与运行

```sh
./build.sh      # → pgtbl_demo
```
```bat
build.bat       # cl 版本 → pgtbl_demo.exe
```

## 阅读顺序建议
`pgtbl.h`（PTE 位定义）→ `pt_walk` → `tlb_translate`（hit/slow/fault/CoW 四路径）→ `proc_fork_cow`。
与 xv6 `kernel/vm.c` 对照时注意：xv6 PTE 里直接放 PPN<<10，这里放 PA；xv6 的 U 位与 R/W/X 在
`PTE(9)` 内编码——位布局不同，机制完全相同。
