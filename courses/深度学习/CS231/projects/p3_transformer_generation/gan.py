"""P3 · 玩具 GAN（对应 L13 1.3；A3 的 2D 极简版）。

    min_G max_D  E_x[log D(x)] + E_z[log(1-D(G(z)))]
二分类判别器（softmax 头，L02）+ MLP 生成器（L04）。
D 与 G 交替更新：G 的梯度 = 冻结 D 反传到假样本像素，再穿过 G。
"""
import numpy as np
from mlp import MLP, softmax_loss_forward


class ToyGAN:
    def __init__(self, dim=2, hz=2, hh=16, rng=None):
        rng = rng or np.random.default_rng(0)
        self.G = MLP([hz, hh, hh, dim], rng)
        self.D = MLP([dim, hh, hh, 2], rng)
        self.rng = rng
        self.vG, self.vD = {}, {}

    def _d_loss(self, X, labels):
        s, c = self.D.forward(X)
        loss, dS = softmax_loss_forward(s, labels)
        return loss, dS, c

    def train(self, real, iters=3000, batch=64, lr=0.01, report_every=500):
        n_real = len(real)
        for it in range(iters):
            # ---- 1) 训练 D：真=0，假=1 ----
            xr = real[self.rng.integers(0, n_real, batch)]
            z = self.rng.standard_normal((batch, self.G.params[0]["w"].shape[0]))
            xg, _ = self.G.forward(z)
            X = np.vstack([xr, xg])
            y = np.r_[np.zeros(batch, int), np.ones(batch, int)]
            dloss, dS, cD = self._d_loss(X, y)
            _, gD = self.D.backward(dS, cD)
            self.D.update(gD, lr=lr, vel=self.vD)
            # ---- 2) 训练 G：让 D 把假样本判成真（label=0） ----
            z = self.rng.standard_normal((batch, self.G.params[0]["w"].shape[0]))
            xg, cG = self.G.forward(z)
            gloss, dSg, cD2 = self._d_loss(xg, np.zeros(batch, int))
            dxg, _ = self.D.backward(dSg, cD2)          # 冻结 D：只用其 dx 梯度
            _, gG = self.G.backward(dxg, cG)
            self.G.update(gG, lr=lr, vel=self.vG)
            if (it + 1) % report_every == 0:
                m, sd = self.mode_stats(real, xg)
                print(f"iter {it+1:5d}  Dloss {dloss:.3f} Gloss {gloss:.3f}  "
                      f"假样本均值 {np.round(m, 2)} 覆盖模式 {sd}/3")

    def mode_stats(self, real, xg):
        """模式覆盖：每个真高斯附近是否有假样本（反"模式崩溃"观察窗）。"""
        centers = np.array([[2.0, 0.0], [-1.0, 1.7], [-1.0, -1.7]])
        d = np.linalg.norm(xg[:, None] - centers[None], axis=2)
        near = (d < 1.2).any(axis=0)
        return xg.mean(axis=0), int(near.sum())
