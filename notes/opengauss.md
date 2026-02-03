# opengauss
单机的？
GaussDB单机架构—openGauss
https://opengauss.org/zh/download/

https://gitcode.com/opengauss
https://github.com/opengauss-mirror/openGauss-server

华为
openGauss是一款开源的关系型数据库管理系统，它具有多核高性能、全链路安全性、智能运维等企业级特性。 openGauss内核早期源自开源数据库PostgreSQL，融合了华为在数据库领域多年的内核经验，在架构、事务、存储引擎、优化器及ARM架构上进行了适配与优化。作为一个开源数据库，期望与广泛的开发者共同构建一个多元化技术的开源数据库社区。

从新核心技术平台上线开始，到新核心运维平台的上线，不到半年时间，两大重量级系统分别出炉，邮储银行对数字化银行的建设进入快车道，取得了骄人的成绩。未来伴随着国际汇款业务的上线，明年上半年新核心的整体上线，作为邮储银行金融数据资产的核心管控数据库，还有很多发挥空间。openGauss会持续进步，与邮储银行发展同步，全力支持加速建设智慧化金融。
https://blog.csdn.net/weixin_49727236/article/details/122362777

数据库是“软件产业皇冠上的明珠”，是数字基础设施不可或缺的底座之一。但是数据库难度大，产业投入周期长，迫切需要凝聚产业力量共建基础能力。openGauss定位是企业级开源数据库，面向核心业务场景，支持企业业务数字化转型。自2020年6月30日正式开源上线以来，在数据库核心技术方面持续突破，与产业链伙伴共建国內数据库开源根社区，共同繁荣数据库开源生态、并在行业核心场景中规模应用，成为中国发展最快的开源数据库社区。技术方面，openGauss基于华为多年在数据库领域的技术和经验积累，与伙伴协同创新，“四高”能力持续演进突破。高性能：多核NUMA感知及融合存储引擎的高性能技术，单节点实现230万tpmC 性能 ，帮助客户应对数字化转型的性能挑战。高可用：数据零丢失、RTO<10s（业务恢复时间小于10秒），支持基于Paxos的金融级多地多中心可用性。高安全：通过全密态技术，让存储在数据库的数据“可用不可见，可见不可改，篡改可追溯”，保障数据全生命周期的安全可信，当前已获得国内首个全球数据库安全最高等级的CC EAL 4+认证。高智能：融合异构硬件的高智能技术，包括突破异构计算算子加速技术，突破基于异构硬件模型训练加速算法，突破基于向量化图片检索等技术，极大提高运维效率、释放生产力。持续深耕创新，openGauss已经成为中国最具创高新力的开源数据库。除了在技术上的持续创新，openGauss社区也愈发繁荣。截至目前，openGauss已在技术、生态、商业和社区治理等稳健推进，快速成长，185家企业和机构加入社区，4000多名开发者参与社区贡献，社区版本下载量超100万次。同时，携手产业链伙伴聚焦行业客户应用场景需求，为客户提供领先的产品与方案。目前openGauss与海量数据、云和恩墨、神舟通用、南大通用等10余家伙伴合作发行数据库商业版，与ISV伙伴联合构筑基于openGauss的行业解决方案500余个，并在国计民生行业实现规模商用，其中已在中国移动、邮储银行、中国海油、中国人寿、国家电网、民生银行、比亚迪等客户的核心系统批量上线。openGauss坚持创新，聚焦数据库根技术发展，使能企业数字化转型。openGauss坚持开源开放，与产业链创新力量一起，共建、共享、共治，协力打造全球领先的开源数据库开源社区和技术生态。

## 版本
6.0.0 2024年10月14日
5.1.0 2023年10月7日
5.0.0 2023年9月27日

高斯数据库核心团队成员
1. 张政（华为高斯数据库首席架构师）
华为高斯数据库的早期核心创始成员之一
负责数据库内核架构设计和研发
在分布式数据库领域有深厚的技术积累

