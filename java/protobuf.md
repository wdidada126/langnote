# protobuf



base http



brpc
从其他语言通过HTTP+json访问基于protobuf的协议.

maven idea先装插件


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


会依赖target下面的java类，不会报错







[基于http协议使用protobuf进行前后端交互](https://segmentfault.com/a/1190000018161715)

"Content-Type"："application/x-protobuf"


基于http协议的




### protobuf-wireshark plugins

wireshark抓包

https://blog.csdn.net/zhangmiaoping23/article/details/80394472