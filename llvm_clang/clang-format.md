·# clang-format

预览格式化后的代码，就是直接把格式化后的代码显示在终端。

clang-format main.cpp
直接在源文件上格式化代码

clang-format -i main.cpp
设置格式化代码的风格

clang-format -style=google main.cpp
以上的命令在Windows下需要用.\clang-format.exe代替clang-format。