# kaldi

http://www.kaldi-asr.org/
http://kaldi-asr.org/doc/
http://kaldi-asr.org/doc/annotated.html

https://github.com/kaldi-asr/kaldi

https://github.com/edidada/kaldi

语音识别

关于Kaldi的相关书籍，我了解到有两本相关的书籍：
《Kaldi语音识别实战》 本书以目前流行的开源语音识别工具Kaldi为切入点，深入浅出地讲解了语音识别前沿的技术及它们的实践应用，适合语音技术相关研究人员及互联网从业人员学习参考。
《解析深度学习：语音识别实践》 本书是首部介绍语音识别中深度学习技术细节的专著，适合有一定机器学习或语音识别基础的学生、研究者或从业者阅读。

小米去年 6 月就开源了移动端深度学习框架 MACE。在两天前，MACE 框架发布了最新的更新，在此次更新中可以看到，框架已支持了知名开源语音识别系统 Kaldi。
MACE 开源地址：https://github.com/XiaoMi/mace/releases

深度学习:语音识别技术实践


https://zhuanlan.zhihu.com/p/352452501?utm_id=0


接下来进行 Kaldi 的第一部分安装，第一部分主要是针对 Kaldi 依赖工具的安装比如 Openfst、Portaudio 等。安装步骤如下：

cd tools && extras/check_dependencies.sh
apt-get install  g++ zlib1g-dev make automake autoconf bzip2 unzip wget sox libtool subversion python2.7 python3 libatlas-dev libatlas-base-dev
extras/install_irstlm.sh
make

cd tools && extras/check_dependencies.sh
sudo yum install atlas.x86_64 -y

Kaldi 安装的第二部分为源码编译部分，这里的首要条件是第一部分正常安装之后，第二部分才能顺利完成。安装步骤如下：

cd /opt/kaldi/src 
./configure --shared
make depend -j 8
make -j 8

centos

```shell
git clone https://github.com/kaldi-asr/kaldi.git -b 5.4
cd kaldi
cd tools && extras/check_dependencies.sh
extras/install_irstlm.sh
sudo yum install  sox subversion -y

```
