# L17 隐马尔可夫模型 HMM：滤波、平滑、Viterbi

> 对应 AIMA Ch.15.4；Klein 讲义 "HMMs / Filtering & Smoothing"。官方 P5（Sense/Pursue）主题。

## 1. 核心概念

- **结构**：隐状态 X_t → 观测 Y_t（发射）；X_{t-1} → X_t（转移）。两假设：马尔可夫（转移只看前一步）+ 观测条件独立。
  - 参数三件套：初始分布 π₀、转移矩阵 A、发射矩阵 B。
- **滤波（filtering）**：P(X_t | y_{1:t})——"现在鬼在哪"；
  - **前向递推**：O(T·S²)，朴素重枚举是 O(T·S^T)。
- **预测**：P(X_{t+1}|y_{1:t})（滤波前移一步）；**证据更新**：乘 B(y_t|x) 再归一。
- **平滑（smoothing）**：P(X_t | y_{1:T})——离线利用未来信息，前向后向两遍。
- **Viterbi**：argmax_x_{1:T} P(x_{1:T}|y_{1:T})——最大概率**路径**（注意与逐点滤波 MAP 不同，可能路径不一致！取 max 换成 sum 就退回滤波）。
- **HMM 学习**：Baum-Welch = EM（L11 的应用）。

## 2. 关键伪码

```
# 滤波
b_t(x) ∝ B(y_t|x) Σ_x' A[x',x] b_{t-1}(x')
# Viterbi（DP）
δ_1(x)=π0(x)B(y1|x); δ_t(x)=B(yt|x)·max_{x'}[δ_{t-1}(x')A[x',x]]
回溯指针 argmax 得最优路径；把 max→sum 即前向算法 P(y_{1:t})
```

## 3. 直觉例子

- **海盗宝藏地图**（Klein 例）：隐状态=是否下雨/是否有宝藏，观测=商人是否撑伞——从伞的序列推断天气与位置。
- 2 状态 HMM 手推（本讲课堂计算）：P(Rain_t|umbrella_{1:t}) 三步迭代即收敛到稳态，展示递归滤波"无限数据有限内存"。
- 语音识别：音素=隐状态，频谱帧=观测，Viterbi 解码出最可能词序列（历史主角级应用）。

## 4. 前后讲联系

- 前承 L09-L10（HMM = 展开成时间片的 BN，VE 在链上跑 = 前向递推）、L12（转移矩阵 A = MDP 的 T 固定策略特例）；后接 L18（粒子滤波：HMM 大了/非线性时蒙特卡洛版滤波）、DBN/L20（RNN≈可微 HMM 推广）。
- Viterbi 与 L07 树上 DP、L12 值迭代同属"最优子结构 + 记忆化"家族。

## 5. 跨课程联系

- **6.006**：Viterbi = 加权 DAG 最长路 DP 的逐层版本；编辑距离/拼写纠正（Norvig 例）是 2-state 通道模型。
- **CS229**：HMM（生成式，状态马尔可夫）vs CRF（判别式，可全局特征）——CS229 结构化预测一讲的正反两面。
- **CS231n**：CTC 损失 = 对路径求和的 HMM 前向；视频目标跟踪 DeepSORT 的卡尔曼滤波 = 高斯线性 HMM。
- **DDCA**：Viterbi 解码器有硬件实现（LDPC/卷积码基带芯片），DP 流水化 + 加比选单元阵列——"算法到硅"的经典样本。
- **MIT6.824**：时钟同步/故障探测器对系统状态（up/down）的推断就是 HMM 滤波的工程化（Gray-coded 状态机版本）。

## 6. 开源项目应用

- **pomegranate**：`HiddenMarkovModel`（含 Viterbi、Baum-Welch），API 与本课记号几乎一致。
- **hmmlearn**（sklearn 系）、**seqhmm**（Rust，生物信息快）。
- **Biopython/GeneMark**：基因预测（HMM 成名地）。
- 项目实战：`projects/bayes` 扩展题 + 官方 Pacman P5（滤波驱动幽灵追踪）。

## 7. 延伸阅读

- AIMA 4e §15.4；CS188 Note "HMMs"；Rabiner "A Tutorial on HMMs" (1989)——领域引用最高的入门文献。
- Jurafsky & Martin §4（语音/POS 的 HMM→历史）；Baum-Welch (1966 技术报告)。
