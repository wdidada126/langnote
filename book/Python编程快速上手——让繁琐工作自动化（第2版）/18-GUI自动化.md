# 第 18 章 用 GUI 自动化控制键盘和鼠标（原书 pp.约446–约470）

> `pyautogui` 模拟键鼠，做跨应用自动化。基线：原书 Python 3.8；本目录按 3.12+ 校验。

## 本章地图

| 小节 | 内容 | 结论 |
|---|---|---|
| 18.1 移动/点击 | `moveTo`/`click` | 坐标操控 |
| 18.2 键盘 | `typewrite`/`hotkey` | 模拟输入 |
| 18.3 截图/定位 | `screenshot`/`locateOnScreen` | 图像识别 |
| 18.4 安全 | `FAILSAFE` | 防失控 |

## 核心精讲

教学示意，不参与构建（需 `pip install pyautogui`，图形环境；第3版已换栈 🔧）：

```python
import pyautogui
pyautogui.FAILSAFE = True          # 急停：鼠标甩到角落
pyautogui.moveTo(100, 100, duration=0.5)
pyautogui.click()
pyautogui.hotkey("ctrl", "c")
```

## 版本演进

- 原书基于 `pyautogui` 1.x；第3版（2024 起）改用 `pyautogui`/`mouse`/`keyboard` 等新栈（🔧 以官网为准）。
- 坐标自动化脆弱，优先用 API/CLI 而非模拟键鼠。

## 经典论文与原始文献

- pyautogui 文档：https://pyautogui.readthedocs.io/ 规范文档。

## 近年研究与工业界开源实践（2015–2026）

- 能调 API/CLI 就别模拟 GUI；Web 自动化用 Playwright（见浏览器自动化 skill）。
- 终端 UI 自动化用 `pyautogui` 同类、`keyboard`/`mouse` 库。

## 常见误区与本书需修正之处

| 原书说法 | 问题 | 2026 正确写法 |
|---|---|---|
| 坐标写死 | 换分辨率即崩 | 用图像定位/相对坐标 |
| 无急停 | 失控 | FAILSAFE=True |
| GUI 模拟优先 | 脆弱 | 优先 API/CLI |

## 与其他章 / 其他书的联系

- 自动化总纲见本目录定位；更多项目见 [../Python极客项目编程.md](../Python极客项目编程.md)。
