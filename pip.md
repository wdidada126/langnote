# pip

pip3 install --user conan==2.0.6
pip3 install conan==2.0.6

https://www.runoob.com/w3cnote/python-pip-install-usage.html

pip
有python2 3的区别，属于破坏性升级

pip3

### pip whl 大陆镜像
pip install --index https://pypi.mirrors.ustc.edu.cn/simple/ wxPython


`pip install -r requirements.txt`

pip install --index https://pypi.mirrors.ustc.edu.cn/simple/ -r requirements.txt

pip install下载的文件在哪里
lib/site-packages

pypi镜像使用帮助
https://pypi.org/
	
Python包索引（PyPI）是Python编程语言的软件存储库。PyPI帮助你查找与安装由Python社区开发和共享的软件。软件包作者使用PyPI来分发他们的软件。
https://mirrors.tuna.tsinghua.edu.cn/help/pypi/

PyPI（Python Package Index）是一个Python软件包仓库，Python开发人员可以在其中发布、分享和下载Python软件包。pip（Python Package Installer）是一个Python包管理工具，用于方便地下载、安装、升级和删除Python软件包。pip可以从PyPI上搜索、下载和安装Python包，并且可以自动处理依赖关系。

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package

pip install -i http://mirrors.aliyun.com/pypi/simple some-package

镜像网站
清华大学：https://pypi.tuna.tsinghua.edu.cn/simple
阿里云：https://mirrors.aliyun.com/pypi/simple
中国科技大学：http://pypi.mirrors.ustc.edu.cn/simple
豆瓣：http://pypi.douban.com/simple
中国科学技术大学：http://pypi.mirrors.ustc.edu.cn/simple

比较常用的pip指令
安装库：pip install库名
(eg: pip install pylint)
卸载库：pip uninstall 库名
(eg: pip uninstall pylint)
升级库：pip install -U 库名
(eg: pip install -U pylint)
查看已安装的库：pip freeze/pip list
(eg: pip list)
查看单看库：pip show 库名
(eg: pip show pylint)
pylint:代码错误提示库


C:\Users\edidada\Downloads\GreaterWMS-V2.1.1>pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
Writing to C:\Users\edidada\AppData\Roaming\pip\pip.ini

pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

pip安装特定版本
pip install autobahn==21.3.1