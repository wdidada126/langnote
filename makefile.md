# makefile
在 Makefile 中定义变量后，你可以使用 `$(`和`)` 或 `${`和`}` 来引用这些变量。以下是两种常用的引用变量的方式：

1. 使用 `$(` 和 `)`：
```
VARIABLE_NAME = value

target:
    $(VARIABLE_NAME)
```

在上述示例中，`$(VARIABLE_NAME)` 会被替换为变量 `VARIABLE_NAME` 的值。

2. 使用 `${` 和 `}`：
```
VARIABLE_NAME = value

target:
    ${VARIABLE_NAME}
```

在这个示例中，`${VARIABLE_NAME}` 也会被替换为变量 `VARIABLE_NAME` 的值。

无论使用哪种方式，当 Makefile 执行时，这些变量的引用部分都会被替换为其对应的值。

请注意，变量引用区分大小写。确保在引用变量时使用正确的大小写和变量名称。

此外，你还可以在变量引用中添加其他文本和命令，例如：
```
target:
    echo $(VARIABLE_NAME) is the value
```
这将在执行 `target` 目标时打印变量的值。

希望这个解释对你有所帮助！如果还有其他问题，请随时提问。


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