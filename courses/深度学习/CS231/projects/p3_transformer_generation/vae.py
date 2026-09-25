"""P3 · 玩具 VAE（对应 L13 1.2；A3 的 ELBO 极简版）。

    log p(x) ≥ E_{q(z|x)}[log p(x|z)] − KL(q(z|x) ‖ N(0,I))
编码器输出 μ,logσ²，解码器输出重建均值（固定方差 σ_dec²）；
重参数化 z = μ + σ⊙ε 把随机性移出计算图，反向传播照常（L04）。
2D 数据上 KL 与高斯 NLL 都有闭式，梯度全程手推。
"""
import numpy as np
from mlp import MLP


class ToyVAE:
    def __init__(self, dim=2, hz=1, hh=32, dec_std=0.4, rng=None):
        rng = rng or np.random.default_rng(0)
        self.enc = MLP([dim, hh, hh, 2 * hz], rng)       # → (mu, logvar)
        self.dec = MLP([hz, hh, hh, dim], rng)
        self.dec_std = dec_std
        self.rng = rng
        self.hz = hz
        self.vE, self.vD = {}, {}

    def elbo(self, X):
        N = X.shape[0]
        stats, ce = self.enc.forward(X)
        mu, logvar = stats[:, :self.hz], stats[:, self.hz:]
        std = np.exp(0.5 * logvar)
        eps = self.rng.standard_normal(mu.shape)
        z = mu + std * eps                               # 重参数化技巧
        xhat, cd = self.dec.forward(z)
        # 高斯 NLL（常数略）与 KL 闭式
        recon = np.sum((X - xhat) ** 2 / (2 * self.dec_std ** 2))
        kl = 0.5 * np.sum(mu ** 2 + np.exp(logvar) - logvar - 1)
        loss = (recon + kl) / N
        # ---- 梯度手推 ----
        dxhat = (xhat - X) / N / self.dec_std ** 2       # d recon / d xhat
        dz, gD = self.dec.backward(dxhat, cd)
        dmu = dz + mu / N                                # dz/dmu=1；dKL/dmu=mu/N
        dlogvar = dz * eps * 0.5 * std + (np.exp(logvar) - 1.0) / N   # dz/dlogvar=ε·σ/2
        dstats = np.concatenate([dmu, dlogvar], axis=1)
        _, gE = self.enc.backward(dstats, ce)
        self.gE, self.gD = gE, gD
        return loss, float(recon / N), float(kl / N)

    def train(self, X, iters=1500, batch=64, lr=5e-3, report_every=250):
        n = len(X)
        for it in range(iters):
            idx = self.rng.integers(0, n, batch)
            loss, rec, kl = self.elbo(X[idx])
            self.enc.update(self.gE, lr=lr, vel=self.vE)
            self.dec.update(self.gD, lr=lr, vel=self.vD)
            if (it + 1) % report_every == 0:
                print(f"iter {it+1:5d}  -ELBO {loss:8.3f}  (recon {rec:6.3f} + kl {kl:5.3f})")

    def sample(self, n=200):
        """先验采样生成：z~N(0,I) → x̂。"""
        z = self.rng.standard_normal((n, self.hz))
        x, _ = self.dec.forward(z)
        return x
