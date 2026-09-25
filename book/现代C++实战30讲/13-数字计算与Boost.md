# 讲 23 + 讲 24｜数字计算与 Boost：你需要的「瑞士军刀」

> **一句话**：讲到第三方库，先问一句「标准库里有没有」；再问「Boost 里有没有」——过去二十年里，**绝大多数被写进标准的 C++ 特性，最早都能在 Boost 里找到原型**。

---

## 本章地图

| 节 | 来源 | 内容 | 结论 |
| --- | --- | --- | --- |
| 数值计算的现实 | 23 | BLAS/LAPACK、SIMD、多线程 | 原地造矩阵库通常是最差选择，除非你就是卖这个 |
| `std::complex` 与浮点 | 23 | 复数语义、累积误差、比较 | 数值代码的第一课是「误差不会消失」 |
| 现代线性代数库 | 23 | Eigen / Blaze / xtensor | 表达式模板带来的性能，通常接近手写汇编 |
| 高精度与任意精度 | 23 | `Boost.Multiprecision` | 需要时再引入，代价是速度 |
| Boost 全景 | 24 | 各子库定位 | Boost 不是「一个大库」，而是数十个独立子库的集合 |
| 「进了标准的那批」 | 24 | `optional`/`variant`/`shared_ptr`/`filesystem`/`asio`/`endian` | 优先用标准版本 |
| 「停更/改名/被认知为旧」的那批 | 24 | `Boost.Lambda`、`Boost.Bind` 的 derivatives、`Boost.Xpressive` | 新代码不要用旧功能，也不必维护旧代码 |
| 使用与打包 | 24 | 头文件库、编译库、版本共存 | 用包管理器锁定版本，不要直接拷贝头文件进仓库 |
| 🔧 现代补充 | 23/24 + 2026 | C++23 的 `std::expected` 与数值错误、编译期数值、`std::format` 打印数值 | 数值库的错误通道正在从异常转向返回值 |

---

## 核心精讲

> 以下均为**教学示意，不参与构建**。

### 1. 数值计算的层次：别从零开始

| 层次 | 代表 | 适合 |
| --- | --- | --- |
| 语言内建 | `std::complex`、`<cmath>` | 单变量复数、初等函数 |
| 表达式模板库 | Eigen、Blaze、xtensor | 稠密/稀疏矩阵、张量运算 |
| 成熟数值库 | LAPACK / BLAS / FFTW / GSL | 分解、特征值、积分、随机 |
| GPU / 加速 | CUDA Thrust、SYCL、cuBLAS | 数据并行的超大矩阵 |

```cpp
// 教学示意：一个典型的线性代数场景（不参与构建）
Eigen::Matrix3d A; A << 1, 2, 3, 4, 5, 6, 7, 8, 10;
Eigen::Vector3d b(1, 2, 3);
Eigen::Vector3d x = A.fullPivLu().solve(b);   // LU 分解求解：比手写高斯消元可靠得多
```

> 表达式模板（`A * B + C` 一次成型而不产生临时矩阵）是这些库快到接近手写的根本原因；代价是编译错误信息与编译时间都不友好（这也是讲 28 Concepts 的动机之一）。

### 2. 浮点数的三条常识

```cpp
// 教学示意：浮点比较与累积误差（不参与构建）
double sum = 0;
for (double x : values) sum += x;            // 顺序不同结果不同；雷诺数大的先加会更准
// if (sum == 1.0) { ... }                    // 错误：不要直接比较
if (std::abs(sum - 1.0) < 1e-9) { /* 容差比较 */ }

std::complex<double> z{1.0, 2.0};
auto w = std::sqrt(z);                        // 复数运算的选择分支（象限、0 的情况）是实现相关的细节
```

1. **浮点不是实数**：结合律不成立，求和顺序会影响结果；
2. **直接比较相等几乎总是错的**（除非是整数值的定点用法）；
3. **`long double` 不保证更大精度**（x86 上是 80 位扩展精度，ARM 上可能与 `double` 相同）。

### 3. Boost：拆开看才有用

