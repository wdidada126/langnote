# bash

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