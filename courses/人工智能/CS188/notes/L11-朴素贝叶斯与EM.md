# L11 朴素贝叶斯与最大似然；EM 入门

> 对应 AIMA Ch.14.6, 19（Klein "Naive Bayes / EM" 讲义）。从"用 BN"跨到"学 BN"。

## 1. 核心概念

- **参数学习（MLE）**：给定结构与数据，估 CPT。频率估计 P̂(+|pa) = count(+,pa)/count(pa)；
  - **拉普拉斯平滑**：(count+1)/(count+|X|)——防零概率（对小样本/罕见父配置是救命稻草）；推广到 add-k。
- **朴素贝叶斯分类器**：星型 BN（类 C → 特征 F_i 条件独立）：
  - P(c|f₁…f_n) ∝ P(c)·Π_i P(f_i|c)。分类只需比较不同 c 的右侧乘积（取 log 防下溢）。
  - 独立假设"错得离谱却好用"：分类只需要排序对，不需要概率准（与 LR 的对偶关系）。
  - 多项事件模型（词袋）vs 伯努利事件模型（词出现与否）。
- **最大似然视角**：MLE = argmax_θ Σ log P(x_i|θ)；对指数族等价于最小化 KL(P_data‖P_θ)。
- **EM（期望最大化）**（Dempster 1977）：隐变量 Z 使似然不可分解时：
  - E 步：用当前 θ 算后验 P(z|x;θ_old)；M 步：以"完全数据"期望对数似然做 MLE。
  - 保证似然单调不减（Jensen 不等式），只到局部最优；经典应用：混合模型、HMM 参数（Baum-Welch）、缺失数据。

## 2. 关键公式

```
Naive Bayes:  argmax_c  log P(c) + Σ_i log P(f_i|c)
Laplace:      P̂(x_i|pa) = (N(x_i,pa)+k) / (N(pa)+k·|Dom(X_i)|)
EM:  θ^{t+1} = argmax_θ  Σ_{x,z} P(z|x;θ^t) · log P(x,z;θ)
```

## 3. 直觉例子

- 垃圾邮件：P(spam)·Π P(word|spam)，"free/lottery" 权重爆炸；平滑处理未见词。
- EM 猜硬币：两枚硬币不知谁抛的，先随机分工（E 步软指派）→ 重估各自正面率（M 步）→ 迭代收敛；"先猜再修正，用期望补全数据"。

## 4. 前后讲联系

- 前承 L09-L10（朴素贝叶斯是最简 BN；EM 的 E 步要跑一次 L10 推断）；后接 L17（HMM 学习用 Baum-Welch=EM）、L19（感知机=另一种参数学习，判别式）、L13（RL 中的 soft-EM/policy expectation）。
- 与 L12 并列：本课"学习"三部曲（监督 L11/L19-20、强化 L13-14、无监督 EM）。

## 5. 跨课程联系

- **CS229**：NB 是生成式模型代表，LR 判别式对照表（CS229 作业第一题的经典问题"何时 NB 渐近优于 LR"——Ng & Jordan 2001）。
- **CS231n**：softmax 分类 loss = LR 的多类推广；NB 可看作特征条件独立下的 softmax。
- **DDCA**：片上学习（类比学习/comparison 学习）是 NB 式计数器的硬件实现——存计数字节而非权重浮点。

## 6. 开源项目应用

- **scikit-learn**：`GaussianNB/MultinomialNB` 垃圾邮件教程是标准入门。
- **pgmpy `ParameterEstimator`**：MLE/Bayesian/EM 三接口对 BN 参数学习。
- **probbayes / EM-Mahout**：分布式 EM（Hadoop 时代经典，与 MIT6.824 精神相通）。

## 7. 延伸阅读

- AIMA 4e §14.6, §19.1-19.3, §21.2；CS188 Note "EM / Naive Bayes"。
- Dempster, Laird, Rubin "Maximum Likelihood from Incomplete Data" (1977)；McCallum & Nigam "A Comparison of Event Models for NB" (1998)；Ng & Jordan "On Discriminative vs Generative" (2001)。
