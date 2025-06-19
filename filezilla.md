# filezilla

ubuntu系统编译FileZilla3
ubuntu跨平台编译win下的可执行文件

svn switch https://svn.filezilla-project.org/svn/FileZilla3/tags/3.56.0
configure: error: You must use wxWidgets 3.0.x, wxWidgets 3.2 or higher is not yet supported.

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


## libfilezilla
https://lib.filezilla-project.org/doc/
libfilezilla是啥，哪儿可以下载


libfilezilla是一个小型的现代C++ 库，用于构建高性能、跨平台的程序。它提供了一些基本功能，比如类型安全的多线程事件系统、用于定期事件的定时器、处理TCP通信的套接字类、TLS层安全通信、限速套接字层控制流量、处理时间戳的日期时间类以及简单的进程处理等。

libfilezilla的下载方式如下：
- 使用包管理工具（以GNU Guix为例）：如果你使用的是GNU Guix包管理系统，可以在终端输入`guix install libfilezilla`来安装最新版本，也可以指定版本安装，如`guix install libfilezilla@0.39.2`。
- 从FileZilla官方网站下载：FileZilla官方网站是获取libfilezilla的可靠来源。你可以访问[FileZilla官方网站](https://lib.filezilla-project.org/doc/)，在相关文档和资源中找到libfilezilla的下载链接或获取源代码的指引。
- 从软件源下载：对于一些常见的操作系统，其软件源中可能包含libfilezilla。例如，在基于Linux的系统中，你可以使用系统的包管理工具，如Ubuntu中的`apt`，Fedora中的`dnf`等，通过搜索`libfilezilla`来查找并安装可用版本。

svn co https://svn.filezilla-project.org/svn/libfilezilla/trunk libfilezilla
