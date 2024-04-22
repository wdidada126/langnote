# gdb

## ubuntu/debian安装gdb
在Ubuntu 20.04上安装GDB（GNU Debugger）的步骤如下：
打开终端，可以通过按下Ctrl + Alt + T组合键来快速打开终端。
运行以下命令更新软件包列表：

```bash
sudo apt update
```

安装GDB：

```bash
sudo apt install gdb -y
```

在安装过程中，系统可能会要求您提供管理员密码进行确认。
4. 安装完成后，您可以通过运行以下命令来验证GDB是否成功安装：

```bash
gdb --version
```

如果成功安装，终端将显示GDB的版本信息。
现在，您已经成功在Ubuntu 20.04上安装了GDB。您可以使用它来调试和分析程序，以帮助您解决软件开发中的问题。
如果您想在GDB中安装并使用PEDA插件（一个用于GDB的Python脚本，用于增强调试功能），可以按照以下步骤进行：
确保已安装gdb-multiarch和gcc：

```bash
sudo apt-get install gdb-multiarch  
sudo apt-get install gcc
```

下载gdb-peda的源文件：
```bash
git clone https://github.com/longld/peda.git ~/peda
```

将PEDA添加到GDB的初始化脚本中：
```bash
echo "sour
```


问：g++ 生成gdb调试信息
答：

[GDB的基本工作原理](https://blog.csdn.net/weiwangchao_/article/details/11884639)

1. 背景
程序的发布方式有两种，debug模式和release模式
debug 通常称为调试版本，它包含调试信息，并且不作任何优化，便于程序员调试程序。
Release 称为发布版本，它往往是进行了各种优化，使得程序在代码大小和运行速度上都是最优的，以便用户很好地使用。
Linux gcc/g++编译出来的二进制程序，默认是release模式
因此要使用gdb调试，必须在源代码生成二进制程序的时候, 加上 -g 选项
2. gdb调试界面命令汇总
进入：gdb binFile
退出：ctrl + d 或 quit/q

调试命令：

l(list) 行号：显示binFile源代码，接着上次的位置往下列，每次列10行。
l(list) 函数名：列出某个函数的源代码。
r(run)：运行程序。
n(next）：逐过程执行(不会进入函数内部)。
s(step)：逐语句执行
b(break) 行号：在某一行设置断点
b(break) 函数名：在某个函数开头设置断点
i b(info break) ：查看断点信息。
disable 断点号：禁用断点
enable 断点号：启用断点
p(print)：打印表达式的值，通过表达式可以修改变量的值或者调用函数
p 变量：打印变量的值。
bt/where：当前函数的调用堆栈，显示的结果由下至上为函数的调用顺序
f(floor) 函数序号：显示某一正在调用的函数的临时变量的信息。
finish：执行到当前函数返回，然后停下来等待命令
set var：修改变量的值
c(continue)：从当前位置开始连续而非单步执行程序
delete breakpoints：删除所有断点
delete breakpoints n：删除序号为n的断点
i(info) breakpoints：参看当前设置了哪些断点
display 变量名：跟踪查看一个变量，每次停下来都显示它的值
undisplay：取消对先前设置的那些变量的跟踪
until X(行号)：跳至X行
breaktrace(或bt)：查看各级函数调用及参数
info（i) locals：查看当前栈帧局部变量的值
q(quit)：退出gdb


那么，gdb到底是凭什么接管的一个进程的执行呢？其实，很简单，通过一个系统调用：ptrace。ptrace系统调用的原型如下：

```c

#include <sys/ptrace.h>
long ptrace(enum __ptrace_request request,  pid_t pid, void *addr, void *data);

```
说明：ptrace系统调用提供了一种方法来让父进程可以观察和控制其它进程的执行，检查和改变其核心映像以及寄存器。 主要用来实现断点调试和系统调用跟踪。（man手册）
其实，说到这里，一切原理层面应该都比较明朗了（且先不去管内核中是怎么实现ptrace的）。gdb就是调用这个系统调用，然后通过一些参数来控制其他进程的执行的。

https://blog.csdn.net/weiwangchao_/article/details/11884639

b -- break

gdb-subscribe@sourceware.org

https://www.gnu.org/software/gdb/documentation/





https://blog.csdn.net/xiongxinlei/article/details/78119714





gdb调试技巧

gdb disas clion debug（注意不是run） 进断点后，

clion gdb界面 输入disas

https://www.cnblogs.com/Forever-Kenlen-Ja/p/8631663.html

![clion gdb disas](../imgs/clion_gdb_disas.png)




[使用GDB对程序进行汇编级调试](http://www.cnblogs.com/diylab/archive/2009/07/16/1524483.html)



 下断点
 (gdb) b *0x0804ce2b
  b 表示 break

 单步步过
 (gdb) ni  (next instruction)
 单步步入 
 (gdb) si  ( step instruction )
 继续执行
 ( gdb )c

 执行到返回

