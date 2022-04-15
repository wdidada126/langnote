# bazel


IDEA有bazel插件

Bazel 默认支持多种开发语言，如Java，C++，Javascript, Android

为什么我要使用Bazel？
Bazel可以成倍提高构建速度，因为它只重新编译需要重新编译的文件。类似的，它会跳过没有被改变的测试。
Bazel产出确定的结果。这消除了增量和干净构建，开发机器和持续集成之间的构建结果的差异。
Bazel可以使用同一个工程下的相同的工具来构建不同的客户端和服务器端应用程序。例如，你可以在一次提交里修改一个客户端/服务器协议，然后测试更新后的手机程序和服务器端程序能够正常工作，构建时使用的是同样的工具，利用的都是上面提到的Bazel的特性。
我可以看到例子吗？
是的，一个简单的例子，见：
https://github.com/google/bazel/blob/master/examples/cpp/BUILD

Bazel源代码本身提供了更复杂的例子，例如：
https://github.com/google/bazel/blob/master/src/main/java/BUILD
https://github.com/google/bazel/blob/master/src/test/java/BUILD


### 安装
 yum install bazel4 -y



windows上支持java？