# dirname

http://www.gnu.org/software/coreutils/
coreutils是GNU操作系统中的标准工具集，包括以下几个命令：

1. `ls`：列出目录内容。
2. `cp`：复制文件或目录。
3. `mv`：移动或重命名文件或目录。
4. `rm`：删除文件或目录。
5. `cat`：连接文件并打印到标准输出设备上。
6. `more`、`less`：分页显示文件内容。
7. `head`、`tail`：显示文件的开头几行或结尾几行。
8. `grep`：在文件中搜索指定的字符串。
9. `find`：在文件系统中查找文件。
10. `chmod`、`chown`、`chgrp`：修改文件或目录的权限和所有权。
11. `df`：显示磁盘空间使用情况。
12. `du`：显示目录或文件的磁盘使用情况。
13. `sort`：对文本文件进行排序。
14. `uniq`：去除重复行。
15. `wc`：统计文件的行数、单词数和字节数。


cd `dirname $0`
解释：$0当前Shell程序的文件名
dirname $0，获取当前Shell程序的路径
cd `dirname $0`，进入当前Shell程序的目录

https://blog.csdn.net/sunflowerfsw/article/details/52240270

https://blog.csdn.net/peter_cloud/article/details/9308333
https://blog.csdn.net/qq_27870421/article/details/93724188

dirname命令用于获取文件路径中的目录部分。它返回给定文件路径的父目录路径。

[wdidada@10-23-29-39 bin]$ dirname /home/wdidada/
/home
[wdidada@10-23-29-39 bin]$ dirname /home/wdidada/testmavenplugin-1.0-SNAPSHOT
/home/wdidada
[wdidada@10-23-29-39 bin]$ dirname /home/wdidada/testmavenplugin-1.0-SNAPSHOT/bin/
/home/wdidada/testmavenplugin-1.0-SNAPSHOT
[wdidada@10-23-29-39 bin]$ dirname /home/wdidada/testmavenplugin-1.0-SNAPSHOT/bin/restart.sh 
