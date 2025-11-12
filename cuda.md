# cuda
Nvidia 很早(2007)就推出CUDA了，那时候 Rust 甚至都没出来，有这个历史基石在，自然很多高性能计算相关的库都在用 C++ 写。向量数据库的话，Rust 现在有一个 Qdrant。

CUDA其实也是C的方言（语法和C基本一致，只是要抛开一些CPU编程的思维定式）啦。

the popular parallel computing platform and programming model from NVIDIA 

[cuda navidia blog](https://devblogs.nvidia.com/even-easier-introduction-cuda/)

cuda csdn blog

github codespaces支持cuda吗？
https://github.com/orgs/community/discussions/45402
不支持，推荐gcp或者aws

阿里云 gpu服务器
nvcc -V

包月费用
最低 3695.00元

英伟达终为CUDA添加原生Python支持

## CUDA 代码开源吗？—— 2025 年最新全景解答

> 一句话总结：  
> CUDA 本身不开源（NVIDIA 专有），但你可以用它写 100% 开源代码 —— 就像用闭源编译器（MSVC、ICC）写开源 C++ 一样。

### 1. CUDA 的“开源”分层拆解

| 层级 | 是否开源 | 说明 | 许可证 |
|------|----------|------|--------|
| CUDA Toolkit（编译器、库、工具） | 不开源 | `nvcc` 编译器、`cuBLAS`、`cuDNN` 等是 NVIDIA 专有 | 专有 EULA |
| CUDA 驱动 / Runtime API | 不开源 | 运行时必须装 NVIDIA 驱动 | 专有 |
| CUDA 头文件（`.h`） | 部分开源 | 可在 GitHub 找到，但受 EULA 限制 | EULA |
| 你写的 `.cu` 代码 | 100% 可开源 | 你的算法、内核、主机代码 | 你决定（MIT/GPL/Apache） |
| 开源 CUDA 替代生态 | 部分开源 | 如 ZLUDA（CUDA on AMD）、HIP（AMD）、SYCL（Intel） | 开源（MIT/BSD） |

### 2. NVIDIA 官方立场（2025 年）

| 项目 | 状态 | 链接 |
|------|------|------|
| CUDA Toolkit | 闭源 | https://developer.nvidia.com/cuda-downloads |
| CUDA Samples | 开源（BSD-3） | https://github.com/NVIDIA/cuda-samples |
| NVIDIA 开源库 | 部分开源 | 如 Thrust（Apache 2.0）、CUB（BSD） |
| cuDNN | 闭源 | 需注册下载 |
| TensorRT | 闭源 | 免费使用 |

> 结论：你不能开源 `nvcc` 编译器，但可以开源所有用 CUDA 写的代码。

### 3. 合法开源 CUDA 代码的 3 种方式

#### 方式 1：纯源码发布（推荐）
```cuda
// kernel.cu（MIT 许可证）
__global__ void vecAdd(float *a, float *b, float *c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];
}
```
- 用户自行安装 CUDA Toolkit 编译
- 常见于 GitHub 项目（如 MiniOB GPU 加速）

#### 方式 2：提供 CMake + CUDA 支持
```cmake
# CMakeLists.txt
find_package(CUDA REQUIRED)
cuda_add_executable(myapp main.cu)
```
- 自动检测 CUDA，跨平台

#### 方式 3：用 HIP/SYCL 写“可移植”开源代码
```cpp
// vec_add.hip.cpp（HIP = CUDA 语法）
__global__ void vecAdd(float *a, float *b, float *c, int n) { ... }
```
- 编译为 CUDA（NVIDIA）或 ROCm（AMD）
- 代表项目：PyTorch、TensorFlow

### 4. 真实开源 CUDA 项目（2025 热门）

| 项目 | 语言 | 许可证 | 亮点 |
|------|------|--------|------|
| Thrust | C++ | Apache 2.0 | STL-like 并行算法 |
| CUB | C++ | BSD-3 | 基础并行原语 |
| ArrayFire | C++ | BSD-3 | 高层线性代数 |
| Faiss (GPU) | C++/Python | MIT | 向量搜索（HNSW + GPU） |
| cuGraph | C++ | Apache 2.0 | 图算法 |
| RAPIDS | Python/C++ | Apache 2.0 | GPU 数据科学全栈 |

> MiniOB GPU 版（复赛方向）：可用 Faiss-GPU 实现 ANN 加速，代码 100% 开源（MIT）。

### 5. 常见误区澄清

| 误区 | 真相 |
|------|------|
| “CUDA 代码不能开源” | 错！ 你的 `.cu` 代码可以开源 |
| “必须提供预编译 `.so`” | 不需要，用户自编译 |
| “cuDNN 必须闭源” | 对，cuDNN 是闭源依赖，但你可以用 MIOpen（AMD 开源替代） |
| “开源 = 必须支持 AMD” | 不需要，可声明 “Requires NVIDIA GPU” |

### 6. 如何在GitHub开源CUDA项目（最佳实践）

```markdown
# MyAwesomeCUDA
MIT License | Requires CUDA 11.8+

## 编译
```bash
mkdir build && cd build
cmake .. -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda
make -j
```

## 依赖
- CUDA Toolkit >= 11.8
- CMake >= 3.18

## 许可证
MIT - 自由使用、修改、分发
```

### 7. 未来趋势（2025-2030）

| 趋势 | 影响 |
|------|------|
| ZLUDA（CUDA on AMD） | CUDA 代码可运行在 AMD GPU |
| SYCL 2020 | 统一异构编程标准 |
| NVIDIA 开源驱动（ Nouveau ） | 长期可能 |
| AI 编译器（如 TVM、IREE） | 屏蔽 CUDA 依赖 |

### 8. 一句话总结

> “CUDA 是闭源的锤子，但你用它钉的房子（代码）可以 100% 开源”  
> —— 合法、常见、推荐。

建议：  
写 CUDA 代码时，用 MIT/Apache 2.0 许可证，提供 `CMakeLists.txt`，声明 CUDA 版本要求 —— 你的项目就能在 GitHub 合法开源，被全球开发者复用。

如需 MiniOB + CUDA ANN 加速开源模板，我可以 3 分钟生成完整仓库结构！
