# jmeter

jmeter测试dubbo



 命令介绍
jmeter -n -t <testplan filename> -l <listener filename>
示例： jmeter -n -t testplan.jmx -l test.jtl

示例含义：则表示以命令行模式运行testplan.jmx文件，输出的日志文件为test.jtl
参数介绍
这里是我们使用非 GUI 模式运行测试脚本时可以使用的一些命令，Jmeter官网用户手册介绍如下：
-h, –help -> prints usage information and exit
-n, –nongui -> run JMeter in nongui mode
-t, –testfile <argument> -> the jmeter test(.jmx) file to run
-l, –logfile <argument> -> the file to log samples to
-r, –runremote -> Start remote servers (as defined in remote_hosts)
-H, –proxyHost <argument> -> Set a proxy server for JMeter to use
-P, –proxyPort <argument> -> Set proxy server port for JMeter to use
具体的含义如下：
-h 帮助 -> 打印出有用的信息并退出
-n 非 GUI 模式 -> 在非 GUI 模式下运行 JMeter
-t 测试文件 -> 要运行的 JMeter 测试脚本文件
-l 日志文件 -> 记录结果的文件
-r 远程执行 -> 在Jmter.properties文件中指定的所有远程服务器
-H 代理主机 -> 设置 JMeter 使用的代理主机
-P 代理端口 -> 设置 JMeter 使用的代理主机的端口号
例如：jmeter -n -t test1.jmx -l logfile1.jtl -H 192.168.1.1 -P 8080



jmeter命令行执行压力测试 百度搜索


1、jmeter插件
2、自定义脚本


https://zhuanlan.zhihu.com/p/74692060

jmeter（二十四）dubbo接口测试
https://www.cnblogs.com/imyalost/p/9545505.html

各参数说明如下：
Protocol：注册协议，包括zookeeper、multicast、Redis、simple；
Address：注册地址，dubbo服务的IP+Port：
①、当使用zk，address填入zk地址，集群地址使用","分隔；
②、使用dubbo直连，address填写直连地址和服务端口；
Protocol：使用的dubbo协议，包括dubbo、rmi、hessian、webservice、memcached、redis，根据自己的协议类型选择对应的选项即可；
Timeout：请求超时时间，单位ms，根据dubbo具体配置填写；
Version：版本，dubbo不同版本之间差异较大，不同版本之间不能互相调用，这里指定dubbo版本，是为了方便识别和说明；
Retries：异常重试次数（类似这种分布式服务通信框架，大多都有重试机制，是为了保证事务成功率）；
Cluster：集群类型，包括failover、failfast、failsafe、failback、failking；
Group：组类型，如果有的话，根据配置填写即可；
Connections：连接数，同上，根据配置填写；
Async：服务处理类型，包括sync（同步）、async（异步），根据配置填写；
Loadbalance：负载均衡策略，包括random（随机）、roundrobin（轮询）、leastactive（最少活跃数）、consistenthash（一致性哈希）；
Interface：接口名（因为dubbo服务大多是开发根据规范自行命名的，因此这里需要填写完整的接口名+包名）；
Method：当前接口下的方法名，按照开发提供的API文档填写即可；
Args：接口报文，根据API文档填写，如上图所示，添加输入行，输入对应的参数类型和值即可（参数类型和值如何定义填写，请参考上面的链接）；
①、paramType：参数支持任何类型，包装类直接使用java.lang下的包装类，小类型使用：int、float、shot、double、long、byte、boolean、char，自定义类使用类完全名称；
②、paramValue：基础包装类和基础小类型直接使用值，例如：int为1，boolean为true等，自定义类与List或者Map等使用json格式数据；

https://github.com/thubbo/jmeter-plugins-for-apache-dubbo/wiki/%E7%94%A8%E6%88%B7%E6%8C%87%E5%8D%97
