# 18 · GUI 自动化（键鼠控制）

> 一句话定位：`pyautogui` 模拟鼠标键盘，操控任意图形界面——「没有 API 也能自动化」。
> 原书 pp. 英文 3e 第 18 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 18.1 | 鼠标 | `moveTo/click/drag` |
| 18.2 | 键盘 | `write/press/hotkey` |
| 18.3 | 屏幕识别 | `locateOnScreen` |
| 18.4 | 弹窗 | `confirm/prompt` |
| 18.5 | 故障保护 | `FAILSAFE` |

## 核心精讲

```
# 教学示意，不参与构建
import pyautogui
pyautogui.FAILSAFE = True              # 鼠标甩到角落即急停
pyautogui.moveTo(100, 100, duration=0.25)
pyautogui.click()
pyautogui.write('hello', interval=0.1)
pyautogui.hotkey('ctrl', 's')
```

- `pyautogui` 跨平台控制鼠标键盘；坐标基于屏幕像素。
- `locateOnScreen` 找图像位置，实现「看屏操作」（依赖截图匹配，分辨率敏感）。
- `FAILSAFE=True`：鼠标移到左上角触发 `FailSafeException`，紧急中止。
- 操作前 `pyautogui.PAUSE = 0.5` 加间隔，避免过快。

## 版本演进

- `pyautogui` 长期维护；底层 macOS 用 `pyobjc`、Windows 用 `pywin32`/ctypes。
- 现代替代：`playwright` 对 Web 应用更稳；RPA 工具（如 `uiautomation`）。
- 图像匹配对 DPI/主题敏感，脆弱；优先用可访问性 API。

## 经典论文与原始文献

- PyAutoGUI 文档：https://pyautogui.readthedocs.io/
- RPA 概念（Robotic Process Automation）。

## 近年研究与工业界开源实践（2015–2026）

- `playwright`/`selenium` 对网页比 GUI 模拟更可靠。
- `uiautomation`(Windows) 走 UI Automation，比图像匹配稳。
- 企业 RPA：UiPath/Power Automate 低代码。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 不开启 FAILSAFE | 务必 `FAILSAFE=True`，防失控 |
| 依赖图像坐标硬编码 | 分辨率/缩放变化即失效，用相对/识别 |
| 操作太快 | 设 `PAUSE` 间隔 |
| 🔧 本书未提 `playwright`/`uiautomation` | Web/Win 应用优先这些 |

## 与其他章 / 其他书的联系

- 截图见[第17章 图像处理](17-图像处理.md)。
- Web 自动化见[第11章 网页抓取](11-网页抓取.md)。
- 与已建中文版同书，见 [`Python编程快速上手——让繁琐工作自动化（第2版）/00-总览与阅读地图.md`](../Python编程快速上手——让繁琐工作自动化（第2版）/00-总览与阅读地图.md)。
