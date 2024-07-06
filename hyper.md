# hyper-v

hyper-v 开源吗？

Hyper-v免费但不开源。微软是一个商业公司,很难有完整的解决方案开源的。

Hyper-v做为微软虚拟化和云计算产品的重要角色,开源的可能性很低。

与Docker类似，Hyper是Linux基金会OCI官方支持的两种容器技术之一，同时Google（Kubernetes）的工程师们也表示，Hyper是整个容器行业的关键技术和力量（key contributor）。通过在Linux基金会和Google的合作，Hyper逐渐获得了Red Hat、Google、Docker、IBM、华为等大公司的支持。
究竟Hyper的虚拟化容器是什么？
赵鹏介绍说：“表面上看，Hyper是一个容器，但实际上它是一个虚拟机。相对虚拟机而言，Hyper的特点就是小巧轻便，可以在0.1秒内完成虚机的启动，并且只需4M内存就可以运行一个虚机（阿里云最小虚机需要512M内存）；而对Docker来说，Hyper又是一个拥有虚机级别安全性的容器。它的特别之处在于，它将虚拟机和Docker两者的优势集于一身。”


在 Windows 10 中，Hyper-V 和 VirtualBox 可能会发生冲突，因为这两个虚拟化平台都需要独占访问虚拟化硬件。如果你希望在同一台机器上运行 VirtualBox 虚拟机而不受到 Hyper-V 的影响，你需要临时禁用 Hyper-V。以下是操作步骤：

### 禁用 Hyper-V

1. 通过 Windows 功能界面禁用 Hyper-V

   1. 打开“控制面板”。
   2. 点击“程序”。
   3. 点击“启用或关闭 Windows 功能”。
   4. 在弹出的窗口中，取消勾选“Hyper-V”。
   5. 点击“确定”，并根据提示重启计算机。

2. 通过命令行禁用 Hyper-V

   使用管理员权限打开命令提示符或 PowerShell，然后输入以下命令来禁用 Hyper-V：

   ```bash
   dism.exe /Online /Disable-Feature:Microsoft-Hyper-V-All
   ```

   完成后，重新启动计算机。

### 验证 Hyper-V 是否禁用

在禁用 Hyper-V 并重新启动后，可以通过命令提示符或 PowerShell 验证 Hyper-V 是否已禁用：

```bash
systeminfo
```

在系统信息中查找“Hyper-V Requirements”部分。如果列出的所有条目都显示“No”，则表示 Hyper-V 已成功禁用。

### 启动 VirtualBox

禁用 Hyper-V 并重启计算机后，VirtualBox 应该能够正常运行并启动虚拟机。

### 临时禁用和启用 Hyper-V

如果你需要频繁地在 Hyper-V 和 VirtualBox 之间切换，可以创建批处理脚本来简化启用和禁用 Hyper-V 的过程。

#### 禁用 Hyper-V 脚本

创建一个名为 `disable_hyperv.bat` 的批处理文件，内容如下：

```bash
@echo off
dism.exe /Online /Disable-Feature:Microsoft-Hyper-V-All
pause
```

#### 启用 Hyper-V 脚本

创建一个名为 `enable_hyperv.bat` 的批处理文件，内容如下：

```bash
@echo off
dism.exe /Online /Enable-Feature:Microsoft-Hyper-V /All
pause
```

执行相应的批处理文件，然后根据提示重新启动计算机。

### 参考资料

- [VirtualBox and Hyper-V on the same Windows machine](https://forums.virtualbox.org/viewtopic.php?f=6&t=62339)
- [Microsoft Docs: Disable Hyper-V](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v)
