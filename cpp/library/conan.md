# conan

查看它的包描述。
$ conan inspect poco/1.9.4
 conan profile new default --detect  # Generates default profile detecting > GCC and sets old ABI
$ conan profile update settings.compiler.libcxx=libstdc++11 default  # Sets libcxx to C++11 ABI

如果特定配置的二进制包不存在conan将会抛出一个错误。
使用conan install .. --build=missing来从源码构建你需要的二进制包，当然这需要你要的二进制配置被包的说明文件所支持。

https://ccup.github.io/conan-docs-zh/05-creating-packages.html

## conan generators

https://docs.conan.io/en/latest/reference/generators.html#generators-reference


conan new会在当前文件夹下生成conanfile.py
如果开发人员要作为生产者角色(producer),把自己的项目也封装成conan包上传到conan服务器供第三方使用，conanfile.txt是不能满足要求的，必须使用全能的confile.py脚本来定义包的配置,事实上conan在分发包时就是基于python脚本的灵活性通过conanfile.py来定义包的全部配置的。所以当我们执行conan new命令创建一个新的conan配置时，自动生成的是conanfile.py脚本。
https://docs.conan.io/1/reference/conanfile.html

Options
我们看到在执行conan install的时候可以指定配置。例如conan install .. -s build_type=Debug。这里指定的一般都是客户机器上的项目级别的配置，一般没法在包配置中指定默认值。例如，在包配置中指定使用“Visual Studio”作为默认编译期就不合理，因为类似这些配置最好由最终用户指定，否则对于在linux工作上的用户就不友好。

但是包配置中的[options]最好用于指定包普遍适用的配置，以及指定默认值。例如一个包可以指定默认为静态链接，这样用户一般情况就不用再指定了。

可以使用类似conan get poco/1.9.4@的命令查看指定包的的options。也可以通过conan inspect命令，如下：

$ conan inspect poco/1.9.4@ -a=options
$ conan inspect poco/1.9.4@ -a=default_options

## conan profiles
https://ccup.github.io/conan-docs-zh/04-using-package.html#%E4%BD%BF%E7%94%A8profiles

https://docs.conan.io/1/reference/profiles.html


cat .conan2/profiles/default
[settings]
arch=x86_64
build_type=Release
compiler=gcc
compiler.cppstd=gnu14
compiler.libcxx=libstdc++11
compiler.version=9
os=Linux

`libstdc++` 是 GNU C++ 标准库的实现，它提供了 C++ 标准库的各种功能和特性。而 `libstdc++11`、`libstdc++14`、`libstdc++17` 是 `libstdc++` 的不同版本，它们对应于不同的 C++ 标准。
下面是它们之间的区别：
1. `libstdc++11`：这是对应 C++11 标准的 `libstdc++` 版本。C++11 是 C++ 标准的一个重要版本，引入了许多新的语言功能和库特性，如 lambda 表达式、右值引用、线程支持等。`libstdc++11` 包含了 C++11 标准库的实现。
2. `libstdc++14`：这是对应 C++14 标准的 `libstdc++` 版本。C++14 是 C++ 标准的下一个版本，对 C++11 进行了一些扩展和改进。它添加了一些新功能，如二进制字面量、泛型 lambda 表达式、`constexpr` 函数的放宽要求等。`libstdc++14` 包含了 C++14 标准库的实现。
3. `libstdc++17`：这是对应 C++17 标准的 `libstdc++` 版本。C++17 是 C++ 标准的下一个版本，引入了一系列新功能和改进，如结构化绑定、`if constexpr`、折叠表达式等。`libstdc++17` 包含了 C++17 标准库的实现。
每个版本的 `libstdc++` 实现了相应版本的 C++ 标准，并提供了相应的功能和特性。因此，选择使用哪个版本取决于您的项目需求和目标平台的支持情况。通常情况下，您应该选择与您的编译器和目标平台兼容的版本。

