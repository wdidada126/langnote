# p05 决策树 + 集成（L11-L12，纯 numpy）

## 讲次与知识点
- **L11** 基尼/熵不纯度、连续特征增量扫描 O(n log n)、预剪枝、CART 代价复杂度后剪枝 `R_α(T)=R̂+α|T|`、树的高方差
- **L12** bootstrap 森林与 OOB、特征子集去相关（等相关方差公式实证）、AdaBoost 桩（α_t 与加权错误）、平方损失 GBDT（拟合负梯度）

## 文件
| 文件 | 内容 |
| --- | --- |
| `tree.py` | CART 全套：fit/predict/count_leaves/prune_ccp + 4 组实验 |
| `ensemble.py` | `fit_tree` 之上：随机森林、bagging 对照、AdaBoost(stumps)、迷你 GBDT |

## 运行
```
bash run.sh          # Windows: run.bat
python tree.py
python ensemble.py
```
依赖：**numpy（唯一第三方依赖）**。复杂度：单树训练 O(d·n·m·log m) 级（每列排序扫描），
森林 ×B——数据保持小规模（n≤800），与 sklearn `HistGradientBoosting` 的分箱加速对照见 notes L12。

## 观察点
1. `tree.py` 实验 2：α 序列 = 嵌套树序列；验证 acc 先升后降——L09 结构风险的树版。
2. `ensemble.py` 实验 1：全特征 bagging vs m=√d 森林的 test/OOB acc 差距，即"ρ̄ 才是 B→∞ 的天花板"。
3. AdaBoost train err→0 后 test err 仍缓降？观察 α 分布（早期大 α = 难样本被纠正后权重塌缩）。

## 可扩展实验
- 给 `fit_tree` 存类别计数实现精确增益比（C4.5）与悲观剪枝；
- 把 `gbdt_regression` 的常数步长 lr 换成 Friedman 线搜索步长（每叶最优值）；
- OOB 与 5-fold CV 的误差一致性比较（L09/L12）。
