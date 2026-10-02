# 06 章 ASCII 艺术（原书 pp.89–99）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 原理 | 像素亮度→字符 | 字符密度近似灰度 |
| 读图 | Pillow `Image` | `convert("L")` 转灰度 |
| 量化映射 | 字符梯度表 | 暗→密集字符 |
| 输出 | 终端 / 文本文件 | 等宽字体才保形 |
| 进阶 | 彩色 / 多尺度 | 可叠加 ANSI 色 |

## 核心精讲

把图像转灰度后，按亮度映射到一组「从疏到密」的字符；逐行输出即 ASCII 画。

```python
# 教学示意，不参与构建
from PIL import Image

CHARS = " .:-=+*#%@"          # 暗→亮（或反向，视终端背景）

def img_to_ascii(path, cols=80):
    im = Image.open(path).convert("L").resize((cols, int(cols * 0.5)))
    w, h = im.size
    px = im.load()
    lines = []
    for y in range(h):
        row = "".join(CHARS[px[x, y] * (len(CHARS) - 1) // 255] for x in range(w))
        lines.append(row)
    return "\n".join(lines)

print(img_to_ascii("photo.jpg"))
```

> 要点：终端字符高宽比约 2:1，故 `resize` 高度取宽度的 0.5 才能不变形；字符表顺序决定「暗密/亮疏」。

## 版本演进

- 原书用 Pillow（PIL 分支）；现仍是最主流图像库。
- 现代可用 `numpy` 一次性向量化「亮度→字符索引」，避免像素级循环。
- 彩色 ASCII：用 ANSI 转义或 rich 库上色。

## 经典论文与原始文献

- ASCII 艺术属「文本模式图形」民俗，无专属论文；Pillow 文档：https://pillow.readthedocs.io 。
- 相关：图像量化（误差扩散 dithering，Floyd–Steinberg）可提升观感。
- 无专属 PEP。

## 近年研究与工业界开源实践（2015–2026）

- 终端美化：rich / `img2txt`（caca-utils）、`chafa` 把图转终端字符画。
- 趣味落地：CI 徽章、README 头像、终端欢迎屏。
- 与 LLM 结合：把图像先转 ASCII 再喂模型做「低带宽视觉」实验（🔧 社区探索）。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 忽略字符高宽比 | 高度乘 0.5 左右，否则拉伸 |
| 字符表方向错 | 需与终端背景（黑/白）匹配暗密/亮疏 |
| 用 `cv2` 而非 Pillow | 二者皆可，Pillow 更轻 |
| Py2 `print` 行尾 | 3.x 用 `print()`；输出含中文注意编码 |

## 与其他章 / 其他书的联系

- 同属「玩图像」部分，接 [07-照片马赛克.md](07-照片马赛克.md)、[08-立体图Autostereograms.md](08-立体图Autostereograms.md)，均依赖 Pillow。
- Pillow 基础见 [01-解析iTunes播放列表.md](01-解析iTunes播放列表.md)（无，但 matplotlib 同理）。
- 图像处理进阶见 [../Python数据科学手册2e.md](../PythonDataScienceHandbook2e.md)（numpy 图像）。
