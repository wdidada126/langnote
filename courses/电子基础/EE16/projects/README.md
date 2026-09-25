# projects/ — EE16A/B 配套小项目计划（本轮只列计划，不写代码）

语言：**Python（NumPy/SciPy/Matplotlib）** 做信号与数据分析；**C** 做 MCU 侧采集；电路仿真用 **ngspice/LTspice** 网表（文本文件即项目产物之一）。

| 章节 | 建议语言 | 小项目 | 编译 / 运行方式 |
| --- | --- | --- | --- |
| A2, A5 节点法 | Python | `nodal_solver.py`：输入元件表，自动装配电导矩阵 G·v=i 并求解节点电压（含电压源改进节点法） | `python nodal_solver.py circuit.csv` |
| A7 传感器标定 | Python | `sensor_calibrate.py`：热敏/光敏分压数据 → 最小二乘反标 + 误差传播分析 | `python sensor_calibrate.py` |
| A9–A10 一阶/二阶响应 | Python + SPICE | `rc_rlc_step.py` + `rlc_tran.cir`：数值解与 ngspice 瞬态仿真对拍，标注阻尼类别 | `python rc_rlc_step.py`；`ngspice -b rlc_tran.cir` |
| A11–A12 运放电路 | SPICE + Python | `opamp_filters.cir`：反相放大、积分器、施密特触发器的传输特性扫描与波特图 | `ngspice -b opamp_filters.cir` → `python plot_ac.py out.csv` |
| A13–A14 数字逻辑 | Verilog + Yosys | `alu_small.v`：4 位 ALU + Logisim 仿真，Yosys 综合看门级面积/延迟 | `yosys -p "read_verilog alu_small.v; synth; stat"` |
| A15–A16 差分方程 | Python | `difference_solve.py`：一阶/二阶递推的齐次+特解符号解 vs 数值解，稳定性判据 | `python difference_solve.py` |
| B2–B4 频域 | Python | `fourier_series_lab.py`：方波/三角波谱合成与吉布斯现象；滤波前后对比 | `python fourier_series_lab.py` |
| B5–B7 滤波与采样 | Python | `aliasing_demo.py`：变采样率采集正弦 + 抗混叠滤波，量化 SNR vs 位数关系 | `python aliasing_demo.py` |
| B8–B9 噪声与回归 | Python | `sensor_denoise.py`：白噪声 + 1/f 噪声注入，移动平均/维纳/匹配滤波对比 | `python sensor_denoise.py` |
| B10 PCA | Python | `imu_pca.py`：三轴加速度数据去相关与主方向估计（静止姿态标定） | `python imu_pca.py` |
| B11–B12 状态空间与控制 | Python | `cartpole_lqr_pid.py`：线性化模型上比较 PID 与 LQR 的阶跃响应与稳定裕度 | `python cartpole_lqr_pid.py` |
| B14 生物信号 | Python | `heart_rate_ppg.py`：合成/录制 PPG 数据提取心率（带通 + 峰值检测 + 自相关校验） | `python heart_rate_ppg.py ppg.csv` |
| B15 综合 | C + Python | `edge_node/`：MCU 端采集（ADC + 定时中断）→ 串口 → PC 端分析与可视化 | MCU 侧 `make flash`（PlatformIO/esp-idf 任选），PC 侧 `python plot_stream.py` |

约定：
- Python 依赖写入 `projects/requirements.txt`（numpy、scipy、matplotlib、pandas）；
- SPICE 网表与 Yosys 脚本随项目存放，输出统一到 `out/`；
- **本轮不写代码、不编译**，由用户后续集中执行。
