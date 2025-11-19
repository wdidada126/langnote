csapp

https://www.cnblogs.com/JayL-zxl/p/14338707.html
这是恐龙书（和 CSAPP）的败笔，他先讲 semaphore，再把 mutex 当成前者的特例来介绍（其实 mutex 无论从语意上还是实现上都不是 semaphore 的特例）。我认为应该先讲 mutex ，再讲 condition variable，因为实际开发中这两个最常用，可以完全替代 semaphore（别抬杠说 signal handler 里只可以用 semaphore），然后在习题或小字里提一句 semaphore 就行了。