2. 王海峰（华为高斯数据库研发负责人）
负责高斯数据库整体研发管理
在数据库优化器和执行引擎方面有重要贡献
带领团队完成多个重大版本的技术突破

3. 王磊（华为高斯数据库存储引擎专家）
专注于存储引擎和事务处理
在WAL、MVCC等核心机制上有深入研究
负责数据库高性能存储架构设计

4. 李飞飞（华为云数据库业务负责人）
虽然不直接参与高斯数据库具体研发，但负责产品化和商业化
在数据库即服务(DBaaS)领域有丰富经验
推动高斯数据库在华为云上的应用和推广

清华大学
李国娇 - 数据库系统、大数据管理
王建民 - 大数据系统、时序数据库、工业大数据
张勇 - 图数据库、数据挖掘
邢春晓 - 数据库理论、数据安全
刘英博 - 工业大数据、时序数据库
北京大学
崔斌 - 分布式数据库、大数据系统
高军 - 图数据管理、社交网络分析
杨智 - 数据库理论、数据质量管理
唐振明 - 数据挖掘、数据库系统
中国人民大学
杜小勇 - 数据库理论、XML数据库
陆嘉恒 - 分布式数据库、云数据库
范举 - 数据集成、数据清洗
华东师范大学
钱卫宁 - 分布式数据库、事务处理
周傲英 - 数据库理论、大数据管理
宫学庆 - 查询优化、分布式系统
复旦大学
王晓阳 - 数据挖掘、数据库系统
周水庚 - 数据库理论、生物信息学
汪卫 - 数据仓库、OLAP
浙江大学
陈刚 - 数据库系统、信息检索
高云君 - 数据质量管理、数据库理论
孙建伶 - 分布式数据库、云原生数据库
哈尔滨工业大学
王宏志 - 数据质量管理、大数据处理
李建中 - 数据库理论、传感器网络数据管理
南京大学
黄宜华 - 大数据系统、分布式计算
顾荣 - 图计算、分布式数据库
上海交通大学
邱锡鹏 - 自然语言处理与数据库结合
赵海 - 分布式系统、数据库
中国科学技术大学
金培权 - 时空数据库、移动数据管理
岳丽华 - 数据挖掘、数据库系统
华中科技大学
冯丹 - 存储系统、数据库
曹仰杰 - 分布式数据库、大数据系统
中山大学
印鉴 - 数据挖掘、数据库理论
吴迪 - 数据库系统、大数据管理
北京航空航天大学
吕卫锋 - 大数据系统、数据库
李建欣 - 数据安全、数据库
中国科学院
石勇（计算技术研究所）- 大数据分析、数据库
程学旗（计算技术研究所）- 大数据系统、信息检索
工业界研究机构
微软亚洲研究院：郑宇、谢幸等
阿里巴巴：李飞飞、周靖人等
腾讯：王永霞、刘威等
百度：窦德景、陈曦等
研究方向分布
这些学者的研究方向涵盖：
分布式数据库系统
云原生数据库
图数据库与图计算
时序数据库
NewSQL/NoSQL系统
查询优化与处理
事务处理技术
数据安全与隐私
AI4DB/DB4AI
多模数据库
内存数据库

国内数据库研究社区非常活跃，每年举办的中国数据库学术会议（NDBC） 是学者们交流的重要平台。近年来，随着国产数据库的兴起，学术界与工业界的合作也越来越紧密。


国内人工智能领域的学者非常多，以下按主要高校和科研机构分类介绍：

清华大学
• 张钹 - 人工智能元老，知识工程、机器学习
• 朱军 - 机器学习、贝叶斯方法、深度学习理论
• 孙富春 - 机器人学、智能控制
• 刘知远 - 自然语言处理、知识图谱
• 唐杰 - 社会计算、数据挖掘
• 李建 - 计算机视觉、多媒体分析
• 刘永进 - 人机交互、智能图形学
• 汪玉 - AI芯片、智能计算系统
• 翟季冬 - 分布式机器学习系统

