# 第2章 wxWidgets 程序分析 —— 三套 Hello World 与程序骨架五件套

> **本章 2012 口径 → 2026 现状**：2012 年用 wxWidgets 2.8 讲"程序入口→初始化→主窗口→消息循环→退出"五件套；2026 年这套骨架在 wxWidgets 3.x 中**结构原封未动**（`wxIMPLEMENT_APP` 仍是宏），但 Hello World 的对照组已从"Win32 SDK vs GTK+ vs wx"变成"wx vs Qt vs SDL/raylib vs Electron"，且现代 C++（override、nullptr、noexcept）改写了骨架里每个回调的写法。

导航：[总索引](../C++系列·总索引.md) · [原书单文件](../wxWidgets跨平台程序开发.md) · [返回总览](00-总览与阅读地图.md) · 上一章 [01-概述](01-概述.md) · 下一章 [03-事件处理](03-事件处理.md)

### 原书目录（本章，逐字实抓，含三级小节）

```text
第2章 wxWidgets程序分析
2.1 编写Hello World程序
  2.1.1 用Win32 SDK编写程序  2.1.2 用GTK+编写程序  2.1.3 用wxWidgets编写程序
2.2 wxwidgets程序框架分析            ←（原书大小写如此）
2.3 wxWidgets程序框架实现
  2.3.1 程序入口   2.3.2 程序初始化  2.3.3 主窗口的创建
  2.3.4 消息循环   2.3.5 程序退出
```

## 一、动机：为什么先摆三套 Hello World（2.1）

书用 Win32 SDK、GTK+、wxWidgets 三版 Hello World 对照（2.1.1–2.1.3），让读者看到同一件事（注册窗口类→建窗→消息泵→绘制"Hello"）在三个抽象层各要多少行。这个教学结构本身就是第 1 章论点的实证：Win32 约 60+ 行样板、GTK 约 30 行、wx 约 15 行——**抽象层每薄一度，样板翻倍**。2026 年补一个诚实脚注：若拿 Qt6 Widgets 或 SDL 对比，行数与 wx 同量级甚至更少（Qt Designer 可以零 C++ 出窗口），"wx 最省代码"的 2012 结论在今天的选型矩阵里已不成立。

## 二、机制：五件套逐个拆（2.2 / 2.3）

**程序入口（2.3.1）**：`wxIMPLEMENT_APP(MyApp);` 宏展开出平台各自的 `main`/`WinMain`——Windows 上还要吃 `hInstance/nCmdShow`。这是 wx 第一个"宏藏平台差异"的点（第二个是第 3 章事件表）。C++03 时代 `WinMain` 的 `int WINAPI` 签名细节书里花了不少篇幅，今天只需知道：入口签名平台各异是事实，藏进宏是设计决策。

**程序初始化（2.3.2）**：`wxApp::OnInit()` 返回 `bool`——**false 直接终止**，这是"不用异常做失败信号"的 C++03 式 API 设计。2026 写法：`bool OnInit() override;`（override 让签名写错当场编译失败，见 [03 章实测 B](03-事件处理.md) 同款机制）。

**主窗口创建（2.3.3）**：`new MyFrame(...)` **堆上 new、永不 delete**——所有权移交 wx 运行时，窗口销毁由框架负责。这条"反 RAII"规矩是全书最容易踩坑的约定，第 4 章用纯 C++ 复刻其析构协议并实测。三段式构造（构造函数 + `Create()` + 查 `IsOk()`）也在此章露脸：为什么不用构造函数报错？C++03 无 `noexcept`、异常在 DLL 边界不可靠（对照 [C++API设计·错误处理](../C++API设计/05-设计流程与错误处理.md)），于是 wx 选了"构造只做赋值、Create 做可失败的真初始化"。

**消息循环（2.3.4）**：`wxEventLoop` 包住 Win32 `GetMessage/DispatchMessage`、GTK main loop、Cocoa run loop；空闲时进 `OnIdle`。**程序退出（2.3.5）**：`Delete()` 请求关闭→最后一个顶层窗口亡→`ExitMainLoop`→`OnExit` 收尾。

### 2012 式骨架（依书口径重构的最小形，非原文逐字；GUI 未实测——本机无 wx 库 ⚠️）

```cpp
class MyApp : public wxApp {
public:
    virtual bool OnInit();          // 2.8 时代不写 override，靠宏与习惯
};
class MyFrame : public wxFrame {
public:
    MyFrame();
};
IMPLEMENT_APP(MyApp)                // 2.8 宏名（3.x 推荐 wxIMPLEMENT_APP）
MyFrame::MyFrame() : wxFrame(NULL, wxID_ANY, "Hello",
                             wxDefaultPosition, wxSize(300,200)) {}
bool MyApp::OnInit() {
    MyFrame* f = new MyFrame();     // 堆上 new：所有权交给框架
    f->Show(true);                  // 首个顶层窗口显示 => 循环有活干
    return true;                    // false 则立即退出
}
```

启动时序（把 2.3 五节串成一条线）：

```text
WinMain/main(宏生成) → wxEntry → OnInit [建 Frame(new)] → Show
      ↑ false 则直接 cleanup 退出        ↓
wxEventLoop::Dispatch 循环 { GetMessage → 翻译 → 分派事件表/Bind }
      ↑ Close→Destroy(删窗口, 最后顶层亡)  ↓ OnIdle 穿插
OnExit → wxEntryCleanup → return exitCode
```

### 2026 等价写法（同一骨架的现代拼写）

