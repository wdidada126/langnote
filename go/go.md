# go

https://pkg.go.dev/std

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

## Go 综合笔记（截至 2026-08）

### 定位与版本边界

Go 的优势在于静态编译、简单部署、标准库网络能力、可观测运行时和适合服务端的并发模型。它适合 API、基础设施、云原生控制面、网络代理、CLI、存储/中间件组件和高并发 I/O 服务；它不是“更好的 C”或自动高性能的保证。算法、数据库、网络、分配、锁竞争和系统调用仍然决定最终吞吐与 P99。

截至 2026-08，稳定主线为 Go 1.26，最近补丁为 Go 1.26.5（2026-07-07）。Go 1.26 保持 Go 1 的兼容性承诺，并对语言、工具链、运行时和标准库持续演进。生产构建应固定 `go`/`toolchain` 版本并及时跟进受支持版本的安全补丁，不应只因“代码能编译”长期停留在旧工具链。

官方参考：

- 发布历史：https://go.dev/doc/devel/release
- Go 1.26 Release Notes：https://go.dev/doc/go1.26
- 标准库：https://pkg.go.dev/std
- 内存模型：https://go.dev/ref/mem

### 类型、接口、错误与资源边界

Go 的接口是隐式实现，适合在消费侧定义小接口并用具体类型构造实现。不要为每个 struct 预先声明“万能接口”，也不要用 `any` 绕过领域模型。`nil` interface 与“接口值持有一个 nil 指针”不同，后者的接口本身不为 nil，是常见的错误判断来源。

```go
type Store interface {
	Find(ctx context.Context, id string) (Order, error)
}

func Load(ctx context.Context, s Store, id string) (Order, error) {
	order, err := s.Find(ctx, id)
	if err != nil {
		return Order{}, fmt.Errorf("find order %q: %w", id, err)
	}
	return order, nil
}
```

错误是显式返回值。用 `fmt.Errorf("...: %w", err)` 保留因果链，调用方用 `errors.Is`/`errors.As` 判断可恢复错误；不要靠字符串匹配错误，也不要在基础库中随意 `panic`。`panic` 适用于不可恢复的程序不变量或初始化失败，不应用作常规请求错误控制流。`defer` 适合成对释放文件、锁、span 和 rollback，但它在函数返回时执行，循环内大量 `defer` 可能使资源持有到整个函数结束；应提取小函数或显式关闭。

### GMP、channel 与内存模型

G（goroutine）是用户态执行单元，M 是操作系统线程，P 是执行 Go 代码所需的调度资源。`GOMAXPROCS` 控制可同时执行 Go 代码的 P 数量，通常默认等于可用 CPU 数；它不等于 M 的总数。运行时会在阻塞系统调用、网络轮询、work stealing、抢占和 GC 中调度 G/M/P，实际线程数会因 cgo、阻塞调用等高于 P 数量。

channel 既传递数据也建立同步关系，但不是“解决并发问题”的万能抽象，更不是跨进程 MQ。并发困难仍来自所有权、取消、背压、失败、资源生命周期和共享状态。传递工作流/所有权时用 channel 很自然；保护共享 map、计数器、缓存或不变量时 `sync.Mutex`、`sync.RWMutex`、`sync.Once`、`sync/atomic` 往往更直接。

| 问题 | 推荐机制 | 不要依赖 |
| --- | --- | --- |
| 单一所有者串行处理任务 | channel + 明确关闭方 | 多个 goroutine 随意 close 同一 channel。 |
| 共享 map/复合状态 | mutex 或单 owner goroutine | 并发读写 map，运行时可能直接 fatal。 |
| 一次性初始化 | `sync.Once` | 无同步的 double-check。 |
| 计数/状态位 | `sync/atomic` 或 mutex | `volatile` 式直觉；Go 没有该关键字。 |
| 并发上限 | 有界 worker pool、semaphore/channel | 每个请求无界 `go func()`。 |

Go 内存模型保证无 data race 的程序可按顺序一致性理解（DRF-SC）。channel send/receive、mutex unlock/lock、WaitGroup、atomic 等可建立 happens-before；仅启动 goroutine 或等待其“看起来运行过”不构成完成同步。`go test -race ./...` 是重要防线，但只能发现实际执行到的竞态，不能替代所有权设计和压力测试。

### Context、取消与 goroutine 生命周期

`context.Context` 用于传递请求范围的 deadline、取消和少量跨 API 元数据。入口创建/接收 context，所有可阻塞调用向下传递，退出时取消；不要把 context 放进 struct 长期保存，不要用 string 作为 context key，也不要把可选业务参数塞进 context。

每一个启动的 goroutine 都必须能回答：谁拥有它、何时退出、如何取消、如何等待、失败如何上报。HTTP 请求结束、上游超时、服务关闭时，数据库、RPC、MQ、worker 和重试都应收到取消信号。使用 `errgroup.WithContext` 或 `WaitGroup` 协调生命周期，带缓冲 channel 时仍需考虑生产者退出后谁消费、消费者退出后谁停止生产。

```go
func RunWorkers(ctx context.Context, jobs <-chan Job, n int) error {
	g, ctx := errgroup.WithContext(ctx)
	for i := 0; i < n; i++ {
		g.Go(func() error {
			for {
				select {
				case <-ctx.Done():
					return ctx.Err()
				case job, ok := <-jobs:
					if !ok {
						return nil
					}
					if err := handle(ctx, job); err != nil {
						return err
					}
				}
			}
		})
	}
	return g.Wait()
}
```