需要注意的是，不同的编译器可能具有不同的命名约定和默认版本。因此，确保在编译代码时正确配置编译器选项，以便使用所需的 `libstdc++` 版本。
ERROR: Invalid setting 'libstdc++17' is not a valid 'settings.compiler.libcxx' value.
Possible values are ['libstdc++', 'libstdc++11']

conan 需要python文件去定义
xmake 需要lua文件去定义

## template
templates: basic,
cmake_lib, cmake_exe, meson_lib, meson_exe,
msbuild_lib, msbuild_exe, bazel_lib, bazel_exe,
autotools_lib, autotools_exe. E.g. 'conan new
cmake_lib -d name=hello -d version=0.1'. You can
define your own templates too by inputting an absolute
path as your template, or a path relative to your
conan home folder.
## 安装特定版本的conan
pip3 install conan==1.62.0

conan server
virtual = local + remote
local仅仅是本地的
remote是远程的
这个跟maven不一样
https://blog.51cto.com/u_15926338/5979962

https://github.com/conan-io/conan

Decentralized, open-source (MIT), C/C++ package manager.

Homepage: https://conan.io/
Github: https://github.com/conan-io/conan
Docs: https://docs.conan.io
Slack: https://cpplang.slack.com (#conan channel. Please, click here to get an invitation)
Twitter: https://twitter.com/conan_io

https://conan.io/center

Conan是一款免费开源的C/C++语言的依赖项和包管理器，适用于所有平台，包括Windows、Linux、OSX、FreeBSD、Solaris等。它集成了所有构建系统，例如：CMake、Visual Studio（MSBuild）、Makefiles、SCons等。

## conan server

JFrog Artifactory Community Edition

bintray.com/conan是一个用于存储和分发C/C++语言依赖项和包的在线平台，它由Bincrafters团队维护并开放给OSS社区使用。你可以把它想象为一个仓库，这里包含了大量由贡献者创建的各种各样的Conan包。
Conan本身是一款免费开源的依赖项和包管理器，适用于所有平台，包括Windows，Linux，OSX，FreeBSD，Solaris等。它使用起来非常灵活，可以应用于各种开发目标，包括嵌入式、移动（iOS，Android）和裸机。此外，它还与所有build系统集成，如CMake，Visual Studio（MSBuild），Makefiles，SCons等，以及其他专有系统。
在分布式的架构中，Conan遵循客户端-服务器模式。在这种模式下，客户端可以从不同的远端服务器上获取或上传包。服务端主要负责包的存储，并不负责包的构建和生成。实际上，包的构建和生成都在客户端完成。

JFrog，现更名为捷蛙科技（北京）有限公司，是一家全球领先的软件分发和管理解决方案提供商。公司成立十多年以来，在全球拥有成千上万的客户和数百万用户，已成为DevOps数据库与版本和更新管理领域不可忽视的标准。

其主要产品包括JFrog Artifactory企业制品库和JFrog Platform混合DevOps平台。JFrog Artifactory支持所有开发语言，是整个DevOps流水线中所有软件包、容器映像和Helm图表的单一数据源。它具备丰富的元数据和资产可见性，可以自动化开发生命周期。而JFrog Platform则是一个通用的、端到端的混合DevOps平台，通过二进制文件管理、CI/CD流水线和DevSecOps工具自动执行从构建到生产的软件升级。

这些产品和服务的核心目标是实现“流式软件”的愿景，即允许二进制制品从开发端无缝、安全地流向边缘应用节点。

Conan是一个开源的、跨平台的、去中心化的C++包管理器，它允许您安装、解决构建依赖，更重要的是可以直接集成到Build System中使用。同时，它也支持私有仓库的搭建，以满足私有项目的需求。

要搭建Conan私有仓库，首先需要在服务器上安装Conan。然后，可以使用以下命令创建一个新的私有仓库：

```bash
conan create . user/channel
```

