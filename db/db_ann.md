# db_ann

### ANN 集成 ann-benchmarks 指南（MiniOB 2024 复赛视角，2025 版）

ANN（Approximate Nearest Neighbor，近似最近邻搜索） 是向量数据库的核心技术，用于高效处理高维数据（如嵌入向量）的相似性检索。ann-benchmarks 是 Erik Bernhardsson 等开发的 Python 基准测试框架，用于评估各种 ANN 算法的性能（如 HNSW、FAISS、Annoy），焦点在 查询速度（QPS）、召回率（Recall）和索引大小。它不直接提供 C++ 库，而是通过 Python 包装器和 Docker 容器运行基准测试，适合比较不同实现。

在 MiniOB 2024 复赛中，集成 ann-benchmarks 是关键任务：需修改 MiniOB 支持 ANN 搜索（如 HNSW 索引），并用 ann-benchmarks 测试性能（内存 <1GB，单 CPU）。以下基于官方仓库（https://github.com/erikbern/ann-benchmarks）和复赛文档，完整指南。框架不支持直接 C++ 集成，但可复现其测试管道验证 MiniOB 的向量模块。

#### 1. ann-benchmarks 核心概念
- 数据集：预生成 HDF5 格式（如 glove-100-angular、sift-128-euclidean），包含 train/test 分割和 top-100 ground truth。维度 100-1000，适合 RAM 内测试。
- 指标：
  - Recall@K：召回率（e.g., 0.9 表示 90% 真实邻居被找回）。
  - QPS：每秒查询数。
  - Build Time/Index Size：构建时间和空间。
- 约束：单 CPU、无多线程；支持 L2（欧氏）、IP（内积）、Hamming 等距离。
- 为什么集成？复赛需用 ann-benchmarks 跑 MiniOB 的 ANN 实现，生成 plot 证明优化（如 QPS > 1000@0.95 Recall）。

#### 2. 安装与运行 ann-benchmarks
克隆仓库并安装（Python 3.8+）：

```bash
# 克隆
git clone https://github.com/erikbern/ann-benchmarks.git
cd ann-benchmarks

# 安装依赖（包括 h5py、matplotlib、Docker）
pip install -r requirements.txt

# 构建所有算法的 Docker 容器（10-30 分钟）
python install.py  # 构建 HNSW、FAISS 等

# 运行基准测试（全套可能几天；指定数据集加速）
python run.py --dataset glove-100-angular  # 运行 glove 数据集

# 生成图表
python plot.py --x-scale logit --y-scale log  # Recall vs QPS 曲线

# 生成网站（HTML 报告）
python create_website.py  # 输出到 results/ 目录
```

- 指定参数：`--test-set-size 10000 --queries 10000` 控制规模；`--seed 42` 确保可复现。
- 输出示例：生成 `results/glove-100-angular/index.html`，包含交互图（点击查看 Recall@10、Build Time）。

#### 3. 添加新索引（为 MiniOB 准备）
ann-benchmarks 通过 Python 包装器添加算法。复赛中，需为 MiniOB 的 C++ ANN 模块写 Python 桥接（e.g., 用 pybind11 暴露接口）。

1. 创建文件夹：`ann_benchmarks/algorithms/miniob/`。
2. 写 Python 包装器（`module.py`）：继承基类，实现 `fit()`、`query()`。
   ```python
   # ann_benchmarks/algorithms/miniob/module.py
   import numpy as np
   import miniob_pybind  # 假设用 pybind11 暴露 MiniOB C++ 接口

   class MiniOBIndex:
       def __init__(self, metric, kwargs):
           self.index = miniob_pybind.VectorIndex(kwargs['dimension'], metric=='angular')  # C++ HNSW

       def fit(self, X):
           for i, vec in enumerate(X):
               self.index.addVector(vec.astype(np.float32), i)  # 添加向量

       def query(self, q, k):
           return self.index.search(q.astype(np.float32), k)  # 返回 IDs

   def get_algorithm_class():
       return MiniOBIndex
   ```
