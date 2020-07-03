# caffeine

深入剖析来自未来的缓存-Caffeine

https://blog.csdn.net/weixin_34233618/article/details/86754051
传统的LFU受时间周期的影响比较大。所以各种LFU的变种出现了，基于时间周期进行衰减，或者在最近某个时间段内的频率。同样的LFU也会使用额外空间记录每一个数据访问的频率，即使数据没有在缓存中也需要记录，所以需要维护的额外空间很大。
所以W-TinyLFU结合了LRU和LFU，以及其他的算法的一些特点。
