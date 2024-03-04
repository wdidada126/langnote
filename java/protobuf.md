# protobuf

https://github.com/protocolbuffers/protobuf

sudo apt update
sudo apt-get install g++ git bazel -y
git clone https://github.com/protocolbuffers/protobuf.git
cd protobuf
git submodule update --init --recursive
bazel build :protoc :protobuf
cp bazel-bin/protoc /usr/local/bin

vcpkg install protobuf protobuf:x64-windows
vcpkg install protobuf[zlib] protobuf[zlib]:x64-windows

```shell
rpm -ivh protobuf-3.11.2-2.el8.x86_64.rpm 
error: Failed dependencies:
	libstdc++.so.6(CXXABI_1.3.8)(64bit) is needed by protobuf-3.11.2-2.el8.x86_64
	libstdc++.so.6(CXXABI_1.3.9)(64bit) is needed by protobuf-3.11.2-2.el8.x86_64
	libstdc++.so.6(GLIBCXX_3.4.20)(64bit) is needed by protobuf-3.11.2-2.el8.x86_64
	libstdc++.so.6(GLIBCXX_3.4.21)(64bit) is needed by protobuf-3.11.2-2.el8.x86_64
```


base http



brpc
从其他语言通过HTTP+json访问基于protobuf的协议.

maven idea先装插件

```xml
<plugin>
    <groupId>org.xolstice.maven.plugins</groupId>
    <artifactId>protobuf-maven-plugin</artifactId>
    <version>0.6.1</version>
   <configuration>
        <protocArtifact>
            com.google.protobuf:protoc:3.1.0:exe:${os.detected.classifier}
        </protocArtifact>
        <pluginId>grpc-java</pluginId>
        <pluginArtifact>
            io.grpc:protoc-gen-grpc-java:1.11.0:exe:${os.detected.classifier}
        </pluginArtifact>
    </configuration>
    <executions>
        <execution>
            <goals>
                <goal>compile</goal>
                <goal>compile-custom</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

会依赖target下面的java类，不会报错


[基于http协议使用protobuf进行前后端交互](https://segmentfault.com/a/1190000018161715)

"Content-Type"："application/x-protobuf"


基于http协议的


### protobuf-wireshark plugins

wireshark抓包

https://blog.csdn.net/zhangmiaoping23/article/details/80394472