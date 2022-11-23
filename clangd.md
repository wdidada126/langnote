# clangd

centos 安装不了，源码编译？

https://github.com/clangd/clangd/releases/tag/12.0.0


https://clangd.llvm.org/


目前支持 LSP 协议的 IDE/Editor：

Visual Studio Code
Neovim
Sublime Text
Emacs
Fleet
Eclipse
...



echo $LD_LIBRARY_PATH



[wdidada@10-23-29-39 ~]$ cat /etc/ld.so.conf
include ld.so.conf.d/*.conf
[wdidada@10-23-29-39 ~]$ cd /etc/ld.so.conf.d
[wdidada@10-23-29-39 ld.so.conf.d]$ ls
bind-export-x86_64.conf  dyninst-x86_64.conf  kernel-3.10.0-1062.9.1.el7.x86_64.conf  kernel-3.10.0-1160.15.2.el7.x86_64.conf  llvm-x86_64.conf  mysql-x86_64.conf  postgresql-pgdg-libs.conf
[wdidada@10-23-29-39 ld.so.conf.d]$ pwd
/etc/ld.so.conf.d
[wdidada@10-23-29-39 ld.so.conf.d]$ vim /etc/ld.so.conf


http://blog.chinaunix.net/uid-25304914-id-3046279.html



Linux 动态库的默认搜索路径是 /lib 和 /usr/lib 。动态库被创建后，一般都复制到这两个目录中。当程序执行时需要某动态库， 并且该动态库还未加载到内存中，则系统会自动到这两个默认搜索路径中去查找相应的动态库文件，然后加载该文件到内存中，这样程序就可以使用该动态库中的函数，以及该动态库的其它资源了。在 Linux 中，动态库的搜索路径除了默认的搜索路径外，还可以通过以下三种方法来指定。方法一：在配置文件 /etc/ld.so.conf 中指定动态库搜索路径。每次编辑完该文件后，都必须运行命令 ldconfig 使修改后的配置生效 。方法二：通过环境变量 LD_LIBRARY_PATH 指定动态库搜索路径。export LD_LIBRARY_PATH = /share/lib: /usr/mylib方法三：在编译目标代码时指定该程序的动态库搜索路径。-Wl, 表示后面的参数将传给 link 程序 ld （因为 gcc 可能会自动调用ld ）。参数 "-Wl,-rpath," 指定。当指定多个动态库搜索路径时，路径之间用冒号 " ： " 分隔。# gcc -o pos main.c -L. -lpos -Wl,-rpath=.:..:lib#查看 可执行程序的 rpath
$ objdump -x 可执行程序| grep rpath搜索动态库的先后顺序编译目标代码时指定的动态库搜索路径LD_LIBRARY_PATH/etc/ld.so.cachedefault path /lib, and then /usr/lib.

作者：吾竹清风
链接：https://zhuanlan.zhihu.com/p/402426195