其中，`.`表示要将新仓库创建在当前目录下，`user`是用户名，`channel`是频道名称。您可以根据实际需求自行更改这些值。
此外，如果您正在使用Artifactory，也可以快速方便地搭建Conan私有仓库。具体来说，可以参考JFrog官网上的文档来进行设置和配置。
在NVD（美国国家漏洞数据库）提供的CVE（公共漏洞和暴露）的基础上，JFrog还提供了VulnDB这一商业漏洞数据库。而VulnDB提供了更大范围的安全漏洞数据


https://blog.csdn.net/qqqq123qqqqqqq/article/details/79421686

https://blog.csdn.net/h511555/article/details/8904143

https://conan.io/

通用的 C++ 软件包管理器

https://www.infoq.cn/article/does-cpp-need-a-universal-package-manager

C++ 在软件包管理器上并不存在短板。当前有大量的工具可用，例如
[buckaroo](https://www.buckaroo.pm/)、
[cget](http://cget.readthedocs.io/en/latest/)、
[conan](https://conan.io/)、
[conda](https://conda.io/docs/)、
[cpm](http://www.cpm.rocks/)、
[cppan](https://cppan.org/)、
[hunter](https://docs.hunter.sh/en/latest/)
等等，不胜枚举。

https://github.com/LoopPerfect/buckaroo/

https://bintray.com/conan/conan-center

官网搜索
搜索库
maven 在官方仓库搜索，根据group arfitfect搜索
conan search grpc
xrepo search grpc
用'conan search mysql'搜索不出来

pistache 只支持Linux目前

pistache/d5608a1@conan/stable: Downloaded recipe revision 0
ERROR: pistache/d5608a1@conan/stable: Error in configure() method, line 24
        raise ConanException("Only Linux supported")
        ConanException: Only Linux supported

conan找不到mysqlclient

folly

Pistache

有Poco

https://github.com/conan-io/conan

油管博主 @Lötwig Fusel
https://www.youtube.com/watch?v=T6RZ5On3xz8
https://zhuanlan.zhihu.com/p/613174589

合肥某车企，招聘conan ci/cd工程师

conan支持企业内部自建库管理，conan下载一个库，先编写conanfile文件，然后下载到本地文件夹

Conan是一个开源的C++包管理器，它主要用于方便地安装、管理和使用C++开发中的各种库和工具。它并不直接提供搭建公司内部仓库的功能，但是可以作为公司内部仓库的一个组成部分。
要搭建公司内部的Conan仓库，可以按照以下步骤进行：
在公司内部服务器上安装Conan服务端。
Conan服务端是一个基于Python的Web应用程序，它提供了Conan仓库的存储和管理功能。安装Conan服务端时，需要确保服务器上已经安装了Python和相关的依赖库。
配置Conan服务端。
安装完成后，需要对Conan服务端进行配置。配置内容包括设置仓库名称、设置仓库中保存的包信息、设置用户和权限等。
部署Conan客户端。
Conan客户端是用于与Conan服务端进行 交互的工具。在公司内部，需要为每个开发人员部署Conan客户端，并确保他们使用相同的配置。
上传包到Conan仓库。
当开发人员完成了C++库的开发后，可以使用Conan客户端将库文件上传到Conan服务端。上传时需要指定包的名称、版本号和相关信息。
配置其他开发工具使用内部仓库。
最后，需要配置其他开发工具（如Visual Studio、Eclipse等）使用公司内部的Conan仓库。配置方法因开发工具而异，一般需要在开发工具的选项中指定Conan仓库的地址和凭据信息。
综上所述，Conan本身并不提供完整的公司内部仓库搭建功能，但可以作为公司内部仓库的一个组成部分，方便开发人员管理和使用C++库和工具。如需搭建公司内部仓库，可以结合使用其他工具和方法来实现。

可以按照以下步骤在CentOS 7.2上安装Conan Server：

安装Conan Server
在CentOS 7.2上安装Conan Server需要先安装Python和一些Python依赖库。首先，使用以下命令安装Python：

```shell
sudo yum install -y python
```
然后，使用以下命令安装pip（Python包管理工具）：

```shell
sudo yum install -y python-pip
```
接下来，使用pip安装Conan Server：

```shell
    sudo pip install conanserver
```
安装完成后，您可以使用以下命令启动Conan Server：

```shell
sudo conanserver start
```
配置Conan Server
Conan Server的配置文件位于~/.conan/server.conf。您可以使用文本编辑器打开该文件，根据您的需求进行配置。例如，您可以设置管理员权限、禁用PVP等。
3. 设置虚拟环境

为了使用Conan Server，您需要创建一个虚拟环境。可以使用以下命令创建一个新的虚拟环境：

```shell
sudo conan env create --file=conans/myenv.yml
```
其中，conans/myenv.yml是包含虚拟环境配置的文件。您可以根据您的需求修改该文件中的内容。然后，使用以下命令激活虚拟环境：

```shell
sudo conan env activate myenv
```
创建和管理Conan仓库
Conan Server可以用于创建和管理Conan仓库。您可以使用以下命令创建一个新的Conan仓库：

```shell
sudo conan new myrepo/1.0.0 -g=BASIC -u=myusername -p=mypassword --url=https://myrepo.com
```
其中，myrepo是您为仓库取的名称，1.0.0是您为仓库设置的版本号。-g=BASIC表示使用基本认证方式，-u=myusername和-p=mypassword表示设置用户名和密码，--url=https://myrepo.com表示设置仓库的URL。您需要将myrepo、1.0.0、myusername、mypassword和https://myrepo.com替换为您自己的值。然后，使用以下命令激活虚拟环境：source activate myenv。

conan可以支持cmake autotools
qmake
msbuild
跨平台

nget支持windows

Conan_examples
https://github.com/conan-io/examples

https://gitee.com/edidada/estconan

pip install conan
pip3 install conan

https://docs.conan.io/en/latest/installation.html

要求python3吗？

conan search grpc -r conancenter


默认远程地址 conancenter

默认配置文件
~/.conan/conan.conf
编译

conan install .

conan install -c conxxx.txt
conanfile.txt
```
[requires]
# gtest/1.8.0@lasote/stable
# zlib/1.2.11@conan/stable
# Poco/1.8.1@pocoproject/stable
pistache/d5608a1@conan/stable
# opencv/3.4.1@garrick/stable

[generators]
cmake

[options]
# opencv:shared=True
```

conan remote add/remove xxx

安装

conan inspect poco/1.9.4

`conan install cjson/1.7.13@`
`conan install packagename/1.0@`
@很重要，有这个后缀才conan install才会把输入参数当做一个包名，如果没有@,conan install 会把 cjson/1.7.13当做一个路径


************************* WARNING: GCC OLD ABI COMPATIBILITY ***********************
 
Conan detected a GCC version > 5 but has adjusted the 'compiler.libcxx' setting to
'libstdc++' for backwards compatibility.
Your compiler is likely using the new CXX11 ABI by default (libstdc++11).
If you want Conan to use the new ABI for the default profile, run:
    $ conan profile update settings.compiler.libcxx=libstdc++11 default
Or edit '/home/wdidada/.conan/profiles/default' and set compiler.libcxx=libstdc++11
************************************************************************************

## conan 添加自定义的库
创建包
https://blog.csdn.net/hezhanran/article/details/112170151

## conan 2

```shell
conan version
version: 2.0.14
python
  version: 3.10.13
  sys_version: 3.10.13 (main, Nov 16 2023, 19:48:55) [GCC 9.4.0]
```

~/.conan/profiles/default

~/.conan2/profiles/default

## vcpkg和conan
conan支持选择库版本，vcpkg默认安装最新版本
apt yum也是安装特定版本
