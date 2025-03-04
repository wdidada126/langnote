# powershell

oh-my-posh

powershell 查看文件及其子文件夹文件列表
dir -s "C:\Program Files\Microsoft Visual Studio"

https://github.com/PowerShell/PowerShell/releases/download/v7.4.4/PowerShell-7.4.4-win-x64.msi

powershell 汉字乱码

https://blog.csdn.net/weixin_43426860/article/details/83348284
打开 控制面板—>区域—>管理—>更改系统区域设置
勾选：使用Unicode UTF-8提供全球语音支持
重启电脑

搞定了

在 PowerShell 中，可以使用以下命令来查看当前的代码页：
chcp

chcp
Active code page: 65001

给 Windows 的终端配置代理

 https://zcdll.github.io/2018/01/27/proxy-on-windows-terminal/


"D:\Program Files\CMake\bin\cmake.exe" --version

启动nacos，
浣犵殑涓绘満涓殑杞欢涓浜嗕竴涓凡寤虹 珛鐨勮繛鎺ャ€?

chcp 65001

powershell 运行删除文件的命令，为什么在在一开始输入符号 &

在 PowerShell 中，`&` 符号是用于调用/执行命令或脚本的运算符。

当您在 PowerShell 中键入命令时，通常只需直接输入命令名称，例如：

```shell
Get-Process
```

但是，有些命令在 PowerShell 中可能会被解释为字符串而不是可执行命令。在这种情况下，您可以使用 `&` 符号来显式地告诉 PowerShell 运行命令。这种情况通常发生在以下情况下：

1. 命令名称包含空格或特殊字符。
2. 命令名称存储在变量中。

通过在命令名称前加上 `&` 符号，PowerShell 将正确解释和执行命令。例如：

```shell
& "C:\Program Files\MyApp\app.exe"
```

在上述示例中，命令路径包含空格，因此我们使用 `&` 符号将其包裹在引号中，以确保 PowerShell 正确解析并执行该命令。

对于删除文件的命令，通常无需在一开始输入 `&` 符号，除非您遇到了上述提到的情况。以下是一个删除文件的示例：

```shell
Remove-Item "C:\path\to\file.txt"
```

在上述示例中，我们直接使用 `Remove-Item` 命令来删除指定路径下的文件。

请注意，`Remove-Item` 是一个强大的命令，删除的操作是不可逆的，请谨慎使用。

## proxy

$env:HTTP_PROXY="http://127.0.0.1:10800"
$env:HTTPS_PROXY="https://127.0.0.1:10800"

set all_proxy=socks5://127.0.0.1:7890
windows
cmd
设置临时代理（关闭cmd即设置的代理消失）
set all_proxy=socks5://127.0.0.1:10808 (端口号为你代理软件socks5协议的端口)
删除临时代理
set all_proxy=
查看当前环境变量
set
查看当前公网ip判断代理是否成功
curl cip.cc

powershell
设置临时代理（关闭powershell即设置的代理消失）
$env:all_proxy="socks5://127.0.0.1:10808" (端口号为你代理软件socks5协议的端口)
删除当前临时代理
$env:all_proxy=""
查看当前环境变量
ls env:*
