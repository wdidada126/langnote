# apt

`sudo apt-get --only-upgrade install google-chrome-stable`



自己开发的包，如何上传到apt仓库



Debian/Ubuntu自有软件包构建私有源

https://www.cnblogs.com/lidp/archive/2009/02/26/1696283.html



[ubnutu/apt 与 apt-get/更新某一软件](https://blog.csdn.net/superjunenaruto/article/details/95173065)



apt可以安装共享库

apt install之后，二进制文件安装路径？



[Ubuntu中apt-get安装的文件位置](https://blog.csdn.net/younothings/article/details/103208387)



形如 apt-get install apps 这样的命令，一般会将下载文件放在 /var/cache/apt/archives目录下，然后安装。

如果不及时清理，这个目录所占空间会越来越大，幸运的是apt提供了相应的管理工具apt-get clean删除/var/cache/apt/archives/ 和 /var/cache/apt/archives/partial/目录下所有包(锁定的除外)。
apt-get autoclean仅删除不再能被下载的包。 

另外，aptitude clean也可删除/var/cache/apt/archives/ 和 /var/cache/apt/archives/partial/目录下所有包(锁定的除外)。



https://www.cnblogs.com/mch0dm1n/p/5422179.html





sudo apt install libpoco-dev -y
dpkg -l | grep libpoco
dpkg -L libpoco-dev
http://blog.chinaunix.net/uid-23254875-id-341021.html
https://blog.csdn.net/Kenny_GuanHua/article/details/123842699


apt-cache pkgnames | grep -i crypto++

apt-cache pkgnames | grep -i mysqlclient
apt-cache pkgnames | grep -i rapidjson

