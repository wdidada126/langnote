# conan


## conan server
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

C++ 在软件包管理器上并不存在短板。当前有大量的工具可用，例如[ buckaroo ](https://www.buckaroo.pm/)、[ cget ](http://cget.readthedocs.io/en/latest/)、[ conan ](https://conan.io/)、[ conda ](https://conda.io/docs/)、[ cpm ](http://www.cpm.rocks/)、[ cppan ](https://cppan.org/)、[ hunter ](https://docs.hunter.sh/en/latest/)等等，不胜枚举。

https://github.com/LoopPerfect/buckaroo/

https://bintray.com/conan/conan-center

官网搜索
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
Conan客户端是用于与Conan服务端进行交互的工具。在公司内部，需要为每个开发人员部署Conan客户端，并确保他们使用相同的配置。
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
