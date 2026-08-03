# WizTree

https://www.diskanalyzer.com/download

发现 C 盘快满了。打开 WizTree 一看，发现 .codex/sessions 占了 416.8GiB，气笑了。

特点：它是目前 Windows 下扫描速度最快的磁盘空间分析工具。因为它直接读取 NTFS 文件系统的 MFT（主文件表），而不是像 SpaceSniffer 那样一个个遍历文件夹。
扫描时间：扫描整个 1TB 的硬盘通常只需要 1-3 秒。你看到的 416.8G 那个大块头，就是在那一瞬间被它精准“逮捕”的。
操作：在 WizTree 界面里，你可以直接按 文件大小排序，然后右键那个最大的文件或文件夹，选择“打开位置”或直接“删除”。
个人使用免费：WizTree 对个人用户是免费的，商业使用才需要付费