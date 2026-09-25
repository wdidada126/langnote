# p04 有限状态机：1011 序列检测器 + 交通灯控制器

## 对应讲次
- notes/L06.md §1.1（FSM 五步流程）、§1.2（两个经典例题）、§1.4（三段式规范）
- notes/L05.md §4（异步输入同步、输出打拍）在本项目 TB 中体现
- notes/L10.md（多周期控制器就是更复杂的 FSM——交通灯是它的玩具版）

## 知识点
- `seq_detect.v`：Mealy 型重叠序列检测器。**失败回退边**（"1011" 命中后回 "1" 态、"1010" 回 "10" 态）
  是 KMP 失效函数的电路化；三段式写法 + default 安全态。
- `traffic_light.v`：Moore 型 + 内嵌秒计数器；行人请求使红灯提前放行（最短 2s）——
  演示"输入改变时序图分支"与"计数器是 FSM 并行分量"两种模式。
- `tb_p04.v`：序列对照表法（13 位流 + 期望 hit 位串）；交通灯整周期计数检查 + 提前放行窗口检查。

## 编译与运行（需安装 iverilog）
```sh
cd p04_fsm
./build.sh          # 或 build.bat
iverilog -g2005 -o sim.vvp tb_p04.v seq_detect.v traffic_light.v
vvp sim.vvp         # 期望：P04: ALL TESTS PASSED
```

## 延伸实验
1. 把检测序列换成 "1101"，重新推导回退边——体会"换个模式，FSM 骨架不变"。
2. 改 Moore 版序列检测器：hit 比 Mealy 晚一拍，对照两版时序图（L06 §4 输出对齐）。
3. 交通灯输出 red/yellow/green 各加一级 FF（输出打拍），观察响应晚一拍与毛刺消失的权衡。
4. 用 p03 的 counter 模块给交通灯产生真正的 1Hz tick（50 MHz 分频），替换 TB 的手工脉冲。
