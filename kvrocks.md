kvrocks

https://kvrocks.apache.org/

A distributed key value NoSQL database that uses RocksDB as storage engine and is compatible with Redis protocol


https://kvrocks.slack.com/join/shared_invite/zt-p5928e3r-OUAK8SUgC8GOceGM6dAz6w#/shared-invite/email


这是 Kvrocks 进入 Apache 孵化器的第一个 Release, 距离上一个版本也有半年了。里面有挺多有意思的特性，比如类似 MySQL 的 GTID, Kvrocks 也增加了唯一的复制 ID 来解决主从切换过程可能导致数据不一致问题，具体发布日志见: github.com/apache/incubator-kvrocks/releases/tag/v2.1.0