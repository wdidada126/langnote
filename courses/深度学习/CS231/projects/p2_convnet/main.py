"""P2 · ConvNet 全流程演示入口（对应 L05-L07 / 作业 A2 的 numpy 玩具版）。

顺序：1) naive vs fast 卷积等价性；2) 端到端梯度检查；
3) BN 开关与快慢计时；4) 短训练循环（小数据、少 epoch，CPU 秒级）。
"""
import time
import numpy as np

import data
import layers as L
import gradient_check as gc
from model import SimpleConvNet


def main(seed=0):
    print("== P2: naive -> fast ConvNet (numpy) ==")

    # ---- 1) 卷积等价性（L05：同一数学，两种实现）----
    res = gc.check_conv_equivalence()
    print("[conv naive-vs-fast] " + "  ".join(f"{k}={v:.2e}" for k, v in res.items())
          + ("  OK" if max(res.values()) < 1e-10 else "  FAIL"))

    # ---- 2) 端到端梯度检查（含 BN 参数）----
    rng = np.random.default_rng(seed)
    Xc = rng.standard_normal((6, 1, 16, 16))
    yc = rng.integers(0, 3, size=6)
    m = SimpleConvNet(seed=seed)
    m.fast = False                     # 以 naive 为"黄金实现"检查
    gc.grad_check_model(m, Xc, yc)
    m.fast = True                      # fast 版梯度必须同样正确
    gc.grad_check_model(m, Xc, yc)

    # ---- 3) 快慢对比 ----
    X, y = data.make_shape_dataset(n_per_class=80, seed=seed)
    (Xtr, ytr), (Xva, yva), (Xte, yte) = data.split_data(X, y, seed=seed)
    batch = Xtr[:64]
    for fast in (False, True):
        m = SimpleConvNet(seed=0)
        m.fast = fast
        t0 = time.time()
        for _ in range(5):
            m.forward(batch, ytr[:64])
            m.backward()
        print(f"[time] {'fast ' if fast else 'naive'} 5 次前向+反向: {time.time()-t0:.2f}s")

    # ---- 4) 训练循环（L07 纪律：小 lr 起步、看 val、早停意识）----
    print("\n-- 训练 CONV-BN-RELU-POOL x2 + FC --")
    model = SimpleConvNet(seed=seed)
    model.fast = True
    lr, epochs = 0.05, 25
    N = len(ytr)
    for ep in range(epochs):
        perm = np.random.default_rng(ep).permutation(N)
        for i in range(0, N - 31, 32):
            idx = perm[i:i + 32]
            loss = model.forward(Xtr[idx], ytr[idx])
            model.backward()
            model.step(lr=lr, momentum=0.9)
        tr = model.accuracy(Xtr[:300], ytr[:300])
        va = model.accuracy(Xva, yva)
        print(f"epoch {ep+1:3d}  loss {loss:.4f}  train {tr:.3f}  val {va:.3f}")
        if va > 0.95:
            break
    # 推理模式：BN 换用 running 统计（L06 的 train/eval 差异）
    model.mode = "eval"
    print(f"\ntest acc = {model.accuracy(Xte, yte):.4f}")
    print("完成。下一步：L06 案例研究（给这个玩具加深/加残差会怎样？）")


if __name__ == "__main__":
    main()
