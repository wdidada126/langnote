# go

https://pkg.go.dev/

从事服务器开发，且同时使用过C++、Erlang和golang，说说我对golang并发编程的看法。
golang使用协程加chan来实现并发编程，golang的协程相比C++，更轻量，写法简单，但是随着C++也支持协程后，只剩写法简单一个优势了。相比Erlang的进程我觉得是谈不上孰好孰坏。
再来说说golang的chan，我觉得是败笔。chan没有解决传统多线程编程的问题，使用chan进行协程间的通信同样极易出现死锁等资源竞态问题，而且chan居然不支持跨进程使用，虽然网上有第三方的netChan，但是和原生用法不兼容。相比Erlang提出了一种解决传统多线程编程问题的方法，真的解决了，并且实现的很易用。
总的来说，golang简化了多线程编程的写法，但是并没有解决核心问题，多线程编程之所以难，并不是因为语言的语法复杂，而是因为线程间的同步处理难，golang的做法并没有解决这个问题。


ginkgo
go测试库

## go blog

https://blog.golang.org/h2push

## go Modules
https://github.com/golang/go/wiki/Modules

https://github.com/zeromicro/go-zero

https://go.dev/dl

go编译器
自举

一看评论就是半吊子技术，python那种混乱的包管理还有洗地的，go1.12以前是很混乱，但是1.13扶正用mod之后，一直到现在的1.20已经很好用了，用过python 的pip，java的maven gradle，php的composer，就问哪个能直接给你replace来改第三方代码调试，剔除依赖，语义化版本规范，我刚刚提的那些包管理，哪一个能打，是不是gomod最简洁，用起来最舒服

Go知识体系
https://www.processon.com/view/link/5ff500aa1e08531de81e1288


https://golang.google.cn/

Go是更好的c

Godi是一个用来检查Go程序包依赖哪些其他包的

### 使用Go的地区
美国 日本 中国

go 会自动生成一个 go.sum 文件来记录 dependency tree



go env
set GO111MODULE=on
set GOARCH=amd64
set GOBIN=
set GOCACHE=C:\Users\edidada\AppData\Local\go-build
set GOENV=C:\Users\edidada\AppData\Roaming\go\env
set GOEXE=.exe
set GOFLAGS=
set GOHOSTARCH=amd64
set GOHOSTOS=windows
set GOINSECURE=
set GONOPROXY=
set GONOSUMDB=
set GOOS=windows
set GOPATH=C:\Users\edidada\go
set GOPRIVATE=
set GOPROXY=https://goproxy.cn
set GOROOT=D:\Go14
set GOSUMDB=sum.golang.org
set GOTMPDIR=
set GOTOOLDIR=D:\Go14\pkg\tool\windows_amd64
set GCCGO=gccgo
set AR=ar
set CC=gcc
set CXX=g++
set CGO_ENABLED=1
set GOMOD=NUL
set CGO_CFLAGS=-g -O2
set CGO_CPPFLAGS=
set CGO_CXXFLAGS=-g -O2
set CGO_FFLAGS=-g -O2
set CGO_LDFLAGS=-g -O2
set PKG_CONFIG=pkg-config
set GOGCCFLAGS=-m64 -mthreads -fmessage-length=0 -fdebug-prefix-map=C:\Users\edidada\AppData\Local\Temp\go-build842397178=/tmp/go-build -gno-record-gcc-switches


go国内镜像 七牛云

go env
在这堆中看到这个GOPROXY，这个就是镜像的位置，默认为https://proxy.golang.org

go env -w GO111MODULE=on
go env -w GOPROXY=https://goproxy.cn/



 呼出命令行（快捷键 Win + R），输入cmd，执行下方两行命令
go env -w GO111MODULE=on

go env -w GOPROXY=https://goproxy.cn,direct


https://www.cnblogs.com/jokingremarks/p/15095304.html


## go mod

go mod介绍

go modules 是 golang 1.11 新加的特性。现在1.12 已经发布了，是时候用起来了。Modules官方定义为：

