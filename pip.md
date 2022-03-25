# pip

pip

有python2 3的区别，属于破坏性升级

pip3

### pip whl 大陆镜像
pip install --index https://pypi.mirrors.ustc.edu.cn/simple/ wxPython


`pip install -r requirements.txt`



pip install --index https://pypi.mirrors.ustc.edu.cn/simple/ -r requirements.txt


pip install下载的文件在哪里
lib/site-packages


pypi 镜像使用帮助
https://mirrors.tuna.tsinghua.edu.cn/help/pypi/


pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package

pip install -i http://mirrors.aliyun.com/pypi/simple some-package



镜像网站
清华大学：https://pypi.tuna.tsinghua.edu.cn/simple
阿里云：https://mirrors.aliyun.com/pypi/simple
中国科技大学：http://pypi.mirrors.ustc.edu.cn/simple
豆瓣：http://pypi.douban.com/simple
中国科学技术大学：http://pypi.mirrors.ustc.edu.cn/simple


比较常用的pip指令
安装库：pip install 库名
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