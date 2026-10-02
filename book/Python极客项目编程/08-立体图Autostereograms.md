# 08 章 立体图 Autostereograms（原书 pp.117–130）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 原理 | 随机点 + 重复位移 | 双眼视差产生 3D 错觉 |
| 深度图 | 灰度=距离 | 每像素决定重复间距 |
| 生成 | 按深度错位复制 | Pillow 逐列绘制 |
| 观看 | 散焦/对眼 | 大脑融合出立体 |
| 进阶 | 彩色 / 动画 | 可序列帧 |

## 核心精讲

「魔术眼」立体图：先生成一张随机点纹理，按深度图让某些列「重复错位」——左右眼看到不同相位，大脑解读成凹凸。

```python
# 教学示意，不参与构建
from PIL import Image
import numpy as np

def make_stereo(depth_path, out="stereo.png", sep=80):
    depth = np.asarray(Image.open(depth_path).convert("L"))
    h, w = depth.shape
    img = np.random.rand(h, w)          # 随机点（这里用灰度示意）
    for y in range(h):
        for x in range(w):
            d = int(depth[y, x] / 255 * sep)   # 深度→位移
            if 0 <= x - d:
                img[y, x] = img[y, x - d]       # 按深度复制左邻
    Image.fromarray((img*255).astype("uint8")).save(out)
```

> 要点：深度越大位移越大；「复制左邻」把随机纹理以视差间距重复，制造隐式 3D。真实实现常用「每 `sep` 像素强制同相」。

## 版本演进

- 原书用 Pillow 逐像素生成；现代可 numpy 向量化整行错位（用 `np.roll` + 掩码）。
- 彩色立体图：对 RGB 三通道各自或同步错位。
- 观看方式：平行眼（看远）或交叉眼，🔧 个人习惯不同。

## 经典论文与原始文献

- C. W. Tyler, J. E. Clark, *The Autostereogram*（1990s，发现随机点立体图可裸眼观看）——现代「魔术眼」基础。
- 双眼视差（binocular disparity）源自立体视觉生理研究（J. Wheatstone 1838 体视镜）。
- 无专属 PEP；Pillow / numpy 文档。

## 近年研究与工业界开源实践（2015–2026）

- 社区生成器：`magic-eye`/`autostereogram` 多个 PyPI 包，支持深度图导入。
- 与 SIRDS（单图像随机点立体图）算法同源。
- 趣味：把分形/高度场转立体图做科普演示。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 位移与深度反向 | 通常深度大→位移大，需与观看方式一致 |
| 逐像素 Python 循环 | 用 numpy 向量化整行错位提速 |
| 随机种子不固定 | 固定 `seed` 才能复现同一张图 |
| 深度图未归一化 | 须 0–255 映射到位移区间 |

## 与其他章 / 其他书的联系

- 同「玩图像」三章：见 [06-ASCII艺术.md](06-ASCII艺术.md)、[07-照片马赛克.md](07-照片马赛克.md)，均依赖 Pillow + numpy。
- 3D 感知衔接 [09-理解OpenGL.md](09-理解OpenGL.md)、[11-体渲染.md](11-体渲染.md)（真实 3D 而非错觉）。
- 数组操作见 [../Python数据科学手册2e.md](../PythonDataScienceHandbook2e.md)。
