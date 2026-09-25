# UCB EE16A / EE16B 信息器件与系统

> 状态：**骨架**

## 一、课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 / 课程号 | UCB EECS 16A & EE 16B **Designing Information Devices and Systems I & II**（信息器件与系统设计 I、II）；先导实验课为 EECS 16AL（实验/版图） |
| 学校 | University of California, Berkeley |
| 主讲 | 课程组轮值，长期负责人为 Borivoje Nikolić（集成电路与系统方向）；Kristofer Pister（器件/MEMS，现 Berkeley 副校长）、Bernhard Boser（MEMS 与传感器）等先后参与建设，每学期 by-staff 名单见课程官网 |
| 教材 | 无固定教材，以课程 Notes + Lab 手册为主；参考：Agarwal & Lang《Foundations of Analog and Digital Electronic Circuits》、Razavi《Fundamentals of Microelectronics》、Oppenheim《Signals and Systems》 |
| csdiy 路径 | `电子基础/EE16` |
| 最新期次 | **Spring 2025**（EECS 16A 春季开设，EE 16B 紧随其后；官方站点 `e16b.org` / `ee16a@berkeley`，疫情后全部 lab 提供远程在线版本，适合在家自学） |
| 先修要求 | 无（csdiy 标注）；数学上并行学习线代与微积分最顺 |
| 难度 / 学时 | 🌟🌟🌟 ／ 约 150 小时（两学期合计） |
| 编程语言 | Python（NumPy/Matplotlib，lab 大量使用），另涉及 LTspice、Logisim、微控制器 |
| 状态 | 骨架 |

## 二、为什么学

1. **伯克利电子/CS 交叉的大一入口课**：不是讲"怎么解电路题"，而是讲"如何设计一个从环境中采集信息、分析并反馈的系统"——传感器 → 电路 → 信号 → 算法 → 执行器的完整链条。
2. **动手密度极高**：每周 lab（有远程版）从搭电路、量数据到写 Python 分析，把抽象数学（线性代数、复指数、频域）落在真实器件上。
3. **打通数学与工程**：18.06 的线性方程组在这里变成节点电压法；复指数变成滤波器；特征值变成系统稳定性；概率变成信号噪声分析。
4. **后续课程的门票**：EE120（信号与系统）、EE106（控制）、EE141/EE142（器件与射频）、CS160 硬件交互、嵌入式与机器人方向都以此为基。

## 三、先修与知识联系

```
18.06 线性代数（方程组、特征值、正交性）+ 18.01/18.02 微积分（ODE、复指数、积分）+ 基础编程（CS61A）
        │
        ▼
   EECS 16A ── 电路抽象 / 节点法 / 一阶二阶系统 / 数字抽象 / 差分方程
        │
        ▼
   EE 16B  ── 频域（傅里叶）/ 采样 / 滤波器 / 随机信号 / 回归与 PCA / 反馈控制
        │
        ├──► UCB EE120 信号与系统（本课 II 的深化与严格化）
        ├──► MIT 6.007 信号与系统（Oppenheim 版对照学习）
        ├──► UCB CS70 / EE C126（概率与随机过程部分的前置）
        ├──► EE106/控制、EE141 器件、EE142 通信与射频
        └──► 机器学习：回归、PCA、特征工程在传感数据上的直接应用
```

| 关联课程 | 用到的本课程内容 |
| --- | --- |
| 电子基础/signal (EE120) | 频域、采样、滤波、系统函数的严格版 |
| 电子基础/Signals_and_Systems_AVO (6.007) | 同一主题的 MIT/Oppenheim 讲法 |
| 数学基础/MITLA | 节点分析 = 线性方程组；状态空间 = 特征值 |
| 数学进阶/CS70、CS126 | 布尔代数、信号中的噪声与估计 |
| 体系结构/CS61C | 数字抽象、逻辑门与组合/时序电路 |

## 四、最新年份（Spring 2025 版 16A + 16B）讲义章节目录（骨架）

