# RocksDB

Centos 7 安装RocksDB
https://blog.51cto.com/860143/2452514?source=drt

嵌入式数据库RocksDB是Facebook基于LevelDB开发的一种嵌入式Key-value存储系统，该数据库能够充分利用闪存的性能，大大提升应用服务器的速度。
Rocksdb. 这个开源引擎是基于 Google 的 leveldb 1.5 版本, 但据称做了许多优化, 性能相对 leveldb 有了很大的提升, 而且解决了 leveldb 主动限制写的问题.

[KV存储的对比](https://colobu.com/2017/10/10/comparision-of-kv-datastore/)

存储引擎的类型
类型	全称
btree	
LSH	Log-Structured Hash Table
LSM	Log-Structured Merge Tree
FractalTree	分型树

[rocksdb](https://github.com/facebook/rocksdb)

Facebook Database Engineering Team

http://rocksdb.org/

http://rocksdb.org/docs/getting-started.html

C++写的，Java有库

<dependency>
    <groupId>org.rocksdb</groupId>
    <artifactId>rocksdbjni</artifactId>
    <version>6.6.4</version>
</dependency>
https://wanghenshui.github.io/rocksdb-doc-cn/doc/RocksJava-Basics.html

vcpkg Win 10可以一键安装c++库

```shell
Exception in thread "main" java.lang.UnsatisfiedLinkError: org.rocksdb.RocksDB.closeDatabase(J)V
at org.rocksdb.RocksDB.closeDatabase(Native Method)
at org.rocksdb.RocksDB.close(RocksDB.java:464)
at org.example.testrocksdbjni.RocksDBMain.main(RocksDBMain.java:30)
```

https://github.com/facebook/rocksdb/issues/6480

git clone https://github.com/facebook/rocksdb.git
cd rocksdb
make
