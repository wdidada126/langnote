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
