# less

zless

：G进入最后一行

进入vi？
按v可以直接调用vi进行编辑

less -V
less 458 (GNU regular expressions)
Copyright (C) 1984-2012 Mark Nudelman

less comes with NO WARRANTY, to the extent permitted by law.
For information about the terms of redistribution,
see the file named README in the less distribution.
Homepage: http://www.greenwoodsoftware.com/less

在 Linux 系统中，可以使用 `less` 命令来编辑文件。当文件内容过长时，可以使用以下方法进入 Vim 编辑器进行编辑：

1. 打开终端。
2. 使用 `less` 命令打开文件，例如：`less /path/to/your/file.txt`。
3. 按下 `:e` 键，进入 Vim 编辑器。
4. 在 Vim 编辑器中进行编辑操作。
5. 保存并退出 Vim 编辑器，可以按下 `:wq` 键。

在 less 查看器中，? 和 / 都是搜索命令，但搜索方向相反：
/ 是向前搜索（向下搜索），从当前位置向文件末尾方向查找匹配的内容。
? 是向后搜索（向上搜索），从当前位置向文件开头方向查找匹配的内容。
使用 n 键可以重复上一次搜索方向，N 键则反向重复搜索。例如，使用 /keyword 搜索后，按 n 会继续向下查找下一个匹配项，按 N 会向上查找上一个匹配项。