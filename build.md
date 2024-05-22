# build

Java也不能特别好的解决冲突问题，原因也很简单，jar依赖jar，那只要有版本要求不一样，就会有潜在的冲突风险。不过这几年加起来，我也只遇到过两三次就是了。相比起来c和c++的依赖处理简直是犯罪，不同平台，不同版本，不同编译器都……反正写c/c++的普遍没我头发多。Go早期一个gopath解决，后面改为vendor，甚至允许vendor嵌套，到现在用go mod，跟maven有异曲同工之妙了。


最著名的是linux系统的coreutils，包括一大堆常用工具，像cd、ls、who
https://github.com/northerntechie/coreutils-cpp/tree/main/src
https://www.zhihu.com/question/35080565/answer/1566402701


https://linux.cn/lfs/LFS-BOOK-7.7-systemd/chapter06/coreutils.html

purecpp大会就听过一个美女大佬介绍过这个项目

发现知乎上牛逼的C++开发大多数是做游戏的，貌似这个方向对C++水平要求很高，音视频对C++要求反而一般。

好歹用个函数内的static变量把这种全局变量封装起来啊。都8102年了，bison早就可以生成c++接口的parser了。

我们来对比一下windows和linux关于c语言这块谁更加方便的问题。很不幸，c/cpp是少数几个没有统一的包管理的语言之一，其他语言，比如go的module，ruby的gem，bundle，python的pip，rust的cargo，lua的rocks，php的Composer，先不论他们好不好用，至少他们有。这样你在开发c/cpp的时候难免会用到libxxx库。

