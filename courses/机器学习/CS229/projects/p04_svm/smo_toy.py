"""L06-L07 路线二：简化 SMO——在核上直接解 SVM 对偶 QP（玩具规模）。

对偶：max_α Σα − ½ ΣΣ α_iα_j y_iy_j K_ij，s.t. 0≤α≤C, Σα_i y_i=0。
每轮选一个违反 KKT 的 i，再解析求解"一对 (i,j)"的二维子问题
（Platt SMO 的最小可教学版：L/H 盒约束 + η<0 曲率检查 + b 双规则更新）。
复杂度标注：朴素成对扫描 O(m²)/违例点 × 子问题 O(m)，故 m≲150 可用；
真实 SMO 训练总代价 O(m²·n)~O(m³)（L07 §1.4），测试 O(#SV)。
唯一第三方依赖：numpy。运行：python smo_toy.py
"""
import numpy as np


def two_moons(n=140, seed=0):
    rng = np.random.default_rng(seed)
    t0 = rng.uniform(0, np.pi, n // 2)
    c0 = np.stack([np.cos(t0), np.sin(t0)], 1) + [-0.5, -0.3]
    t1 = rng.uniform(0, np.pi, n // 2)
    c1 = np.stack([1 - np.cos(t1), 1 - np.sin(t1)], 1) + [0.5, 0.3]
    X = np.vstack([c0 + rng.normal(0, 0.15, c0.shape),
                   c1 + rng.normal(0, 0.15, c1.shape)])
    y = np.concatenate([-np.ones(n // 2), np.ones(n // 2)])
    return X, y


def gram(X, kind="rbf", gamma=1.0, coef0=1.0, degree=3):
    sq = np.sum(X ** 2, 1)
    if kind == "linear":
        return X @ X.T
    if kind == "rbf":
        d2 = np.maximum(sq[:, None] + sq[None] - 2 * X @ X.T, 0)
        return np.exp(-gamma * d2)
    if kind == "poly":
        return (X @ X.T + coef0) ** degree
    raise ValueError(kind)


def gram_pair(X, Z, kind, gamma, coef0=1.0, degree=3):
    if kind == "linear":
        return Z @ X.T
    if kind == "rbf":
        d2 = np.maximum(np.sum(Z ** 2, 1)[:, None] + np.sum(X ** 2, 1)[None]
                        - 2 * Z @ X.T, 0)
        return np.exp(-gamma * d2)
    return (Z @ X.T + coef0) ** degree


class ToySVM:
    def __init__(self, X, y, C=1.0, kind="rbf", gamma=1.0, tol=1e-3):
        self.X, self.y, self.C, self.kind, self.gamma = X, y, C, kind, gamma
        self.K = gram(X, kind, gamma)
        self.alpha = np.zeros(len(y))
        self.b = 0.0
        self.tol = tol

    def _f(self):
        return self.K @ (self.alpha * self.y) + self.b

    def solve(self, max_passes=100):
        y, C, K, a = self.y, self.C, self.K, self.alpha
        m = len(y)
        passes, examined = 0, 0
        while passes < max_passes:
            changed = 0
            for i in range(m):
                fvec = self._f()
                Ei = fvec[i] - y[i]
                vii = (y[i] * Ei < -self.tol and a[i] < C) or \
                      (y[i] * Ei > self.tol and a[i] > 0)
                if not vii:
                    continue
                examined += 1
                best = None
                E = fvec - y                             # 全部误差一次算好
                for j in range(m):                       # 选 |Ei−Ej| 最大的 j（二阶启发式）
                    if j == i:
                        continue
                    score = abs(Ei - E[j])
                    if best is None or score > best[0]:
                        best = (score, j, E[j])
                if best is None:
                    continue
                _, j, Ej = best
                if y[i] == y[j]:
                    L, H = max(0, a[i] + a[j] - C), min(C, a[i] + a[j])
                else:
                    L, H = max(0, a[j] - a[i]), min(C, C + a[j] - a[i])
                if L >= H:
                    continue
                eta = 2 * K[i, j] - K[i, i] - K[j, j]
                if eta >= 0:                          # 子问题不严格凸：跳过
                    continue
                aj_old, ai_old = a[j], a[i]
                a[j] = np.clip(aj_old + y[j] * (Ei - Ej) / eta, L, H)
                if abs(a[j] - aj_old) < 1e-9:
                    continue
                a[i] = ai_old + y[i] * y[j] * (aj_old - a[j])   # 保持 Σαy=0
                self._update_b(i, j, aj_old, ai_old)
                changed += 1
            passes += 1 if changed == 0 else 0        # 全轮零更新才计"稳定一轮"
            if changed == 0 and passes >= 3:
                break
        return self

    def _update_b(self, i, j, aj_old, ai_old):
        y, K, a = self.y, self.K, self.alpha
        # b 候选：对更新后仍处 (0,C) 开区间的 α 用等式 y_i = w·x_i + b 解出
        wsum = (a * y) @ K                            # Σ α_k y_k K_·k（不含常数项）
        cands = []
        for t in (i, j):
            if 0 < a[t] < self.C:
                cands.append(y[t] - wsum[t])          # b = y_t − Σα y K
        if len(cands) == 2:
            self.b = float(np.mean(cands))            # 数值上取平均更稳（L07 §1.3）
        elif len(cands) == 1:
            self.b = float(cands[0])
        # 两侧都触界时保留旧 b

    def n_sv(self):
        return int((self.alpha > 1e-6).sum()), int((self.alpha > self.C - 1e-6).sum())

    def predict(self, Xz):
        Kz = gram_pair(self.X, Xz, self.kind, self.gamma)
        return np.sign(Kz @ (self.alpha * self.y) + self.b)


def dual_objective(m):
    a = m.alpha
    return float(a.sum() - 0.5 * (a * m.y) @ m.K @ (a * m.y))


def main():
    rng = np.random.default_rng(0)
    X, y = two_moons(140, seed=1)
    mu, sd = X.mean(0), X.std(0)
    X = (X - mu) / sd                                 # L06 陷阱 2
    idx = rng.permutation(len(y))
    tr, te = idx[:100], idx[100:]
    print("核/C 扫描（对偶玩具 SMO；m=100，KKT 容差 1e-3）")
    for kind, C, gamma in [("linear", 1.0, 0.0), ("linear", 10.0, 0.0),
                           ("rbf", 1.0, 2.0), ("rbf", 5.0, 2.0), ("poly", 1.0, 0.0)]:
        m = ToySVM(X[tr], y[tr], C=C, kind=kind, gamma=max(gamma, 1e-9))
        m.solve()
        nsv, nsvC = m.n_sv()
        acc_tr = np.mean(m.predict(X[tr]) == y[tr])
        acc_te = np.mean(m.predict(X[te]) == y[te])
        print(f"  {kind:<6} C={C:<5} γ={gamma:<3} #SV={nsv:>3}(触顶 {nsvC:>3}) "
              f"train={acc_tr:.3f} test={acc_te:.3f} b={m.b:+.3f} "
              f"dualObj={dual_objective(m):.2f}")
    print("→ 解读：linear 在双月数据上欠拟合（边界必须弯）；rbf/poly 上升；")
    print("  #SV 触顶(=C) 者即违例点（L07 §1.3 三种角色）；dualObj 随 C 增大而增大。")
    print("→ 验证练习：KKT 残差 |y_i·f_i−1| 对 0<α<C 的支持向量应 ≈0。")


if __name__ == "__main__":
    main()
