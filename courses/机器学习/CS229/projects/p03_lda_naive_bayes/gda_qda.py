"""L05 生成式模型：GDA（高斯判别分析）与逻辑回归的正面交锋 + QDA 对照。

知识点：GDA 闭式参数、共享协方差⟹线性边界、GDA 解与 LR 解重合（假设成立时）、
协方差不同⟹QDA 二次边界、GDA 假设被破坏时 LR 更稳（Ng & Jordan 2001 的玩具版）。
唯一第三方依赖：numpy。运行：python gda_qda.py
"""
import numpy as np
import sys
sys.path.insert(0, ".." + "/p01_linear_logistic")   # 复用 p01 的数据与 LR
from common import make_blobs_2d, add_bias          # noqa: E402
from logistic import newton_irls                    # noqa: E402


def fit_gda(X, y):
    """共享协方差的 GDA 闭式 MLE（L05 §1.2），返回 (w, b) 形式的线性打分。"""
    m = len(y)
    phi = y.mean()
    mu0 = X[y == 0].mean(0)
    mu1 = X[y == 1].mean(0)
    D = np.vstack([X[y == 0] - mu0, X[y == 1] - mu1])
    Sigma = D.T @ D / m                              # 类内合并协方差（陷阱 4 的反面教材见 qda）
    Sinv = np.linalg.inv(Sigma + 1e-9 * np.eye(X.shape[1]))
    w = Sinv @ (mu1 - mu0)
    b = -0.5 * mu1 @ Sinv @ mu1 + 0.5 * mu0 @ Sinv @ mu0 + np.log(phi / (1 - phi))
    return np.concatenate(([b], w)), Sigma   # θ=(b, w) 与 add_bias 约定一致


def predict(X, theta):
    return (add_bias(X) @ theta >= 0).astype(int)


def accuracy(X, y, theta):
    return float(np.mean(predict(X, theta) == y))


def main():
    print("场景 A：协方差相同（GDA 假设成立）——GDA 与 LR 殊途同归")
    X, y = make_blobs_2d(400, seed=7)
    theta_gda, _ = fit_gda(X, y)
    Xb = add_bias(X)
    theta_lr, _ = newton_irls(Xb, y)
    print(f"acc(GDA)={accuracy(X, y, theta_gda):.4f}  acc(LR)={accuracy(X, y, theta_lr):.4f}")
    cos = theta_gda @ theta_lr / (np.linalg.norm(theta_gda) * np.linalg.norm(theta_lr))
    print(f"θ_GDA 与 θ_LR 夹角余弦 = {cos:.5f}（≈1：同一边界；比例因子不同不影响决策面）")

    print("\n场景 B：协方差被旋转拉长（GDA 假设破产）")
    X, y = make_blobs_2d(600, seed=11, anisotropic=True)
    theta_gda, _ = fit_gda(X, y)
    theta_lr, _ = newton_irls(add_bias(X), y)
    acc_g, acc_l = accuracy(X, y, theta_gda), accuracy(X, y, theta_lr)
    # QDA：各类自估协方差（二次边界）
    mu0, mu1 = X[y == 0].mean(0), X[y == 1].mean(0)
    S0 = np.cov(X[y == 0].T) + 1e-9 * np.eye(2)
    S1 = np.cov(X[y == 1].T) + 1e-9 * np.eye(2)

    def qda_score(X):
        d0 = np.einsum("ij,jk,ik->i", X - mu0, np.linalg.inv(S0), X - mu0)
        d1 = np.einsum("ij,jk,ik->i", X - mu1, np.linalg.inv(S1), X - mu1)
        return -0.5 * d0 - 0.5 * np.log(np.linalg.det(S0)) + 0.5 * d1 + 0.5 * np.log(np.linalg.det(S1))
    acc_q = float(np.mean((qda_score(X) >= 0).astype(int) == y))
    print(f"acc(GDA/LDA)={acc_g:.4f}  acc(LR)={acc_l:.4f}  acc(QDA)={acc_q:.4f}")
    print("→ 共享假设破坏后 QDA 赢训练内误差，但 LR 靠'弱假设+优化'兜底（L05 §1.2 结论）；")
    print("  样本减半时 QDA 的 O(n²) 参数会反噬方差（陷阱：bias-variance 具体化）。")

    print("\n场景 C：小样本下 QDA vs LR（方差反噬演示）")
    for m in [40, 100, 400]:
        X, y = make_blobs_2d(m, seed=11, anisotropic=True)
        theta_gda, _ = fit_gda(X, y)
        theta_lr, _ = newton_irls(add_bias(X), y)
        Xte, yte = make_blobs_2d(2000, seed=11, anisotropic=True)   # 真值分布测试集
        print(f"  m={m:>4}  GDA acc={accuracy(Xte, yte, theta_gda):.4f}  "
              f"LR acc={accuracy(Xte, yte, theta_lr):.4f}")
    print("→ 生成式的'强假设=低方差'与判别式的'样本效率'在此显形（Ng & Jordan 2001）。")


if __name__ == "__main__":
    main()
