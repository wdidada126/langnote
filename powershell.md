# powershell

powershell 汉字乱码

https://blog.csdn.net/weixin_43426860/article/details/83348284

搞定了

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

希望这个解答能够解决您的疑惑。如果您有其他问题，请随时提问。