```cpp
class MyApp : public wxApp {
public:
    bool OnInit() override;         // override 防签名漂移（N2928 谱系）
};
wxIMPLEMENT_APP(MyApp);             // 官方前缀宏
bool MyApp::OnInit() {
    auto* f = new MyFrame();        // 仍堆上 new——所有权协议没变（第 4 章实测）
    f->Centre();                    // 高 DPI 下逻辑尺寸，交给布局器
    f->Show();
    return true;
}
```

## 三、权衡：宏藏入口 vs 显式 main

- wx：零平台代码、但"程序从哪开始"不可见，调试启动期问题（manifest、DPI、CRT 初始化顺序）要翻宏展开。
- Qt：`QApplication app(argc, argv)` 显式，可读性换重复样板。
- SDL/raylib：`int main()` 完全裸写，游戏圈路线——没有事件循环概念，自己 `while(running)`。

2026 年重估：wx 的选择对"平台差异大到无法显式"的年代是对的；当 CMake + 现代工具链把平台差异压进构建系统后，显式 main 派（SDL/raylib 甚至 Qt）心智负担更低。

## 四、相邻概念：App / Frame / Panel 三角色

骨架里三个类职责必须分清，否则第 4 章布局全乱：`wxApp` 是**进程生命周期**（一次性）、`wxFrame` 是**顶层窗口**（标题栏/菜单宿主）、`wxPanel` 是**键盘焦点与背景容器**（客户区里几乎什么都放 Panel 上，因为裸 wxWindow 在 Windows 上背景绘制与 tab  traversal 行为不佳——这条 2.8 时代经验在 3.x 仍成立，属"抽象漏底"活例）。

## 核心概念速览（中英对照）

- **程序入口宏** — `wxIMPLEMENT_APP`：展开平台 main/WinMain 的总开关
- **OnInit 布尔协议** — bool-returning init：以返回值而非异常报告启动失败
- **三段式构造** — two-phase construction（Create/Init + IsOk）：把可失败初始化挪出构造函数
- **主窗口** — top-level frame：`wxFrame`，拥有菜单/状态栏/工具栏
- **面板容器** — wxPanel：焦点遍历与客户区背景的承担者
- **事件循环** — event loop：封装 GetMessage/GTK main loop/Cocoa run loop
- **空闲事件** — idle event（`OnIdle`/`wxEVT_IDLE`）：消息队列抽空时的兜底任务钩子
- **Delete 请求** — `wxWindow::Delete()`：异步安全销毁请求，区别于同步 delete
- **所有权移交** — ownership transfer to framework：new 出的窗口由 wx 在关闭时释放
- **ExitMainLoop** — loop quit：不销毁窗口而让循环先返回的通道

## 最新演进与工业实践

- **骨架未变**：3.2/3.3 的官方最小示例（docs/samples）仍是 `wxIMPLEMENT_APP` + `OnInit` + Frame 三件套；跨 14 年的 ABI 与习惯兼容性是 wx 的招牌（也是它被批评"不敢破窗"的证据）。
- **noexcept 时代**：`noexcept`（C++11）让"构造函数不抛异常、二段 Create"从"平台逼的"变成"仍值得守的 ABI 纪律"——库边界构造函数若行为不可预测，析构路径即 UB。对照 [C++API设计](../C++API设计/05-设计流程与错误处理.md) 的错误处理章。
- **override 全面补写**：书中所有 `DECLARE_EVENT_TABLE` 风格章节（含本章 OnInit）在 2026 代码评审里都会被要求加 `override`；N2928（"Deviating from virtual function implementation"，wg21.link 实测 302）是该关键字的出处。
- **HiDPI 是本章 2012 版最大盲区**：2.8 的 `WinMain` 展开没有 manifest DPI-aware 声明，4K 屏发虚是当年真实症状；3.x 起 wxMSW 默认 per-monitor DPI + 缩放感知（机制转述 ⚠️，本机无 wx 无法实测），2026 年任何桌面书不写 DPI 即过时。
- **对比当代最小 GUI**：一个"能开窗"的 2026 候选清单——Qt6 `QApplication`+`QWidget`（约 12 行）、SDL3（约 25 行，无控件）、Slint（声明式 .slint + Rust/C++ main，官网实测可达）。wx 的 Hello World 行数优势已不构成选型理由，选型回到第 1 章"三必须"框架。

## 本章小结

1. 骨架五件套（入口/初始化/主窗/循环/退出）在 3.x 仍是同一形状，学习价值在"机制"而非"版本号"。
2. `new` 后不 `delete`、`OnInit` 返 bool、两段式 `Create` 是三条必须内化的反直觉约定。
3. 2012 的"三平台 Hello World 对照"要升级为"wx/Qt/SDL/Web 容器"四路对照才配 2026 选型。
4. 自查三问：`OnInit` 返回 false 会发生什么（框架清理并退出，无崩溃）？`f->Show(true)` 前 return 会怎样（无顶层可见窗口→某些平台事件循环立刻空闲退出，2.8 经典坑）？程序退出与 `wxApp::OnExit` 的关系（后者优先于 CRT 静态析构，放对话框收尾逻辑）？
5. 关联件：所有权细节在 [04](04-图形用户界面.md)；事件循环内部机制在 [03](03-事件处理.md)；入口宏的"平台差异藏宏"手法与 [01 章框架结构](01-概述.md)一脉相承。
6. 一句话版本：本章是"读任何 wx 代码前先装好的坐标系"——所有回调都住在宏生成的 `main` 之后的那个循环里。

---
*本篇为《wxWidgets跨平台程序开发》目录版章节：返回 [00-总览与阅读地图](00-总览与阅读地图.md) · [C++系列·总索引](../C++系列·总索引.md) · [原书单文件](../wxWidgets跨平台程序开发.md)*