| 类别 | 子库 | 备注 |
| --- | --- | --- |
| 已进入标准 | `shared_ptr`/`unique_ptr`、`optional`、`variant`、`tuple`/`any`、数组与 `array`、正则（`<regex>` 已弃用） | 优先用标准版本 |
| 事实标准、尚未进标准 | `Boost.Asio`、`Boost.Filesystem`、`Boost.Thread`（并入 `Boost.Context` 后另有一套）、`Boost.System`、`Boost.Endian`、`Boost.Uuid`、`Boost.Lockfree` | 新项目的主力依赖 |
| 数值与泛型 | `Boost.Multiprecision`、`Boost.Math`、`Boost.Geometry`、`Boost.MPL`/`Boost.Hana`、`Boost.Spirit` | 解析与元编程的-old-school 强项 |
| 已停更 / 弃用 | `Boost.Lambda`、`Boost.Bind` 的旧用法、`Boost.Xpressive`、`Boost.Serialization`（有替代方案但仍在维护） | 新代码不要再用；老代码建议逐步替换 |

> **发布节奏**：Boost 大体与 C++ 标准同步发布，每个大版本会带一批「已进标准的子库被移除」（例如 `boost/optional.hpp` 仍在，但基础功能已由 `std::optional` 覆盖）。这意味着：**新项目引用 Boost 时，务必确认该子库在最新版中的状态**，而不是照着五年前的教程抄。

```cpp
// 教学示意：Boost 的典型用法（不参与构建）
#include <boost/asio.hpp>                     // 网络与 IO：仍是 C++ 异步编程的旗舰之一
#include <boost/multiprecision/cpp_int.hpp>   // 任意精度整数
using bigint = boost::multiprecision::cpp_int;

bigint fact(int n) { bigint r = 1; for (int i = 2; i <= n; ++i) r *= i; return r; }
```

### 4. 依赖引入的工程纪律

| 做法 | 评价 |
| --- | --- |
| 用包管理器（vcpkg/Conan）锁定版本 | 推荐：可复现、可升级 |
| CMake `FetchContent`/CPM 拉源码 | 推荐：对头文件库尤其合适 |
| 把 `boost/` 目录整个拷贝进仓库 | 不推荐：体积大、升级困难、版本冲突难查 |
| 直接 `#include` 一个可能与标准冲突的旧 Boost 头 | 不推荐：`boost/std/...` 之外的路径在现代项目里要谨慎 |

---

## 版本演进

| 版本 | 变化 |
| --- | --- |
| 2000s | Boost 成为事实标准库集合，`shared_ptr`、`regex`、`bind` 等从这里进入 C++11 |
| C++11 | `shared_ptr`、`tuple`、`regex`、`random`、`chrono`、`system_error` 陆续入标准 |
| C++17 | `std::optional`、`string_view`、`filesystem`、`variant` 入标准；`<regex>` 的实现质量成为长期批评对象 |
| C++20 | 更多的 Boost 内容进入语言与库（Ranges、concepts 正是参考了 Boost.Range / Concept 研究） |
| **C++23** | **`std::expected` 入标准**（源自 `boost::expected` 的经验）、`std::flat_map`（思路源自 Boost.Multi-index 的容器） |
| 2026 | Boost 继续按大版本迭代，重心转向尚未标准化的部分（Asio、Geometry、Math、Hana 等） |

---

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed. | **SIAM 2002** | 数值算法误差分析的权威教材 |
| Demmel, *Applied Numerical Linear Algebra* | **SIAM 1997** | 线性代数求解器的工程视角 |
| *Boost C++ Libraries* 官方文档与《The Boost C++ Libraries》 | **Beman Dawes 主编，O'Reilly 起** | 各子库的权威说明 |
| ISO/IEC 14882，`<complex>`/`<cmath>`/`<random>` | C++ 标准 | 数值设施的正式语义（含实现相关的条款） |
| LAPACK Users' Guide | **SIAM 1999** | 数值线性代数的事实标准 |

---

## 近年研究与工业界开源实践（2015–2026）

