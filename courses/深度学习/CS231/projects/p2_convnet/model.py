"""P2 · 小型 ConvNet 与手动反传训练循环（对应 L05-L07，A2 玩具版）。

结构：CONV→BN→ReLU→POOL ×2 → FC → softmax。
手写前向/反向把 layers.py 的积木串起来——这正是 PyTorch autograd 替你做的事。
"""
import numpy as np
import layers as L


def he_init(shape, rng):
    """He 初始化（L07）：std=sqrt(2/fan_in)，ReLU 网络标配。"""
    fan_in = np.prod(shape[1:])
    return rng.standard_normal(shape) * np.sqrt(2.0 / fan_in)


class SimpleConvNet:
    def __init__(self, C=1, H=16, W=16, f1=8, f2=16, num_classes=3, seed=0):
        rng = np.random.default_rng(seed)
        self.params, self.bn_cache = {}, {}
        self.params["w1"] = he_init((f1, C, 3, 3), rng)
        self.params["b1"] = np.zeros(f1)
        self.params["g1"] = np.ones(f1)
        self.params["be1"] = np.zeros(f1)
        self.params["w2"] = he_init((f2, f1, 3, 3), rng)
        self.params["b2"] = np.zeros(f2)
        self.params["g2"] = np.ones(f2)
        self.params["be2"] = np.zeros(f2)
        H2 = (H - 2) // 2 + 1                     # pool 2x2 stride2（L05 尺寸公式）
        W2 = (W - 2) // 2 + 1
        H4, W4 = (H2 - 2) // 2 + 1, (W2 - 2) // 2 + 1
        self.flatten_dim = f2 * H4 * W4
        self.params["w3"] = he_init((self.flatten_dim, num_classes), rng)
        self.params["b3"] = np.zeros(num_classes)
        self.conv_param = {"stride": 1, "pad": 1}
        self.pool_param = {"pool_height": 2, "pool_width": 2, "stride": 2}
        self.bn_param = {"momentum": 0.9, "eps": 1e-5}
        self.mode = "train"
        self.fast = True                          # main.py 用两版对照

    # ---------------- 前向 ----------------
    def _bn(self, x, gamma, beta, key):
        if self.mode == "eval":
            r = self.bn_cache.get(key, {})
            if "mean" in r:                          # 推理：用 running 统计（L06）
                mu, var = r["mean"], r["var"]
                xh = (x - mu[None, :, None, None]) / np.sqrt(
                    var[None, :, None, None] + self.bn_param["eps"])
                return gamma[None, :, None, None] * xh + beta[None, :, None, None], None
        return L.spatial_batchnorm_forward(x, gamma, beta, self.bn_param,
                                           self.bn_cache.setdefault(key, {}))

    def forward(self, X, y=None):
        p = self.params
        conv = L.conv_forward_fast if self.fast else L.conv_forward_naive
        s1, c1 = conv(X, p["w1"], p["b1"], self.conv_param)
        n1, cn1 = self._bn(s1, p["g1"], p["be1"], "1")
        r1, cr1 = L.relu_forward(n1)
        q1, cq1 = L.max_pool_forward(r1, self.pool_param)
        s2, c2 = conv(q1, p["w2"], p["b2"], self.conv_param)
        n2, cn2 = self._bn(s2, p["g2"], p["be2"], "2")
        r2, cr2 = L.relu_forward(n2)
        q2, cq2 = L.max_pool_forward(r2, self.pool_param)
        s3, c3 = L.affine_forward(q2, p["w3"], p["b3"])
        if y is None:
            return s3
        loss, cl = L.softmax_loss_forward(s3, y)
        reg = 1e-4 * np.sum(p["w1"] ** 2 + p["w2"] ** 2 + p["w3"] ** 2)
        self.cache = (c1, cn1, cr1, cq1, c2, cn2, cr2, cq2, c3, cl)
        return loss + reg

    # ---------------- 反向（逐层链式，L04 的形状对偶律） ----------------
    def backward(self):
        p = self.params
        c1, cn1, cr1, cq1, c2, cn2, cr2, cq2, c3, cl = self.cache
        g = {k: np.zeros_like(v) for k, v in p.items()}
        ds3 = L.softmax_loss_backward(None, cl)
        dq2, g["w3"], g["b3"] = L.affine_backward(ds3, c3)
        dr2 = L.max_pool_backward(dq2, cq2)
        dn2 = L.relu_backward(dr2, cr2)
        ds2, g["g2"], g["be2"] = L.spatial_batchnorm_backward(dn2, cn2)
        if self.fast:
            dq1, g["w2"], g["b2"] = L.conv_backward_fast(ds2, c2)
        else:
            dq1, g["w2"], g["b2"] = L.conv_backward_naive(ds2, c2)
        dr1 = L.max_pool_backward(dq1, cq1)
        dn1 = L.relu_backward(dr1, cr1)
        ds1, g["g1"], g["be1"] = L.spatial_batchnorm_backward(dn1, cn1)
        if self.fast:
            _, g["w1"], g["b1"] = L.conv_backward_fast(ds1, c1)
        else:
            _, g["w1"], g["b1"] = L.conv_backward_naive(ds1, c1)
        reg = 2e-4
        for k in ("w1", "w2", "w3"):
            g[k] += reg * p[k]
        self.grads = g

    # ---------------- 训练一步（L03：SGD+momentum） ----------------
    def step(self, lr=0.05, momentum=0.9):
        if not hasattr(self, "vel"):
            self.vel = {k: np.zeros_like(v) for k, v in self.params.items()}
        for k in self.params:
            self.vel[k] = momentum * self.vel[k] - lr * self.grads[k]
            self.params[k] += self.vel[k]

    def accuracy(self, X, y):
        scores = self.forward(X)
        return float(np.mean(np.argmax(scores, axis=1) == y))
