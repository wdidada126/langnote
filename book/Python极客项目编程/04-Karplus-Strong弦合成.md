# 04 章 Karplus-Strong 弦合成（原书 pp.55–69）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 原理 | 噪声脉冲过延迟线 + 低通 | 物理建模拨弦音色 |
| 仿真 | 环形缓冲实现延迟线 | `collections.deque` 天然 FIFO |
| 写 WAV | 标准库 `wave` + `struct`/`array` | 落盘为可播放文件 |
| 小调五声音阶 | 频率→音符映射 | 按音名算采样 |
| 依赖 | `pyaudio` 实时播放 | 🔧 3.12+ 安装困难 |
| 命令行 | 批量生成音阶 | 可脚本化 |

## 核心精讲

Karplus-Strong：用一段白噪声初始化环形缓冲（延迟线），每步输出缓冲头部、并把「头部与下一值的平均」压回尾部，形成衰减的周期信号——即拨弦音色。

```python
# 教学示意，不参与构建
from collections import deque
import wave, struct, math

def karplus_strong(freq, sr=44100, dur=1.0, N=441):
    buf = deque((random.random()*2-1 for _ in range(N)))  # N≈sr/freq
    out = []
    steps = int(sr * dur)
    for _ in range(steps):
        x = buf.popleft()
        nxt = buf[0] if buf else 0.0
        buf.append((x + nxt) / 2.0)          # 一阶低通 + 反馈
        out.append(int(x * 32767))
    return out

def write_wav(path, samples, sr=44100):
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(b"".join(struct.pack("<h", s) for s in samples))
```

> 要点：延迟线长度 `N ≈ sr / freq` 决定音高；平均反馈是「损失型低通」，能量随周期衰减。

## 版本演进

- 原书用标准库 `wave` 写文件、`pyaudio` 实时播放。
- ⚠️ PEP 594（Python 3.13）将 `wave`/`aifc`/`sunau`/`chunk` 标记为**弃用**，未来可能移除。🔧 生产建议改用 `soundfile`（基于 libsndfile）读写。
- `pyaudio` 在 Python 3.12+ 上 wheel 稀缺，安装常失败；🔧 改用 `sounddevice` 或 `simpleaudio` 播放。

## 经典论文与原始文献

- K. Karplus, A. Strong, *Digital Synthesis of Plucked-String and Drum Timbres*（1979, Computer Music Journal）——算法原始论文。
- 改进版：J. Smith, *Physical Audio Signal Processing*（斯坦福，在线教材，含 KS 扩展）。
- 标准库文档：`collections.deque` https://docs.python.org/3/library/collections.html ；`wave` https://docs.python.org/3/library/wave.html （🔧 注意弃用提示）。
- 相关 PEP：PEP 594（标准库弃用清单，含 `wave`）。

## 近年研究与工业界开源实践（2015–2026）

- 物理建模合成仍是音频 DSP 主流方法之一（与 FM、加法、波表并列）。
- Python 音频生态：`numpy`（信号）、`scipy.signal`（滤波）、`soundfile`/`librosa`（IO 与分析）、`pydub`（便捷剪辑）。
- 实时：`sounddevice`（PortAudio 封装）、`python-sounddevice` 回调模型成熟。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 用 `wave` 放心写新代码 | 3.13+ 已弃用（PEP 594），🔧 改用 `soundfile` |
| `pyaudio` 直接 `pip install` | 3.12+ 易失败，🔧 换 `sounddevice`/`simpleaudio` |
| 延迟线长度随意 | 须 `≈ sr/freq`，否则音高漂移 |
| 平均反馈系数 | `(x+nxt)/2` 是简化；可调衰减系数控制延音 |

## 与其他章 / 其他书的联系

- 概念专篇：[concepts/Karplus-Strong弦合成与环形缓冲.md](concepts/Karplus-Strong弦合成与环形缓冲.md)。
- 环形缓冲与 `deque` 同样见于 [05-Boids鸟群模拟.md](05-Boids鸟群模拟.md)（状态队列）。
- 硬件落地见 [12-Arduino入门.md](12-Arduino入门.md)、[13-激光音频显示.md](13-激光音频显示.md)。
- 信号处理基础见 [../Python算法教程（第2版）.md](../Python算法教程（第2版）.md)（数值方法）。
