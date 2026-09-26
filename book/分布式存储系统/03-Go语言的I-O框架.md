# 第 3 章　Go 语言的 I/O 框架

> 原书第 3 章把 Go 标准库的 I/O 体系拆开讲：从 `io.Reader`/`io.Writer` 这套基础接口，
> 到字节/字符串/网络/文件/缓冲五类标准库拓扑，再到 `fs.FS` 文件系统抽象。
> 这是全书从「Go 语法」跨到「存储编程」的桥——后面所有读写都建立在这套接口上。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 3.1 I/O 的定义 | 基础类型（Reader/Writer）、组合类型（ReadWriter/ReadWriteCloser）、进阶类型（SectionReader/TeoReader 等） | I/O 被抽象成「读/写接口」，一切皆可组合 |
| 3.2 通用 I/O 函数 | 面向 I/O 接口的操作（io.Copy/ReadFull）、文件 I/O 操作函数 | 标准库提供与具体介质无关的搬运函数 |
| 3.3 文件系统 | FS 接口定义（fs.FS）、实现与扩展（嵌入、子树、包装） | fs.FS 让「文件系统」成为可替换的抽象 |
| 3.4 I/O 标准库拓扑 | 字节 I/O、字符串 I/O、网络 I/O、文件 I/O、缓冲 I/O | 五类拓扑共享同一套接口，互相可套娃 |
| 3.5 文件 I/O 和网络 I/O | 文件读写、网络读写（net 包、conn 即 Reader/Writer） | 文件与 socket 在 Go 里都是 Reader/Writer |
| 3.6 本章小结 | 承上启下 | 第 4 章起进入 Linux 存储栈的「另一侧」 |

> 注：3.1 三层类型名（基础/组合/进阶）取自当当目录；3.3.2、3.4 各类名依目录列出。

## 核心精讲

（以下为教学性梳理，代码均**教学示意，不参与构建**。）

### 3.1 一切皆 Reader/Writer

Go I/O 的精髓是**小接口 + 组合**：

```go
// 教学示意，不参与构建：io.Reader / io.Writer 的最小契约
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
// 组合类型如 io.ReadWriter = Reader + Writer；进阶如 io.SectionReader 限制读范围
```

因为协议极小，**任何东西**只要实现 `Read`/`Write` 就能接入整套生态：
文件、网络、内存缓冲、压缩流、加密流、HTTP body 全都串得起来。

### 3.2 与介质无关的搬运

`io.Copy(dst, src)` 不需要知道 dst/src 是什么，只认接口——这正是「缓冲/网络/文件可互相拷贝」的原因：

```go
// 教学示意，不参与构建：把文件拷到 HTTP 响应，零业务样板
io.Copy(httpResp, fileReader)   // fileReader 是 *os.File（实现了 Reader）
```

### 3.3 fs.FS：文件系统的可替换抽象

Go 1.16 引入的 `fs.FS` 把「一个文件系统」抽象成接口，于是**内存 FS、zip FS、嵌入 FS、远程 FS**
都能以同一方式访问，是写测试与可插拔存储后端的利器（也直接服务于第 15 章用户态 FS）：

```go
// 教学示意，不参与构建：用 fs.FS 抽象读写，后端可替换
type FS interface {
    Open(name string) (fs.File, error)
}
// os.DirFS("./data") 是磁盘后端；fstest.MapFS 是内存后端；embed.FS 是编译期嵌入
```

### 3.4–3.5 五类拓扑与文件/网络 I/O

- **字节/字符串 I/O**：`bytes.Buffer`、`strings.Reader`——内存里的流；
- **缓冲 I/O**：`bufio.Reader/Writer` 在底层 Reader/Writer 外面包一层缓冲，
  **把大量小读写攒成少量大读写**，是降系统调用次数的关键（见第 5 章）；
- **文件 I/O**：`os.Open` 返回 `*os.File`，落点是第 4 章的 Linux 系统调用；
- **网络 I/O**：`net.Conn` 既是 Reader 又是 Writer，socket 与文件在 Go 里同构。

## 版本演进

- 本章 `io`/`fs`/`bufio`/`net` 体系在 Go 1.16（`fs.FS`）之后基本稳定，2024 年书出版时与当前一致。
- 🔧 **2026 视角补入**：Go 1.23 的 `iter` 迭代器新增 `bytes`、`slices`、`maps` 的迭代函数，
  以及 `fs` 相关的遍历更顺手；流式处理（3.4 字节 I/O 段）可用 `iter.Seq[[]byte]` 表达分块读，
  比 `io.Reader` 回调式更直观。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| 《The Go Programming Language Specification》— `io`、`fs`、`bufio` 包 | golang.org 规范 | 本章所有接口的权威定义 |
| Russ Cox《JSON and Go》/《The Go Blog: io 包设计》 | Go Blog | Reader/Writer 组合哲学的工程说明 |
| Pike《Go's design philosophy for I/O》 | GopherCon 演讲集 | 「小接口组合」为何适合系统编程 |

> 均为 Go 官方规范/博客，属工程文档，非同行评审论文。

## 近年研究与工业界开源实践（2015–2026）

- **Go I/O 生态仍是存储项目的骨架**：`minio/minio`（61350★）、`juicedata/juicefs`（14471★）、
  `seaweedfs/seaweedfs`（34989★）都在 `io.Reader/Writer`/`fs.FS` 之上构建各自的读写管线，
  印证 3.1–3.3 的「接口可组合」价值。
- **FUSE 绑定实现 FS 接口**：`hanwen/go-fuse`（2376★）、`bazil/fuse`（1738★）把 `fs.FS`
  接到内核 FUSE 协议上（见 [15-用户态文件系统.md](15-用户态文件系统.md)），是 3.3 的实战落点。
- **高性能网络 I/O**：`panjf2000/gnet`（11251★）提供类 net 但更高吞吐的事件驱动网络框架，
  是 3.5 网络 I/O 的性能向延伸（见 [07-并发I-O模型.md](07-并发I-O模型.md)）。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「io.Copy 会一次读进内存」 | io.Copy 用固定大小缓冲（默认 32KB）分块搬，不会整文件入内存 |
| 2 | 「bufio 总是更快」 | bufio 对小随机读写帮助大；但对已是大块顺序 I/O 反而多一层拷贝，未必更快 |
| 3 | 「网络 I/O 和文件 I/O 是两回事」 | Go 里两者都实现同一套 Reader/Writer，可统一处理 |
| 4 | 「fs.FS 只能读磁盘」 | fs.FS 后端可内存/zip/embed/远程，是可替换抽象 |
| 5 | 🔧 流式示例只给 Reader 回调 | Go 1.23 起可补 `iter` 迭代器写法（2026 视角） |

## 与其他章 / 其他书的联系

- **本书内**：3.1 接口 → [04-Linux存储基础.md](04-Linux存储基础.md)（文件的系统调用落点）
  → [05-存储I-O实践.md](05-存储I-O实践.md)（缓冲/零拷贝）；3.3 fs.FS →
  [15-用户态文件系统.md](15-用户态文件系统.md)；3.5 网络 I/O → [07-并发I-O模型.md](07-并发I-O模型.md)。
- [../设计数据密集型应用/03-存储与检索.md](../设计数据密集型应用/03-存储与检索.md)
  ——DDIA 讲操作系统 I/O 与缓冲的底层原理，与本章 bufio 段互补。
- 《The Go Programming Language》（Donovan & Kernighan）第 7 章 I/O 是本章系统教材。
