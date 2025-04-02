# filezilla

filezilla server windows设置登录用户
设置路径映射 windows的路径 G:\BaiduYunDownload

FileZilla发展了很多年，一直是张小方使用的高频软件，其代码质量非常高，尤其是 C++11 标准问世以来，作者也与时俱进，最新的 FileZilla 代码使用 C++17 标准改写，学习这套源码可以学习到大量的 C/C++ 开发技巧和经验。

https://filezilla-project.org/sourcecode.php

https://svn.filezilla-project.org/filezilla/FileZilla3/

https://wiki.filezilla-project.org/Client_Compile


## svn

TortoiseSVN下载后没有`svn.exe`文件，是因为在安装过程中没有选择安装命令行客户端工具，解决办法是重新运行安装程序进行补装。具体步骤如下：
1. 找到TortoiseSVN的安装包，如果是从官网下载的，通常可以在下载目录中找到；如果是通过软件管家等工具下载的，可以在软件管家的下载目录或安装包缓存目录中查找。
2. 双击运行安装包，进入安装向导界面。
3. 在安装向导的步骤中，找到类似于“Custom Setup”（自定义安装）或“Features Selection”（功能选择）的界面。
4. 展开“Command Line Client Tools”（命令行客户端工具）选项，将其设置为“Install”（安装）。默认情况下，该选项可能是未选中状态。
5. 继续按照安装向导的提示完成安装。安装完成后，`svn.exe`文件就会被安装到TortoiseSVN的安装目录下的`bin`子目录中，例如`C:\Program Files\TortoiseSVN\bin`。