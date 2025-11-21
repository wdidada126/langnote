# netstat

yum install net-tools -y

netstat -an | grep ^tcp

https://www.cnblogs.com/yszd/p/10095214.html

netstat -tuln

`netstat -tuln` 是一个常用的 Linux 命令，用于查看当前系统上的网络连接情况。

- `-t` 参数表示显示 TCP 协议的连接信息。
- `-u` 参数表示显示 UDP 协议的连接信息。
- `-l` 参数表示只显示监听状态的连接。
- `-n` 参数表示以数字形式显示 IP 地址和端口号。
-p：显示与连接关联的进程信息。这包括进程标识符和程序名称，使得你可以知道哪个程序正在使用特定的端口。

综合起来，`netstat -tuln` 命令将显示当前系统上所有的 TCP 和 UDP 监听连接的详细信息，包括本地 IP 地址、端口号和连接状态。
请注意，运行 `netstat` 命令可能需要管理员权限（使用 `sudo netstat -tuln`）。

综上所述，netstat -tulnp命令用于显示TCP和UDP的监听端口，以及与之关联的进程信息，同时以数字形式显示地址和端口号，而不进行任何名称解析。这对于快速查看哪些程序正在监听哪些端口，以及这些端口的详细情况非常有用。

```shell
netstat -tulnp | grep 9090
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 0.0.0.0:9090            0.0.0.0:*               LISTEN      16660/java
```

在 Windows 11 中查找占用端口 6379 的进程并关闭的方法如下：

方法一：使用命令行工具

1. 查找占用端口 6379 的进程

# 使用 netstat 查找
netstat -ano | findstr ":6379"

# 或者使用 PowerShell
netstat -ano | findstr "6379"


2. 根据PID查找进程名称

tasklist | findstr "PID号"
# 例如：tasklist | findstr "1234"


3. 结束进程

# 根据PID结束进程（替换为查到的PID）
taskkill /PID 进程号 /F

# 例如：taskkill /PID 1234 /F


方法二：使用 PowerShell（推荐）

查找并结束占用端口的进程：

# 查找占用端口6379的进程
Get-NetTCPConnection -LocalPort 6379 | Select-Object OwningProcess, State

# 结束进程（替换为实际的PID）
Stop-Process -Id 进程号 -Force


一行命令完成查找和结束：

# 查找并结束占用6379端口的进程
$process = Get-NetTCPConnection -LocalPort 6379 | Select-Object OwningProcess
if ($process) {
    Stop-Process -Id $process.OwningProcess -Force
    echo "已结束占用端口6379的进程"
} else {
    echo "没有找到占用端口6379的进程"
}


方法三：使用资源监视器

1. 打开资源监视器：
   • 按 Win + R，输入 resmon.exe

   • 或者在任务管理器 → 性能选项卡 → 打开资源监视器

2. 查找端口占用：
   • 切换到"网络"选项卡

   • 在"TCP连接"中查找本地端口 6379

   • 可以看到对应的PID和进程名

3. 结束进程：
   • 右键点击进程 → 结束进程

完整操作示例

# 1. 查找占用6379端口的进程
netstat -ano | findstr ":6379"

# 输出示例：
# TCP    0.0.0.0:6379           0.0.0.0:0              LISTENING       1234

# 2. 查看进程名称
tasklist | findstr "1234"

# 3. 结束进程
taskkill /PID 1234 /F


预防措施

如果这个端口经常被占用，可以考虑：
• 更改应用程序的默认端口

• 使用端口转发

• 在应用程序配置中修改端口设置

请先运行查找命令，告诉我查到的PID是多少，我可以帮你确认是什么进程后再结束。