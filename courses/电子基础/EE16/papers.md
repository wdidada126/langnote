# papers.md — EE16A/B 信息器件与系统文献

> 本课程偏工程入门，"经典论文"取塑造本领域器件与系统观的里程碑工作；近 5 年条目为线索，精读前请核对元数据。

## 一、经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Atalla & Kahn, *MOS-Transistor / MOSFET 发明（Bell Labs 备忘录与专利）* | 1959–1960 | CMOS 时代的器件起点，A13 数字抽象的物理基础 | A13, A14 |
| Shannon, *A Mathematical Theory of Communication* | 1948 | 比特与信道的量化：整门课"从器件中榨取信息"的目标函数 | A1, B8 |
| Nyquist, *Certain Factors Affecting Telegraph Speed* | 1928 | 采样与带宽限制的先声，B6 采样定理的历史源头 | B6, B7 |
| Kalman, *A New Approach to Linear Stochastic Filtering Problems* | 1960 | 状态空间 + 最优估计，传感器数据处理的范式 | B9–B11 |
| Black & Grayson, *12-bit 40-MHz CMOS A/D Converter*（及开关电容滤波早期工作，Lee & Hodges 1978） | 1976–1980 | 用 CMOS 开关电容实现高精度数据转换，模拟前端工程化 | B5, A12, B6 |
| Middlebrook, *Powerswitch Characterization and Related Applications*（及动态功耗模型工作） | 1974 | 确立 P = CV²f 动态功耗模型，"每比特能量"成为设计核心约束 | A13, A14 |
| Van der Ziel, *Noise in Solid State Devices and Circuits*（专著） | 1970 | 器件噪声（热/散粒/1/f）统一理论，前端设计依据 | B8, B14 |
| Åström & Wittenmark, *Computer-Controlled Systems*（含最小二乘辨识与 PID 整定） | 1984/1997 | 把反馈控制与系统辨识工程化为标准方法 | B9, B12 |
| Hubel & Wiesel, *Receptive Fields and Functional Architecture of Cat Visual Cortex* | 1962 | 感受野/局部滤波的神经证据，B10 特征学习的生物学原型 | B10 |

## 二、近 5 年（2021–2026）论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| TinyML 与边缘推理综述（CMSIS-NN / TensorFlow Lite Micro 后续与 benchmark 论文族） | 2021–2024 | 把模型塞进毫瓦级 MCU，是"传感—计算—反馈"链路的现代版本 | B9, B11, A14 |
| 事件相机（event camera）与异步传感综述（如 *Event-based Vision: A Survey* 的后续系统） | 2021–2024 | 用生物启发的非帧采样突破带宽/功耗权衡 | A7, B6, B8 |
| 可穿戴光电容积脉搏波（PPG）心率/血压估计论文族 | 2021–2025 | 运动伪迹下的自适应滤波与深度学习回归 | B8, B14 |
| 压电/摩擦纳米发电机与自供能传感器 | 2021–2024 | 能量采集使节点免电池，阻抗匹配成为系统设计要点 | A8, B13 |
| 忆阻器/近传感存内计算（in-memory sensing & computing） | 2021–2025 | 打破传感与计算的边界，模拟域矩阵向量乘 | A2, A6, B9 |
| 片上无源/有源滤波器与硅光子前端（RFSoC、photonic interposer 一族） | 2021–2025 | 把滤波器搬到数字边界，抗混叠与线性度设计 | B5, B6 |
| 鲁棒状态估计与传感器融合（LiDAR/IMU/VIO 的滤波 vs 因子图优化路线） | 2021–2025 | 因子图优化（GTSAM/Ceres）成为机器人状态估计主流 | B9–B12 |

## 三、知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 具体用法 |
| --- | --- | --- |
| 电路求解（节点法 / MNA） | `ngspice`（开源 SPICE）, `Xyce`（Sandia 开源 SPICE）, LTspice（商业对照） | 修正节点分析矩阵装配与线性求解 |
| 一阶/二阶响应与滤波器 | `scipy.signal`（`butter`, `sosfilt`）, `JuliaDSP/DSP.jl` | 原型滤波器设计与频率响应绘制 |
| FFT 与谱分析 | `FFTW`, `pocketfft`, `scipy.fft` | 音频/传感数据的实时谱分析 |
| 采样与抗混叠 | `liquid-dsp`, `SoX` 重采样链 | 数字下变频与重采样管线 |
| 最小二乘与回归 | `scikit-learn`（`LinearRegression`, `Ridge`）, `statsmodels` | 传感器标定与特征拟合 |
| PCA 与去相关 | `scikit-learn.decomposition`, `OpenCV`（PCA 模块） | 多通道传感降维、异常检测 |
| 状态空间与控制 | `python-control`（`ControlMatrices`, PID, 根轨迹）, `CasADi`（MPC） | 倒立摆/电机控制的设计与仿真 |
| 数字逻辑与硬件建模 | `YosysHQ/yosys`, `verilator/verilator`, `Logisim-evolution` | 从 Verilog 到门级仿真/综合 |
| 微控制器与传感采集 | `espressif/esp-idf`, `arduino/ArduinoCore-...`, `PlatformIO` | ADC 采集、定时中断、串口上抛数据 |
| 生物信号处理 | `mne-tools/mne-python`, `neurokit2` | ECG/PPG 滤波、峰值检测、HRV 分析 |
