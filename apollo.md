# apollo


https://www.jianshu.com/p/23e4a01bf8d5




C:\Users\edidada>cd/d D:\apache-apollo-1.7.1\bin

D:\apache-apollo-1.7.1\bin>./apollo start
'.' 不是内部或外部命令，也不是可运行的程序
或批处理文件。

D:\apache-apollo-1.7.1\bin>apollo start
Found unexpected parameters: [start]

usage: apollo [--log <log_level>] <command> [<args>]

The most commonly used apollo commands are:
    create           creates a new broker instance
    disk-benchmark   Benchmarks your disk's speed
    help             Display help information
    version          Displays the broker version

See 'apollo help <command>' for more information on a specific command.


D:\apache-apollo-1.7.1\bin>apollo version
1.7.1



D:\apache-apollo-1.7.1\bin>apollo create test
Creating apollo instance at: test
Generating ssl keystore...

You can now start the broker by executing:

   "D:\apache-apollo-1.7.1\bin\test\bin\apollo-broker" run

Or you can setup the broker as Windows service and run it in the background:

   "D:\apache-apollo-1.7.1\bin\test\bin\apollo-broker-service" install
   "D:\apache-apollo-1.7.1\bin\test\bin\apollo-broker-service" start




```shell
D:\apache-apollo-1.7.1\bin>"D:\apache-apollo-1.7.1\bin\test\bin\apollo-broker" run
[0;40;37m
    [1m_____                .__  .__
   /  [32m_  \ [37m______   ____ |  [32m| [37m|  [32m|   [37m____
  /  [32m/[37m_\  [32m\[37m\[32m____ \ [37m/  [32m_ \[37m|  [32m| [37m|  [32m|  [37m/  [32m_ \
 [37m/    |    [32m\  |[37m_> [32m>  <[37m_> [32m)  |[37m_|  [32m|[37m_(  [32m<[37m_> [32m)
 \____[37m|[32m__  /   __/ \____/[37m|[32m____/____/[37m\[32m____/
[9C\/[37m|[32m__|  [37mApache Apollo[2m (1.7.1)
[0m

Loading configuration file 'D:\apache-apollo-1.7.1\bin\test\etc\apollo.xml'.
INFO  | OS     : Windows 8.1 6.3
INFO  | JVM    : Java HotSpot(TM) 64-Bit Server VM 1.7.0_80 (Oracle Corporation)
INFO  | Apollo : 1.7.1 (at: D:\apache-apollo-1.7.1)
INFO  | Starting store: leveldb store at D:\apache-apollo-1.7.1\bin\test\data
INFO  | Accepting connections at: tcp://0.0.0.0:61613
INFO  | Accepting connections at: tls://0.0.0.0:61614
INFO  | Accepting connections at: ws://0.0.0.0:61623/
INFO  | Accepting connections at: wss://0.0.0.0:61624/
INFO  | Administration interface available at: https://127.0.0.1:61681/
INFO  | Administration interface available at: http://127.0.0.1:61680/
```


访问网址
http://localhost:61680/


http://localhost:61680/console/index.html

默认的登录id和密码是 admin 和 password 。


MQTT 发布订阅测试，可以在 Chrome 中下载 MQTTBox 插件 或者 命令行安装 mosquitto 工具

