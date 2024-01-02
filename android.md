# 编译系统源码

https://developer.android.com/studio/releases/gradle-plugin?hl=zh-cn

ffmpeg android

http://trac.ffmpeg.org/wiki/CompilationGuide/Android

./configure

https://www.jianshu.com/p/feab970fd74c

ndk历史版本

https://developer.android.com/ndk/downloads/older_releases.html

Android develop

https://developer.android.google.cn/

https://www.androiddevtools.cn/ 错误，没更新

https://developer.android.google.cn/studio/releases/platform-tools?hl=zh-cn


安卓framework层代码
https://www.zhihu.com/question/350047125/answer/859822575

看一下 腾讯 Matrix 的源码，就知道 Framework 的知识有多重要了。像掉帧监控，函数插桩，慢函数检测，ANR 监控，启动监控，都需要对 Framework 有比较深入的了解，才能知道怎么去做监控，利用什么机制去监控，函数插桩插到哪里，反射调用该反射哪个类哪个方法哪个属性……另外 Framework 作为 Android 框架层，为 App 提供了众多 API 去调用 ，但是很多机制都是 Framework 包装好了给 App 来用的，如果不知道这些机制的原理，那么很难去在这基础上做优化。举个例子，如果你了解 Android App 的启动机制，优化启动速度的时候会更得心应手：定制什么样的 StartingWindow；什么时候可以拿到图片的宽高；DelayLoad 怎么做才会更合适；Service 什么时候启动可以不影响启动速度；Activity onResume 回调的时候真的可见了么？Redex 为什么会加快应用启动速度？ContentProvider 会不会影响启动速度？为什么会影响？再比如我们经常说的 Handler，MessageQueue，Looper。看源码你就可以更好的理解那些概念：ThreadLocal 做什么的；Thread 和 Handler 的关系；为什么不能在子线程更新 UI？idleHandler 什么时候运行？ 主线程为什么循环却不会卡死？ContentProvider、Broadcast、Service 是怎么利用 Message 监控 ANR 的？再比如说 Android 的进程管理机制。AMS 把 Android 进程按照一定的规则，设置不同的优先级，在内存比较低的时候，高优先级的 App 比低优先级的 App 更不容易被系统干掉！那么 AMS 是按照什么规则来设置优先级的呢？了解这些规则是不是可以提高 App 的存活率呢？这都是可以通过熟读 AMS 代码知道的。再比如说 Activity 启动的模式，可能你会熟练使用各种模式，但是如果你学习 Framework 中 Activity 和进程的管理，知道 Activity 栈和 Task 的管理。那么你会对这启动模式的使用更加深刻。

https://github.com/Tencent/matrix

这个是第一个步骤，我们需要获取到symbols才能在gdb调试的时候attach到对应的源码上。
我编译的是 Android 8.1.0 的源码，编译过程可以参照官方文档：https://source.android.com/setup/initializing

使用模拟器运行或者刷机运行系统
我没有对应的手机刷机，所以使用了模拟器来运行编译后的系统。
编译好系统之后，在根目录使用emulator命令就可以启动模拟器了
如果提示没有emulator命令，则需要重新初始化环境变量

http://dodola.top/2018/03/14/GDBGUI-Android/

Linux Assembly

http://dodola.top/2017/01/22/linux_assembly/





termux上看，termux的用户是u108之类的



虚拟机厂商ge

sky

检测应用性能





