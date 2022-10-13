# docker

docker exec -it /bin/bash


tars也使用docker部署了


docker linux上是正宗的，Windows macos上是vm



docker run xxx 从镜像中启动一个容器实例



docker ps 运行的container

docker ps -a 所有container

Docker start



[docker](https://jingyan.baidu.com/article/aa6a2c142dc2774c4c19c4ca.html)
C:\Users\Public\Documents\Hyper-V\Virtual hard disks\MobyLinuxVM.vhdx

docker network create hadoop

docker mac windows都是虚拟机
linux使用了cgroup namespace


         shutdown -h 10          #计算机将于10分钟后关闭，且会显示在登录用户的当前屏幕中
    
         shutdown -h now       #计算机会立刻关机
    
         shutdown -h 22:22     #计算机会在这个时刻关机
    
         shutdown -r now        #计算机会立刻重启
    
         shutdown -r +10         #计算机会将于10分钟后重启
    
         reboot                           #重启
    
         halt                                #关机
    
         当然你如果是centos6.5学过来的，init 0与init 6一样在centos7适用。

docker wordpress
https://www.ruanyifeng.com/blog/2018/02/docker-wordpress-tutorial.html


docker 端口映射
https://www.cnblogs.com/kevingrace/p/9453987.html


轻量级虚拟机

一个项目需要引入docke，可以配置一个DockerFile



coreos竞争



plugin镜像名称 不能包含大写字母

<plugin>
          <groupId>com.spotify</groupId>
          <artifactId>docker-maven-plugin</artifactId>
          <version>1.2.0</version>
          <configuration>
            <!-- 镜像名称 不能包含大写字母-->
            <!--<imageName>${docker.image.prefix}/spring-cloud-producer-curd-withZipkinandAdmin</imageName>-->
            <imageName>${docker.image.prefix}/spring-cloud-producer-curd</imageName>


docker push edidada/spring-cloud-producer-curd-withZipkinandAdmin
invalid reference format: repository name must be lowercase




docker image必须小写

### cgroup

docker的cgroup篇

https://blog.csdn.net/ningyuxuan123/article/details/81981835







Go写的，支持多个系统

docker在原有镜像的基础上构建新的镜像

docker源码已经编译

利用Linux特性
cgroup


```shell

docker search zookeeper

k8s

```

docker打包成镜像
dockerfile

https://github.com/spotify/dockerfile-maven
maven项目打包成docker镜像的工具



[Docker探索系列2之镜像打包与DockerFile](https://www.cnblogs.com/liaojiafa/p/6151768.html)


https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

docker可以根据现有的镜像打包新的镜像
cpp程序 可以直接根据操作系统打包镜像





docker import export

load



docker查看日志



docker logs



docker ip port

输入回车



invoke com.XXXX.media.platform.isomerization.proxy.api.IsomerizationAccessService.access({“prop”: “value”}, 1, “1”)



docker部署image之后，如何登录进去进行操作



docker exec



docker run 和 docker exec 的差异 - 龙凌云端 - 博客园



https://www.cnblogs.com/sparkdev/p/9129334.html



也可以通过 `docker ps -a` 命令查看已经在运行的容器，然后使用容器 ID 进入容器。

`docker exec -it 9df70f9a0714 /bin/bash`



```
docker info
Containers: 11
 Running: 8
 Paused: 0
 Stopped: 3
Images: 10
Server Version: 18.09.2
Storage Driver: overlay2
 Backing Filesystem: extfs
 Supports d_type: true
 Native Overlay Diff: true
Logging Driver: json-file
Cgroup Driver: cgroupfs
Plugins:
 Volume: local
 Network: bridge host macvlan null overlay
 Log: awslogs fluentd gcplogs gelf journald json-file local logentries splunk syslog
Swarm: inactive
Runtimes: runc
Default Runtime: runc
Init Binary: docker-init
containerd version: 9754871865f7fe2f4e74d43e2fc7ccd237edcbce
runc version: 09c8266bf2fcf9519a651b04ae54c967b9ab86ec
init version: fec3683
Security Options:
 seccomp
  Profile: default
Kernel Version: 4.9.125-linuxkit
Operating System: Docker for Mac
OSType: linux
Architecture: x86_64
CPUs: 4
Total Memory: 1.952GiB
Name: linuxkit-025000000001
ID: NSAV:ZK4I:LGUU:O2CR:HL3O:F25E:225E:BTEE:WB64:GJCV:XQJV:WIXB
Docker Root Dir: /var/lib/docker
Debug Mode (client): false
Debug Mode (server): true
 File Descriptors: 93
 Goroutines: 107
 System Time: 2020-08-27T15:01:26.053875352Z
 EventsListeners: 2
HTTP Proxy: gateway.docker.internal:3128
HTTPS Proxy: gateway.docker.internal:3129
Registry: https://index.docker.io/v1/
Labels:
Experimental: false
Insecure Registries:
 127.0.0.0/8
Live Restore Enabled: false
Product License: Community Engine
```





docker 对容器的管理和操作基本都是通过 containerd 完成的



### overlay



**1. Overlay 网络**
**Overlay 技术概述**

Overlay 在网络技术领域，指的是一种网络架构上叠加的虚拟化技术模式，其大体框架是对基础网络不进行大规模修改的条件下，实现应用在网络上的承载，并能与其它网络业务分离，并且以基于IP的基础网络技术为主。Overlay 技术是在现有的物理网络之上构建一个虚拟网络，上层应用只与虚拟网络相关。一个Overlay网络主要由三部分组成：

  边缘设备：是指与虚拟机直接相连的设备
  控制平面：主要负责虚拟隧道的建立维护以及主机可达性信息的通告
  转发平面：承载 Overlay 报文的物理网络

当前主流的 Overlay 技术主要有VXLAN, GRE/NVGRE和 STT。这三种二层 Overlay 技术，大体思路均是将以太网报文承载到某种隧道层面，差异性在于选择和构造隧道的不同，而底层均是 IP 转发。如下表所示为这三种技术关键特性的比较。其中VXLAN利用了现有通用的UDP传输，其成熟性高。总体比较，VLXAN技术相对具有优势。

https://blog.csdn.net/cisco_eigrp/article/details/50829035

https://www.zhihu.com/question/24393680



笔者在前文《[RunC 简介](http://www.cnblogs.com/sparkdev/p/9032209.html)》和《[Containerd 简介](http://www.cnblogs.com/sparkdev/p/9063042.html)》中分别介绍了 runC 和 containerd。本文我们将结合 docker 中的其它组件探索 docker 是如何把这些组件组织起来协调工作的。

Docker CLI(docker)   /usr/bin/docker

Dockerd                     /usr/bin/dockerd

Containerd                /usr/bin/docker-containerd

Containerd-shim      /usr/bin/docker-containerd-shim

Runc                           /usr/bin/docker-runc



![docker compont](https://images2018.cnblogs.com/blog/952033/201806/952033-20180603152512054-430725545.png)





### containerd



### runc





[第一本Docker书（修订版）](https://book.douban.com/subject/26780404/)





[kubernetes权威指南 : 从Docker到Kubernetes实践全接触（第2版）](https://book.douban.com/subject/26902153/)





[Docker——容器与容器云（第2版）](https://book.douban.com/subject/26894736/)

浙江大学SEL实验室

[Spring Cloud与Docker微服务架构实战](https://book.douban.com/subject/27028228/)



[Docker——容器与容器云](https://book.douban.com/subject/26593175/)



[Docker进阶与实战](https://book.douban.com/subject/26701218/)

华为Docker实践小组 





[Docker源码分析](https://book.douban.com/subject/26581184/)





[Docker开发实践](https://book.douban.com/subject/26432893/)


[Docker容器绑定外部IP和端口](https://www.cnblogs.com/linjiqin/p/8670798.html)


docker run -d -P myfirstapp python app.py 

docker run -d -p 9118:8080 edidada/spring-cloud-eureka


`docker exec -it cfb02f1a32c9  /bin/bash`



https://www.cnblogs.com/quanbisen/p/11483118.html