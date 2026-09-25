# -*- coding: utf-8 -*-
"""L09-L10 贝叶斯网络推断项目：枚举 / 变量消元 / 似然加权（纯标准库）

运行:  python bayes_inference.py
对应 notes/L09-*.md, notes/L10-*.md. 经典 Burglary-Alarm 网(AIMA Fig.14.?):

  B(偷盗) --> A(警铃) <-- E(地震);   A --> J(John打电话),  A --> M(Mary打电话)
  查询: P(B | J=真, M=真)  (教科书值约 0.287)

三种推断机器:
  1) 枚举: 构造全联合分布(2^5 原子)再边缘化 -- O(2^n);
  2) 变量消元(VE): 因子乘积+按序求和 -- O(n·d^{w+1}), 打印最大因子规模;
  3) 似然加权(LW): 固定证据采样隐变量, 权重=证据条件概率之积 -- 蒙特卡洛近似.
"""
import itertools
import random


class Factor:
    """因子: 变量元组 + {赋值元组: 概率} 表 (bool 域)."""

    def __init__(self, names, table):
        self.names = tuple(names)
        self.table = table

    def __len__(self):
        return len(self.table)

    def scope_str(self):
        return "(" + ",".join(self.names) + ")"


def full_factor(names, prob_true_fn):
    """按 prob_true_fn(赋值dict)->P(name_last=True|父) 生成因子表."""
    names = list(names)
    table = {}
    for assign in itertools.product([False, True], repeat=len(names)):
        d = dict(zip(names, assign))
        if len(names) == 1:
            table[assign] = prob_true_fn(d) if assign[0] else 1 - prob_true_fn(d)
        else:
            # 约定: 最后一个变量为"子", 其余为父
            child = names[-1]
            p = prob_true_fn({k: v for k, v in d.items() if k != child})
            table[assign] = p if d[child] else 1 - p
    return Factor(names, table)


def restrict(factor, evidence):
    """把证据代入因子, 返回缩减后的因子."""
    keep = [v for v in factor.names if v not in evidence]
    table = {}
    for assign, val in factor.table.items():
        d = dict(zip(factor.names, assign))
        if all(d[k] == v for k, v in evidence.items()):
            new_assign = tuple(d[v_] for v_ in keep)
            table[new_assign] = table.get(new_assign, 0.0) + val
    return Factor(keep, table)


def multiply(f1, f2):
    new_vars = list(f1.names) + [v for v in f2.names if v not in f1.names]
    common = [v for v in f1.names if v in f2.names]
    table = {}
    for a1, v1 in f1.table.items():
        d1 = dict(zip(f1.names, a1))
        for a2, v2 in f2.table.items():
            d2 = dict(zip(f2.names, a2))
            if any(d1[v] != d2[v] for v in common):   # 共享变量赋值须一致
                continue
            d = {**d1, **d2}
            key = tuple(d[v] for v in new_vars)
            table[key] = table.get(key, 0.0) + v1 * v2
    return Factor(new_vars, table)


def sum_out(factor, var):
    keep = [v for v in factor.names if v != var]
    table = {}
    for assign, val in factor.table.items():
        d = dict(zip(factor.names, assign))
        key = tuple(d[v] for v in keep)
        table[key] = table.get(key, 0.0) + val
    return Factor(keep, table)


def normalize(factor, query):
    t = factor.table
    z = sum(t.values())
    out = {}
    for assign, val in t.items():
        d = dict(zip(factor.names, assign))
        out[d[query]] = val / z
    return out


# ---------------- 网络定义 (CPT 取自 AIMA 经典例) ----------------
CPT_A = {(True, True): 0.95, (True, False): 0.94,
         (False, True): 0.29, (False, False): 0.001}
CPT_J = {True: 0.90, False: 0.05}
CPT_M = {True: 0.70, False: 0.01}
P_B, P_E = 0.001, 0.002


def build_factors():
    return [
        full_factor(["B"], lambda d: P_B),
        full_factor(["E"], lambda d: P_E),
        full_factor(["B", "E", "A"], lambda d: CPT_A[(d["B"], d["E"])]),
        full_factor(["A", "J"], lambda d: CPT_J[d["A"]]),
        full_factor(["A", "M"], lambda d: CPT_M[d["A"]]),
    ]


ALL_VARS = ["B", "E", "A", "J", "M"]
ATOM_COUNT = 2 ** len(ALL_VARS)


