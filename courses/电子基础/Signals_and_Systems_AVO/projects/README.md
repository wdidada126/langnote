# projects/ — MIT 6.007 配套小项目计划（本轮只列计划，不写代码）

语言：**Python（NumPy/SciPy/Matplotlib + SymPy）** 替代官方 Matlab；符号推导演算用 SymPy，频域仿真用 SciPy。

| 章节 | 建议语言 | 小项目 | 编译 / 运行方式 |
| --- | --- | --- | --- |
| L1–L4 信号与性质 | Python | `signal_play.py`：基本信号生成器 + 系统五性（线性/时不变/因果/稳定/记忆）的数值检验器 | `python signal_play.py` |
| L5–L9 卷积 | Python | `convolution_lab.py`：连续/离散卷积数值实现，验证交换律、微分性质与系统级联等效 | `python convolution_lab.py` |
| L8 微分方程与响应 | Python | `rc_rlc_response.py`：零输入/零状态分解，画阻尼三类响应并与解析解对拍 | `python rc_rlc_response.py` |
| L10–L12 傅里叶级数 | Python | `fourier_series_viz.py`：方波/三角波谐波叠加、Gibbs 现象与 Parseval 能量校验 | `python fourier_series_viz.py` |
| L13–L14 傅里叶变换 | Python + SymPy | `ft_pairs.py`：常用变换对的数值/符号双验证，可视化时移-频移-尺度对偶 | `python ft_pairs.py` |
| L15 滤波器与失真 | Python | `filter_distortion.py`：理想低通 vs 巴特沃斯对音频波形的幅度/相位失真对比 | `python filter_distortion.py input.wav` |
| L16 采样与重建 | Python | `sampling_recon.py`：变采样率与 sinc 重建误差曲线，演示混叠与抗混叠滤波收益 | `python sampling_recon.py` |
| L17–L20 拉普拉斯与 Bode | Python | `bode_hands.py`：从 H(s) 极零点手绘画 Bode 渐近线，与 `python-control` 结果比较 | `python bode_hands.py` |
| L21–L22 z 变换 | Python | `zplane_iir.py`：极零点图 → 冲激响应/频率响应；比较 FIR 与 IIR 的计算代价 | `python zplane_iir.py` |
| L23 DFT/FFT | Python | `dft_vs_fft.py`：朴素 DFT 与 FFT 的耗时曲线（N 扫描）+ 频谱泄漏与窗函数实验 | `python dft_vs_fft.py` |
| L24–L25 调制与通信 | Python | `am_transmit.py`：AM/DSB-SC 调制、相干解调与包络检波，注入噪声测 SNR 增益 | `python am_transmit.py` |
| L26 反馈 | Python | `feedback_loop.py`：一阶/二阶对象加比例与 PID 反馈，观察带宽、裕度与稳定性边界 | `python feedback_loop.py` |
| 综合 | Python | `6_007_capstone.py`：真实录音 → 抗混叠采样 → 带通滤波 → 频谱显示 → 解调还原的完整链路 | `python 6_007_capstone.py sample.wav` |

约定：
- 依赖写入 `projects/requirements.txt`（numpy、scipy、matplotlib、sympy、python-control、soundfile）；
- 每个脚本注释标注 OCW 讲次与 Oppenheim 教材章节；
- **本轮不写代码、不编译**，由用户后续集中执行。
