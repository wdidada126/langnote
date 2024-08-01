# bash

## 版本
bash-5.2.tar.gz	2022-09-26
bash-5.2.15.tar.gz	2022-12-13

## 官网
https://www.gnu.org/software/bash/

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


folder_name="my_folder"
把字符串赋值给变量，需要加引号,而且等号左右边不能有空格


check_and_create_folder() {
    if [ -d "$1" ]; then
        echo "Folder $1 exists. Deleting..."
        rm -r "$1"
    fi

    echo "Creating folder $1..."
    mkdir "$1"
}

#### 调用函数检测并处理文件夹
folder_name="my_folder"
check_and_create_folder "$folder_name"


在 Bash 脚本中，`$(pwd)` 和 `$pwd` 表达了不同的含义和行为。

1. `$(pwd)`: 这是命令替换（command substitution）的语法形式，它将命令的输出结果作为字符串进行替换。在这种情况下，`$(pwd)` 表示执行 `pwd` 命令并将其输出的当前工作目录作为字符串进行替换。因此，`$(pwd)` 将返回当前工作目录的路径。

   示例代码：
   ````bash
   #!/bin/bash

   current_path=$(pwd)
   echo "Current path: $current_path"
   ```

   当您运行该脚本时，`$(pwd)` 将在命令替换发生时返回当前的工作目录。

2. `$pwd`: 这是一个变量引用（variable reference），用于访问名为 `pwd` 的变量的值。在 Bash 中，`$` 后跟变量名用于引用该变量的值。但是，在默认情况下，`pwd` 并不是一个预定义的变量，因此 `$pwd` 通常表示空字符串。

   示例代码：
   ````bash
   #!/bin/bash

   pwd="Hello, World!"
   echo "The value of pwd variable: $pwd"
   ```

   当您运行该脚本时，`$pwd` 将被替换为变量 `pwd` 的值，即 `"Hello, World!"`。

综上所述，`$(pwd)` 表示执行 `pwd` 命令并返回当前工作目录的路径，而 `$pwd` 表示引用变量 `pwd` 的值。

希望这个解释能够帮助您理解 `$(pwd)` 和 `$pwd` 的区别。如果您有其他问题，请随时提问。


macOS 的早期版本（如 macOS Catalina 及之前版本）默认使用 Bash 作为系统的默认 shell。从 macOS Catalina 开始，macOS 将默认 shell 更改为 Zsh（Z shell），但是仍然会提供 Bash 作为备用选项。

