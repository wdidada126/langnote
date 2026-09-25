# 概念专篇：Amdahl 定律与可伸缩性度量

> 对应《Java并发编程实战》第 11 章"性能与可伸缩性"。把"为什么加线程不一定更快"从直觉变成公式，并补齐现代容量规划工具（USL）。

## 一、本章地图（专篇结构）

| 主题 | 内容 |
| --- | --- |
| Amdahl 定律 | `S(N)=1/((1-F)+F/N)`，串行比例 `F` 决定天花板 |
| Gustafson 定律 | 固定时间、放大问题规模 → 并行收益可随规模增长 |
| USL（通用可伸缩性定律） | Gunther：在 Amdahl 上叠加**一致性开销 σ** 与**竞争开销 κ**，能解释"超线性回落" |
| 度量工具 | JMH、Little 定律、利用率 U、队列长度 Q |
| 近年修正 | 虚拟线程把"阻塞 I/O"的串行部分消除 → Amdahl 的 `F` 变小 |

## 二、核心精讲

### 2.1 Amdahl 定律
- 若程序有比例 `F` 必须串行，则 N 核加速比 `S(N) = 1 / ((1-F) + F/N)`。
- 关键推论：**即使 `F` 很小，N→∞ 时 `S ≤ 1/F`**。例如 `F=5%` → 最多 20 倍，无论多少核。
- 这是第 11 章"减少锁竞争"的理论总纲：锁 = 串行部分 = 抬高 `F`。

### 2.2 Gustafson 定律（互补视角）
- Amdahl 假设"问题规模固定"；Gustafson 指出：给更多核时，人们会**跑更大的问题**——并行比例随规模上升，加速比可接近线性。
- 对并发程序设计的启示：把"串行部分"做成**与规模无关的小常数**，就能在大负载下吃满核。

### 2.3 USL（Universal Scalability Law, Gunther）
- 在 Amdahl 上加两项开销：`S(N) = N / (1 + σ(N-1) + κN(N-1))`。
  - `σ`（一致性/同步开销）：类似 Amdahl 的串行部分。
  - `κ`（竞争/争用开销，如锁冲突、缓存一致性流量）：**超线性劣化的根源**——线程越多，彼此拖后腿越严重。
- USL 能拟合真实曲线（先升、到顶、再**回落**），Amdahl 做不到这点。工业界用它做**容量规划 / 找最优并发度**。

### 2.4 度量（别拍脑袋）
- **Little 定律**：`L = λW`（系统中平均数 = 到达率 × 停留时间）——验证吞吐/延迟自洽。
- **利用率 `U` 与队列 `Q`**：高 U 下 Q 指数增长（M/M/1）→ 延迟恶化预警。
- **务必用 JMH**：JDK 8+ 微基准唯一正确工具（见 `concepts/并发测试方法论.md`）。

## 三、版本演进

- **1967 Amdahl**（IBM）：定律提出。
- **1988 Gustafson**：放宽固定规模假设。
- **1993 Gunther**：USL 论文，后成容量规划工业标准（书的 *"The Practical Performance Analyst"* / *"Guerrilla Capacity Planning"*）。
- **JDK 8 JMH**：工业级微基准。
- **JDK 21 虚拟线程**：让"阻塞 I/O"的 `F` 趋近 0（I/O 等待不占平台线程），Amdahl 对 I/O 服务的束缚大幅松绑。

## 四、经典论文 / 原始文献

- **Amdahl, "Validity of the Single Processor Approach..." (AFIPS 1967)**——定律源头。
- **Gustafson, "Reevaluating Amdahl's Law" (CACM 1988)**。
- **Gunther, "A Simple Capacity Model of Massively Parallel Transaction Systems" (CMG 1993) / "The Practical Performance Analyst"**——USL。
- **Little, "A Proof for the Queueing Formula L=λW" (Operations Research 1961)**。

## 五、工业界开源

| 项目 | Stars | 关联 |
| --- | --- | --- |
| **openjdk/jmh** | — | 微基准，量 `F`/`κ` 的唯一正确手段 |
| **async-profiler** | 11k | 量化锁竞争（`-e lock`）→ 对应 USL 的 `κ` |
| **ben-manes/caffeine** | 17.9k | 高可伸缩缓存，USL 实战：把 `κ` 打到极低 |
| **LMAX-Exchange/disruptor** | 18.5k | 消除锁 → 把 `F`/`κ` 双压低到极致 |

## 六、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "核翻倍吞吐翻倍" | Amdahl：`F>0` 时永远到不了 |
| 2 | "加线程总能更快" | USL：`κ` 让曲线**回落**，存在最优并发度 |
| 3 | "只看吞吐不看延迟" | Little 定律：高 U 下延迟先炸 |
| 4 | "虚拟线程让 Amdahl 失效" | 只消除**I/O** 的 `F`；CPU 密集仍受 Amdahl 约束 |
