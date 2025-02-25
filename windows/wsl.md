# wsl

以下是关于WSL Ubuntu所在文件夹以及配置Antimalware Service Executable让Microsoft Defender Antivirus Service不扫描的相关内容：

### WSL Ubuntu所在文件夹
在Windows系统中，WSL Ubuntu文件系统默认存储在`C:\Users\[用户名]\AppData\Local\Packages`文件夹下。进入该文件夹后，可以找到与Ubuntu相关的文件夹，一般以发行版名称和版本号命名，如`CanonicalGroupLimited.Ubuntu22.04LTS_79rhkp1fndgsc`等。进入这个文件夹后，在`LocalState`子文件夹中可以找到根文件系统等重要文件。

也可以在WSL Ubuntu系统内，通过命令行查看挂载的Windows系统路径，例如`/mnt/c`对应Windows系统的C盘，`/mnt/d`对应D盘等。

### 配置Antimalware Service Executable让Microsoft Defender Antivirus Service不扫描
1. **添加排除文件夹**
    - 打开Windows的“设置”，选择“更新与安全”。
    - 点击“Windows安全中心”，选择“病毒与威胁保护”。
    - 在“病毒与威胁保护设置”中，点击“管理设置”。
    - 找到“排除项”，点击“添加或删除排除项”，将WSL Ubuntu所在的文件夹路径添加到排除列表中，比如`C:\Users\[用户名]\AppData\Local\Packages\[Ubuntu相关文件夹]`以及Ubuntu系统内挂载的常用工作目录等，如`/mnt/c/Users/[用户名]/Documents`等你在WSL中经常使用到的文件夹。
2. **添加排除进程**
    - 按照上述同样的路径进入到“病毒与威胁保护”的“管理设置”中的“排除项”。
    - 点击“添加或删除排除项”，选择“进程”，输入在WSL Ubuntu中运行时不希望被扫描的进程名称，比如一些开发工具的进程等。
3. **更改扫描计划**
    - 按下`Win+R`，输入`taskschd.msc`，打开任务计划程序。
    - 在任务计划程序中找到与Windows Defender相关的任务，如“Windows Defender Scheduled Scan”等。
    - 右键点击这些任务，选择“属性”，在“常规”选项卡中，取消“使用最高权限运行”；在“条件”选项卡中，取消“只有在计算机使用交流电源时才启动此任务”等条件；在“触发器”选项卡中，可根据需要调整扫描的触发时间和频率，减少不必要的扫描。