模块是相关Go包的集合。modules是源代码交换和版本控制的单元。go命令直接支持使用modules，包括记录和解析对其他模块的依赖性。modules替换旧的基于GOPATH的方法来指定在给定构建中使用哪些源文件。

go mod官方自带的构建工具



例子：github.com/edidada/testmemberlist

go mod 

- download
- edit
- graph
- init
- tidy
- vendor
- verify
- why


go help mod
Go mod provides access to operations on modules.

Note that support for modules is built into all the go commands,
not just 'go mod'. For example, day-to-day adding, removing, upgrading,
and downgrading of dependencies should be done using 'go get'.
See 'go help modules' for an overview of module functionality.

Usage:

        go mod <command> [arguments]

The commands are:

        download    download modules to local cache
        edit        edit go.mod from tools or scripts
        graph       print module requirement graph
        init        initialize new module in current directory
        tidy        add missing and remove unused modules
        vendor      make vendored copy of dependencies
        verify      verify dependencies have expected content
        why         explain why packages or modules are needed

Use "go help mod <command>" for more information about a command.


https://golang.google.cn/


- ### [go-personal-develop](https://github.com/edidada/go-personal-develop)

- ### [gostltest](https://github.com/edidada/gostltest)

- ### [testpflag](https://github.com/edidada/testpflag)





java跟go很像的方案是actor，也就是akka，但并没有协程漂亮，这也没办法，因为java没法像c一样可以随意修改自己的栈空间





https://github.com/duanxr/cvc



go显然是彻底解决了io问题，从底层消灭了阻塞io，却又封装成同步接口，看起来用的是socket，实际上是epoll，并发又好，开发效率又高（详见此文章https://zhuanlan.zhihu.com/p/32997421）。计算性能和编译速度，也是有巨大改进的，但这个稍微次要一些。

但go，对于大型业务项目来说，我们遇到几个问题。

1、生态不完善

生态不完善，要么自己造轮子，要么心惊胆战地去用开源的轮子。自己造轮子没时间，一堆开源轮子也不知道是哪个阿猫阿狗写的，特别不放心。前两天遇到一个基础conf库，在get的时候进行delete，panic了。zk、redis、hbase等要命的玩意儿的client都不是官方的。

2、没解决依赖问题

编译是用文件依赖来解决，官方的解法（还没完成）是靠git 版本实现，这就导致做业务拆分很困难（翻墙不易），不同业务想依赖同一个项目的不同版本很麻烦，只能各种山寨办法模仿nexus。

3、语法问题

语法其实都是有利有弊，这里也不算问题吧，只是我们做一些基础轮子的时候，反射不强大，总是需要写出一堆需要业务写defer的逻辑，跨业务error也是坑。不太容易做到“面向乱搞编程”，防止使用者乱搞。

总之我的理解，目前go不太适合做稍微大规模一点的团队替代整个技术栈，可以考虑做一些做小而美的基础服务，比如像etcd这种东东。做大型业务，绝对会拖垮开发效率。



说实话，如果感觉机器性能吃的厉害，往往不是换语言的问题，当然人家愿意搞，其实也挺好的。如果是我，在没有历史包袱的情况下，是不会选择go的，我的价值观是用技术成就商业，而不是用公司的资源去成就一门技术。





grpc是支持go语言的框架

b站开源go开发框架
https://github.com/bilibili/kratos

go get