北京大学
• 高文 - 计算机视觉、多媒体技术
• 查红彬 - 计算机视觉、机器人感知
• 林宙辰 - 机器学习、计算机视觉
• 田永鸿 - 多媒体分析、类脑计算
• 黄铁军 - 计算机视觉、类脑计算
• 李文新 - 人工智能基础理论

中国科学院
• 谭铁牛 - 模式识别、计算机视觉（自动化所）
• 刘成林 - 模式识别、文档分析（自动化所）
• 陈熙霖 - 计算机视觉、多媒体计算（计算所）
• 山世光 - 人脸识别、计算机视觉（计算所）
• 王亮 - 模式识别、生物特征识别（自动化所）
• 陶建华 - 人机交互、情感计算（自动化所）

上海交通大学
• 杨小康 - 计算机视觉、多媒体分析
• 卢策吾 - 计算机视觉、机器人学习
• 张伟楠 - 强化学习、推荐系统
• 严骏驰 - 机器学习、数据挖掘

浙江大学
• 潘云鹤 - 人工智能、知识工程
• 吴飞 - 人工智能、跨媒体计算
• 蔡登 - 计算机视觉、多媒体分析
• 李石坚 - 普适计算、人机交互

哈尔滨工业大学
• 刘挺 - 自然语言处理、社会计算
• 秦兵 - 自然语言处理、情感分析
• 车万翔 - 自然语言处理、深度学习
• 张宇 - 人工智能、智能控制

南京大学

• 周志华 - 机器学习、数据挖掘

• 黎铭 - 机器学习、数据挖掘

• 高阳 - 人工智能、多智能体系统

• 俞扬 - 强化学习、机器学习

中国科学技术大学

• 陈恩红 - 数据挖掘、推荐系统

• 刘淇 - 数据挖掘、社会计算

• 熊辉 - 数据挖掘、商业智能

复旦大学

• 邱锡鹏 - 自然语言处理、深度学习

• 黄萱菁 - 自然语言处理、文本挖掘

• 张奇 - 自然语言处理、信息检索

• 肖仰华 - 知识图谱、大数据分析

中国人民大学

• 文继荣 - 信息检索、数据挖掘

• 赵鑫 - 自然语言处理、社会计算

• 窦志成 - 信息检索、机器学习

北京航空航天大学

• 李未 - 人工智能、分布式计算

• 吕卫锋 - 大数据智能、社会计算

• 牛建伟 - 普适计算、移动智能

中山大学

• 赖剑煌 - 计算机视觉、生物特征识别

• 谢晓华 - 数据挖掘、生物信息学

同济大学

• 苗夺谦 - 粗糙集、粒计算

• 赵卫东 - 商务智能、流程挖掘

产业界研究机构

微软亚洲研究院

• 洪小文 - 人工智能、语音识别

• 周明 - 自然语言处理、机器翻译

• 刘铁岩 - 机器学习、信息检索

百度

• 王海峰 - 自然语言处理、知识图谱

• 吴甜 - 深度学习平台、AI开发

阿里巴巴

• 华先胜 - 计算机视觉、视频分析

• 司罗 - 自然语言处理、智能客服

腾讯

• 刘威 - 计算机视觉、多媒体分析

• 俞栋 - 语音识别、深度学习

商汤科技

• 王晓刚 - 计算机视觉、深度学习

• 林达华 - 计算机视觉、机器学习

主要研究方向分布

基础理论

• 机器学习理论

• 深度学习理论

• 强化学习

• 贝叶斯方法

核心技术

• 计算机视觉

• 自然语言处理

• 语音识别与合成

• 知识图谱与推理

应用领域

• 机器人学

• 智能驾驶

• 医疗AI

• 金融科技

• 智慧城市

交叉学科

• AI4Science

• 脑科学与类脑计算

• AI芯片与系统

