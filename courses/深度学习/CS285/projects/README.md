# CS285 配套项目计划

> 对齐 5 个 HW 线（模仿→离线→模型基→探索/目标条件→自由项目）。Python (PyTorch) + gymnasium 环境；底层算法裸写为主以吃透推导。本轮只写不编译。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L2-L4 策略梯度 | Python (numpy) | CartPole 上 REINFORCE（含基线消融） | `python pg/reinforce.py --baseline none/vf` |
| L4 PPO | Python (PyTorch) | 裸写 PPO-Clip 训练 Pendulum/HalfCheetah | `python ppo/main.py --env pendulum` |
| L5 模仿（HW1 对应） | Python (PyTorch) | 行为克隆 + DAgger 对比协变量偏移曲线 | `python il/train.py --algo bc/dagger` |
| L6-L7 值方法 | Python (PyTorch) | DQN 玩 Atari 子集；SAC 连续控制 | `python dqn/atari.py --rom breakout` |
| L8-L9 探索 | Python (PyTorch) | 伪计数/随机网络内在奖励对比（Montezuma-lite） | `python explore/train.py --iric/rnd` |
| L10 离线（HW2 对应） | Python (PyTorch) | IQL 复现（hopper-mixed 数据集） | `python iql/main.py --dataset hopper-mixed-v2` |
| L11-L12 模型基（HW3） | Python (PyTorch) | 学模型 + CEM/MPC 规划；RSSM 简化版 | `python mbrl/mpc.py --horizon 15` |
| L13-L15 | Python | MuZero-lite（五子棋/2048）；HER 目标条件 | `python muzero/main.py`、`python her/train.py` |
| L16-L18 LLM-RL | Python | 用 GRPO 在算术任务上 RL 微调小模型 | `python grpo/train.py --task arithmetic` |
| L19-L21 机器人 | Python | Diffusion Policy 复现（Push-T 任务） | `python dp/train.py --task pusht` |
| 自由项目（HW5） | Python | 自选环境+算法对照实验，LaTeX 报告 | `make -C report_pdf/` |
