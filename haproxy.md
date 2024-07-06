# haproxy

muduo支持高级特性signalfd。--嗯，听起来很高级，不过signalfd不是muduo支持的，而是kernel支持的。一个网络编程库，timer是重中之重，比到底是用epoll还是select都重要。当然，话说回来，再吊的库无非也就是个heap为本的数据结构在支持，无非是有些库喜欢说自己的heap实现比别人都高效，比如haproxy。但muduo却独辟蹊径，用timerfd，泥玛又是一个高级特性啊，很唬
无非是有些库喜欢说自己的heap实现比别人都高效，比如haproxy

c语言写的

https://github.com/haproxy/haproxy

HAProxy Load Balancer's development branch (mirror of git.haproxy.org)

