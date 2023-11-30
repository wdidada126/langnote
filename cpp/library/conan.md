# conan

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

shell
sudo conan new myrepo/1.0.0 -g=BASIC -u=myusername -p=mypassword --url=https://myrepo.com
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

conan 添加自定义的库

https://blog.csdn.net/hezhanran/article/details/112170151