# ninja

yum install cmake -y
yum install ninja-build -y

类似于make，编译速度快

cmake生成build.ninja

chrome source code

ninja -c build


[The Ninja build system]( https://ninja-build.org/manual.html)

vs支持cmake，就是用ninja这个generator

clion不支持ninja

ninja类似make
build.ninja这个文件
make使用makefile






[使用 Ninja 代替 make](https://blog.csdn.net/rankun1/article/details/80420301)


当直接执行 ninja 命令是，它会在当前目录下默认寻找 build.ninja 文件来进行编译。
ninja 的语法格式是：

ninja [options] TARGETs
上述 options 如果没有则可以省略。比如，直接执行 ./ninja ninja_test 将会生成可执行文件 ninja_test，然后再执行 ninja_test 就可以看到测试结果。