• AI安全与伦理

重要学术平台

• 中国人工智能学会（CAAI）

• 中国计算机学会人工智能专委会

• 全国人工智能学术会议（CCAI）

• 中国机器学习会议（CCML）

这个领域发展迅速，新的优秀学者不断涌现。以上列出的是在各方向上具有较高知名度和影响力的部分学者。


以下是人工智能方向的一些优秀教学Lab开源项目，类似Huadb、MiniOB：

机器学习/深度学习基础

1. 微软AI教育项目 (AI-School)

• 负责人: 微软亚洲研究院

• 源代码: https://github.com/microsoft/AI-School

• 特点: 完整的AI教学课程和实验项目

2. Stanford CS231n课程项目

• 负责人: 李飞飞教授

• 源代码: https://github.com/cs231n/cs231n.github.io

• 特点: 计算机视觉经典课程，包含完整实验

3. 动手学深度学习 (D2L)

• 负责人: 李沐（亚马逊首席科学家）

• 源代码: https://github.com/d2l-ai/d2l-zh

• 特点: 中文版《动手学深度学习》，Jupyter Notebook形式

自然语言处理

4. Stanford CS224n课程项目

• 负责人: Christopher Manning教授

• 源代码: https://github.com/stanfordnlp/cs224n-winter17-notes

• 特点: NLP经典课程实验

5. Hugging Face Transformers教程

• 负责人: Hugging Face团队

• 源代码: https://github.com/huggingface/transformers

• 特点: 最新的Transformer模型实践教程

计算机视觉

6. MMLab系列 (OpenMMLab)

• 负责人: 香港中文大学MMLab

• 源代码: https://github.com/open-mmlab

• 包含项目:

  • MMDetection: https://github.com/open-mmlab/mmdetection

  • MMPreTrain: https://github.com/open-mmlab/mmpretrain

  • MMSegmentation: https://github.com/open-mmlab/mmsegmentation

7. PaddleCV

• 负责人: 百度PaddlePaddle团队

• 源代码: https://github.com/PaddlePaddle/PaddleCV

• 特点: 基于飞桨的计算机视觉工具库

强化学习

8. 天授 (Tianshou)

• 负责人: 清华大学计算机系

• 源代码: https://github.com/thu-ml/tianshou

• 特点: 基于PyTorch的强化学习平台

9. 蘑菇书 (MushroomRL)

• 负责人: 北京大学等高校

• 源代码: https://github.com/MushroomRL/mushroom-rl

• 特点: 强化学习教学项目

AI系统与框架

10. MindSpore教程

• 负责人: 华为MindSpore团队

• 源代码: https://github.com/mindspore-ai/mindspore

• 特点: 华为开源AI框架教学项目

11. PaddlePaddle教育版

• 负责人: 百度PaddlePaddle团队

• 源代码: https://github.com/PaddlePaddle/Paddle

• 特点: 飞桨深度学习平台教育版本

专门的教学实验室项目

12. AI-EdLab

• 负责人: 多所高校联合

• 源代码: https://github.com/AI-EdLab/ai-edu

• 特点: 专门为AI教育设计的实验平台

13. DeepLearning-500-questions

• 负责人: 复旦大学等

• 源代码: https://github.com/scutan90/DeepLearning-500-questions

• 特点: 深度学习500问，配套代码实践

14. AiLearning

• 负责人: 个人开发者（ApacheCN）

• 源代码: https://github.com/apachecn/AiLearning

• 特点: 机器学习实战代码和教程

国内高校特色项目

15. 清华大学计图 (Jittor)

• 负责人: 清华大学计算机系图形学实验室

• 源代码: https://github.com/Jittor/jittor

• 特点: 基于元算子和统一内存的深度学习框架

16. 北京大学AI教学项目

• 负责人: 北京大学人工智能研究院

• 源代码: https://github.com/pku-ai-edu/ai-course

• 特点: 北大AI课程配套实验

