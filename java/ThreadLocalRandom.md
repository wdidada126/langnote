# ThreadLocalRandom

java.util.concurrent.ThreadLocalRandom
1. Random 的问题
所有线程共用一个随机种子
多线程同时获取随机数时会加锁竞争
高并发下性能暴跌
2. ThreadLocalRandom 的优势
每个线程自带独立种子
完全无锁
并发越高，速度比 Random 快几十倍
使用一样简单