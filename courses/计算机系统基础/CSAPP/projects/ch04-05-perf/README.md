# ch04-05-perf —— Cache 友好遍历 + 性能测量脚手架

**关联讲次**：L10（存储器层次/缓存）、L09（循环变换与依赖）、L11（展开/向量化收益观察）。
对应 CSAPP 官方 **Cache Lab / Performance** 材料的核心思想。

## 内容

| 文件 | 说明 |
| --- | --- |
| `src/perf_util.h` | 单调时钟封装（POSIX `clock_gettime` / Win32 `QueryPerformanceCounter`）+ `TIME_IT` 宏 |
| `src/matrix.c` | 三组实验：A 行/列遍历、B 朴素 vs 分块矩阵乘、C 步长冲突扫描 |

## 观察点

- **A**：列优先比行优先慢数倍到数十倍——空间局部性丢失 + 每列一步跨一整行。
- **B**：分块(TILE=32) 让工作集 ≈ 32×32×8B×2 装进 L1，复用率骤增。
- **C**：stride 扫到「缓存行 × 组数」的倍数时 ns/访存跳变 = 组冲突（颠簸）。
- `volatile double g_sink` 防死代码消除；若去掉，`-O2` 下时间趋近 0（L09 教训）。
- 换 `-O1/-O2/-O3` 重跑，感受"编译器替你做分块/展开"的边界。

## 构建与运行

```sh
./build.sh              # gcc -O2，输出 bin/matrix
CFLAGS=-O0 ./build.sh   # 关掉优化看未优化基线
```

```bat
build.bat               :: cl /O2，需 vcvarsall x64 环境
```

> Windows 上 `QueryPerformanceCounter` 是全局共享硬计数器，多进程并发会引入噪声，
> 取多次最小值（脚本已用 best-of-N 策略）。Linux 建议 `taskset -c 0` 绑核。
