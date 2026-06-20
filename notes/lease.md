# lease

分布式系统技术系列--租约(lease)
https://blog.csdn.net/weixin_33813128/article/details/85814264

**租约**（lease）在英文中的含义是“租期”、“承诺”，在分布式中一般描述如下：

- Lease 是由授权者授予的在一段时间内的承诺。
- 授权者一旦发出 lease，则无论接受方是否收到，也无论后续接收方处于何种状态，只要 lease 不过期，授权者一定遵守承诺，按承诺的时间、内容执行。
- 接收方在有效期内可以使用颁发者的承诺，只要 lease 过期，接收方放弃授权，不再继续执行，要重新申请Lease。
- 可以通过版本号、时间周期，或者到某个固定时间点认为Lease证书失效

关于Lease最经典的解释来源于Lease的原始论文<<Leases: An Efficient Fault-Tolerant Mechanism for Distributed File Cache Consistency>>：

  ***a lease is a contract that gives its holder specific rights over property for a limited period of time***
即Lease是一种带期限的契约，在此期限内拥有Lease的节点有权利操作一些预设好的对象。从更深 层次上来看，Lease就是一把带有超时机制的分布式锁，如果没有Lease，分布式环境中的锁可能会因为锁拥有者的失败而导致死锁，有了lease死锁 会被控制在超时时间之内。