此模式仍要由调用方定义重试、幂等、任务 channel 的唯一关闭者和 `context.Canceled` 是否应向外返回。不能在 `handle` 内忽略 context 后又期待取消能及时生效。

### Modules、工作区与供应链

Modules 已取代 GOPATH 的源码定位模式；但 `GOPATH/pkg/mod` 仍是模块缓存位置，GOPATH 不是“完全消失”。`go.mod` 记录模块路径、语言版本、直接/间接依赖和 replace/retract 等指令，`go.sum` 记录下载内容的校验和，两者都应提交。最小版本选择（MVS）使构建依赖图可预测，但不自动等于依赖没有漏洞或行为兼容。

| 文件/变量 | 用途 | 实践 |
| --- | --- | --- |
| `go.mod` | 模块 API 与依赖需求 | 评审变更，避免无理由大范围升级。 |
| `go.sum` | 模块内容校验 | 提交到仓库，不手工随意删除。 |
| `go.work` | 本地多个模块协同开发 | 通常不提交个人临时 workspace，除非仓库明确采用。 |
| `replace` | 本地调试或临时替换 | 不应随发布版本泄漏到生产依赖图。 |
| `GOPRIVATE` | 私有模块路径匹配 | 同时配置 `GONOSUMDB`/`GONOPROXY` 策略，避免泄露私有路径。 |

常用闭环：`go mod tidy` 后检查 diff；`go mod verify` 校验缓存；`go list -m -u all` 查看可升级模块；`govulncheck ./...` 与 SBOM/依赖扫描进入 CI；私有依赖使用受控 Git/代理和最小权限 token。不要把 `GOSUMDB=off` 或全局 `GOINSECURE` 当作永久网络问题解决方案。

参考：[Modules Reference](https://go.dev/ref/mod)、[开发和发布模块](https://go.dev/doc/modules/developing)。

### HTTP、数据库与服务端实践

`net/http` 服务应设置 `ReadHeaderTimeout`、`ReadTimeout`、`WriteTimeout`、`IdleTimeout` 和最大请求体，限制并发与队列，配置优雅关闭。每个出站 HTTP/RPC/数据库调用都需要 context deadline；没有 deadline 的重试会在故障时堆积 goroutine、连接和内存。`http.Client`/Transport、数据库 `sql.DB` 都是可复用连接池，不应每请求创建，也要设置最大连接、空闲连接与生命周期。

数据库事务只包住必要的数据库操作，不要在事务中调用远程 HTTP、等待 MQ 或做长时间计算。使用参数化 SQL、防止 N+1、检查索引和执行计划；对死锁、序列化冲突和临时网络错误执行有限次数、带退避且幂等的整体重试。服务契约要显式处理超时、取消、重复请求、部分成功和可观测错误码。

### 测试、诊断与性能

| 工具 | 目的 | 使用注意 |
| --- | --- | --- |
| `go test ./...` | 单元/集成测试 | 并发测试要等待所有 goroutine，不要用任意 `Sleep` 断言。 |
| `go test -race ./...` | 发现已执行路径的数据竞态 | 有开销，CI 和预发布压力测试都应覆盖。 |
| fuzz testing | 探索解析/边界输入 | 固化触发样本并限制资源。 |
| benchmark + `-benchmem` | 吞吐、分配和回归比较 | 固定输入/CPU，避免把网络波动当优化结果。 |
| `pprof` / trace | CPU、heap、goroutine、block、mutex、调度分析 | 先采样定位，避免凭感觉加池/改 GC。 |

线上 pprof 必须鉴权或仅暴露在受控管理网，不能直接公开 `/debug/pprof`。排障先区分 CPU 饱和、分配/GC、goroutine 泄漏、锁竞争、block、网络、数据库和下游限流；官方诊断文档说明 `pprof` 可分析 CPU/heap 等 profile，不同诊断工具也可能互相干扰，采样时一次聚焦一个假设。

官方参考：[Go Diagnostics](https://go.dev/doc/diagnostics)、[Race Detector](https://go.dev/doc/articles/race_detector)、[Context 模式](https://go.dev/blog/context)。

### 常见问答与学习路线

- **goroutine 很轻，能无限创建吗？** 不能。每个 goroutine 有栈、调度、闭包/引用和下游资源；无界 fan-out 会耗尽内存、连接或触发级联超时。
- **channel 和 mutex 如何选？** 传递任务/所有权用 channel；保护共享状态用 mutex 往往更简单。选择可证明的生命周期，而不是遵循口号。
- **关闭 channel 谁负责？** 通常唯一发送方负责；接收方不关闭未知生产者仍可能发送的 channel。关闭不是广播错误机制，需配合 context/error。
- **Go 为什么能高并发 I/O？** runtime 将大量 goroutine 调度到少量线程，并集成网络轮询；阻塞业务逻辑、慢下游、无超时和连接耗尽仍会使服务失败。
- **`go mod tidy` 能随时运行吗？** 可以作为维护工具，但会改变依赖图；应在 CI/评审中检查原因，不能把大版本升级和业务改动混在一次提交。

学习顺序：语言/接口/错误/测试 -> slices、maps、escape 与 GC -> context、channel、mutex、内存模型 -> Modules 与供应链 -> `net/http`、数据库、RPC -> pprof/trace/race -> runtime 源码。仓库可继续阅读 [Go Modules](go_module.md)、[调度器](../backend-interview/Go/go-scheduler.md)、[etcd](etcd/etcd.md)、[memberlist](go_memberlist.md)。真正掌握 Go 的标准是能解释一个请求的超时与取消如何穿透、共享数据如何同步、goroutine 如何退出、依赖如何可复现，以及性能结论来自哪份 profile。

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
