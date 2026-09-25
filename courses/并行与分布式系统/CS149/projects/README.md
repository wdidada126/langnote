# CS149 配套项目计划

> 原则：章节 → 语言 → 小项目 → 编译方式。本轮只写代码与 build 脚本，不执行编译（集中验证由用户统一进行）。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
|---|---|---|---|
| L3-L4 数据并行 | C++ (OpenMP) | 图像卷积滤波：标量版 → OpenMP 版，测加速比 | `make omp-conv`（g++ -fopenmp -O3） |
| L4/L7 归约与扫描 | C++ | work-efficient prefix sum（数组求前缀和 + 直方图） | `make scan` |
| L5 任务并行 | C++ | fork-join 递归 Mandelbrot + 简易工作窃取调度器 | `make tasks`（C++17 threads） |
| L6 同步 | C++ | 无锁栈 / 单生产者单消费者环形队列 + TSan 验证脚本 | `make lockfree`（-fsanitize=thread 双产物） |
| L8 通信 | C (MPI) | Jacobi 迭代解热方程：halo 交换 + 强/弱扩展实验 | `mpicc -O3 jacobi.c`（需 MPICH/OpenMPI） |
| L10 GPU | CUDA C++ | 分块矩阵乘三重优化：naive → shared memory → 向量化 | `nvcc -O3 mm.cu`（需 CUDA Toolkit） |
| L10 GPU 备选 | Python (Triton) | Triton 版 softmax kernel 与 PyTorch naive 对拍 | `python bench.py`（依赖 triton） |
| L11 集合通信 | Python (torch.distributed) | 手写 ring all-reduce 与 NCCL 对比带宽 | `torchrun --nproc_per_node=4 ring_ar.py` |
| L12 分布式框架 | Python/Java | 迷你 MapReduce：wordcount + 倒排索引（单机多线程模拟） | `make minmr` |
| L14 评测 | C++ | roofline 小实验：不同算术强度的 kernel 画 ridge 图 | `make roofline` + `python plot.py` |

## 目录约定（后续填充）

```
projects/
  01_openmp_conv/    Makefile src/
  02_prefix_scan/
  ...
projects/README.md   (本文件)
```

每个子项目自带 `make` 目标与 `NOTES.md`（预期输出/测量口径）；跨平台注意事项（Windows 下 OpenMP/MPI/CUDA 环境差异）统一记录在本文件末尾，待实现时补充。
