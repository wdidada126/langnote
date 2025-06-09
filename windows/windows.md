# windows 命令行

## windows安全扫描排除文件夹

当 Windows 10 系统中 Microsoft Defender Antivirus Service（即 Antimalware Service Executable 进程）占用过多 CPU 资源时，通过添加文件夹免除扫描是一个有效的解决办法。以下是具体操作步骤：

### 方法一：通过设置界面添加排除项
1. 打开“病毒和威胁防护”设置
    - 按下 `Win + I` 组合键打开“设置”窗口，然后点击“更新和安全”。
    - 在左侧菜单中选择“Windows 安全中心”，接着在右侧窗口中点击“病毒和威胁防护”。
2. 进入“排除项”设置
    - 在“病毒和威胁防护设置”区域，点击“管理设置”。
    - 向下滚动找到“排除项”，点击“添加或删除排除项”。
3. 添加文件夹排除项
    - 点击“添加排除项”，在弹出的菜单中选择“文件夹”。
    - 在文件资源管理器中找到你想要排除扫描的文件夹，选中后点击“选择文件夹”即可。

### 方法二：通过组策略编辑器添加排除项（适用于专业版、企业版等）
1. 打开组策略编辑器
    - 按下 `Win + R` 组合键，输入 `gpedit.msc` 并回车，打开“本地组策略编辑器”。
2. 定位到相关策略设置
    - 在左侧导航栏中依次展开“计算机配置”→“管理模板”→“Windows 组件”→“Microsoft Defender Antivirus”→“扫描”。
3. 配置“指定排除的文件夹”策略
    - 在右侧窗口中找到“指定排除的文件夹”，双击打开该策略设置。
    - 选择“已启用”，然后点击“显示”。
    - 在弹出的“显示内容”窗口中，点击“值”列下的空白处，输入要排除扫描的文件夹的完整路径，输入完成后点击“确定”。
4. 保存设置
    - 依次点击“确定”关闭所有窗口，使设置生效。

### 方法三：通过命令行添加排除项
1. 以管理员身份运行 PowerShell
    - 在开始菜单中找到“Windows PowerShell”，右键点击它并选择“以管理员身份运行”。
2. 执行命令添加排除项
    - 在 PowerShell 窗口中输入以下命令，将 `C:\YourFolder` 替换为你要排除扫描的文件夹的实际路径：
```powershell
Add-MpPreference -ExclusionPath "C:\YourFolder"
```
    - 输入命令后按下回车键执行，即可完成文件夹排除扫描的设置。

添加排除项后，Microsoft Defender Antivirus 将不会对指定的文件夹进行扫描，这可能会在一定程度上减少该服务对 CPU 资源的占用。但需要注意的是，排除扫描可能会降低系统的安全性，因此建议仅对那些你确定安全的文件夹进行排除设置。 

## 其他
新建wifi
netsh wlan set hostednetwork mode=allow ssid=dada-wins10 key=5Edidada
netsh wlan start hostednetwork

因为win系统很实诚的把你卸载的过程给你看。
而手机系统不太老实，它先把图标删了，然后再到你看不见的后台暗戳戳的删文件。

NETSTAT.EXE
C:\Windows\System32\NETSTAT.EXE

windows关闭ftp服务器的防火墙

直接把所有防火墙全关闭才行

入站出站规则添加21不行，电脑重启之后都不行

https://blog.csdn.net/caodinke/article/details/45101119

`dir`

[windows-commands](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/dir)

