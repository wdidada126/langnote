# etcd

--endpoints=https://127.0.0.1:2379

etcdctl get / --prefix --keys-only

key-value merory db

etcd在高并发场景下比zk好

[Etcd，Zookeeper，Consul 比较](https://blog.csdn.net/lingzhiwangcn/article/details/78853137)

[etcd、Zookeeper和Consul一致键值数据存储的性能对比](https://blog.csdn.net/github_32521685/article/details/89953710)

etcd压测报告全球
https://blog.csdn.net/kobelovestuding/article/details/53675306

Zookeeper系统设计的缺陷
https://zhuanlan.zhihu.com/p/37894143


https://etcd.io/

https://etcd.io/docs/v3.4/learning/api/

etcdctl --write-out="json" get foo

etcdctl --write-out="json" get foo
{"header":{"cluster_id":14841639068965178418,"member_id":10276657743932975437,"revision":48306,"raft_term":2},"kvs":[{"key":"Zm9v","create_revision":46292,"mod_revision":46292,"version":1,"value":"SGVsbG8gV29ybGQh"}],"count":1}

etcdctl endpoint health
etcdctl endpoint status

## etcd src

go写的

etcd 内部的 raft

### etcd http REST API

root@158bfa3d5562:/var/lib/rancher# curl http://127.0.0.1:2379/version
{"etcdserver":"3.4.3","etcdcluster":"3.4.0"}

root@158bfa3d5562:/var/lib/rancher# etcdctl  put foo "Hello World!"
OK
root@158bfa3d5562:/var/lib/rancher# etcdctl  get foo
foo
Hello World!
root@158bfa3d5562:/var/lib/rancher# which etcdctl
/usr/bin/etcdctl

root@158bfa3d5562:/var/lib/rancher# etcdctl endpoint health
127.0.0.1:2379 is healthy: successfully committed proposal: took = 1.8593ms
root@158bfa3d5562:/var/lib/rancher# etcdctl endpoint status
127.0.0.1:2379, 8e9e05c52164694d, 3.4.3, 13 MB, true, false, 2, 51821, 51821,

etcdctl --write-out=table snapshot status my.db

该版本只有grpc接口

自etcd v3.3起，gRPC网关endpoint已更改：

etcd v3.2 or before uses only [CLIENT-URL]/v3alpha/*.
etcd v3.3 uses [CLIENT-URL]/v3beta/* while keeping [CLIENT-URL]/v3alpha/*.
etcd v3.4 uses [CLIENT-URL]/v3/* while keeping [CLIENT-URL]/v3beta/*.
[CLIENT-URL]/v3alpha/* is deprecated.
etcd v3.5 or later uses only [CLIENT-URL]/v3/*.
[CLIENT-URL]/v3beta/* is deprecated.


curl -L http://localhost:2379/v3/kv/put -X POST -d '{"key": "Zm9v", "value": "YmFy"}'

root@158bfa3d5562:/var/lib/rancher# curl -L http://localhost:2379/v3/kv/put -X POST -d '{"key": "Zm9s", "value": "YmFy"}'
{"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"56741","raft_term":"2"}}

curl -L http://localhost:2379/v3/kv/range -X POST -d '{"key": "Zm9s"}'

根据你提供的《etcd-advance 如何处理“惊群”》这份文档，以及当前社区的最新动态，开源的 etcd 在设计和实现上存在几个值得关注的典型问题，主要分布在性能与架构设计、安全与认证和运维复杂性这几个方面。

### 1. 性能与架构设计的固有挑战

就像你文档里提到的，etcd 在“惊群”问题上避免的是 ZooKeeper 那种注册风暴，但并没有消除事件广播（fan-out）的成本。除此以外，它还有一些其他性能和架构上的问题：

*   “无数据”新成员加入引发的集群抖动：这是 etcd 运维中最常见的挑战之一。一个新加入的成员节点因为没有数据，会向 Leader 大量拉取更新日志，这可能导致 Leader 网络过载，甚至阻塞心跳，从而引发不必要的领导者选举和集群短暂不可用。
*   对底层磁盘 I/O 极度敏感：etcd 的共识算法（Raft）依赖将元数据持久化到磁盘。如果磁盘写入延迟过高（例如使用机械硬盘），就会拖慢整个集群的提交延迟，甚至导致心跳超时和选举，严重影响集群稳定性。
*   Auth 相关读操作的性能开销：社区曾发现，etcd 处理认证（auth）相关的读操作（如 `UserGet`）时，可能会通过 Raft 共识向所有节点转发请求，增加了不必要的网络和性能开销。理论上，这类操作应可通过线性一致性读通知（`linearizableReadNotify`）来优化，仅由接收请求的节点查询后端即可。
*   持续 Watch 模型下的投递效率：你文档中提到的“写线程内顺序执行 `consumer.accept(event)`”以及慢消费者会反压写入的问题，是当前`InMemoryRevisionedKv`实现的一个待改进项。它的广播语义决定了无法消掉 N 份通知，但可以通过异步队列、多路复用器（Multiplexer）等方式优化，避免阻塞写入路径。

### 2. 安全与认证机制的缺陷

最近披露的一个高危安全漏洞（CVE-2026-33413）揭示了 etcd 在自带的认证和授权机制上存在严重问题。

*   认证/授权绕过漏洞：该漏洞允许未经授权的用户，在启用了 etcd 认证的集群中，调用某些敏感 API。攻击者可以：
    *   调用 `MemberList`，泄露集群拓扑信息（如成员 ID 和访问地址）。
    *   调用 `Alarm` 接口，进行拒绝服务（DoS）攻击。
    *   滥用 `Lease` API，干扰基于 TTL 的键和租约所有权。
    *   触发 `Compaction`（压缩），永久删除历史修订版本，破坏 Watch、审计和恢复流程。
*   影响范围与缓解：不过需要注意的是，这个漏洞不影响典型的 Kubernetes 部署，因为 Kubernetes 的 API Server 自己处理认证授权，并不依赖 etcd 内置的 auth 机制。受影响的主要是直接将 etcd 的 gRPC API 暴露给不可信客户端的场景。官方已在 3.4.42、3.5.28、3.6.9 及更高版本中修复了此问题。除了升级，官方也建议通过 mTLS 和严格的网络访问控制来加强防护。此外，社区也曾讨论过 Lease 相关 API 默认无鉴权的设计问题，认为它可能带来 DoS 风险。

### 3. 集群成员变更的运维风险

etcd 的成员变更（Membership Reconfiguration）操作具有潜在风险，操作不当可能导致集群失联（Quorum Lost）。

*   两步操作的陷阱：成员变更需要先执行 `etcdctl member add`，再启动新的 etcd 进程。如果 `member add` 时配置了无效的 URL，新节点将无法启动。一旦集群因其他原因丢失了多数派（Quorum），就再也没办法通过正常的 API 来回滚这次变更，只能手动使用 `--force-new-cluster` 强制重建，这通常意味着数据丢失或服务中断。
*   网络分区下的雪上加霜：在集群发生网络分区时进行成员变更，会改变 Quorum 的大小，可能让情况变得更糟，甚至直接导致集群失去 Quorum 并触发选举。

### 总结

etcd 作为一个成熟的分布式 KV 存储，在性能和一致性方面表现出色，但也需要正确配置和维护。它的主要问题可以归纳为：
1.  架构级挑战：磁盘 I/O 和网络延迟是永恒的性能瓶颈，成员变更操作需要格外小心。
2.  安全短板：内置的认证授权机制曾曝出严重漏洞，生产环境强烈建议通过 mTLS 和网络隔离来保障安全，或依赖上层（如 Kubernetes）的认证层。
3.  运维复杂性：节点的优雅加入、故障恢复和配置正确性维护，对运维人员要求较高。
