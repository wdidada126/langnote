# Performance Analysis and Tuning on Modern CPUs

## 版本与 ISBN

- 书名：*Performance Analysis and Tuning on Modern CPUs*（2nd Edition）
- 作者：Denis Bakhvalov（easyperf.net，Intel）等
- 出版方式：作者自出版（Amazon KDP），第2版 2024-11 上架纸质/Kindle
- 第1版纸质 ISBN（Amazon ASIN/ISBN-13）：`979-8575614234`（2020，Independently Published）
- 第2版电子版可在 GitHub 免费下载（CC BY 授权）：https://github.com/dendibakh/perf-book

> 2026-09-22 由 202609 月度笔记（性能优化书单）整理。

## 笔记

- 现代 CPU 性能分析实战必备：测量方法、微架构（流水线/分支预测/存储层次）、PMU 硬件计数器、top-down 分析法。
- 实战章节覆盖源码级优化：循环优化、向量化（SIMD）、分支优化、内存布局、PGO 等。
- 自出版性质决定了没有传统出版社 ISBN；引用时用第2版（2024）+ GitHub 仓库标识即可。

## 跨年摘录（2020–2026 日常笔记聚合，2026-09-23 整理）

### 2020-11
> 另外，即便只说学习，光看完《C++ Primer》还不够，因为多数人并不能领会其中的深意，只是看到它最表面的语法层面的部分。《Effective C++》 《More Effective C++》 《C++ Common Knowledge》都看完才算是入门了。《Exceptional C++》《C++ Templates》也读懂了才算是对这门语言有所了解。学C++，你要懂的非常多，基本功非常扎实，才能在实际工作中得心应手，否则就会遇到很多看不懂的代码，莫名其妙的错误和崩溃。而学其他的语言基本上一本书就可以搞定了，想成为高手的人才需要钻研钻研原理和底层的东西。稍微举个例子，c++想实现网络通信要学习socket，学习windows和linux等平台下的api，或者研究一下现在开源的库里面有没有比较好用并且会用的（能分析出这个就已经不是新手了）。而很多其他语言只要一个标准库的类或者函数就搞定了，标准库把细节封装好了，作为使用者直接使用就可以了，不仅简单方便，而且不容易犯错误。