def enumerate_query(evidence, query):
    """全联合枚举: 逐原子相乘再按证据筛选求和."""
    dist = {False: 0.0, True: 0.0}
    for assign in itertools.product([False, True], repeat=len(ALL_VARS)):
        d = dict(zip(ALL_VARS, assign))
        if any(d[k] != v for k, v in evidence.items()):
            continue
        p = P_B if d["B"] else 1 - P_B
        p *= P_E if d["E"] else 1 - P_E
        p *= CPT_A[(d["B"], d["E"])] if d["A"] else 1 - CPT_A[(d["B"], d["E"])]
        p *= CPT_J[d["A"]] if d["J"] else 1 - CPT_J[d["A"]]
        p *= CPT_M[d["A"]] if d["M"] else 1 - CPT_M[d["A"]]
        dist[d[query]] += p
    z = dist[True] + dist[False]
    return {k: v / z for k, v in dist.items()}


def variable_elimination(evidence, query, order):
    factors = [restrict(f, evidence) for f in build_factors()]
    factors = [f for f in factors if f.table]
    max_size = max(len(f) for f in factors)
    for var in order:
        relevant = [f for f in factors if var in f.names]
        others = [f for f in factors if var not in f.names]
        prod = relevant[0]
        for f in relevant[1:]:
            prod = multiply(prod, f)
        max_size = max(max_size, len(prod))
        others.append(sum_out(prod, var))
        factors = others
    joint = factors[0]
    for f in factors[1:]:
        joint = multiply(joint, f)
        max_size = max(max_size, len(joint))
    return normalize(joint, query), max_size


def likelihood_weighting(n_samples, evidence, query, seed=188):
    """拓扑序 B,E,A,J,M 采样隐变量, 证据按条件概率计入权重."""
    rng = random.Random(seed)
    w_q = {False: 0.0, True: 0.0}
    for _ in range(n_samples):
        s = {}
        w = 1.0
        for name in ALL_VARS:                      # 拓扑序
            if name in evidence:
                s[name] = evidence[name]
            elif name == "B":
                s[name] = rng.random() < P_B
            elif name == "E":
                s[name] = rng.random() < P_E
            elif name == "A":
                s[name] = rng.random() < CPT_A[(s["B"], s["E"])]
            elif name == "J":
                s[name] = rng.random() < CPT_J[s["A"]]
                w *= CPT_J[s["A"]] if evidence["J"] == s["J"] else 1 - CPT_J[s["A"]]
            else:
                s[name] = rng.random() < CPT_M[s["A"]]
                w *= CPT_M[s["A"]] if evidence["M"] == s["M"] else 1 - CPT_M[s["A"]]
        w_q[s[query]] += w
    z = w_q[True] + w_q[False]
    return {k: v / z for k, v in w_q.items()}


def fmt(dist, name="query"):
    return "P({}=True)={:.4f}  P({}=False)={:.4f}".format(
        name, dist[True], name, dist[False])


def main():
    ev = {"J": True, "M": True}
    print("Burglary 网络  查询 P(B | J=真, M=真)")
    print(f"枚举规模提示: 全联合原子数 = 2^5 = {ATOM_COUNT} (n 增大指数爆炸)")

    d1 = enumerate_query(ev, "B")
    print("\n[1] 枚举:          " + fmt(d1, "B"))

    for order in (["E", "A"], ["A", "E"]):
        d2, mx = variable_elimination(ev, "B", order)
        tag = " > ".join(order)
        print(f"[2] VE 消元序 {tag:<8} {fmt(d2, 'B')} 最大因子条目={mx}")
    assert abs(d1[True] - d2[True]) < 1e-9, "VE 与枚举必须一致"

    d3 = likelihood_weighting(20000, ev, "B")
    print("[3] 似然加权(2万样本): " + fmt(d3, "B") + "  (蒙特卡洛近似, 存在采样误差)")

    print("\n[4] 反例观察: 证据罕见时 LW 退化")
    ev2 = {"J": True, "M": True, "B": True, "E": False}
    d4 = likelihood_weighting(20000, ev2, "A")
    print("    查询 P(A | b, ¬e, j, m) -- " + fmt(d4, "A"))
    print("    (权重由 A 决定: LW 在此退化为按先验抽 A 再加权, 有效样本量下降)")


if __name__ == "__main__":
    main()