- **「不重新发明数值库」成为共识**：几乎所有需要矩阵运算的 C++ 项目最终都在用 Eigen/Blaze 的一个子集；手写 `matmul` 很难在数值稳定性与性能上同时胜出。
- **表达式模板的编译时间代价被讨论**：Eigen 的模板展开让编译变慢、报错变长；2026 年的做法是在头文件边界上隐藏模板（用 `std::function`/PIMPL 收敛 Instantiation 面）。
- **GPU/SIMD 路径**：SYCL 与 CUDA 让「同一份数值代码跑在加速卡上」成为现实，C++ 侧的接口设计也随之收敛。
- **Boost 的分层策略**：工业项目常见做法是「只用 Boost 里那几个还没进标准的子库（Asio、Geometry、Math），进标准的那批一律换 `std::`」。
- 🔧 **数值错误通道的统一**：`std::expected` 入标准后，数值库（如解析、求根、矩阵分解）开始提供「返回 `expected` 而非抛异常」的变体，便于在禁异常的工程里使用。
- 🔧 **编译期数值计算**：`constexpr` 容器与 `consteval` 落地后，多项式展开、滤波系数表、查找表可以直接在编译期算好（本章第 3 节的 `fact` 就是最简单的例子）。

| 仓库 | star | 说明 |
| --- | --- | --- |
| `xtensor-stack/xtensor` | **3.8k★** | C++ 侧的 N 维数组与线性代数栈，配合 xtl 使用 |
| `boostorg/boost` | **8.6k★** | Boost 总仓入口（各子库在 `boostorg/` 下独立仓库） |
| `boostorg/asio` | **1.6k★** | 网络与异步 IO，讲 27 的重点之一 |
| `boostorg/multiprecision` | **265★** | 任意精度运算，讲 23 的任意精度部分 |
| `google/benchmark` | **10.4k★** | 数值内核的微基准 |
| Eigen / Blaze | **star 未核验** | Eigen 主仓在 `gitlab.com/libeigen/eigen`，Blaze 在 Bitbucket，本次 GitHub 查询为 404，故不列 star |

---

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Boost 是一个要整体引入的大库」 | 它由数十个独立子库组成；只需包含需要的那些头 |
| 2 | 「`boost::optional` 和 `std::optional` 差不多」 | 标准版本已覆盖主要用例；新代码用 `std::` |
| 3 | 「`boost::regex` 就是正则的正确答案」 | 标准库 `<regex>` 至今实现质量参差；新项目建议 `std::regex_iterator` 之外改用专用库 |
| 4 | 「手写 matmul 能追上 Eigen」 | 表达式模板 + 向量化 + 分块缓存通常胜出；除非你的内核非常专用 |
| 5 | 「浮点比较用 `abs(a-b) < eps` 就够了」 | eps 的取值依赖量级；相对误差、Ulp 比较与区间算术各有适用场景 |
| 6 | 🔧 本讲未把「选库」写成流程 | 2026 年的判断顺序应是：`std::` → 成熟的单一用途库（Eigen 等）→ Boost 里未标准化的那批 → 自己写（前三条都不满足时） |
| 7 | 🔧 未提 Boost 子库的维护状态差异 | 部分子库已停更、部分被认知为「旧」；引用前应先确认它在最新发布版里的状态，而不是照抄老教程 |
| 8 | 🔧 缺少数值结果的**验证手段** | 建议引入性质测试（如 `A·x = b` 的残差、随机输入的自反性检查），比人工核对有用得多 |

---

## 与其他章 / 其他书的联系

- **`05-异常与错误处理的现代化.md`**：`boost::system::error_code` 与 `std::error_code` 是「不用异常的错误通道」的经典实现。
- **`12-工具漫谈与构建依赖.md`**：Boost/Eigen 的引入方式正是这一章讨论的依赖管理案例。
- **`08-模板编译期多态与编译期计算.md`**：表达式模板是「模板零开销」最有力的证明，也是编译时间问题的源头。
- **`15-REST-SDK与网络应用.md`**：讲 27 的 HTTP 层与 Asio 出自同源（Boost.Asio → 标准网络库提案），可对照阅读。
- **`book/C++标准库.md`**：标准库设施的完整清单。
- **`book/ModernCMakeforC++.md`**：第三方库的 CMake 集成细节。