17. 浙江大学AI实验室

• 负责人: 浙江大学人工智能研究所

• 源代码: https://github.com/zju-ai/zju-ai-lab

• 特点: 浙大AI课程实验项目

18. 上海交通大学AI教学

• 负责人: 上海交通大学人工智能研究院

• 源代码: https://github.com/sjtu-ai/ai-course-materials

• 特点: 交大AI课程资料和实验

特色小型教学项目

19. numpy-ml

• 负责人: 个人开发者

• 源代码: https://github.com/ddbourgin/numpy-ml

• 特点: 仅用NumPy实现机器学习算法

20. neural-networks-and-deep-learning

• 负责人: Michael Nielsen

• 源代码: https://github.com/mnielsen/neural-networks-and-deep-learning

• 特点: 神经网络与深度学习经典教程代码

使用建议

1. 初学者: 推荐《动手学深度学习》(D2L) 和 AiLearning
2. 计算机视觉: 推荐MMLab系列和CS231n
3. 自然语言处理: 推荐Hugging Face和CS224n
4. 强化学习: 推荐天授(Tianshou)和蘑菇书
5. 系统学习: 推荐各大高校的完整课程项目

这些项目大多有详细的中文文档和活跃的社区支持，非常适合教学和自学使用。

以下是计算机网络方向的优秀教学Lab开源项目：

网络协议栈实现

1. TinyWebServer

• 负责人: qinguoyi

• 源代码: https://github.com/qinguoyi/TinyWebServer

• 特点: Linux下C++轻量级Web服务器，包含线程池、Epoll、定时器等

2. mTCP

• 负责人: 首尔大学

• 源代码: https://github.com/mtcp-stack/mtcp

• 特点: 高性能用户态TCP/IP协议栈，用于教学和研究

3. lwIP

• 负责人: 瑞典计算机科学研究所

• 源代码: https://github.com/lwip-tcpip/lwip

• 特点: 轻量级TCP/IP协议栈，适合嵌入式系统教学

网络编程实战

4. Linux网络编程实战

• 负责人: 游双《Linux高性能服务器编程》配套代码

• 源代码: https://github.com/riba2534/Linux-Network-Programming

• 特点: Linux网络编程完整实例

5. CppNet

• 负责人: caozhiyi

• 源代码: https://github.com/caozhiyi/CppNet

• 特点: C++11编写的高性能网络库，适合学习现代C++网络编程

知名大学课程实验

6. Stanford CS144: Introduction to Computer Networking

• 负责人: Stanford University

• 源代码: https://github.com/stanford-netlab/cs144

• 特点: 实现完整的TCP协议栈，著名网络课程实验

7. MIT 6.829: Computer Networks

• 负责人: MIT

• 课程网站: https://web.mit.edu/6.829/www/currentsemester/

• 特点: 包含路由器实现、拥塞控制等实验

8. UCB CS168: Computer Networks

• 负责人: UC Berkeley

• 课程资料: https://inst.eecs.berkeley.edu/~cs168/fa20/

• 特点: 伯克利计算机网络课程实验

国内高校优秀项目

9. 清华大学网络课程实验

• 负责人: 清华大学计算机系

• 源代码: https://github.com/THU-CS-Lab/NetLab

• 特点: 清华计算机网络课程配套实验

10. 浙江大学网络编程实验

• 负责人: 浙江大学计算机网络研究所

• 源代码: https://github.com/ZJU-Network-Lab

• 特点: 网络协议分析和实现实验

11. 北京大学计算机网络实验

• 负责人: 北京大学信息科学技术学院

• 课程资料: https://github.com/PKU-Network-Lab

• 特点: Socket编程、协议分析等基础实验

网络工具和框架

12. libevent

• 负责人: Niels Provos

• 源代码: https://github.com/libevent/libevent

• 特点: 事件驱动网络库，适合学习高性能网络编程

13. Boost.Asio

• 负责人: Boost社区

