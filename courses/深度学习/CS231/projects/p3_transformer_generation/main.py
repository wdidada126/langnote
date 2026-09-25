"""P3 · 入口：attention/ViT 梯度检查 + 玩具 GAN/VAE 训练（对应 L08/L13）。

用法：
    python main.py vit    # 注意力&LayerNorm 梯度检查 + TinyViT 训练
    python main.py gan    # 2D 三高斯 GAN
    python main.py vae    # 2D 三高斯 VAE
    python main.py all    # 依次全部运行
"""
import sys
import numpy as np

import data
import layernorm as ln
import gradient_check as gc
from attention import MultiHeadAttention
from vit import TinyViT, patchify
from gan import ToyGAN
from vae import ToyVAE


def run_vit(seed=0):
    print("== ViT: 梯度检查 + 四象限斑点图分类 ==")
    rng = np.random.default_rng(seed)
    N, T, D = 3, 5, 12
    x = rng.standard_normal((N, T, D))
    mha = MultiHeadAttention(D, 3, rng)
    gc.grad_check_callable("MHA(dx)", lambda xx: _mha_scalar(mha, xx), x,
                           lambda xx: _mha_grad(mha, xx))
    ln_p = {"g": rng.standard_normal(D) * 0.1 + 1.0, "b": rng.standard_normal(D) * 0.1}
    gc.grad_check_callable("LayerNorm(dx+g+b)", lambda z: _ln_scalar(z, ln_p), x,
                           lambda z: _ln_grad(z, ln_p))

    X, y = data.make_quad_images(n_per_class=40, seed=seed)
    (Xtr, ytr), (Xva, yva) = data.split_data(X, y, seed=seed)
    tok_tr = patchify(Xtr[:, 0], 2)
    model = TinyViT(D_in=4, Dm=24, nH=3, K=4, T=tok_tr.shape[1], rng=rng)
    N = len(ytr)
    for ep in range(30):
        perm = np.random.default_rng(ep).permutation(N)
        for i in range(0, N - 31, 32):
            idx = perm[i:i + 32]
            model.forward(tok_tr[idx], ytr[idx])
            model.backward()
            model.step(lr=0.08, momentum=0.9)
        va = model.accuracy(patchify(Xva[:, 0], 2), yva)
        if (ep + 1) % 5 == 0:
            print(f"epoch {ep+1:3d}  val acc {va:.3f}")
    print("注意：位置嵌入(pos)+注意力让模型学会'看哪个 patch'——卷积的平移不变性在此被刻意打破（L08 1.3）。")


def _mha_scalar(mha, x):
    out, _ = mha.forward(x)
    return float(np.sum(out * 0.01))


def _mha_grad(mha, x):
    out, c = mha.forward(x)
    dout = np.full_like(out, 0.01)
    dx, _ = mha.backward(dout, c)
    return dx


def _ln_scalar(z, p):
    out, _ = ln.layernorm_forward(z, p["g"], p["b"])
    return float(np.sum(out))


def _ln_grad(z, p):
    out, c = ln.layernorm_forward(z, p["g"], p["b"])
    dx, _, _ = ln.layernorm_backward(np.ones_like(out), c)
    return dx


def run_gan(seed=0):
    print("\n== GAN: 学习 2D 三高斯分布 ==")
    real, _ = data.make_two_d_data(n=500, seed=seed)
    gan = ToyGAN(rng=np.random.default_rng(seed))
    gan.train(real, iters=3000, batch=64, lr=0.01)
    print("模式覆盖 <3 → 观察到了模式崩溃/欠覆盖（L13 1.3 的头号病理）。")


def run_vae(seed=0):
    print("\n== VAE: ELBO = 重构 + KL ==")
    X, _ = data.make_two_d_data(n=800, seed=seed)
    vae = ToyVAE(hz=2, rng=np.random.default_rng(seed))
    vae.train(X, iters=1500, batch=64, lr=5e-3)
    xs = vae.sample(300)
    print(f"先验采样均值 {np.round(xs.mean(axis=0), 2)}  标准差 {np.round(xs.std(axis=0), 2)}")
    print("VAE 样本偏'糊'（回归平均），与 GAN 的锐利但易崩溃互补（L13 1.4）。")


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("vit", "all"):
        run_vit()
    if which in ("gan", "all"):
        run_gan()
    if which in ("vae", "all"):
        run_vae()
    print("\n完成。下一步：L14 扩散模型（notes/L13.md 结尾）/ 用 PyTorch 写 A3 正版本。")


if __name__ == "__main__":
    main()
