# macports

https://www.macports.org/

MacOS 如果系统自带的 clang/clang++ 太老怎么办？

俺喜欢用 MacPORTS
sudo port install clang-17
当然， 直接把 CWD 切换到 clang-17 所在的目录无疑是个办法。
可是
MacPORTS有更简洁的办法。

mbp71bkb:~ wx$ sudo port install gcc13 clang-17

https://zhuanlan.zhihu.com/p/689572200