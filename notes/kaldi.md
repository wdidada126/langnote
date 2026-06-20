# kaldi
“Kaldi 库”通常指的是语音识别领域中著名的开源工具。Kaldi 集成了多种语音识别模型，被广泛应用于语音识别任务。
小米有新一代 Kaldi 团队，该团队由“Kaldi 之父”、小米集团首席语音科学家 Daniel Povey 领衔。他们的新一代 Kaldi 项目主要由四个子项目构成：核心算法库 k2、通用语音数据处理工具包 lhotse、解决方案集合 icefall 以及服务端引擎 sherpa，方便开发者轻松训练、部署自己的智能语音模型。
新一代 Kaldi 团队关于语音识别声学模型的论文《zipformer: A faster and better encoder for automatic speech recognition》被 ICLR 2024 接收为 oral（top 1.2%）。Zipformer 作为一种新型的自动语音识别（ASR）模型，相比其他主流 ASR 模型，具有效果更好、计算更快、更省内存等优点，在常用的 ASR 数据集上都取得了当前最好的实验结果。
如果你对小米新一代 Kaldi 项目的具体内容或相关技术细节感兴趣，可以访问相关的项目链接或论文进一步了解。新一代 Kaldi 项目链接：https://github.com/k2-fsa ；论文链接：https://arxiv.org/pdf/2310.11230.pdf 。同时，团队也在不断进行研究和创新，为语音识别领域的发展做出贡献。这些技术和项目可以帮助开发者更好地进行语音识别相关的开发和应用。
语音识别是指将人类的语音信号转换为文字或其他可理解的形式的技术。它涉及信号处理、模式识别、机器学习等多个领域的知识和技术。通过使用深度学习算法，如循环神经网络（RNN）、长短时记忆网络（LSTM）、卷积神经网络（CNN）以及 Transformer 等架构，可以对语音信号进行建模和识别。
在语音识别过程中，通常需要对语音信号进行预处理，例如降噪、分帧等操作。然后，使用训练好的模型对语音特征进行分析和预测，以生成相应的文字输出。语音识别技术在许多领域都有广泛的应用，如语音助手、语音输入法、智能客服、语音翻译等，为人们的生活和工作带来了便利和效率。

今天，很多机器学习的算法已经开源了，有些应用已经有公司和研究机构投入科研力量开发过，比如基本的图形识别和语音识别技术，但是深度的自然语言理解其实还不属于这个范畴。
感觉语音需求不多呀，而且方案是开源的，数据是企业自己的，除了少数优秀的算法工程师，感觉其他老员工相比应届生也没太大优势

语音识别引擎还有kaldi这些都是c++,相对来说对c++还比较熟悉

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