• 源代码: https://github.com/boostorg/asio

• 特点: C++跨平台网络编程库，工业级标准

14. Muduo

• 负责人: 陈硕（《Linux多线程服务端编程》作者）

• 源代码: https://github.com/chenshuo/muduo

• 特点: 现代C++网络库，国内经典教学项目

协议分析和仿真

15. Wireshark插件开发

• 负责人: Wireshark团队

• 源代码: https://github.com/wireshark/wireshark

• 特点: 学习网络协议分析和插件开发

16. ns-3网络模拟器
• 负责人: ns-3开发团队
• 源代码: https://gitlab.com/nsnam/ns-3
• 特点: 离散事件网络模拟器，用于协议性能评估

17. Mininet
• 负责人: Stanford University
• 源代码: https://github.com/mininet/mininet
• 特点: SDN网络仿真平台

特定协议实现
18. Simple HTTP Server
• 负责人: 多个开源贡献者
• 代表性项目: https://github.com/ankushagarwal/nweb

• 特点: 简易HTTP服务器实现，适合初学者

19. DNS服务器实现
• 负责人: 多个开源项目
• 代表性项目: https://github.com/rs/dns

• 特点: DNS协议学习和实现

20. QUIC协议实现
• 负责人: Google等
• 代表性项目: https://github.com/cloudflare/quiche
• 特点: 学习新一代传输协议QUIC

网络安全方向

21. Scapy
• 负责人: Philippe Biondi
• 源代码: https://github.com/secdev/scapy
• 特点: 网络数据包制作和发送工具

22. Metasploit Framework
• 负责人: Rapid7
• 源代码: https://github.com/rapid7/metasploit-framework
• 特点: 渗透测试框架，学习网络安全
综合实验平台

23. NetKit
• 负责人: 多个大学联合
• 源代码: http://www.netkit.org/
• 特点: 网络实验虚拟环境

24. GNS3
• 负责人: GNS3团队
• 源代码: https://github.com/GNS3/gns3-gui
• 特点: 网络拓扑设计和仿真平台

推荐学习路径

初学者路线：
1. TinyWebServer → 理解Web服务器基本原理
2. Linux网络编程实战 → 掌握Socket编程
3. Simple HTTP Server → 实现HTTP协议

进阶路线：
1. Stanford CS144 → 实现TCP协议栈
2. Muduo网络库 → 学习高性能网络编程
3. Wireshark源码 → 深入协议分析

研究方向：
1. ns-3/Mininet → 网络协议仿真
2. QUIC实现 → 新一代传输协议
3. 网络安全工具 → 网络攻防技术

这些项目涵盖了从基础网络编程到高级协议实现的各个层面，适合不同层次的学习需求。大多数项目都有详细的中文文档和活跃的社区支持。


以下是数据库方向的其他优秀教学Lab开源项目：

关系型数据库教学项目

1. SQLite源代码

• 负责人: D. Richard Hipp

• 源代码: https://github.com/sqlite/sqlite

• 特点: 工业级轻量数据库，代码简洁适合学习

2. PostgreSQL教学版

• 负责人: PostgreSQL全球开发组

• 源代码: https://github.com/postgres/postgres

• 特点: 完整的企业级数据库源码

3. DuckDB

• 负责人: 荷兰Centrum Wiskunde & Informatica (CWI)

• 源代码: https://github.com/duckdb/duckdb

• 特点: 嵌入式分析型数据库，代码现代清晰

4. TerarkDB

• 负责人: 字节跳动

• 源代码: https://github.com/bytedance/terarkdb

• 特点: 基于LSM-tree的KV存储，工业级实现

知名大学课程项目

5. CMU 15-445/645 Database Systems

• 负责人: Andy Pavlo (CMU教授)

• 源代码: https://github.com/cmu-db/bustub

• 特点: CMU著名数据库课程，实现关系型数据库核心组件

