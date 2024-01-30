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

综合起来，`netstat -tuln` 命令将显示当前系统上所有的 TCP 和 UDP 监听连接的详细信息，包括本地 IP 地址、端口号和连接状态。

请注意，运行 `netstat` 命令可能需要管理员权限（使用 `sudo netstat -tuln`）。
