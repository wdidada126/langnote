# boost


boost.test
https://blog.csdn.net/Betterc5/article/details/86291109





https://blog.csdn.net/weixin_33656634/article/details/86133362



Boost库系列：基于boost::asio的http、https serve实现方式总结

https://www.boost.org/doc/libs/1_67_0/doc/html/boost_asio/examples/cpp03_examples.html

1、http::server，简单的单线程服务器，只有一个主线程；
2、 http::server2  多个io_contex响应socket连接
3、 http::server3 一个io_context多个线程run()
4、 http::server4 单线程的协程