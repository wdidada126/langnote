# pkg-config

pkg-config --cflags --libs log4cpp
-pthread -I/usr/local/include -L/usr/local/lib -llog4cpp

cmake CMakeLists.txt
maven pom.xml
pkg-config .pc

sudo apt-get install pkg-config

什么是pkg-config
pkg-config是一个linux下的命令，用于获得某一个库/模块的所有编译相关的信息。

例子：

pkg-config opencv –libs –cflags

结果：

-I/usr/include/opencv

/usr/lib/x86_64-linux-gnu/libopencv_calib3d.so

https://www.cnblogs.com/rainsoul/p/10567390.html

pkg-config --cflags --libs libcurl
-I/usr/include/x86_64-linux-gnu -lcurl
