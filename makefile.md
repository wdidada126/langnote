# makefile



http://blog.csdn.net/haoel/article/details/2886/
跟我一起写 Makefile（一）



https://seisman.github.io/how-to-write-makefile/overview.html
跟我一起写 Makefile（二）



命名规则
一般来说将Makefile命名为Makefile或makefile
自定义文件名

```shell
make -f XXX
```

基本规则
Makefile的基本规则为：
目标：依赖
test: test.c ​ gcc test.c -o test
其中，第一行中的test就是要生成的目标，test.c就是依赖，第二行就是由test.c生成test的规则
make clean:
清除编译过程中产生的中间文件（.o文件）及最终目标文件。



make linux可执行程序



makefile 生成这个问价的工具automake