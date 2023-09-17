# rpc

其实rpc不是一种协议，rpc是一种调用过程的方案/范式/实现。

http+retrofit同样也可以实现rpc风格的http调用。

dubbo框架同样也支持http(2)传输协议。

拿rpc和http对比没啥意义，应该是拿rpc底层的通信协议（如dubbo/grpc）对http，序列化协议（如hessian/protobuf）对json这样比较才有意义。

我觉得你说到点上了。rpc这个概念可能太多地方用了。如果是作为IPC、LPC这一级别概念来说，只是说互联网两台不同主角之间的调用来说。目前前后端那种或者说后端微服务那种都算。但是目前的rpc更多的是一种设计风格和规范，把方法和参数放在一起传递过去，他其实对标的是restful规范，资源方法用uri指定，参数另外放。http协议对标thrift。http的json序列化对标thrift的binaryprotocal。至于他们所说的rpc用http传输本质上都没说到点上，其实就是基于http协议实现rpc的设计风格，要是有功夫你基于thrift协议实现一套restful风格也没毛病
是的，其实这个可以从dubbo的invoker分层中可以很直观了解到，protocol/exchange/serialize/remoting等，开头也很不理解这种分层，直到后面接触异构通信多了才明白这样分层真的很有意义。

其实rpc不是一种协议，rpc是一种调用过程的方案/范式/实现。
http+retrofit同样也可以实现rpc风格的http调用。
dubbo框架同样也支持http(2)传输协议。
拿rpc和http对比没啥意义，应该是拿rpc底层的通信协议（如dubbo/grpc）对http，序列化协议（如hessian/protobuf）对json这样比较才有意义。
mq http比较

架构师的例子
https://github.com/edidada/EasyRPC


找比较流行的 RPC 框架（例如 Protobuf，Thrift，Avro）， 从 API Document 开始读， 然后到 Stackoverflow 上读相关的热门讨论， 自己动手写些 toy， 还想深入就读源码。

这是我能找到的最有效的方法。 每一本出版的书都有对你来说是废话的篇章， 以及你想知道却没有包括的内容。



https://www.ibm.com/developerworks/cn/aix/library/au-rpc_programming/





