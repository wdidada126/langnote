# obsidian

还有 typora 这个恶心的公司前期养鱼，后期杀，1.0版本开始收费，而且价格比较贵，推荐你用 obsidian，更好用，而且支持笔记脑图关联。

https://obsidian.md/


obsidian打开md文件后
warning: in the working copy of 'java/mybatis/mybatis.md', LF will be replaced by CRLF the next time Git touches it

这个警告是由 Git 引起的，它表示在你的工作副本中，文件的换行符格式为 LF（即 Unix/Linux 下的换行符），但是 Git 会将其转换成 CRLF（即 Windows 下的换行符）。这种转换可能会导致一些问题，例如在 Windows 下使用 git diff 查看差异时，可能会出现换行符格式的问题，从而导致差异无法正确显示。

为了解决这个问题，你可以在 Git 中配置换行符的转换规则。具体来说，你可以在 Git 的配置文件（即 .git/config 文件）或全局配置文件（即 ~/.gitconfig 文件）中添加以下配置：

```
[core]
    autocrlf = input
```

这个配置会告诉 Git 在提交代码时将换行符转换为 LF，而在检出代码时不进行换行符转换。这样可以保持代码的换行符格式不变，避免出现上述问题。

另外，如果你使用的是 Windows 操作系统，并且使用的是 Git Bash 或 Git GUI 等 Git 工具，那么建议将终端的换行符格式设置为 LF，以避免类似的问题。你可以在 Git Bash 的选项中将“Text”选项卡下的“Default line ending”设置为“LF”，或者在 Git GUI 的“Options”菜单中将“Default line ending”设置为“LF”。