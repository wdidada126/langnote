# 03 章 Conway 生命游戏（原书 pp.41–52）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 规则 | 2D 元胞自动机 | 存活/出生/死亡三条件 |
| 网格表示 | 列表的列表 / numpy 数组 | numpy 更快、向量化 |
| 初始条件 | 随机或图案种子 | `random` 撒点 |
| 边界条件 | 环形（toroidal）环绕 | 越界取模，无边界丢失 |
| 规则实现 | 邻域计数 | 卷积或直接 8 邻域求和 |
| 命令行参数 | `argparse` 传入尺寸/步数 | 可复现实验 |
| 动画 | matplotlib `FuncAnimation` | 实时演化展示 |

## 核心精讲

Conway 生命游戏：每个细胞看 8 邻域存活数。
- 存活细胞邻域存活数 = 2 或 3 → 继续存活；否则死亡。
- 死亡细胞邻域存活数 = 3 → 出生。

```python
# 教学示意，不参与构建
import numpy as np

def step(grid):
    # grid: bool 二维数组；环形边界用 roll 实现
    nbrs = sum(np.roll(np.roll(grid, i, 0), j, 1)
               for i in (-1, 0, 1) for j in (-1, 0, 1)
               if (i, j) != (0, 0))
    return (nbrs == 3) | (grid & (nbrs == 2))

grid = np.random.rand(50, 50) < 0.3
for _ in range(100):
    grid = step(grid)
```

> 要点：`np.roll` 天然实现环形（toroidal）边界；`(nbrs==3)|(grid&(nbrs==2))` 一行表达全部规则。

## 版本演进

- 原书用纯 Python 列表 + 嵌套循环；现代用 numpy 向量化（如上）提速数量级。
- 边界：原书明确用「环形（torus）」环绕；也可选「死边界」「镜面边界」，🔧 视实验而定。
- 大型网格渲染：matplotlib `imshow` + `FuncAnimation`。

## 经典论文与原始文献

- J. H. Conway, *The Game of Life*（1970，Scientific American「数学游戏」专栏）。
- 经典文献：E. Berlekamp, J. Conway, R. Guy, *Winning Ways for Your Mathematical Plays*（生命游戏详尽理论）。
- Python `argparse`（PEP 389，🔧 编号以官方为准）。

## 近年研究与工业界开源实践（2015–2026）

- 元胞自动机在复杂系统/人工生命研究仍是模型基础（如染色质建模、交通流）。
- GPU 加速：`numba` `@njit`、PyTorch/Cupy 张量化演化超大网格。
- 趣味扩展：多状态自动机（Brian's Brain、Day & Night）、3D 生命游戏（见 2e 第 10 章 Torus 变体）。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 邻域计数含自身 | 8 邻域应排除中心格 |
| 边界直接丢弃 | 明确选边界策略；原书用环形环绕 |
| 纯循环太慢 | 大网格用 numpy 向量化或 numba |
| 误以为「随机即混沌」 | 存在滑翔机/振荡器等稳定结构，可种子复现 |

## 与其他章 / 其他书的联系

- 概念专篇：[concepts/Conway生命游戏与邻域规则.md](concepts/Conway生命游戏与邻域规则.md)。
- numpy 向量化范式见 [04-Karplus-Strong弦合成.md](04-Karplus-Strong弦合成.md)（环形缓冲）、[10-粒子系统.md](10-粒子系统.md)。
- 算法复杂度背景见 [../像计算机科学家一样思考Python（第2版）/concepts/大O记号与算法分析.md](../像计算机科学家一样思考Python（第2版）/concepts/大O记号与算法分析.md)。
- 3D 扩展见 [11-体渲染.md](11-体渲染.md)（空间数据结构）。
