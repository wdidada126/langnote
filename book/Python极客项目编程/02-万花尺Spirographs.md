# 02 章 万花尺 Spirographs（原书 pp.17–37）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 参数方程 | 摆线/内旋轮线数学 | 用 R/r/l 三个参数描述曲线 |
| Spirograph 方程 | 内旋轮线参数化 | 直接映射成 (x, y) 序列 |
| turtle 图形 | 标准库 `turtle` 绘制 | 逐点 `goto` 连线 |
| Spiro 类 | 封装构造/绘制 | 面向对象组织状态 |
| SpiroAnimator | 多线程/定时器动画 | 持续生成随机曲线 |
| 保存曲线 | 导出 PNG | `turtle.getcanvas().postscript` 或截图 |

## 核心精讲

「万花尺」是内旋轮线（hypotrochoid）：小圆在大圆内滚动，笔尖轨迹即曲线。参数方程：

```python
# 教学示意，不参与构建
import math, turtle, random

def hypo(R, r, l, theta):
    # R: 固定圆半径, r: 滚动圆半径, l: 笔尖距滚动圆心比例
    k = r / R
    x = R * ((1 - k) * math.cos(theta) + l * k * math.cos((1 - k) / k * theta))
    y = R * ((1 - k) * math.sin(theta) - l * k * math.sin((1 - k) / k * theta))
    return x, y

def draw_spiro(R=200, r=55, l=0.9, steps=1000):
    t = turtle.Turtle()
    t.speed(0)
    for i in range(steps):
        theta = 2 * math.pi * i / steps * (r // math.gcd(R, r))  # 周期使曲线闭合
        x, y = hypo(R, r, l, theta)
        t.goto(x, y)
```

> 关键：`gcd(R, r)` 决定曲线在多少圈后闭合；R、r 互质时图案最密。

## 版本演进

- 原书用 `turtle`（标准库，至今仍在，但属教学模块）。
- 现代更常用 matplotlib 的 `LineCollection` 或 `plot` 直接画整条曲线并 `savefig`，无需 GUI 窗口。
- 随机参数生成（`genRandomParams`）逻辑不变，仅随机数 API 用 `random`。

## 经典论文与原始文献

- 内旋轮线（hypotrochoid）/ 外旋轮线（epitrochoid）属经典微分几何，无专属 PEP。
- Python `turtle` 模块文档：https://docs.python.org/3/library/turtle.html
- `math.gcd` 自 3.5 起为标准（原 `fractions.gcd` 已弃用）。

## 近年研究与工业界开源实践（2015–2026）

- 参数曲线生成是 generative art 的常见起手式，社区多用 `numpy` 向量化 + matplotlib/`cairosvg` 导出 SVG。
- `turtle` 仅适合教学演示；生产艺术图走 `Pillow`/`cairo`/`manim`。
- 相关趣味实现：`pycairo`、`vpype`（SVG 画笔路径优化）。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 直接用 `theta` 上界 2π | 需乘 `r/gcd(R,r)` 才闭合，否则图案残缺 |
| turtle 用于生产绘图 | 仅教学；批量出图用 matplotlib/cairo |
| 参数 l 越界 | l∈(0,1] 控制笔尖在圆内/外，超出形态怪异 |
| Py2 `print`/除法 | 按 3.x：真除法、`print()` |

## 与其他章 / 其他书的联系

- 参数曲线与动画循环见 [03-Conway生命游戏.md](03-Conway生命游戏.md)（动画驱动）。
- 用 matplotlib 出图见 [01-解析iTunes播放列表.md](01-解析iTunes播放列表.md)（直方图）。
- 同类生成艺术进阶见 [10-粒子系统.md](10-粒子系统.md)（着色器粒子）。