6. MIT 6.830/6.814 Database Systems
• 负责人: Sam Madden (MIT教授)
• 源代码: https://github.com/MIT-DB-Class/simple-db-hw
• 特点: MIT数据库课程，实现SimpleDB

7. Stanford CS245 Database Principles

• 负责人: Stanford数据库组
• 课程项目: 多个课程实验项目
• 特点: 查询优化、事务处理等核心主题

8. UW CSE 544 Database Internals

• 负责人: University of Washington
• 课程资料: https://courses.cs.washington.edu/courses/cse544
• 特点: 数据库内核实现深度课程

国内高校项目

9. 清华大学数据库课程实验

• 负责人: 李国娇教授等

• 相关项目: https://github.com/thu-pacman

• 特点: 分布式数据库、查询优化等实验

10. 北京大学数据库实验室

• 负责人: 崔斌教授等
• 相关项目: https://github.com/pkudb
• 特点: 分布式数据库系统研究

11. 浙江大学数据库课程

• 负责人: 陈刚教授等
• 课程项目: 数据库系统实现实验
• 特点: 完整的数据库系统实现

12. 华东师范大学数据库实验室

• 负责人: 钱卫宁教授等
• 相关项目: https://github.com/ecnu-datalab
• 特点: 分布式事务处理、NewSQL系统

分布式数据库教学项目

13. TiDB教学版
• 负责人: PingCAP
• 源代码: https://github.com/pingcap/tidb
• 特点: 工业级NewSQL数据库，文档完善

14. CockroachDB Lite
• 负责人: Cockroach Labs
• 源代码: https://github.com/cockroachdb/cockroach
• 特点: 分布式SQL数据库，架构清晰

15. YugabyteDB
• 负责人: Yugabyte
• 源代码: https://github.com/yugabyte/yugabyte-db
• 特点: 高性能分布式数据库

特定组件教学项目

16. LSM-Tree实现
• 负责人: 多个开源项目
• 代表性项目: https://github.com/google/leveldb
• 特点: Google LevelDB，LSM-tree经典实现

17. B+Tree实现
• 负责人: 多个教学项目
• 代表性项目: https://github.com/begeekmyfriend/bplustree

• 特点: B+树索引结构教学实现

18. 查询优化器教学

• 负责人: 多个研究项目

• 代表性项目: https://github.com/cwida/duckdb

• 特点: DuckDB的优化器代码清晰

19. 事务处理教学

• 负责人: 多个学术项目

• 代表性项目: https://github.com/ept/hermitage

• 特点: 事务隔离级别测试框架

嵌入式数据库教学

20. UnQLite

• 负责人: Symisc Systems

• 源代码: https://github.com/symisc/unqlite

• 特点: 文档型嵌入式数据库，代码简洁

21. Berkeley DB教学版

• 负责人: Oracle

• 源代码: https://github.com/berkeleydb/libdb

• 特点: 经典嵌入式数据库引擎

云原生数据库教学

22. Vitess

• 负责人: PlanetScale

• 源代码: https://github.com/vitessio/vitess

• 特点: MySQL的云原生中间件

23. PolarDB for PostgreSQL

• 负责人: 阿里巴巴

• 源代码: https://github.com/alibaba/PolarDB-for-PostgreSQL

• 特点: 云原生数据库开源版本

时序数据库教学

24. InfluxDB

• 负责人: InfluxData

• 源代码: https://github.com/influxdata/influxdb

• 特点: 时序数据库典型代表

25. TimescaleDB

• 负责人: Timescale

• 源代码: https://github.com/timescale/timescaledb

• 特点: 基于PostgreSQL的时序数据库

图数据库教学

26. Neo4j社区版

• 负责人: Neo4j

• 源代码: https://github.com/neo4j/neo4j

• 特点: 主流图数据库源码

27. JanusGraph

• 负责人: Linux基金会

• 源代码: https://github.com/JanusGraph/janusgraph

• 特点: 分布式图数据库

推荐学习路径

初学者路线：

