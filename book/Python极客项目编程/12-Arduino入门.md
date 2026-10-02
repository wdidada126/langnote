# 12 章 Arduino 入门（原书 pp.235–247）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 串口通信 | `pyserial` 读写 | PC↔Arduino 桥梁 |
| 点灯 | 控制 GPIO/LED | 协议字符串即可 |
| 读传感器 | 串口回传模拟值 | 实时绘图 |
| 固件 | Arduino 草图 | 板端跑 C++ |
| 进阶 | 接 13 章激光 | 组合成系统 |

## 核心精讲

PC 端用 `pyserial` 打开 Arduino 的串口，发命令/收数据；板端烧录 C++ 草图解析串口指令并操作引脚。

```python
# 教学示意，不参与构建
import serial, time

ser = serial.Serial("COM3", 9600, timeout=1)   # Linux 常为 /dev/ttyUSB0
time.sleep(2)                                  # 等 Arduino 复位
ser.write(b"on\n")                             # 板端解析: 点亮 LED
line = ser.readline().decode().strip()         # 读回传感器值
print("模拟读数:", line)
ser.close()
```

> 要点：波特率两端必须一致；`readline` 依赖板端 `Serial.println` 以换行结尾；跨平台端口名不同。

## 版本演进

- 原书用 `pyserial`（现包名 `pyserial` 仍维护，导入 `serial`）。现代也可用 `paho`/原生方案，但 `pyserial` 最通用。
- Arduino 生态已扩展：新板（ESP32）支持 WiFi/蓝牙，可用 MicroPython 直接跑 Python（🔧 替代方案）。
- 实时绘图：原书 matplotlib 动态刷新，现可 `matplotlib.animation` 或 `pyqtgraph`。

## 经典论文与原始文献

- Arduino 官方文档：https://www.arduino.cc/reference/en/ 。
- `pyserial` 文档：https://pyserial.readthedocs.io 。
- 无专属 PEP（串口属系统/硬件层）。

## 近年研究与工业界开源实践（2015–2026）

- MicroPython / CircuitPython 让「板子直接跑 Python」成为主流（Adafruit 推动），弱化 PC 串口中转。
- 物联网：ESP32 + MQTT（见 [14-树莓派天气监测器.md](14-树莓派天气监测器.md) 思路延伸）。
- 数据回传：用 `pyserial` + `pandas` 做实验室采集常见。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 端口写死 COM3 | Linux/macOS 是 /dev/tty*，需配置化 |
| 不等待复位 | 打开串口后延时 1–2s 防丢首帧 |
| 波特率不一致 | 板端 `Serial.begin` 须与 PC 同值 |
| Py2 `print`/字符串 | 3.x 用字节 `b"..."` 发、`decode` 收 |

## 与其他章 / 其他书的联系

- 接 [13-激光音频显示.md](13-激光音频显示.md)（同一串口驱动外设）。
- 数据入库/展示见 [14-树莓派天气监测器.md](14-树莓派天气监测器.md)（SQLite）。
- 信号/采样理念见 [04-Karplus-Strong弦合成.md](04-Karplus-Strong弦合成.md)（音频采样）。
- 嵌入式系统底层见 [../CPython设计与实现.md](../CPython设计与实现.md)。
