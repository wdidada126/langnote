# Dynamo

分布式kv系统



[重读 Amazon Dynamo 论文有感](https://zhuanlan.zhihu.com/p/98640498)



[Amazon Dynamo架构分析](https://blog.csdn.net/anderscloud/article/details/7179107)



[Amazon的Dynamo中用到的几种技术](https://www.cnblogs.com/xiongji/p/3602051.html)



介绍亚马逊 Dynamo 系统如何保证弱一致性。最后，讨论乱序编程的两个方面：CRDTs and the CALM理论。



CRDT——解决最终一致问题的利器

https://yq.aliyun.com/articles/635632?utm_content=m_1000015503

面对大型分布式系统, 不免要讨论CAP理论，在跨区域多活的场景下如何取舍？显然P(网络分区)是首要考虑因素。其次，跨区域部署就是为了提高可用性，而且对于常见的一致性协议，不管是2PC、Paxos还是raft，在此场景下都要做跨区域同步更新，不仅会降低用户体验，在网络分区的时候还会影响可用性，因此C必定被排在最后。那是不是C无法被满足了呢？事实并非如此，退而求其次，最终一致也是一种选择。CRDT(Conflict-Free Replicated Data Type)1是各种基础数据结构最终一致算法的理论总结，能根据一定的规则自动合并，解决冲突，达到强最终一致的效果。2012年CAP理论提出者Eric Brewer撰文回顾CAP[3]时也提到，C和A并不是完全互斥，建议大家使用CRDT来保障一致性。自从被大神打了广告，各种分布式系统和应用均开始尝试CRDT，redislabs[4]和riak[5]已经实现多种数据结构，微软的CosmosDB[6]也在azure上使用CRDT作为多活一致性的解决方案。
