"""L11 决策树（纯 numpy）：基尼/熵分裂、连续特征增量扫描、预剪枝 + CART 后剪枝。

知识点：不纯度增益贪心最大化（权重 n_v/n）、max_depth/min_samples_leaf 预剪枝、
代价复杂度剪枝 R_α(T)=R̂(T)+α·|leaves| 的自底向上塌缩、树的方差（bagging 动机）。
唯一第三方依赖：numpy。运行：python tree.py
"""
import numpy as np


def gini(p):
    return 1.0 - np.sum(p ** 2)


def entropy(p):
    p = p[p > 0]
    return -np.sum(p * np.log2(p))


CRITERION = {"gini": gini, "entropy": entropy}


class Node:
    __slots__ = ("feature", "thresh", "left", "right", "value", "counts",
                 "impurity")

    def __init__(self, feature, thresh, left, right, value, counts, impurity):
        self.feature, self.thresh, self.left, self.right = feature, thresh, left, right
        self.value, self.counts, self.impurity = value, counts, impurity


def _counts(y, classes):
    return np.array([(y == c).sum() for c in classes], float)


def _best_split(X, y, classes, crit, counts_parent):
    m = len(y)
    parent = CRITERION[crit](counts_parent / m)
    best = (None, None, 0.0)
    total = counts_parent.copy()
    for j in range(X.shape[1]):
        order = np.argsort(X[:, j], kind="stable")
        xs, ys = X[order, j], y[order]
        left = np.zeros(len(classes))
        for i in range(m - 1):
            left[classes == ys[i]] += 1
            if xs[i] == xs[i + 1]:
                continue
            nl, nr = i + 1, m - i - 1
            gl = CRITERION[crit](left / nl)
            gr = CRITERION[crit]((total - left) / nr)
            gain = parent - (nl / m) * gl - (nr / m) * gr
            if gain > best[2]:
                best = (j, (xs[i] + xs[i + 1]) / 2.0, gain)
    return best


def fit_tree(X, y, crit="gini", max_depth=6, min_samples_leaf=5):
    classes = np.unique(y)

    def rec(Xr, yr, depth):
        cnt = _counts(yr, classes)
        imp = CRITERION[crit](cnt / len(yr))
        leaf = Node(None, None, None, None, classes[np.argmax(cnt)], cnt, imp)
        if depth >= max_depth or imp == 0 or len(yr) < 2 * min_samples_leaf:
            return leaf
        j, t, gain = _best_split(Xr, yr, classes, crit, cnt)
        if j is None or gain <= 1e-12:
            return leaf
        mask = Xr[:, j] <= t
        if mask.sum() < min_samples_leaf or (~mask).sum() < min_samples_leaf:
            return leaf
        left = rec(Xr[mask], yr[mask], depth + 1)
        right = rec(Xr[~mask], yr[~mask], depth + 1)
        return Node(j, t, left, right, leaf.value, cnt, imp)

    return rec(X, y, 0)


def predict_tree(root, X):
    out = np.empty(len(X), dtype=float)
    stack = [(root, np.arange(len(X)))]
    while stack:
        nd, idx = stack.pop()
        if len(idx) == 0:
            continue
        if nd.left is None:
            out[idx] = nd.value
        else:
            mask = X[idx, nd.feature] <= nd.thresh
            stack.append((nd.left, idx[mask]))
            stack.append((nd.right, idx[~mask]))
    return out


def count_leaves(nd):
    return 1 if nd.left is None else count_leaves(nd.left) + count_leaves(nd.right)


def subtree_misclass(nd):
    """子树在自身训练样本上的误分类数：Σ_leaf (n − max count)。"""
    if nd.left is None:
        return nd.counts.sum() - nd.counts.max()
    return subtree_misclass(nd.left) + subtree_misclass(nd.right)


def prune_ccp(nd, alpha):
    """自底向上代价复杂度剪枝：塌缩成叶当且仅当
    (R̂_leaf + α) ≤ (R̂_subtree + α·leaves)。"""
    if nd.left is not None:
        nd.left = prune_ccp(nd.left, alpha)
        nd.right = prune_ccp(nd.right, alpha)
        leaves = count_leaves(nd)
        r_sub = subtree_misclass(nd)
        r_leaf = nd.counts.sum() - nd.counts.max()
        if r_leaf + alpha <= r_sub + alpha * leaves:
            return Node(None, None, None, None, nd.value, nd.counts, nd.impurity)
    return nd


def acc(nd, X, y):
    return float(np.mean(predict_tree(nd, X) == y))


def moons(n=500, seed=0):
    rng = np.random.default_rng(seed)
    t0 = rng.uniform(0, np.pi, n // 2)
    c0 = np.stack([np.cos(t0), np.sin(t0)], 1)
    t1 = rng.uniform(0, np.pi, n // 2)
    c1 = np.stack([1 - np.cos(t1), 0.5 - np.sin(t1)], 1)
    X = np.vstack([c0 + rng.normal(0, 0.15, c0.shape),
                   c1 + rng.normal(0, 0.15, c1.shape)])
    y = np.concatenate([np.zeros(n // 2), np.ones(n // 2)])
    noise = rng.normal(0, 1, (n, 2))              # 2 个纯噪声特征
    return np.hstack([X, noise]), y


def main():
    X, y = moons(500, seed=1)
    rng = np.random.default_rng(2)
    idx = rng.permutation(len(y))
    tr, va = idx[:350], idx[350:]
    print("实验 1：max_depth 预剪枝扫描")
    print("  depth  train acc  val acc  #leaves")
    for d in [1, 2, 3, 5, 8, 12]:
        t = fit_tree(X[tr], y[tr], max_depth=d)
        print(f"  {d:>5}  {acc(t, X[tr], y[tr]):>9.4f}  {acc(t, X[va], y[va]):>8.4f}"
              f"  {count_leaves(t):>7}")
    print("→ 验证 U 形；深树 train=1.0 来自'每样本一叶'（L11 §1.1）。")

    print("\n实验 2：CART 后剪枝（α 序列在验证集上选）")
    full = fit_tree(X[tr], y[tr], max_depth=12)
    print("    α      train     val    #leaves")
    for alpha in [0.0, 0.2, 0.5, 1.0, 2.0, 5.0]:
        t = prune_ccp(full, alpha)
        print(f"  {alpha:>5.1f}  {acc(t, X[tr], y[tr]):.4f}  {acc(t, X[va], y[va]):.4f}"
              f"  {count_leaves(t):>7}")
    print("→ α 是结构风险系数（L09 语言）：每片叶按 α 收'复杂度税'。")

    print("\n实验 3：熵 vs 基尼")
    for crit in ["gini", "entropy"]:
        t = fit_tree(X[tr], y[tr], crit=crit, max_depth=6)
        print(f"  {crit:<8} val acc={acc(t, X[va], y[va]):.4f} #leaves={count_leaves(t)}")

    print("\n实验 4：高方差展示——5 个抽样子集的叶子数（同深度限）")
    sizes = []
    for s in range(5):
        sub = np.random.default_rng(100 + s).choice(len(y), 300, replace=False)
        t = fit_tree(X[sub], y[sub], max_depth=4)
        sizes.append(count_leaves(t))
    print(f"  leaves={sizes} → 结构剧烈摇摆 = bagging/森林的治疗对象（L12）。")


if __name__ == "__main__":
    main()
