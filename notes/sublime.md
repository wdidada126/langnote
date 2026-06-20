# sublime

有时，我们可能需要将文件中的换行符替换为其他字符，比如英文逗号、分号等。

利用 Sublime编辑器可以很容易实现，且有两种方法。
第一种方法
第一步，使用快捷键 Ctrl + H，打开查找替换窗口。
第二步，在查找框输入 Ctrl + Shift + Enter，替换框输入英文逗号。
第三步，点击 Replace All 即可。
第二种方法
另外一种方法，就是使用正则表达式（Regular expression）替换。
第一步，使用快捷键 Ctrl + H，打开查找替换窗口。然后，按下 Alt + R 快捷键开启正则替换模式。
第二步，在查找框输入 \n，替换框输入英文逗号。
第三步，点击 Replace All即可。

https://blog.csdn.net/lamp_yang_3533/article/details/96765402

打开文件夹

## 正则表达式查找替换
要将 Sublime Text 中的空格替换为换行符，你可以使用 Sublime Text 的查找和替换功能，并使用特殊字符表示空格和换行符。下面是在 Sublime Text 中如何完成这个操作：
1. 打开 Sublime Text 编辑器。
2. 使用快捷键 `Ctrl + H`（在 Windows 和 Linux 系统上）或 `Cmd + Option + F`（在 macOS 上）打开查找和替换功能。
3. 在弹出的查找和替换面板中，点击输入框旁边的 `.*` 图标，启用正则表达式模式。
4. 在查找框中输入 `\s+`，这表示匹配一个或多个空格。
5. 在替换框中输入 `\n`，这表示换行符。
6. 确认你想要替换的是所有匹配，然后点击替换按钮或按下 `Alt + Enter`（在 Windows 和 Linux 系统上）或 `Ctrl + Command + Enter`（在 macOS 上）来执行替换操作。
这样，Sublime Text 将会将所有的空格替换为换行符。请确保在操作之前备份你的文件，以防出现意外情况。