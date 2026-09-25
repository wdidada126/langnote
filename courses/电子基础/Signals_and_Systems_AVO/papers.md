# papers.md — MIT 6.007 信号与系统（Oppenheim）文献

## 一、经典论文与奠基著作

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Fourier, *Théorie analytique de la chaleur* | 1822 | 用三角级数展开解热方程，频域观点的诞生 | L10–L13 |
| Laplace, *Mémoire sur la théorie de l'attraction des planètes elliptiques*（含变换思想的后续） | 1782–1812 | 积分变换与微分方程求解的工具化 | L17–L19 |
| Heaviside, *Electromagnetic Induction and its Propagation*（算子演算） | 1892–1905 | 算子法/阻抗概念，工程界使用拉普拉斯变换的先驱 | L18, L20 |
| Shannon, *Communication in the Presence of Noise* (Proc. IRE) | 1949 | 采样定理严格形式与带限信号重建的完整表述 | L16 |
| Nyquist, *Certain Factors Affecting Telegraph Speed* / *Topics on Specific Transmission* | 1928 | 带宽—速率关系的实验与理论依据 | L16, L25 |
| Wiener, *Extrapolation, Interpolation, and Smoothing of Stationary Time Series* | 1949 | 平稳过程的最优滤波，频域方法与统计估计的融合 | L15, L20 |
| Cooley & Tukey, *An Algorithm for the Machine Calculation of Complex Fourier Series* | 1965 | FFT，让离散频域分析在工程上可行 | L23 |
| Bellman, *Dynamic Programming*（专著与论文族） | 1957 | 递推最优决策与状态观点，连接本课与后续控制课程 | L2, L26 |
| Bode, *The Design of Feedback Amplifiers*（BSTJ 论文族） | 1945 | 用幅相曲线与裕度量化反馈稳定性，本课应用部分的支柱 | L20, L26 |
| Oppenheim & Willsky（with Nawab）, *Signals and Systems*（教材） | 1983/1996 | 把 LTI + 傅里叶 + 拉普拉斯 + z 组织成标准课程结构 | 全课程 |
| Oppenheim & Schafer, *Discrete-Time Signal Processing* | 1975/2010 | 离散时间侧的权威整理：DTFT/DFT/滤波器设计/实现 | L21–L23 |

> 精读时请按 OCW RES.6-007 的参考文献表补充原始出处；本表只保留与讲次直接对应的里程碑工作。

## 二、近 5 年（2021–2026）论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| 谱方法与傅里基在神经算子中的应用（FNO 及其后续变体） | 2021–2025 | 把频域乘法定理变成可学习层，用于 PDE 与三维重建 | L12–L14, L23 |
| 压缩感知/稀疏采样在医学成像与雷达中的现代系统（MRI 加速、稀疏阵列） | 2021–2024 | 用结构先验突破采样率对硬件资源的约束 | L16, L25 |
| 光子与射频 integrated 前端的信号处理（微波光子滤波、photonic delay lines） | 2021–2025 | 用光学带宽实现传统电学滤波器的极限性能 | L15, L20 |
| 采样锁相环/混合信号前端中的时延与抖动建模论文族 | 2021–2025 | 在离散采样系统里重估 LTI 假设的适用范围 | L16, L22, L26 |
| 学习型波束成形与阵列信号处理（自适应波束 + 深度学习联合） | 2021–2025 | 频域空间滤波（波束）与数据驱动方法的融合 | L15, L24 |
| 音频/语音的时频表示现代化（Mel 谱、小波与 STFT 参数选择研究） | 2021–2024 | 短时傅里叶变换的窗口与分辨率权衡仍是工程核心 | L14, L23 |
| 事件/异步采样理论（signal representations for event cameras） | 2022–2025 | 非均匀采样下的带限与重建理论扩展 | L16 |

## 三、知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 具体用法 |
| --- | --- | --- |
| 卷积与 LTI 系统 | `numpy`（`convolve`）, `scipy.signal`（`lfilter`, `lti`） | 冲激响应仿真与线性滤波的基础原语 |
| 傅里叶级数/变换 | `FFTW`, `pocketfft`, `scipy.fft` | 谱分析、PDE 求解与图像处理的频域内核 |
| 采样与重建 | `scipy.signal.resample_poly`, `pysoxr`, `liquid-dsp` | 采样率转换、抗混叠与重采样管线 |
| 滤波器设计与实现 | `scipy.signal`（`butter`, `firwin`, `sosfilt`）, `DSP.jl` | 连续/离散原型滤波器与二阶节实现 |
| 拉普拉斯/传递函数 | `python-control`（`TransferFunction`）, `JuliaControl/ControlSystems.jl` | 极零点分析、稳定性判据与响应仿真 |
| z 变换与差分方程 | `scipy.signal`（`tf2zpk`, `dimpulse`）, `iir`（Python IIR 滤波器库） | IIR 系数生成、零状态/零输入响应 |
| DFT/FFT 应用 | `KissFFT`, `FFTW`, `arrayfire` | 实时频域处理、卷积加速与谱估计 |
| 调制与通信 | `gnuradio/gnuradio`, `srsran/srsRAN_4G`, `liquid-dsp` | 混频、解调、同步与数字通信链路 |
| 反馈控制 | `python-control`, `casadi/casadi`, `PX4/PX4-Autopilot` | 裕度分析、补偿器设计与实时闭环 |
| 分布/冲激与符号计算 | `sympy/sympy`（`DiracDelta`, `fourier_transform`, `laplace_transform`） | 推导验证与作业/笔记中的符号演算 |
