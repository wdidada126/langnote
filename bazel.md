# bazel

Bazel 6 新增了 bzlmod ，支持了包的多版本管理，可以解决菱形依赖的问题。已经完全成熟可用了。
https://bazel.build/build/bzlmod

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

## bazel6

### 安装
yum install bazel4 -y

windows上支持java？

sudo apt install apt-transport-https curl gnupg -y
curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg
sudo mv bazel-archive-keyring.gpg /usr/share/keyrings
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
sudo apt update && sudo apt install bazel