3. Dockerfile：容器化 MiniOB + 依赖。
   ```dockerfile
   # Dockerfile
   FROM ubuntu:20.04
   RUN apt update && apt install -y python3-pip cmake build-essential
   COPY . /app
   WORKDIR /app
   RUN pip install pybind11 numpy h5py
   RUN mkdir build && cd build && cmake .. && make  # 编译 MiniOB
   CMD ["python", "module.py"]
   ```
4. 配置（`config.yml`）：超参数。
   ```yaml
   # config.yml
   ef_construction: 200  # HNSW 参数
   m: 16
   ```
5. 测试：运行 `python run.py --algorithms miniob`；PR 到仓库添加官方支持。

#### 4. 在 C++ 项目（如 MiniOB）中集成 ANN 并用 ann-benchmarks 测试
ann-benchmarks 不直接嵌入 C++，但复赛要求：
- C++ 侧实现 ANN：用 HNSWlib（轻量 C++ 库）建索引。
  ```cpp
  // src/storage/vector_index.h (MiniOB 示例)
  #include <hnswlib.h>
  #include <vector>

  namespace MiniOB {
  class VectorIndex {
  private:
      size_t dim_;
      hnswlib::L2Space space_;  // 或 InnerProductSpace for IP
      std::unique_ptr<hnswlib::HierarchicalNSW<float>> index_;

  public:
      VectorIndex(size_t dim) : dim_(dim), space_(dim), index_(new hnswlib::HierarchicalNSW<float>(&space_, dim, 1000000)) {}

      void AddBatch(const std::vector<float*>& vectors, const std::vector<uint32_t>& ids) {
          for (size_t i = 0; i < vectors.size(); ++i) {
              index_->addPoint(vectors[i], ids[i]);
          }
      }

      std::vector<std::pair<uint32_t, float>> Search(const float* query, size_t k) {
          return index_->searchKnn(query, k);
      }
  };
  }  // namespace MiniOB
  ```
  - 集成到 MiniOB：修改 `src/executor/execute_calc.cpp` 支持 `CALC` 命令的向量查询（解析 HDF5 数据）。

- 桥接到 Python：用 pybind11 暴露 C++ 接口（见上例）。
  ```cpp
  // bindings.cpp
  #include <pybind11/pybind11.h>
  #include <pybind11/numpy.h>
  namespace py = pybind11;

  PYBIND11_MODULE(miniob_pybind, m) {
      py::class_<MiniOB::VectorIndex>(m, "VectorIndex")
          .def(py::init<size_t>())
          .def("addVector", &MiniOB::VectorIndex::AddBatch)
          .def("search", &MiniOB::VectorIndex::Search);
  }
  ```
  编译：`cmake -DUSE_PYBIND=ON .. && make`。

- 复现基准：
  1. 用 HDF5-C++ 加载数据集（e.g., `glove-100-angular.hdf5`）。
     ```cpp
     #include <H5Cpp.h>
     // 加载 train 数据到向量，训练索引
     H5::H5File file("data.hdf5", H5F_ACC_RDONLY);
     // ... 读取 X_train, X_test
     ```
  2. 运行查询，计算 Recall vs QPS（用 chrono 计时）。
  3. 与 ann-benchmarks 结果对比：目标 QPS > FAISS @0.95 Recall。

#### 5. 复赛优化提示（2024 经验）
- 常见坑：内存超 1GB → 用 SIMD 向量化搜索；HNSW M=16, EF=200 平衡速度/精度。
- 性能目标：GloVe 数据集，Recall@10=0.95 时 QPS>500。
- 工具链：VTune 分析 C++ 热点；gprof2dot 可视化调用图。
- 资源：复赛仓库示例（https://github.com/XJCong/miniob-2024）；ann-benchmarks 论文（SISAP 2017）。

集成后，MiniOB 可跑 `python run.py --algorithms miniob`，生成报告提交。需原创代码（查重）。若需具体 HDF5 加载代码或 Docker 示例，提供更多细节！
