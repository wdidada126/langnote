---
title: Mac Grpc 环境安装 + Demo
date: 2018-06-16 12:12:35
tags: CSDN迁移
---
  # GOLANG安装和配置环境变量

 参考：   
 [https://blog.csdn.net/liangguangchuan/article/details/53582152](https://blog.csdn.net/liangguangchuan/article/details/53582152)

 这里没有使用brew 进行安装，而是选择在官网下载安装包进行安装，我下载了最新的go1.10.2.darwin-amd64.pkg版本，直接点击安装，安装提示继续就行啦。   
 安装的路径为： /usr/local/go   
 之后进行环境变量配置：

 
```
vim ~/.bash_profile
//在文件中添加如下内容：

GOROOT=/usr/local/go
GOPATH=/Users/Documents/go //GOPAT可以设置你自己的工作目录
export PATH=$GOROOT/bin:$GOPATH/bin:$PATH
```
 然后使配置生效

 
```
source ~/.bash_profile
```
 到此golang环境变量配置完成。

 
# 安装GRPC

 参考：   
 [https://www.jianshu.com/p/7597a2083cc3](https://www.jianshu.com/p/7597a2083cc3)   
 [https://blog.csdn.net/u010471121/article/details/52605365](https://blog.csdn.net/u010471121/article/details/52605365)   
 [https://blog.csdn.net/u010278923/article/details/70130024](https://blog.csdn.net/u010278923/article/details/70130024)

 这里选择使用brew 安装grpc所以在此之前需要安装brew工具，该工具安装可以参考我的另外一个blog :   
 [https://blog.csdn.net/zhumingyuan111/article/details/80711643](https://blog.csdn.net/zhumingyuan111/article/details/80711643)

 先安装 grpc 依赖工具：autoconf，automake， libtool：

 
```
brew install autoconf automake libtool
```
 安装 grpc、protobuf

 
```
brew tap grpc/grpc
brew install --with-plugins grpc
```
 安装完成之后，可以在GOPATH下看到grpc的相关源码：GOPATH下看到grpc的相关源码：GOPATH/src/github.com/golang/protobuf/protoc-gen-go

 目前为止prtoc命令已经安装成功啦，但是如果使用grpc 的插件，但是当时运行以下命令的时候会报错：   
 protoc-gen-go: program not found or is not executable

 
```
protoc --go_out=plugins=grpc:. *.proto
```
 在网上查了很多文章，好像并不是很好用，我的解决办法是，进入目录   
 $GOPATH/src/github.com/golang/protobuf/protoc-gen-go   
 执行

 
```
go build
```
 这样在该目录下就生成了protoc-gen-go 的可执行文件

 找到protoc可执行文件的目录，可以从/usr/local/bin 查到protoc命令的位置，然后将protoc-gen-go 文件放入该目录下即可。

 
# 代码实例

 下面给出hello world demo.   
 Proto文件

 
```
syntax = "proto3";

option java_package = "io.grpc.examples";

package helloworld;

// The greeter service definition.
service Greeter {
  // Sends a greeting
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

// The request message containing the user's name.
message HelloRequest {
  string name = 1;
}

// The response message containing the greetings
message HelloReply {
  string message = 1;
}

```
 执行命令生成GRPC代码

 
```
protoc --go_out=plugins=grpc:. helloworld.proto
```
 服务端代码

 
```
package main

import (
    "net"

    pb "helloworld"

    "fmt"

    "golang.org/x/net/context"
    "google.golang.org/grpc"
)

const (
    port = ":50051"
)

type server struct{}

func (s *server) SayHello(ctx context.Context, in *pb.HelloRequest) (*pb.HelloReply, error) {
    return &pb.HelloReply{Message: "Hello " + in.Name}, nil
}

func main() {
    lis, err := net.Listen("tcp", port)
    if err != nil {
        fmt.Printf("failed to listen: %v", err)
    }
    s := grpc.NewServer()
    pb.RegisterGreeterServer(s, &server{})
    s.Serve(lis)
}

```
 客户端代码

 
```
package main

//client.go

import (
    "log"
    "os"

    pb "helloworld"

    "fmt"

    "golang.org/x/net/context"
    "google.golang.org/grpc"
)

const (
    address     = "localhost:50051"
    defaultName = "world"
)

func main() {
    conn, err := grpc.Dial(address, grpc.WithInsecure())
    if err != nil {
        fmt.Printf("did not connect: %v", err)
    }
    defer conn.Close()
    c := pb.NewGreeterClient(conn)

    name := defaultName
    if len(os.Args) > 1 {
        name = os.Args[1]
    }
    r, err := c.SayHello(context.Background(), &pb.HelloRequest{Name: name})
    if err != nil {
        fmt.Printf("could not greet: %v", err)
    }
    log.Printf("Greeting: %s", r.Message)
}

```
 分别在两个终端运行命令

 
```
go run server.go
go run client.go
```
   
  