# 项目 6：bayes —— 贝叶斯网络三种推断（`bayes_inference.py`）

## 对应讲次

- **L09 贝叶斯网络表示**、**L10 贝叶斯推断**；对照 **L07**（VE=bucket elimination）、**L18**（采样路线起点）。

## 模型与算法

经典 **Burglary-Alarm 网络**（5 个布尔变量，CPT 取自 AIMA）：查询 P(B | J, M)。

| 组件 | 说明 |
| --- | --- |
| `Factor` | 因子：变量元组 + 赋值表；`restrict/multiply/sum_out` 三个原语 |
| `enumerate_query` | 全联合枚举（2^5 原子逐条相乘）——展示 O(2^n) 的原罪 |
| `variable_elimination` | 先代入证据再按序消元；打印两种消元序与最大因子条目 |
| `likelihood_weighting` | 拓扑序采样 + 证据条件概率加权，2 万样本蒙特卡洛 |

输出：三法结果对照（枚举=VE 精确一致 assert 校验，LW 接近）、罕见证据下 LW 有效样本退化演示。

## 运行方式

```bash
cd projects/bayes
python3 bayes_inference.py     # 或 ./run.sh / run.bat（含 py_compile 自检）
```

## 思考题

1. 手动加一个变量 X 全连接进网络，枚举与 VE 的时间分别涨多少？体会"稀疏即免费午餐"。
2. 交换消元序使某因子含 4 个变量，观察最大因子条目——树宽即复杂度（L07 呼应）。
3. 把 LW 换成拒绝采样，计算命中率的期望——为什么 LW 更快、粒子滤波（L18）又要怎样改进 LW？

## 延伸阅读

- notes/L09/L10；pgmpy `VariableElimination` 跑同网对照数值；Cooper 1990（推断 NP-hard，papers/papers.md）。
