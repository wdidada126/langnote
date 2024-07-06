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
