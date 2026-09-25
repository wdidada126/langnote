"""P1 · 图像分类器完整管线（对应 L01-L04 / 作业 A1 的 numpy 玩具版）。

流程：合成数据 → 预处理/三分 → kNN 交叉验证 → 梯度检查 →
softmax/SVM 小网格调参（只看 val）→ 测试集终报。
"""
import time
import numpy as np

import data
import knn
import softmax as sm
import svm as sv
import gradient_check as gc


def main(seed=0):
    print("== P1: 合成图像分类管线 (kNN / SVM / softmax) ==")
    X, y = data.make_blobs(n_samples=1200, n_features=192, centers=4, seed=seed)
    (Xtr, ytr), (Xva, yva), (Xte, yte) = data.split_data(X, y, seed=seed)
    Xtr, Xva, Xte = data.preprocess(Xtr, Xva, Xte, scale=True)
    Xtr, Xva, Xte = (data.add_bias_column(A) for A in (Xtr, Xva, Xte))
    D, K = Xtr.shape[1], int(y.max()) + 1
    print(f"train/val/test = {len(ytr)}/{len(yva)}/{len(yte)}   dim={D} 类数={K}")

    # ---- 1) kNN 基线：k 与距离度量在验证集上选 ----
    print("\n-- kNN --")
    clf = knn.KNearestNeighbor()
    clf.fit(Xtr, ytr)
    t0 = time.time()
    (metric, k), va_acc, _ = clf.cross_validate(Xva, yva, k_range=(1, 3, 5, 9, 15))
    print(f"best k={k} metric={metric} val acc={va_acc:.4f} "
          f"(搜索耗时 {time.time()-t0:.2f}s，每次预测 O(N·D))")
    print(f"kNN test acc = {data.accuracy(clf.predict(Xte, k=k, metric=metric), yte, is_pred=True):.4f}")

    # ---- 2) 梯度检查（L03：make it right）----
    print("\n-- gradient check --")
    rng = np.random.default_rng(7)
    Xc, yc = Xtr[:40], ytr[:40]
    sm_model = sm.LinearSoftmax(D, K, l2=1e-4)
    gc.gradient_check(sm_model, Xc, yc, label="softmax (expect OK)")
    # hinge 在间隔边界上不可微，误差量级仅作参考
    svm_model = sv.LinearSVM(D, K, l2=1e-4)
    gc.gradient_check(svm_model, Xc, yc, label="svm hinge (subgrad)")
    loop_g = svm_model.loss_grad_loop(Xc, yc)[1]
    vec_g = svm_model.loss_grad(Xc, yc)[1]
    print(f"[loop-vs-vector] svm max diff = {np.abs(loop_g - vec_g).max():.2e}")

    # ---- 3) 小网格调参：lr × λ，只看 val ----
    print("\n-- softmax SGD 网格搜索（val）--")
    best = None
    for lr in (0.05, 0.2, 0.8):
        for l2 in (1e-6, 1e-4, 1e-2):
            m = sm.LinearSoftmax(D, K, l2=l2)
            m.fit(Xtr, ytr, lr=lr, epochs=300, verbose_every=0)
            a = m.score(Xva, yva)
            print(f"lr={lr:<4} l2={l2:<6} val={a:.4f}")
            if best is None or a > best[0]:
                best = (a, lr, l2, m)
    print("\n-- SVM 小梯度下降网格搜索（val）--")
    best_s = None
    for lr in (5e-3, 2e-2, 1e-1):
        for l2 in (1e-6, 1e-4, 1e-2):
            m = sv.LinearSVM(D, K, l2=l2)
            m.fit(Xtr, ytr, lr=lr, epochs=300, verbose_every=0)
            a = m.score(Xva, yva)
            print(f"lr={lr:<6} l2={l2:<6} val={a:.4f}")
            if best_s is None or a > best_s[0]:
                best_s = (a, lr, l2, m)

    # ---- 4) 终报：测试集只碰这一次（L01/L02 纪律）----
    print("\n== 最终测试（test 仅评估一次）==")
    t0 = time.time()
    print(f"softmax  test acc = {best[3].score(Xte, yte):.4f} "
          f"(最优配置 lr={best[1]}, l2={best[2]})")
    print(f"SVM      test acc = {best_s[3].score(Xte, yte):.4f} "
          f"(最优配置 lr={best_s[1]}, l2={best_s[2]})")
    print(f"线性分类器训练+推断总耗时 {time.time()-t0:.2f}s，对比 kNN 的每次 O(N·D)")
    print("完成。下一步：L04 把 W 换成两层 MLP（见 notes/L04.md）。")


if __name__ == "__main__":
    main()
