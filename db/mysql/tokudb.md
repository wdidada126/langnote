# tokudb



[什么是TokuDB](http://xiaohost.com/1235.html)



阿里云最近推出了MySql的事务引擎TokuDB

TokuDB TokuDB是一个支持事务的MySQL引擎，拥有出色的数据压缩能力和极低的资源消耗。





https://www.percona.com/software/mysql-database/percona-tokudb

TokuDB（ Fractal Tree-节点带数据）
TokuDB 底层存储结构为 Fractal Tree,Fractal Tree 的结构与 B+树有些类似, 在 Fractal Tree中， 每一个 child 指针除了需要指向一个 child节点外，还会带有一个Message Buffer ，这个Message Buffer 是一个 FIFO 的队列，用来缓存更新操作。
例如，一次插入操作只需要落在某节点的 Message Buffer 就可以马上返回了，并不需要搜索到叶子节点。这些缓存的更新会在查询时或后台异步合并应用到对应的节点中。