阅读材料：`Notes` = 课程官方 notes/lab 手册；Lab = 每周动手实验。

### EECS 16A · Designing Information Devices and Systems I
| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| A1 | 课程导论：信息器件与系统的思维、抽象与建模 | Notes W1；Lab1 |
| A2 | 系统与线性代数回顾：向量、矩阵、线性方程组 | Notes W1–2 |
| A3 | 电路基本量：电荷、电流、电压与功率 | Notes W2；Lab2 |
| A4 | KCL/KVL 与电路拓扑（图论视角） | Notes W3 |
| A5 | 节点电压法：把电路写成 Ax=b 并求解 | Notes W3；Lab3 |
| A6 | 元件 i–v 特性：电阻、电源、非线性元件工作点 | Notes W4 |
| A7 | 分压器与传感器：把物理量变成电压（光敏/热敏/弯曲） | Notes W4；Lab4 |
| A8 | 叠加与等效：Thevenin/Norton、最大功率传输 | Notes W5 |
| A9 | 储能元件：电容/电感、一阶 RC 时间与频率响应 | Notes W5–6；Lab5 |
| A10 | 二阶系统：RLC、阻尼与固有频率、复数特征根 | Notes W6 |
| A11 | 理想运放：虚短虚断、反相/同相放大、比较器 | Notes W7；Lab6 |
| A12 | 有源电路：积分/微分、施密特触发器与滞回 | Notes W7 |
| A13 | 数字抽象：MOS 开关、反相器、逻辑门与噪声容限 | Notes W8；Lab7 |
| A14 | 组合逻辑与硬件描述（Logisim / Verilog 入门） | Notes W8 |
| A15 | 序列与差分方程：离散时间系统的一阶递推 | Notes W9 |
| A16 | 求解差分方程：齐次 + 特解、稳定性、期末复盘 | Notes W9–10；Project |

### EE 16B · Designing Information Devices and Systems II
| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| B1 | 回顾与系统视角：从器件到信息的链路 | Notes W1 |
| B2 | 正弦与复指数：欧拉公式、相位、线性系统对本征输入的响应 | Notes W1；Lab1 |
| B3 | 傅里叶级数与频谱：周期信号的正交分解 | Notes W2 |
| B4 | 频域分析与系统函数：频率响应、极零点 | Notes W2；Lab2 |
| B5 | 滤波器设计与 Bode 图：低通/高通/带阻、品质因数 | Notes W3 |
| B6 | 模拟到数字：ADC、量化噪声、采样定理与混叠 | Notes W3；Lab3 |
| B7 | DFT/FFT 与谱分析实用技巧：窗、分辨率、音频频谱 | Notes W4；Lab4 |
| B8 | 概率与随机信号：均值、方差、相关与噪声模型 | Notes W5 |
| B9 | 估计与回归：最小二乘、基函数、过拟合与正则 | Notes W5；Lab5 |
| B10 | 特征分析与 PCA：去相关、主成分、传感器融合 | Notes W6 |
| B11 | 动力系统与状态空间：矩阵指数、特征值与稳定性 | Notes W6；Lab6 |
| B12 | 反馈与控制：闭环稳定性、PID、根轨迹直觉 | Notes W7 |
| B13 | 机电/流体类比：阻抗类比与能量守恒的通用形式 | Notes W7 |
| B14 | 生物与工程信号案例：心率、ECG/PPG、运动检测 | Notes W8；Lab7 |
| B15 | 综合设计：从传感—调理—采集—算法—执行的全链路 | 项目周 |
| B16 | 课程复盘与后续路线图（EE120/EE106/EE141） | 复习 |

## 五、学习产出（待填充时勾选）

- [ ] 每讲笔记展开（含电路推导图与 lab 数据截图）
- [ ] 关键 lab 复现：分压器校准、运放滤波、FFT 音频、心率提取
- [ ] `papers.md` 阅读状态标注
- [ ] `projects/` 完成 4 个以上（含 1 个跨 A/B 两期的综合小系统）
