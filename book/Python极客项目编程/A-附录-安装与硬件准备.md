# A 章 附录：安装与硬件准备（原书 pp.297–）

> 本文件合并原书附录 A（软件安装）、B（基础实用电子学）、C（树莓派贴士），作为环境搭建速查。

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| A 软件安装 | Python + 核心库 | pip/venv 管理 |
| B 电子基础 | 电阻/LED/面包板 | 安全焊接与实践 |
| C 树莓派贴士 | 系统烧录/SSH | 远程开发 |

## 核心精讲（2026 修订）

### A. 软件安装

```bash
# 教学示意，不参与构建
python -m venv .venv && source .venv/bin/activate   # 3.x 用 venv，弃用 virtualenv 旧习惯
pip install numpy matplotlib Pillow pygame pyserial
pip install PyOpenGL                             # 🔧 3D 章节；上下文搭建见 09
pip install sounddevice                          # 🔧 替代弃用的 pyaudio
pip install adafruit-circuitpython-dht gpiozero  # 🔧 替代已归档 Adafruit_DHT
```

> 要点：用 `pyproject.toml` + `venv` 管理依赖（见 PEP 518/PEP 621），不要再手写 `requirements.txt` 裸装；`wave` 已弃用（PEP 594），音频写文件用 `soundfile`。

### B. 电子基础（速记）

- 欧姆定律 `V=IR`；LED 必须串联限流电阻（通常 220–330Ω）。
- 面包板供电 3.3V/5V 区分；GPIO 多数 3.3V 容忍，5V 直连易烧。
- ⚠️ 接强电/激光务必断电操作，遵安全规范。

### C. 树莓派贴士

- 用 Raspberry Pi Imager 烧录系统；首启开 SSH + 配置 WiFi。
- 远程：`ssh pi@<ip>`，文件传 `scp`；后台进程用 `systemd`/`cron`。
- 性能敏感任务注意 Pi 架构（ARM），部分 wheel 需对应平台。

## 版本演进

- 原书（2015）用 `pip` 裸装 + virtualenv；现代统一 `venv` + `pyproject.toml`。
- `pyaudio`→`sounddevice`、`Adafruit_DHT`→`adafruit-circuitpython-dht`（均见各章）。
- `turtle`/`wave` 等标准库模块定位变化（PEP 594）。

## 经典论文与原始文献

- Python 打包：PEP 518（pyproject 构建系统）、PEP 621（项目元数据）。
- PEP 594（标准库弃用清单，含 `wave`/`aifc` 等音频模块）。
- 树莓派/电子：官方文档（见 [12](12-Arduino入门.md)/[14](14-树莓派天气监测器.md) 章引用）。

## 近年研究与工业界开源实践（2015–2026）

- 依赖管理：`uv`（Astral，2024）成极速替代 `pip`+`venv` 的新选择（🔧 可试用）。
- 容器化边缘部署：Pi 上跑 Docker 渐多。
- CircuitPython 统一嵌入式 Python 体验（Adafruit）。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 系统 Python 直接 pip install | 必用 venv，避免污染系统 |
| 裸 `requirements.txt` | 现代用 `pyproject.toml`（PEP 621） |
| 沿用 `pyaudio`/`Adafruit_DHT` | 已弃用/归档，🔧 换替代库 |
| 5V 直连 GPIO | Pi GPIO 多 3.3V，5V 易损 |

## 与其他章 / 其他书的联系

- 各章依赖对应：[04](04-Karplus-Strong弦合成.md)（音频）、[09–11](09-理解OpenGL.md)（OpenGL）、[12–14](12-Arduino入门.md)（硬件）。
- 打包/工程化见《架构模式与Python》（🔧 该书尚未在本仓库建章节目录，待建后补链）。
- 虚拟环境/依赖详见 [../Python编程快速上手——让繁琐工作自动化（第2版）/00-总览与阅读地图.md](../Python编程快速上手——让繁琐工作自动化（第2版）/00-总览与阅读地图.md)。
