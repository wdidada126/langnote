# docker



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





docker查看日志



docker logs



docker ip port

输入回车



invoke com.XXXX.media.platform.isomerization.proxy.api.IsomerizationAccessService.access({“prop”: “value”}, 1, “1”)


