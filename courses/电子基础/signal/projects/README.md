# projects/ — UCB EE120 配套小项目计划（本轮只列计划，不写代码）

语言：**Python（NumPy/SciPy/Matplotlib）**，与课程 6 个 lab 完全一致；FFT 性能对比部分可选 **C** 以观察常数与缓存效应。

| 章节 | 建议语言 | 小项目 | 编译 / 运行方式 |
| --- | --- | --- | --- |
| L1–L5 信号与卷积 | Python | `conv_play.py`：图形化演示卷积四步（翻转/滑动/相乘/求和），验证交换律与系统级联 | `python conv_play.py` |
| L6–L9 频域分析 | Python | `spectrum_lab.py`：方波/三角波谐波合成，观察 Gibbs 与理想滤波器的失真 | `python spectrum_lab.py` |
| L10–L11 采样与混叠 | Python | `alias_lab.py`：改变采样率重建正弦，量化混叠误差并设计抗混叠低通 | `python alias_lab.py` |
| L12 FFT（对应课程 Lab3） | Python + C | `my_fft.py` / `fft_c.c`：自实现递归/迭代 FFT，与 `numpy.fft` 做时间与误差对比；C 版测不同 N 的缓存效应 | `python my_fft.py`；`gcc -O2 fft_c.c -o fft_c && ./fft_c 4096` |
| L13–L15 系统函数与滤波 | Python | `pole_zero_play.py`：极零点图 → 冲激响应/频率响应联动；设计 Butterworth 与窗法 FIR 并比较代价 | `python pole_zero_play.py` |
| L14 心率提取（对应 Lab4） | Python | `hr_from_video.py`：读手指/人脸视频帧均值 → 带通 + 谱峰/自相关估计 BPM，报告置信度 | `python hr_from_video.py video.mp4` |
| L18 图像频域去噪（对应 Lab5） | Python | `hubble_denoise.py`：二维 DFT + 维纳/阈值去噪，输出前后对比图与 PSNR | `python hubble_denoise.py img.fits` |
| L16–L17 反馈与状态空间（对应 Lab6） | Python | `cartpole_lqr.py`：线性化倒立摆模型，比较 PID/LQR 的收敛域与采样延迟容限 | `python cartpole_lqr.py` |
| L19 调制解调 | Python | `am_radio.py`：AM/DSB-SC 调制、相干解调与包络检波，加噪声比较 SNR 增益 | `python am_radio.py` |
| L20 随机信号与匹配滤波 | Python | `matched_filter.py`：白噪声中检测已知波形，比较能量检测与匹配滤波的虚警/检测率 | `python matched_filter.py` |

约定：
- 依赖写入 `projects/requirements.txt`（numpy、scipy、matplotlib、opencv-python、astropy 用于 FITS）；
- 每个脚本注释标注讲次与对应课程 lab 编号，固定随机种子；
- **本轮不写代码、不编译**，由用户后续集中执行。