[windows 取消自动更新]([https://answers.microsoft.com/zh-hans/windows/forum/windows_7-update/%E6%80%8E%E4%B9%88%E5%8F%96%E6%B6%88win10%E7%9A%84/717f577b-758d-4f7a-9845-63194fc2b140](https://answers.microsoft.com/zh-hans/windows/forum/windows_7-update/怎么取消win10的/717f577b-758d-4f7a-9845-63194fc2b140))

c写的内核

更新方式变了，滚动更新，不再是发版本

代码管理工具 代码版本管理的变革

Windows Insider

关闭windows更新，最多关闭一个月，以后还要手动关闭

## windows取消屏幕旋转

取消 windows Ctrl  Alt 箭头旋转屏幕 

要取消Windows Ctrl + Alt + 箭头旋转屏幕的功能，你可以按照以下步骤操作：

1. 在桌面上右击，然后选择"图形选项"。
2. 在新打开的菜单中，找到并点击“系统盘图标”。
3. 在新出现的菜单项中，勾选“启用”。
4. 然后找到任务栏上的显示器图标进行右击，从下拉菜单中选择“图形属性”。
5. 在弹出的对话框中选择“高级模式”，然后单击确定。
6. 接下来选择“选项和支持”下的“快捷键管理器”。
7. 最后去掉"启用"前面的勾选框，然后单击应用，再点击确定即可。

## windows11自动更新
当小白鼠


## c c++

C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Tools\MSVC\14.38.33130\include

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        2023/11/30     10:12                onecore
d-----        2023/11/30      9:50                store
d-----        2023/11/30      9:50                uwp
-a----        2023/11/30      9:50         357758 aligned_new.lib
-a----        2023/11/30      9:50           2672 binmode.obj
-a----        2023/11/30      9:50           2220 chkstk.obj
-a----        2023/11/30     10:12         324182 clang_rt.asan_dbg_dynamic-x86_64.lib
-a----        2023/11/30     10:12         283302 clang_rt.asan_dynamic-x86_64.lib
-a----        2023/11/30     10:12         127682 clang_rt.asan_dynamic_runtime_thunk-x86_64.lib
-a----        2023/11/30     10:12         205338 clang_rt.asan_static_runtime_thunk-x86_64.lib
-a----        2023/11/30     10:12         805684 clang_rt.builtins-x86_64.lib
-a----        2023/11/30     10:12       13173746 clang_rt.fuzzer_MD-x86_64.lib
-a----        2023/11/30     10:12       14850696 clang_rt.fuzzer_MDd-x86_64.lib
-a----        2023/11/30     10:12       14821906 clang_rt.fuzzer_MT-x86_64.lib
-a----        2023/11/30     10:12       16587706 clang_rt.fuzzer_MTd-x86_64.lib
-a----        2023/11/30     10:12       13033134 clang_rt.fuzzer_no_main_MD-x86_64.lib
-a----        2023/11/30     10:12       14708622 clang_rt.fuzzer_no_main_MDd-x86_64.lib
-a----        2023/11/30     10:12       14681300 clang_rt.fuzzer_no_main_MT-x86_64.lib
-a----        2023/11/30     10:12       16445636 clang_rt.fuzzer_no_main_MTd-x86_64.lib
-a----        2023/11/30     10:12         757146 clang_rt.profile-x86_64.lib
-a----        2023/11/30     10:12        3475548 clang_rt.stats-x86_64.lib
-a----        2023/11/30     10:12          27178 clang_rt.stats_client-x86_64.lib
-a----        2023/11/30     10:12        4439952 clang_rt.ubsan_standalone-x86_64.lib
-a----        2023/11/30     10:12         162010 clang_rt.ubsan_standalone_cxx-x86_64.lib
-a----        2023/11/30      9:50           2682 commode.obj
-a----        2023/11/30      9:50         422736 comsupp.lib
-a----        2023/11/30      9:50         442110 comsuppd.lib
-a----        2023/11/30      9:50         422574 comsuppw.lib
-a----        2023/11/30      9:50         441956 comsuppwd.lib
-a----        2023/11/30      9:50         119614 concrt.lib
-a----        2023/11/30      9:50         119944 concrtd.lib
-a----        2023/11/30      9:50         109668 delayimp.lib
-a----        2023/11/30      9:50         104144 exe_initialize_mta.lib
-a----        2023/11/30      9:50           5282 invalidcontinue.obj
-a----        2023/11/30      9:50          46296 iso_stdio_wide_specifiers.lib
-a----        2023/11/30      9:50         473716 legacy_stdio_definitions.lib
-a----        2023/11/30      9:50          35670 legacy_stdio_float_rounding.obj
-a----        2023/11/30      9:50          37386 legacy_stdio_wide_specifiers.lib
-a----        2023/11/30      9:50         315392 libcmt.amd64.pdb
-a----        2023/11/30      9:50        6524230 libcmt.lib
-a----        2023/11/30      9:50         315392 libcmtd.amd64.pdb
-a----        2023/11/30      9:50        6528492 libcmtd.lib
-a----        2023/11/30      9:50        2486272 libconcrt.amd64.pdb
-a----        2023/11/30      9:50        7333696 libconcrt.lib
-a----        2023/11/30      9:50        2486272 libconcrt1.amd64.pdb
-a----        2023/11/30      9:50        7334604 libconcrt1.lib
-a----        2023/11/30      9:50        2494464 libconcrtd.amd64.pdb
-a----        2023/11/30      9:50        8058014 libconcrtd.lib
-a----        2023/11/30      9:50        2486272 libconcrtd0.amd64.pdb
-a----        2023/11/30      9:50        8057760 libconcrtd0.lib
-a----        2023/11/30      9:50        2486272 libconcrtd1.amd64.pdb
-a----        2023/11/30      9:50        8058392 libconcrtd1.lib
-a----        2023/11/30      9:50        2584576 libcpmt.amd64.pdb
-a----        2023/11/30      9:50       20578252 libcpmt.lib
-a----        2023/11/30      9:50        2592768 libcpmt1.amd64.pdb
-a----        2023/11/30      9:50       21491386 libcpmt1.lib
-a----        2023/11/30      9:50        2617344 libcpmtd.amd64.pdb
-a----        2023/11/30      9:50       21260406 libcpmtd.lib
-a----        2023/11/30      9:50        2584576 libcpmtd0.amd64.pdb
-a----        2023/11/30      9:50       20292626 libcpmtd0.lib
-a----        2023/11/30      9:50        2600960 libcpmtd1.amd64.pdb
-a----        2023/11/30      9:50       21027188 libcpmtd1.lib
-a----        2023/11/30      9:50         188628 libomp.lib
-a----        2023/11/30      9:50         189642 libompd.lib
-a----        2023/11/30     10:12         188370 libsancov.lib
-a----        2023/11/30     10:12         188086 libsancovd.lib
-a----        2023/11/30     10:12         262118 libvcasan.lib
-a----        2023/11/30     10:12         269404 libvcasand.lib
-a----        2023/11/30      9:50         307200 libvcruntime.amd64.pdb
-a----        2023/11/30      9:50        1943046 libvcruntime.lib
-a----        2023/11/30      9:50         307200 libvcruntimed.amd64.pdb
-a----        2023/11/30      9:50        1924484 libvcruntimed.lib
-a----        2023/11/30      9:50           2855 loosefpmath.obj
-a----        2023/11/30      9:50          52656 Microsoft.VisualC.STLCLR.dll
-a----        2023/11/30      9:50        2441156 msvcmrt.lib
-a----        2023/11/30      9:50        2524230 msvcmrtd.lib
-a----        2023/11/30      9:50        2546494 msvcmrtd_netcore.lib
-a----        2023/11/30      9:50        2463600 msvcmrt_netcore.lib
-a----        2023/11/30      9:50        2060854 msvcprt.lib
-a----        2023/11/30      9:50        2036180 msvcprtd.lib
-a----        2023/11/30      9:50        7945846 msvcrt.lib
-a----        2023/11/30      9:50        8007074 msvcrtd.lib
-a----        2023/11/30      9:50           2423 newmode.obj
-a----        2023/11/30      9:50           3859 noarg.obj
-a----        2023/11/30      9:50           3541 noenv.obj
-a----        2023/11/30      9:50          29925 notelemetry.obj
-a----        2023/11/30      9:50          38549 nothrownew.obj
-a----        2023/11/30      9:50         158706 oldnames.lib
-a----        2023/11/30      9:50           3886 pgobootrun.lib
-a----        2023/11/30      9:50          41830 pgort.lib
-a----        2023/11/30      9:50         839508 ptrustm.lib
-a----        2023/11/30      9:50         856244 ptrustmd.lib
-a----        2023/11/30     10:12         188886 sancov.lib
-a----        2023/11/30     10:12         188602 sancovd.lib
-a----        2023/11/30      9:50           2864 setargv.obj
-a----        2023/11/30     10:12           2434 stl_asan.lib
-a----        2023/11/30      9:50           2463 threadlocale.obj
-a----        2023/11/30      9:50          84562 vcamp.lib
-a----        2023/11/30      9:50          85008 vcampd.lib
-a----        2023/11/30     10:12         263912 vcasan.lib
-a----        2023/11/30     10:12         271154 vcasand.lib
-a----        2023/11/30      9:50        1886708 vccorlib.lib
-a----        2023/11/30      9:50        1913078 vccorlibd.lib
-a----        2023/11/30      9:50          28384 vcomp.lib
-a----        2023/11/30      9:50          28512 vcompd.lib
-a----        2023/11/30      9:50         152602 vcruntime.lib
-a----        2023/11/30      9:50         164462 vcruntimed.lib
-a----        2023/11/30      9:50           2864 wsetargv.obj

comsupp.lib
comsuppd.lib
comsuppw.lib
comsuppwd.lib
concrt.lib
concrtd.lib
这些库文件是与 Microsoft Visual C++ (MSVC) 编译器和 Windows 平台开发相关的库文件，用于支持不同的功能和特性。下面是这些库文件的作用和用途的简要说明：

1. `comsupp.lib` 和 `comsuppd.lib`：
   - `comsupp.lib` 是用于 Release 模式的库文件，`comsuppd.lib` 是用于 Debug 模式的库文件。
   - 这些库文件提供了对 COM (Component Object Model) 的支持，包括 COM 接口、对象创建、引用计数等相关功能。
2. `comsuppw.lib` 和 `comsuppwd.lib`：
   - `comsuppw.lib` 是用于 Release 模式的库文件，`comsuppwd.lib` 是用于 Debug 模式的库文件。
   - 这些库文件是 Unicode 版本的 `comsupp.lib` 和 `comsuppd.lib`，用于提供对 Unicode 字符串的支持。
3. `concrt.lib` 和 `concrtd.lib`：
   - `concrt.lib` 是用于 Release 模式的库文件，`concrtd.lib` 是用于 Debug 模式的库文件。
   - 这些库文件提供了对并发编程的支持，包括异步任务、并行算法、并发容器等。

这些库文件通常用于 Windows 平台的开发，特别是在使用 Microsoft Visual C++ 编译器进行开发时。它们提供了许多常见的功能和特性的支持，如 COM 组件开发、Unicode 字符串处理和并发编程。根据你的项目需求和使用的功能，你可能需要链接其中的一些库文件来正确编译和链接你的代码。

请注意，库文件的具体用途和支持的功能可能因不同的编译器版本和开发环境而有所差异。在使用这些库文件时，建议参考相关文档和官方资料以获得更详细和准确的信息。

## 11
开机启动项
在 任务管理器 里面

## win c c++ api

https://learn.microsoft.com/en-us/windows/win32/apiindex/windows-api-list

Windows 平台上的 C/C++ 开发者可以利用丰富的 Windows API（应用程序编程接口）来实现从图形用户界面、文件系统操作到网络通信等多种功能。以下是一些关键的 Windows API 类别及其用途简介，帮助你快速了解可用的资源：

### 1. 基础 API

- WinBase.h: 包含了基础的 Windows 数据类型和函数，如文件管理、内存管理等。
- Windows.h: 这是使用 Windows API 的核心头文件，包含了大量其他头文件。

### 2. 图形与多媒体

- GDI (Graphics Device Interface): 通过 `wingdi.h` 提供绘图函数，支持基本的图像绘制和文本输出。
- DirectX: 高性能多媒体和游戏开发API，包括 Direct3D（用于3D图形）、Direct2D（用于2D图形）、DirectSound 等。
- GDI+: 支持更高级的图像处理功能，需引用 `gdiplus.h`。

### 3. 用户界面

- User32.dll: 提供创建窗口、对话框以及处理消息的基础函数，通常通过 `windows.h` 访问。
- ComCtl32.dll: 包含通用控件库，提供诸如按钮、列表框等控件的支持。

### 4. 文件系统和注册表

- FileAPI.h: 提供文件操作相关的API，比如创建、读取、写入和删除文件等。
- Registry API: 通过 `winreg.h` 头文件提供的API用于访问和修改Windows注册表。

### 5. 网络编程

- Winsock API: 使用 `winsock2.h` 和 `ws2_32.lib` 库进行网络通信，支持TCP/IP协议族。
- HTTP Client API: 新版本Windows提供了更简便的HTTP请求方式，可以通过 `httpapi.h` 来访问。

### 6. 安全性

- Security APIs: 包括身份验证、授权、加密服务等，涉及多个头文件如 `security.h` 等。

### 7. 系统信息和服务

- SysInfo API: 获取系统配置信息，如处理器架构、已安装内存等，位于 `sysinfoapi.h`。
- Service Control Manager (SCM) API: 管理Windows服务，可通过 `winsvc.h` 接口访问。

### 8. 异步I/O和线程同步

- Thread Pool API: 提供了高效的任务调度机制，适用于需要执行异步操作的应用程序。
- Synchronization Functions: 如互斥量(mutexes)、信号量(semaphores)、事件(events)，用于线程间的同步控制。

为了更好地理解和使用这些API，建议参考微软官方文档，它不仅详细介绍了每个API的功能，还提供了大量的示例代码帮助开发者理解如何在实际项目中应用它们。你可以直接访问 [Microsoft Docs](https://docs.microsoft.com/) 查找具体的API指南和教程。

此外，对于C++开发者来说，除了直接调用Windows API之外，还可以考虑使用一些高层次的库或框架，例如Qt、Boost等，它们封装了底层API，提供了更加便捷和跨平台的解决方案。

在 Windows 平台上，获取和使用 API 主要依赖于微软提供的 Windows SDK（软件开发工具包），它包含了大量用于系统编程的 C 和 C++ API。这些 API 涵盖了从图形用户界面、文件系统操作到网络通信等多种功能。

### 📚 获取 Windows API 的几种方式

---

## ✅ 方法一：通过 MSDN 文档在线查询

微软开发者网络（MSDN）现在被称为 [Microsoft Docs](https://docs.microsoft.com/)，是获取 Windows API 最全面且最新的资源之一。

### 🔗 常用链接：

- Windows API 索引：
  - [Windows API Index](https://docs.microsoft.com/en-us/windows/win32/apiindex/windows-api-list)
  
- 特定功能或技术的详细文档：
  - [File Management Functions](https://docs.microsoft.com/en-us/windows/win32/fileio/file-management-functions)
  - [Process and Thread Functions](https://docs.microsoft.com/en-us/windows/win32/procthread/process-and-thread-functions)
  - [Socket Functions](https://docs.microsoft.com/en-us/windows/win32/winsock/socket-functions-2)

### 示例：查找 `CreateFile` 函数的信息
1. 访问 [Microsoft Docs](https://docs.microsoft.com/)
2. 在搜索框中输入 `CreateFile`
3. 阅读函数的详细说明，包括参数列表、返回值以及示例代码。

---

## ✅ 方法二：安装并使用本地帮助文档

### 🛠 安装步骤：

1. 下载 Windows SDK：
   - 可以从 [Windows SDK 下载页面](https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/) 下载最新版本的 Windows SDK。
   
2. 安装后访问帮助文档：
   - 安装完成后，在开始菜单中找到“Win32 and COM Documentation”或其他相关文档入口点开即可浏览。
   - 或者使用 Visual Studio 内置的帮助查看器（Help Viewer），可以离线访问所有已安装的文档集。

---

## ✅ 方法三：利用 Visual Studio IDE 直接获取帮助

如果你使用的是 Visual Studio，那么可以直接在 IDE 中获取 API 的帮助信息。

### 使用方法：

1. 在编辑器中选中某个 Windows API 函数名。
2. 按下 `F1` 键，Visual Studio 将自动打开相应的帮助页面。
3. 或者右键点击函数名，选择“Go To Definition”来查看其定义，虽然这可能不会直接显示详细的文档，但可以帮助理解如何使用该函数。

---

## ✅ 方法四：使用第三方工具和库

有时候为了简化开发流程，你可能会选择一些封装了底层 Windows API 的第三方库，比如：

- Boost.Asio：对于网络编程非常有用。
- Qt：提供了一套跨平台的 GUI 和系统级编程接口。
- Poco：一个开源的 C++ 类库，提供了对许多 Windows API 的抽象层。

---

## ✅ 常见的 Windows API 分类及示例

### 1. 基础 API
   - 头文件：`Windows.h`
   - 示例函数：`GetLastError`, `FormatMessage`

### 2. 文件管理
   - 头文件：`FileAPI.h`
   - 示例函数：`CreateFile`, `ReadFile`, `WriteFile`, `CloseHandle`

```cpp
HANDLE hFile = CreateFile(L"C:\\example.txt", GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
if (hFile == INVALID_HANDLE_VALUE) {
    // Handle error
}
```

### 3. 进程与线程
   - 头文件：`Processthreadsapi.h`
   - 示例函数：`CreateProcess`, `CreateThread`, `WaitForSingleObject`

```cpp
DWORD WINAPI ThreadProc(LPVOID lpParameter) {
    // Thread logic here
    return 0;
}

HANDLE hThread = CreateThread(NULL, 0, ThreadProc, NULL, 0, NULL);
if (hThread != NULL) {
    WaitForSingleObject(hThread, INFINITE);
    CloseHandle(hThread);
}
```

### 4. 窗口消息处理
   - 头文件：`WinUser.h`
   - 示例函数：`CreateWindowEx`, `DefWindowProc`, `DispatchMessage`

```cpp
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;
        default:
            return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
}
```

### 5. 网络通信
   - 头文件：`WinSock2.h`
   - 示例函数：`WSAStartup`, `socket`, `bind`, `listen`, `accept`

```cpp
WSADATA wsaData;
int result = WSAStartup(MAKEWORD(2, 2), &wsaData);
if (result != 0) {
    // Handle error
}

SOCKET ListenSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
// Further setup...
```

---

希望以上信息能帮助你在 Windows 平台上顺利进行系统编程。如果你有更具体的需求或者问题，欢迎继续提问！我可以为你提供更多关于特定 API 的例子或深入讲解。