"""L05 朴素贝叶斯（多项式 NB）：合成文本语料 + 拉普拉斯平滑扫描。

知识点：词袋条件独立假设、log 域累加防下溢、未见词的零概率灾难与平滑、
测试时语料外词（"the" 问题）的处理。唯一第三方依赖：numpy。运行：python naive_bayes.py
"""
import numpy as np

VOCAB = [f"w{i:03d}" for i in range(60)]        # 玩具词表，60 维词袋


def gen_corpus(n_per_class=150, vocab=VOCAB, seed=3):
    """两类文档：体育/娱乐各按自己的多项式分布采样词袋。"""
    rng = np.random.default_rng(seed)
    V = len(vocab)
    theta0 = rng.dirichlet(np.ones(V) * 0.5)     # 稀疏：少数词高频
    theta1 = rng.dirichlet(np.ones(V) * 0.5)
    docs, labels = [], []
    for k, th in enumerate([theta0, theta1]):
        for _ in range(n_per_class):
            L = rng.integers(30, 120)
            counts = rng.multinomial(L, th)
            docs.append(counts)
            labels.append(k)
    X = np.array(docs, float)
    y = np.array(labels)
    perm = rng.permutation(len(y))
    return X[perm], y[perm], (theta0, theta1)


def fit_nb(X, y, alpha=1.0):
    """多项式 NB + 拉普拉斯平滑：返回 log 先验与 log 条件概率表。"""
    log_prior, log_prob = {}, {}
    for k in np.unique(y):
        Xk = X[y == k]
        log_prior[k] = np.log(len(Xk) / len(y))
        counts = Xk.sum(0) + alpha
        log_prob[k] = np.log(counts / counts.sum())
    return log_prior, log_prob


def predict_nb(X, log_prior, log_prob, unseen_logp=None):
    """log 域打分。unseen_logp：语料外词的显式 log 概率（本语料恒 None，保留接口）。"""
    s = np.stack([log_prior[k] + X @ log_prob[k] for k in log_prior])
    return s.argmax(0), s


def holdout(X, y, alpha, seed=0):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(y))
    tr, te = idx[: len(y) * 3 // 4], idx[len(y) * 3 // 4:]
    lp, lq = fit_nb(X[tr], y[tr], alpha=alpha)
    pred, _ = predict_nb(X[te], lp, lq)
    return float(np.mean(pred == y[te]))


def main():
    X, y, thetas = gen_corpus()
    print("实验 1：平滑参数 α 扫描（train/test holdout）")
    for a in [1e-4, 1e-2, 0.1, 1.0, 5.0, 50.0]:
        print(f"  α={a:<7g} val acc={holdout(X, y, a):.4f}")
    print("→ α→0 时未见词=0 概率毁灭整条链；α 过大把两类分布抹平（欠拟合）。")

    print("\n实验 2：α=0 的零概率灾难（数值演示）")
    with np.errstate(divide="ignore"):           # 允许 log(0) = -inf 而不告警
        lp, lq = fit_nb(X, y, alpha=0.0)
    one_unseen = np.zeros(X.shape[1]); one_unseen[59] = 1   # 该词训练集从未出现
    for k in (0, 1):
        print(f"  class {k}: log p(word59|k) = {lq[k][59] if lq[k][59] > -np.inf else -np.inf}")
    # 一个含该词 1 次的文档：两类后验直接同分或随机？实际是 -inf 比较
    score0 = lp[0] + lq[0][59]
    score1 = lp[1] + lq[1][59]
    print(f"  score0={score0}, score1={score1} → argmax 退化/未定义（numpy 给 0）")
    print("→ 这就是拉普拉斯平滑存在的理由（L05 陷阱 1）。")

    print("\n实验 3：log 域 vs 直接乘积的下溢")
    doc = X[0]
    naive = np.exp(lp[0])
    for j, c in enumerate(doc):
        p = (X[y == 0].sum(0)[j] + 1) / (X[y == 0].sum() + len(VOCAB))
        naive *= p ** c
    print(f"  直接乘积={naive:.3e}   log 域={lp[0] + X[0] @ lq[0]:.3f}（exp 后同量级）")
    print("→ 长度上百的文档下 naive 冲进入 float64 反常区（CSAPP 浮点；NB 一律 log 累加）。")

    print("\n实验 4：训练样本量 vs 平滑的交互（少样本时 α 要更小？验证之）")
    for n in [8, 24, 75, 150]:
        Xs, ys, _ = gen_corpus(n_per_class=n, seed=4)
        best = max([(holdout(Xs, ys, a, seed=5), a) for a in [1e-3, 1e-2, 0.1, 1, 10]])
        print(f"  每类样本 {n:>4} → 最优 α≈{best[1]:<6g} (acc={best[0]:.4f})")


if __name__ == "__main__":
    main()
