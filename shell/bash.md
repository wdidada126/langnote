# bash
Bash 脚本教程 

此时，你需要阮一峰老师写的一本小册：《 Bash 脚本教程 》。

https://www.ruanyifeng.com/blog/2020/04/bash-tutorial.html

https://wangdoc.com/bash/



 
1 简介
 
2 基本语法
 
3 模式扩展
 
4 引号和转义
 
5 变量
 
6 字符串操作
 
7 算术运算
 
8 操作历史
 
行操作
 
目录堆栈
 
脚本入门
 
read 命令
 
条件判断
 
循环
 
函数
 
数组
 
set 命令，shopt 命令
 
脚本除错
 
mktemp 命令，trap 命令
 
启动环境
 
命令提示符

学习bash编程时，应该养成哪些好的习惯？
https://www.zhihu.com/question/29357844/answer/129328743

bash调试
-u

https://zhuanlan.zhihu.com/p/427490686
### 检测环境变量

compile.sh

### 判断语句

if

fi




升级gclic

```shell
unlink /lib64/libc.so.6
ln -s libc-2.14.so /lib64/libc.so.6
ll libc.so.6
strings /lib64/libc.so.6 |grep GLIBC_
```


```shell
bash --help
GNU bash, version 4.2.46(2)-release-(x86_64-redhat-linux-gnu)
Usage:	bash [GNU long option] [option] ...
	bash [GNU long option] [option] script-file ...
GNU long options:
	--debug
	--debugger
	--dump-po-strings
	--dump-strings
	--help
	--init-file
	--login
	--noediting
	--noprofile
	--norc
	--posix
	--protected
	--rcfile
	--rpm-requires
	--restricted
	--verbose
	--version
Shell options:
	-irsD or -c command or -O shopt_option		(invocation only)
	-abefhkmnptuvxBCHP or -o option
Type `bash -c "help set"' for more information about shell options.
Type `bash -c help' for more information about shell builtin commands.
```