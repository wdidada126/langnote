# abi

Linux standard Base（LSB）
噢，这到底是巧合呢？还是什么：所有Linux 程序都是在所有机器上运行。我也带个着这个问题去找一些资料。
想信大家听说到POSIX规范，Linux Standard Base(LSB)规范。起初，我以为LSB是API规范而非ABI规范。当我去深入分析时，发现它是一个ABI规范，它解决两方面的问题：

在发行版Linux A上运行的程序，可以运行在发行版本Linux B上。
应用程序在现在的机器上运行，也能在未来新系统和机器上运行。
最近Linux基金会发起LSB项目就是希望Linux发行商能做到相互兼容，并且也能向前兼容。解决Linux应用的可移植性和兼容性。

LSB实际是是一组ABI接口的定义，它规范了运行环境所需要的类型，宏，变量和函数的二进制接口。


https://blog.csdn.net/linyt/article/details/46841845
