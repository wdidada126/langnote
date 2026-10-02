# 05 章 Boids 鸟群模拟（原书 pp.71–85）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 三规则 | 分离 / 对齐 / 聚合 | Reynolds 1986 经典模型 |
| 向量数学 | 位置/速度/加速度 | 用 numpy 向量或手写 |
| 边界处理 | 环绕或回弹 | 防止飞出视窗 |
| 可视化 | pygame 实时绘制 | 每帧更新并 `flip` |
| 参数调优 | 权重影响形态 | 分离权重过大会散开 |

## 核心精讲

Boids（鸟群）由 Craig Reynolds 提出，每只「boid」依据邻近同伴执行三条规则：分离（避免拥挤）、对齐（同向同速）、聚合（向群中心靠拢）。

```python
# 教学示意，不参与构建
import numpy as np

def boid_step(pos, vel, percep=50.0, sep_w=1.5, ali_w=1.0, coh_w=1.0):
    acc = np.zeros_like(vel)
    for i in range(len(pos)):
        d = pos - pos[i]                       # 到其他个体的向量
        dist = np.linalg.norm(d, axis=1)
        near = (dist > 0) & (dist < percep)
        # 分离：远离过近者
        sep = d[near] / (dist[near, None] + 1e-9)
        acc[i] += sep_w * sep.sum(axis=0)
        # 对齐：趋近邻居平均速度
        ali = vel[near].mean(axis=0) - vel[i]
        acc[i] += ali_w * ali
        # 聚合：趋近邻居质心
        coh = pos[near].mean(axis=0) - pos[i]
        acc[i] += coh_w * coh
    return vel + acc * 0.01
```

> 要点：三条规则是局部、无中心控制的「涌现」——全局秩序来自个体简单交互。

## 版本演进

- 原书用 pygame 实时渲染；现代也可用 matplotlib `FuncAnimation` 或 `manim` 做演示。
- 向量计算可用 numpy 向量化（如上）替代手写循环，提速明显。
- 大规模（万级个体）用空间哈希/网格分桶降低邻域查询开销（🔧 进阶）。

## 经典论文与原始文献

- C. W. Reynolds, *Flocks, Herds, and Schools: A Distributed Behavioral Model*（1986, SIGGRAPH）——Boids 原始论文。
- 涌现（emergence）概念源自复杂系统研究（参见 Holland、Johnson 等）。
- 无专属 PEP；numpy 向量化范式见 numpy 文档。

## 近年研究与工业界开源实践（2015–2026）

- 群体智能（swarm intelligence）应用于无人机编队、交通仿真、游戏 AI。
- 库：`boids`/`swarm` 多个教学实现；生产仿真用 `numpy`+`numba`、或转向 `jax` 微分可微群体模型。
- 与强化学习结合：多智能体 RL 中「涌现协作」是热点（如 OpenAI Multi-Agent Hide and Seek）。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 三规则权重相等 | 实际需调参；分离权重过小会重叠碰撞 |
| 邻域用全量 O(n²) | 大群体用空间网格分桶降复杂度 |
| pygame 直接当生产引擎 | 仅演示；严肃仿真用 numpy/jax |
| Py2 风格循环 | 按 3.x，优先向量化 |

## 与其他章 / 其他书的联系

- 与 [03-Conway生命游戏.md](03-Conway生命游戏.md) 同属「模拟生命」部分，但 Boids 是连续空间、生命游戏是离散网格。
- 性能优化见 [../高性能Python（第2版）.md](../高性能Python（第2版）.md)（numpy/numba）。
- 向量数学与 numpy 也见 [04-Karplus-Strong弦合成.md](04-Karplus-Strong弦合成.md)、[10-粒子系统.md](10-粒子系统.md)。
