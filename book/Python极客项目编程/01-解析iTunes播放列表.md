# 01 章 解析 iTunes 播放列表（原书 pp.3–15）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| iTunes 播放列表文件解剖 | plist（XML）结构 | 用标准库 `plistlib` 直接加载 |
| 需求 | 查重 / 提取 / 交集 / 统计 | 把曲目建模成 dict 列表 |
| 找重复 | 按 `name+artist` 去重 | 输出重复条目便于清理 |
| 提取重复 | 生成新播放列表 | 写回 plist 文件 |
| 跨列表交集 | 多个播放列表共有曲目 | `set` 交集最简洁 |
| 统计与绘图 | 时长分布直方图 | matplotlib 可视化 |
| 命令行参数 | `argparse` 封装 | 可脚本化复用 |

## 核心精讲

iTunes 导出的播放列表是 **XML 格式的 plist**（Property List）。Python 标准库 `plistlib` 可直接往返解析，无需第三方依赖。

```python
# 教学示意，不参与构建
import plistlib
from collections import Counter

def load_tracks(path):
    with open(path, "rb") as f:
        plist = plistlib.load(f)          # 2e/3e 用 load；旧 API 是 readPlist
    return plist.get("Tracks", {})

def find_duplicates(tracks):
    seen, dups = set(), []
    for tid, t in tracks.items():
        key = (t.get("Name"), t.get("Artist"))
        if key in seen:
            dups.append(key)
        else:
            seen.add(key)
    return dups

tracks = load_tracks("exported.xml")
print(f"重复条目数：{len(find_duplicates(tracks))}")
```

> 要点：plist 顶层是 dict，`Tracks` 是「曲库 ID → 曲目 dict」的映射，每首曲目含 `Name`/`Artist`/`Total Time`/`Play Count` 等键。

## 版本演进

- 原书（2015）同时兼容 Py2/3，`plistlib.load` 在 Py3 接收二进制流。
- Py3 中 `plistlib.readPlist`/`writePlist` 已移除，统一用 `load`/`dumps`。
- 统计绘图用 matplotlib；原书示例直接 `pyplot.hist`。

## 经典论文与原始文献

- Apple「Property List」格式规范（苹果开发者文档）——plist 的官方定义。
- Python 标准库 `plistlib` 文档：https://docs.python.org/3/library/plistlib.html
- 无专属 PEP；相关：`argparse` 纳入标准库（原 PEP 389，🔧 具体编号以官方为准）。

## 近年研究与工业界开源实践（2015–2026）

- `plistlib` 长期稳定，仍是 macOS/iOS 生态解析配置的首选。
- 音乐元数据清洗更常见走 `musicbrainzngs` / `mutagen`（读 mp3/flac 标签），而非依赖 iTunes 导出。
- pandas 可直接 `read_xml` 处理通用 XML；但 plist 结构特殊，仍用 `plistlib` 更稳。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 用文本正则硬抠 plist | 直接用 `plistlib.load`，XML 转义/嵌套交给库 |
| 重复判定只看 `Name` | 以 `(Name, Artist)` 复合键更准；🔧 是否含 `Album` 视需求 |
| 时长单位混淆 | `Total Time` 单位为**毫秒**，画图前需 ÷1000 |
| Py2 的 `readPlist` | Py3 用 `load`/`dumps`，🔧 旧代码需改写 |

## 与其他章 / 其他书的联系

- 文件与数据建模思路见 [14-树莓派天气监测器.md](14-树莓派天气监测器.md)（SQLite 入库）。
- 统计可视化基础见 [03-Conway生命游戏.md](03-Conway生命游戏.md)（matplotlib 动画）。
- 通用 Python 文件处理见 [../像计算机科学家一样思考Python（第2版）/14-文件.md](../像计算机科学家一样思考Python（第2版）/14-文件.md)。
