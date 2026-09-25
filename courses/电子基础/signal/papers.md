# papers.md — UCB EE120 信号与系统文献

## 一、经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Fourier, *Théorie analytique de la chaleur*（热的分析理论） | 1822 | 用三角级数解热方程，频域分解的诞生 | L7, L8 |
| Nyquist, *Certain Factors Affecting Telegraph Speed* | 1928 | 给出带宽与采样速率的关系，采样定理的先声 | L10, L12 |
| Shannon, *Communication in the Presence of Noise* | 1949 | 把采样定理严格化并给出有噪信道的采样/容量界 | L10, L19 |
| Whittaker / Kotelnikov / Shannon 的插值与采样系列工作 | 1915–1933 | 带限信号可由等间隔样本完全重建（WKS 采样定理） | L10, L11 |
| Cooley & Tukey, *An Algorithm for the Machine Calculation of Complex Fourier Series* | 1965 | FFT：让 DFT 从 O(n²) 降到 O(n log n)，数字信号处理成为可能 | L12 |
| Laplace / Z 变换相关奠基工作（Ragazzini & Zadeh, *The Analysis of Sampled-Data Systems*） | 1952 | 把 z 变换引入采样数据系统，L14 的历史出处 | L13, L14 |
| Wiener, *Extrapolation, Interpolation, and Smoothing of Stationary Time Series* | 1949 | 平稳信号的最优预测与滤波，功率谱方法基础 | L20 |
| North, *Result of the feedback theories* / Bode, *Feedback Amplifier Design*（专著与论文族） | 1945 | 反馈系统的频域分析方法（Bode 图、稳定裕度） | L16 |
| Oppenheim & Schafer, *Discrete-Time Signal Processing*（及 DSP 算法实现系列论文） | 1975–2010 | 把 DFT/滤波/采样系统化为现代数字信号处理学科 | L12–L15 |
| Kalman, *A New Approach to Linear Stochastic Filtering Problems* | 1960 | 状态空间 + 递推最优估计，连接 L17 与随机信号 | L17, L20 |
| Bracewell, *Two-Dimensional Imaging*（傅里叶切片定理相关论文族） | 1978–1980 | 投影-傅里叶切片定理，CT 与频域成像的数学内核 | L18 |

> 说明：本表个别条目以"奠基工作/专著"形式列出，精读前请核对具体出处与年份。

## 二、近 5 年（2021–2026）论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| 神经隐式表示中的频域方法（Fourier features、NeRF 位置编码分析与后续） | 2021–2024 | 证明"用哪种基/频率编码"直接决定可拟合的函数复杂度 | L7, L8, L18 |
| 可微分 FFT / 频域网络层与谱卷积（FNO 谱算子学习一族） | 2021–2025 | 把 FFT 嵌入端到端训练，用于 PDE 与三维重建 | L12, L9 |
| 稀疏采样与压缩感知在成像中的落地（MRI 加速、单像素成像的工业版） | 2021–2025 | 用稀疏先验突破 Nyquist 采样率的资源消耗 | L10, L18 |
| 事件相机与异步信号处理（时空滤波、事件流频域分析） | 2021–2024 | 非均匀采样下的"带宽"与滤波新框架 | L10, L11 |
| PPG/ECG 无接触心率与呼吸估计（rPPG 深度学习族 + 公开基准） | 2021–2025 | 从视频像素中提取周期信号，滤波 + 谱估计的现代化 | L12, L19, L20 |
| 学习型图像去噪/复原与经典频域方法的融合（扩散先验 + 频域约束） | 2021–2025 | 维纳/小波阈值与生成先验的混合，Lab5 主题的前沿版本 | L18, L20 |
| 采样控制与网络化控制系统中的时延补偿（Lab6 主题的现代版） | 2021–2024 | 在计算/通信延迟约束下保证倒立摆类不稳定系统的稳定 | L14, L16, L17 |

## 三、知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 具体用法 |
| --- | --- | --- |
| 卷积与 LTI 系统 | `numpy`（`convolve`）, `scipy.signal`（`lfilter`, `convolve`） | 滤波与响应计算的基本原语 |
| 傅里叶分析与 FFT | `FFTW`, `pocketfft`, `cupy`/`ArrayFire`（GPU FFT） | 音频/图像/物理仿真的频域加速 |
| 采样与重采样 | `liquid-dsp`, `scipy.signal.resample_poly`, `bebinp/soxr` | 音频采样率转换、通信基带链 |
| 滤波器设计 | `scipy.signal`（`butter`/`cheby1`/`firwin`）, `python-control` | 原型设计与系数生成，嵌入式部署 |
| 谱估计与窗函数 | `mne-tools/mne-python`（多锥谱）, `scipy.signal.spectrogram` | 生物信号与振动分析 |
| Z 变换与 IIR 实现 | `scipy.signal`（`zp2tf`, `lfiltic`）, `DSP.jl`（Julia） | 极零点 ↔ 传递函数 ↔ 结构实现 |
| 图像频域处理 | `opencv/opencv`（DFT 模块）, `scikit-image`（`restoration`） | 去噪、锐化、傅里叶切片式重建 |
| 随机信号与匹配滤波 | `gnuradio/gnuradio`（`gr-digital` 同步与匹配滤波）, `scipy.signal` | 通信接收机与雷达信号处理 |
| 反馈控制 | `python-control/python-control`, `casadi/casadi`（MPC）, `PX4/PX4-Autopilot` | 稳定裕度分析、倒立摆/无人机控制 |
| 状态空间方法 | `python-control`（`StateSpace`）, `scipy.signal.lti`, `JuliaControl/ControlSystems.jl` | MIMO 建模、可控/可观测性分析 |
