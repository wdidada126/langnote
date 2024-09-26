# jmeter

## master slave节点

## .jmx文件

要在 JMeter 中进行集群部署并进行多线程测试 HTTP 接口性能，你可以按照以下步骤进行：
### 1. 准备环境
- 安装 JMeter：确保你在每台机器上安装了相同版本的 JMeter。
- 安装 Java：JMeter 需要 Java 环境，请确保每台机器上都已安装 JDK。
### 2. 配置主控节点（Master）
1. 创建测试计划：
   - 在 JMeter 中创建一个新的测试计划，添加线程组和 HTTP 请求，配置所需的参数。
2. 配置 JMeter 属性：
   - 找到 `bin` 目录下的 `jmeter.properties` 文件，修改以下配置项：
     ```properties
     # 使 JMeter 以远程模式运行
     remote_hosts=192.168.1.2:1099,192.168.1.3:1099  # 其他工作节点的 IP
     ```
### 3. 配置工作节点（Slaves）
1. 启动工作节点：
   - 在每台工作节点上，进入 JMeter 的 `bin` 目录，运行：
     ```bash
     jmeter-server
     ```
   - 确保工作节点的防火墙设置允许接收来自主控节点的连接。
### 4. 运行测试
1. 在主控节点上运行测试：
   - 在 JMeter 的 GUI 界面中，点击“运行”菜单，然后选择“远程启动”。
   - 选择你想要启动的工作节点。
2. 查看结果：
   - 在主控节点上，你可以添加“结果树”、“聚合报告”等监听器来查看测试结果。
   - 测试完成后，可以分析性能指标。
### 5. 使用命令行运行（可选）
如果你希望以非 GUI 模式运行测试，可以使用以下命令：
```bash
jmeter -n -t your_test_plan.jmx -R 192.168.1.2,192.168.1.3
```
### 6. 监控和分析

- 使用 JMeter 的结果监听器查看各项性能指标，如响应时间、成功率等。
- 可以将结果导出为 CSV 或 XML 格式进行进一步分析。

### 注意事项

- 确保所有节点的 JMeter 版本和 Java 版本一致。
- 配置合适的线程数和 Ramp-Up 时间，以避免瞬间的负载冲击。
- 可以使用不同的机器来模拟不同的用户行为。

通过以上步骤，你就可以在 JMeter 中成功地进行 HTTP 接口性能的多线程测试。

当涉及 JMeter 分布式测试时，配置集群并同时执行测试是很有用的。以下是一个简单的 JMeter 分布式测试的教程，包括设置 JMeter 服务器以及执行测试：
### 步骤 1：配置 JMeter 主控制器
1. 下载 JMeter：确保您已经下载并安装了 Apache JMeter。
2. 启动 JMeter：打开 JMeter，并创建一个新的测试计划。
3. 添加线程组和取样器：在测试计划中添加线程组和相应的取样器，配置您的测试。
4. 配置远程服务器：在主控制器中，选择 Run > Remote Start。在 Remote Start 配置中，添加远程服务器的 IP 地址和端口号。
### 步骤 2：配置 JMeter 服务器
1. 部署 JMeter 服务器：在每个要作为 JMeter 服务器的机器上部署 JMeter，确保它们都可以访问到 JMeter 主控制器。
2. 配置 JMeter.properties 文件：在 JMeter 服务器的 `jmeter/bin` 目录中，编辑 `jmeter.properties` 文件。确保以下属性设置正确：
    ```
    # 服务器模式
    server_port=1099
    server.rmi.localport=4000
    ```

3. 启动 JMeter 服务器：在每个 JMeter 服务器上，通过运行以下命令启动 JMeter 服务器：
    ```
    jmeter-server
    ```
### 步骤 3：运行分布式测试
1. 启动测试：在 JMeter 主控制器上，选择 Run > Start 开始测试。
2. 查看结果：查看测试结果，并确保从所有 JMeter 服务器收集到数据。
### 注意事项：
- 防火墙设置：确保防火墙允许 JMeter 主控制器和服务器之间的通信。
- 网络延迟：网络延迟可能会影响测试结果，尽量将 JMeter 服务器放置在靠近被测服务的网络中。

这些是配置 JMeter 分布式测试的基本步骤。通过这种方式，您可以利用多台服务器的性能来模拟更大规模的负载。

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
