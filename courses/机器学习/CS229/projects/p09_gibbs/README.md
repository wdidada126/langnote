# p09 HMM 精确推断 + Gibbs 采样（L19）

## 讲次与知识点
- **L19** 前向-后向（log 域 α/β、γ/ξ 责任度、缩放防下溢）、Viterbi（max-product 半环）、
  Baum-Welch = 离散 EM、Gibbs 采样（全条件分布、细致平衡、burn-in、ESS、临界慢化）
- 对接 **L16**：同一份 GMM 数据，EM（优化责任度）与 Gibbs（采样标签）双路线对照

## 文件
| 文件 | 内容 |
| --- | --- |
| `hmm.py` | 合成 HMM：log 域前向后向 + 暴力枚举核对 + Viterbi vs 平滑 + Baum-Welch 从随机初值重学参数 |
| `gibbs.py` | GMM 标签 Gibbs（z_{−i} 全条件）+ 2D Ising（β 扫描含临界点 0.4407）+ 自相关/ESS |

## 运行
```
bash run.sh          # Windows: run.bat
python hmm.py
python gibbs.py
```
依赖：**numpy（唯一第三方依赖）**。Ising 一轮 L² 次更新、Gibbs-GMM 一帧 m·k 次条件评估——
规模已控制在秒级~十秒级。

## 观察点
1. `hmm.py`：前向递推与暴力路径枚举在截断 T=6 时数值相等（动态规划正确性证书）；
   Viterbi 路径 ≠ 逐点 γ-argmax（"最可能路径"与"逐点最可能状态"是两个问题）。
2. Baum-Welch 学到似然等价类（状态排列自由）——比较参数前先做置换对齐。
3. `gibbs.py` B：β→β_c 时磁化自相关飙升、ESS 骤降——临界慢化；标签互换模式同理（L19 陷阱 4）。

## 可扩展实验
- 给 Gibbs-GMM 跑 3 条不同初始链，比较均值轨迹（Gelman-Rubin 式判敛）；
- Ising 改 Metropolis-Hastings（整网格提议翻转）对照坐标更新；
- HMM 加高斯发射 + 用 hmmlearn 交叉验证本文件参数学习结果。
