# gem

可以用淘宝的Ruby镜像来访问cocoapods。按照下面的顺序在终端中敲入依次敲入命令：

gem sources --remove https://rubygems.org/
//等有反应之后再敲入以下命令
gem sources -a http://ruby.taobao.org/
为了验证你的Ruby镜像是并且仅是taobao，可以用以下命令查看：

gem sources -l
只有在终端中出现下面文字才表明你上面的命令是成功的：


http://ruby.taobao.org/
 

这时候，你再次在终端中运行：

sudo gem install cocoapods

https://www.cnblogs.com/daguo/p/4097295.html


cocoapod
pod install 
pod update