[go bfe](https://github.com/baidu/bfe)

makefile编译

gokit

A standard library for microservices. https://gokit.io





golang 编译器

golang的ssa代码注释写得非常好了。可以通过看一些教材补充上一些知识盲点就行了。Tarjan的求dominator tree的算法正确性证明因为大量使用了反证法（图的东西反证法都挺多），所以不那么直观。golang在ssa上提供的变换其实算非常少的（据说是golang的人不喜欢花哨的优化），主要是DCE，CSE，BCE，在经典的编译器教材都有涉及。golang使用的RegAlloc是贪心的[LSRA](http://link.zhihu.com/?target=http%3A//web.cs.ucla.edu/~palsberg/course/cs132/linearscan.pdf)（类似LLVM），我觉得注释写得足够好了。汇编生成那块，我感觉是golang是疯狂使用peephole来做，在gen目录下有大量的pattern。







go语言高并发服务器开发实战

zhihulive



https://draveness.me/golang/docs/part1-prerequisite/ch02-compile/golang-ir-ssa/





init函数



[GO1.8特性---plugin](https://blog.csdn.net/m0_38132420/article/details/68496881)





https://blog.csdn.net/weixin_33807284/article/details/92567498





go defer



go语言的defer语句



CodingCode关注

go语言defer语句的用法

defer的语法

defer后面必须是函数调用语句，不能是其他语句，否则编译器会出错。



https://www.cnblogs.com/phpper/p/11984161.html



在Go语言中，可以使用关键字defer向函数注册退出调用，即主函数退出时，defer后的函数才被调用。defer语句的作用是不管程序是否出现异常，均在函数退出时自动执行相关代码。 


在函数中,程序员经常需要创建资源(比如:数据库连接、文件句柄、锁等) ,为了在函数执行完 毕后,及时的释放资源,Go 的设计者提供 defer (延时机制)。



可以了解下golang对io的抽象，以及goroutine的调度。真要能把golang的模型在android硬件上做出来，还是比较震撼的。





**2019GO语言就业形势如何**

举个例子来说，目前Java大数据、云计算、微服务、分布式系统等这些都是薪资待遇很好的岗位了，但是这些优厚的待遇背后，也同样是对应的技能栈的要求。也就是说，外部的就业环境再好，对每一个就业的个体而言，本身技能还是要过硬。

https://www.zhihu.com/question/317763907/answer/711992752



GopherChina 2019 1-1 基于 Go 语言的大规模微服务框架设计 滴滴



从事服务器开发，且同时使用过C++、Erlang和golang，说说我对golang并发编程的看法。

golang使用协程加chan来实现并发编程，golang的协程相比C++，更轻量，写法简单，但是随着C++也支持协程后，只剩写法简单一个优势了。相比Erlang的进程我觉得是谈不上孰好孰坏。

再来说说golang的chan，我觉得是败笔。chan没有解决传统多线程编程的问题，使用chan进行协程间的通信同样极易出现死锁等资源竞态问题，而且chan居然不支持跨进程使用，虽然网上有第三方的netChan，但是和原生用法不兼容。相比Erlang提出了一种解决传统多线程编程问题的方法，真的解决了，并且实现的很易用。

总的来说，golang简化了多线程编程的写法，但是并没有解决核心问题，多线程编程之所以难，并不是因为语言的语法复杂，而是因为线程间的同步处理难，golang的做法并没有解决这个问题。

在函数中,程序员经常需要创建资源(比如:数据库连接、文件句柄、锁等) ,为了在函数执行完 毕后,及时的释放资源,Go 的设计者提供 defer (延时机制)。





bilibili go实战

https://blog.csdn.net/ailinyingai/article/details/95113867





`go get github.com/hashicorp/memberlist`





go

pkg

src

bin

memberlist.a







因为 gomod 和 gopath 两个包管理方案，并且相互不兼容有他没我那样。

在 gopath 查找包，按照 goroot 和多 gopath 目录下 src/xxx 依次查找。

在 gomod 下查找包，解析 go.mod 文件查找包，mod 包名就是包的前缀，里面的目录就后续路径了。

在 gomod 模式下，查找包就不会去 gopath 查找，只是 gomod 包缓存在 gopath/pkg/mod 里面。



https://learnku.com/go/t/43016



go mod init github.com/edidada/testmemberlist



## go mod

一看评论就是半吊子技术，python那种混乱的包管理还有洗地的，go1.12以前是很混乱，但是1.13扶正用mod之后，一直到现在的1.20已经很好用了，用过python 的pip，java的maven gradle，php的composer，就问哪个能直接给你replace来改第三方代码调试，剔除依赖，语义化版本规范，我刚刚提的那些包管理，哪一个能打，是不是gomod最简洁，用起来最舒服
