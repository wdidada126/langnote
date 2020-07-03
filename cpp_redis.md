# redis源码



https://blog.csdn.net/breaksoftware/article/details/53435940



一般来说，依赖库都是开源的第三方库。上图可见Redis需要在内部使用到：

Lua脚本引擎。Redis内嵌Lua脚本引擎，那么说明Redis需要Lua语言的解析能力。那么可以进一步猜测应该是用户可以定制Lua脚本让Reids去执行，这相当于Redis开放了一个非常自由的接口供外部使用。
Linenoise是一个命令行编辑库。这个正是我们之前预估的Redis基础功能之一。它的相关资料可见https://github.com/antirez/linenoise
Jemalloc是内存管理库。很多开源项目不使用glibc自带的ptmalloc，而是使用Jemalloc或者Tcmalloc这类更高效的内存管理库。
Hiredis是Redis数据库的C接口。这块和Redis相关性比较大，我们之后也会重点关注下。
Geohash-int是一种地理编码算法。它将二维经纬度信息转换成Int型数据。
————————————————
版权声明：本文为CSDN博主「breaksoftware」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/breaksoftware/article/details/53435940