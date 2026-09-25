# p03 LDA/GDA vs 朴素贝叶斯（L05）

## 讲次与知识点
- **L05** 生成式学习算法：GDA 闭式 MLE、共享协方差⟹线性边界、LDA/QDA、朴素贝叶斯与拉普拉斯平滑、log 域防下溢
- 与 **L03** 逻辑回归对拍（GDA≡LR 在假设成立时；假设破坏时的对照实验）

## 文件
| 文件 | 内容 |
| --- | --- |
| `gda_qda.py` | 场景 A/B/C：同协方差（GDA=LR）、异协方差（QDA 胜出）、小样本方差反噬 |
| `naive_bayes.py` | 合成词袋语料：α 平滑扫描、零概率灾难、log 下溢、样本量×平滑交互 |

## 运行
```
bash run.sh          # Windows: run.bat
python gda_qda.py
python naive_bayes.py
```
依赖：**numpy（唯一第三方依赖）**。`gda_qda.py` 通过 `sys.path` 复用 p01 的
`common.make_blobs_2d` 与 `logistic.newton_irls`（跨项目复用，均为本仓库代码）。

## 观察点
1. 场景 A 的夹角余弦≈0.9999x：两条完全不同的学习路线给出同一边界（L05 §1.2 核心结论）。
2. 场景 B/C：QDA 何时赢、何时因 O(n²) 参数输掉方差（偏差-方差具体化，L09 语言）。
3. 实验 2：α=0 时单个未见词让两类打分同为 −inf——argmax 未定义（L05 陷阱 1）。

## 可扩展实验
- 把共享协方差换成"对角协方差"（= 高斯版 NB），观察 NB 与 GDA 的谱系位置；
- 用真实小语料（如 20newsgroups 两类的词频矩阵，自行离线导出为 .npy）复现实验 1。
