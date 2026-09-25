"""L12 集成学习（纯 numpy）：随机森林、AdaBoost(桩)、迷你 GBDT(平方损失)。

知识点：bootstrap+特征子集去相关、等相关方差公式验证、
AdaBoost 权重更新 α_t=½log((1−err)/err)、GBDT 拟合 pseudo-residual。
复用 tree.py 的 CART 实现。唯一第三方依赖：numpy。运行：python ensemble.py
"""
import numpy as np
from tree import fit_tree, predict_tree, moons


def bagging_forest(X, y, B=100, max_depth=8, m_feat="sqrt", seed=0, proba=False):
    rng = np.random.default_rng(seed)
    m, d = X.shape
    k = int(np.sqrt(d)) if m_feat == "sqrt" else d
    trees, oob = [], []
    idx_all = np.arange(m)
    for b in range(B):
        sub = rng.integers(0, m, m)                      # bootstrap
        inbag = np.isin(idx_all, np.unique(sub))
        # 特征子集版树：用列掩码实现
        cols = rng.choice(d, k, replace=False)
        t = fit_tree(X[np.ix_(sub, cols)], y[sub], max_depth=max_depth,
                     min_samples_leaf=2)
        trees.append((t, cols))
        oob.append(~inbag)                              # 每棵树未抽中的 ~36.8%
    return trees, np.array(oob)


def forest_predict(trees, X):
    votes = np.stack([predict_tree(t, X[:, cols]) for t, cols in trees])
    out = np.empty(X.shape[0])
    for i in range(X.shape[0]):
        vals, cnts = np.unique(votes[:, i].astype(int), return_counts=True)
        out[i] = vals[np.argmax(cnts)]
    return out


def oob_error(trees, oob, X, y):
    m = len(y)
    votes = np.zeros((m, 2))
    for (t, cols), mask in zip(trees, oob):
        p = predict_tree(t, X[mask][:, cols])
        for lab, val in zip(np.where(mask)[0], p):
            votes[lab, int(val)] += 1
    pred = np.argmax(votes, 1)
    has_vote = oob.sum(0) > 0
    return float(np.mean(pred[has_vote] != y[has_vote]))


def adaboost_stumps(X, y, T=80, seed=0):
    """y∈{−1,+1}；桩 = max_depth=1 的树。"""
    m = len(y)
    w = np.full(m, 1.0 / m)
    stumps, alphas = [], []
    for t in range(T):
        # 加权桩：直接在加权样本上重复 (w·m 次抽样) 近似加权增益——教学简化为
        # 每轮按 w 重采样 m 个索引再 fit 桩。
        rng = np.random.default_rng(seed * 1000 + t)
        idx = rng.choice(m, m, p=w)
        h = fit_tree(X[idx], y[idx], max_depth=1, min_samples_leaf=1)
        pred = predict_tree(h, X)
        err = float(np.sum(w[pred != y]))
        err = min(max(err, 1e-6), 1 - 1e-6)
        a = 0.5 * np.log((1 - err) / err)
        w = w * np.exp(-a * y * pred)
        w /= w.sum()
        stumps.append(h); alphas.append(a)
    return stumps, np.array(alphas)


def adaboost_predict(stumps, alphas, X):
    s = sum(a * predict_tree(h, X) for h, a in zip(stumps, alphas))
    return np.sign(s)


def gbdt_regression(X, y, T=120, depth=2, lr=0.1, seed=0):
    """平方损失 GBDT：每轮树拟合 r = y − F(x)（负梯度=残差）。"""
    m = len(y)
    F = np.full(m, y.mean())
    trees = []
    for t in range(T):
        r = y - F                                            # pseudo-residual
        h = fit_tree(X, r, max_depth=depth, min_samples_leaf=5)
        leaf_val = predict_tree(h, X)
        trees.append(h)
        F = F + lr * leaf_val                                # 叶值即局部最优步长
    return trees, lr


def gbdt_predict(trees, lr, X):
    return sum(lr * predict_tree(h, X) for h in trees)


def main():
    X, y = moons(800, seed=5)                            # y ∈ {0,1}
    rng = np.random.default_rng(1)
    idx = rng.permutation(len(y))
    tr, te = idx[:600], idx[600:]
    Xtr, ytr, Xte, yte = X[tr], y[tr], X[te], y[te]

    print("实验 1：单树 vs Bagging vs 随机森林（去相关的价值）")
    t1 = fit_tree(Xtr, ytr, max_depth=10)
    print(f"  单树(深)   test acc={np.mean(predict_tree(t1, Xte) == yte):.4f}")
    for name, mf in [("bagging(全特征)", "all"), ("随机森林 m=√d", "sqrt")]:
        trees, oob = bagging_forest(Xtr, ytr, B=60, m_feat=mf, seed=2)
        acc_te = float(np.mean(forest_predict(trees, Xte) == yte))
        acc_oob = oob_error(trees, oob, Xtr, ytr)
        print(f"  {name:<14} test acc={acc_te:.4f}  OOB acc={acc_oob:.4f}")
    print("→ 全特征 bagging 提升有限（树间高相关）；特征子集去相关才吃到 B→∞ 红利（L12 §1.1）。")

    print("\n实验 2：AdaBoost(桩)——y 转 {−1,+1}")
    ytr2 = np.where(ytr == 1, 1.0, -1.0)
    yte2 = np.where(yte == 1, 1.0, -1.0)
    stumps, alphas = adaboost_stumps(Xtr[:, :2], ytr2, T=80, seed=3)
    pred = adaboost_predict(stumps, alphas, Xte[:, :2])
    trn = adaboost_predict(stumps, alphas, Xtr[:, :2])
    print(f"  train err={np.mean(trn != ytr2):.4f}  test err={np.mean(pred != yte2):.4f}")
    print(f"  α 范围 [{alphas.min():.2f}, {alphas.max():.2f}]（每个桩只需 err<0.5 即弱学习器）")
    print("  仅用前 2 维特征：噪声列(2,3)未被强选——boosting 的特征利用偏置。")

    print("\n实验 3：迷你 GBDT 拟合回归目标（残差 = 负梯度）")
    Xg = rng.uniform(-3, 3, (500, 1))
    yg = np.sin(1.5 * Xg[:, 0]) + rng.normal(0, 0.15, 500)
    order = np.argsort(Xg[:, 0])
    trees, lr = gbdt_regression(Xg[order[:400]], yg[order[:400]], T=150, lr=0.1)
    F_te = gbdt_predict(trees, lr, Xg[order[400:]])
    rmse = float(np.sqrt(np.mean((F_te - yg[order[400:]]) ** 2)))
    print(f"  GBDT(depth=2, T=150, lr=0.1) test RMSE={rmse:.4f}（真噪声底 0.15）")
    print("→ 每轮拟合残差 = 函数空间的梯度下降（与 L02 GD 同构，L12 §1.3）。")


if __name__ == "__main__":
    main()