1. CMU Bustub → 数据库系统核心概念
2. SQLite源码阅读 → 理解完整数据库架构
3. LevelDB → 学习存储引擎实现

进阶路线：

1. PostgreSQL源码阅读 → 企业级数据库实现
2. TiDB/TinySQL → 分布式数据库架构
3. DuckDB → 分析型数据库优化

研究方向：

1. MIT SimpleDB → 学术研究基础
2. CockroachDB → 分布式事务处理
3. TimescaleDB → 时序数据库技术

特色教学资源

28. DB Tutorials

• 负责人: 多个数据库专家

• 资源集合: https://github.com/learnedsystems/BestOfDBPD

• 特点: 数据库领域最佳教程集合

29. Paper Reading Group

• 负责人: 多个高校实验室

• 资源: https://github.com/rxin/db-readings

• 特点: 数据库经典论文阅读列表

30. Database Internals

• 负责人: Alex Petrov

• 配套代码: https://github.com/ben-stopford/books-dbi

• 特点: 《Database Internals》一书配套代码

这些项目涵盖了从基础数据库实现到高级分布式系统的各个层面，适合不同层次的学习需求。大多数项目都有详细的文档和活跃的社区支持。


是的，openGauss 的源代码（官方内核）支持单机部署，也支持分布式部署，但需要区分版本和具体形态。核心架构说明openGauss 本体（内核）是单机/集中式数据库（standalone / centralized architecture）：数据存储在单个物理节点（或主备节点）上。
支持单机部署（standalone mode）：只有一个数据库实例，无高可用。
支持一主多备高可用部署（primary + multiple standbys）：最多支持 8 个备机（早期版本最多 4 个），备机支持只读，提供实例级容灾和读扩展。
官方文档反复强调：openGauss 支持单机部署和一主多备部署两种主要形态。单机部署常用于测试、体验、开发调测场景，不建议用于生产（因为只有一个数据副本，故障后数据丢失风险高，只能靠备份恢复）。

分布式部署：原生内核不直接提供内置分布式（不像 TiDB / CockroachDB 那样原生分片 + 分布式事务）。
但 openGauss 支持通过外部组件实现分布式，主要有两种主流方案：openGauss + ShardingSphere（最常见）：用 Apache ShardingSphere（Proxy 或 JDBC）做分库分表 + 分布式查询/事务，底层多个 openGauss 实例作为存储节点。支持水平扩展、读写分离、两地三中心等，已在生产中使用（例如华为云 GaussDB(for openGauss) 部分基于此）。
openGauss 分布式镜像/企业版扩展：部分版本（如某些 LTS 企业版）提供分布式部署支持，通过 Patroni + HAProxy + Paxos 实现多节点集群、负载均衡、自动 failover 等。

这些分布式方案本质上是多个 openGauss 单机/主备实例 + 中间件/协调层，而不是内核原生分布式。

总结对比部署类型
是否原生支持
典型场景
备注
单机部署
是
测试、开发、POC、小型应用
官方明确支持，一个实例运行在单台机器上，简单快速，但无 HA。
一主多备（HA）
是
中小型生产、读扩展
最多 8 备，最常用 1 主 2 备，提供 RPO=0、RTO<10s 的高可用。
分布式（分片）
间接支持
大规模、海量数据、高并发
靠 ShardingSphere 或类似中间件实现，多个 openGauss 节点组成集群。

实际使用建议想快速上手：直接用单机部署（Lite 版或企业版单机），官网有详细脚本安装指南（gs_preinstall + gs_install）。
需要高可用：一主多备部署。
需要分布式：结合 ShardingSphere 或官方分布式方案，参考社区/华为云文档。

官方文档（最新版如 6.0+）一直把“单机部署”列为标准支持方式。如果你下载的是 openGauss-server 源代码，编译后就能单机跑起来。有具体版本（如 3.x、5.x、6.x）或想看部署步骤的话，可以再细说！


