# 概念专篇：Karplus-Strong 弦合成与环形缓冲

> 跨章主题：第 04 章（PC 合成）+ 第 12/13 章（硬件落地）共用的物理建模合成原理。

## 为什么值得单列

Karplus-Strong 是「用最短代码得到真实拨弦音色」的典范，核心是**环形缓冲（延迟线）**。它同时串起：数据结构（`collections.deque`）、数字信号处理（低通+反馈）、音频 IO（`wave`/PEP 594 弃用提示）。理解它，04 章与硬件章节的代码就通了。

## 算法本质

1. 用一小段白噪声（长度 `N`）初始化延迟线。
2. 每步：取出队头 `x`，把「`(x + 下一值)/2`」压回队尾。
3. 输出 `x`。平均操作是**一阶低通**，能量随每次循环衰减 → 衰减的周期信号 = 拨弦音。

```python
# 教学示意，不参与构建
from collections import deque
import random

def pluck(N=441, dur=1.0, sr=44100):
    buf = deque(random.random()*2-1 for _ in range(N))
    out = []
    for _ in range(int(sr*dur)):
        x = buf.popleft()
        buf.append((x + buf[0]) / 2.0)     # 环形：出头入尾
        out.append(x)
    return out
```

> `deque` 的 `popleft`+`append` 正是 O(1) 环形缓冲；`N ≈ sr/freq` 决定音高。

## 版本演进与 2026 修正

- 原书用标准库 `wave` 写 WAV、`pyaudio` 播放。
- ⚠️ **PEP 594（Python 3.13）** 将 `wave`/`aifc`/`sunau`/`chunk` 标记为**弃用**。🔧 新代码用 `soundfile`（libsndfile）读写：

```python
# 教学示意，不参与构建
import soundfile as sf, numpy as np
sf.write("pluck.wav", np.array(out, dtype=np.float32), 44100)
```

- `pyaudio` 在 3.12+ wheel 稀缺；🔧 改用 `sounddevice`（PortAudio）或 `simpleaudio` 播放。
- 变体：把平均换成「全通/梳状滤波」可调音色（Karplus-Strong 后续改进，🔧 见 J. Smith 教材）。

## 经典论文与原始文献

- K. Karplus, A. Strong, *Digital Synthesis of Plucked-String and Drum Timbres*（1979, Computer Music Journal）。
- J. O. Smith, *Physical Audio Signal Processing*（Stanford，在线教材）。
- PEP 594（标准库弃用清单，含 `wave`）。

## 与其他章的联系

- 主章：[../04-Karplus-Strong弦合成.md](../04-Karplus-Strong弦合成.md)。
- 硬件落地：[../12-Arduino入门.md](../12-Arduino入门.md)、[../13-激光音频显示.md](../13-激光音频显示.md)（DAC/串口下发）。
- 环形缓冲同范式：[../05-Boids鸟群模拟.md](../05-Boids鸟群模拟.md)（状态队列）、[../03-Conway生命游戏.md](../03-Conway生命游戏.md)（numpy roll 边界）。
