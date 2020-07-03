---
title: Ubuntu&GRPC+Idea java demo
date: 2017-07-16 22:09:46
tags: CSDN迁移
---
  Grpc 现在已经非常流行，所以我也进行简单的研究。以下在ubuntu下用Idea 搭建grpc&java 的示例。

 
### pom.xml

 
```
<dependencies>
        <dependency>
            <groupId>com.google.protobuf</groupId>
            <artifactId>protobuf-java</artifactId>
            <version>3.3.0</version>
        </dependency>
        <dependency>
            <groupId>io.grpc</groupId>
            <artifactId>grpc-netty</artifactId>
            <version>1.4.0</version>
        </dependency>
        <dependency>
            <groupId>io.grpc</groupId>
            <artifactId>grpc-protobuf</artifactId>
            <version>1.4.0</version>
        </dependency>
        <dependency>
            <groupId>io.grpc</groupId>
            <artifactId>grpc-stub</artifactId>
            <version>1.4.0</version>
        </dependency>
    </dependencies>
    <build>
        <extensions>
            <extension>
                <groupId>kr.motd.maven</groupId>
                <artifactId>os-maven-plugin</artifactId>
                <version>1.4.1.Final</version>
            </extension>
        </extensions>
        <plugins>
            <plugin>
                <groupId>org.xolstice.maven.plugins</groupId>
                <artifactId>protobuf-maven-plugin</artifactId>
                <version>0.5.0</version>
                <configuration>
                    <protocArtifact>com.google.protobuf:protoc:3.3.0:exe:${os.detected.classifier}</protocArtifact>
                    <pluginId>grpc-java</pluginId>
                    <pluginArtifact>io.grpc:protoc-gen-grpc-java:1.4.0:exe:${os.detected.classifier}</pluginArtifact>
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
        </plugins>
    </build>
```
 以上内容主要参考   
 [https://github.com/grpc/grpc-java/blob/master/README.md](https://github.com/grpc/grpc-java/blob/master/README.md)

 
### proto 文件

 Helloworld.proto

 
```
syntax="proto3";
option java_package="com.grpc.demo";
option java_outer_classname="HelloWorldProto";

message Request{
    int64 id=1;
    string name=2;
    string age=3;
}

message Replay{
    string mes = 1;
}

service HelloService {
    rpc greet(Request) returns (Replay);
}
```
 将proto文件放在src/main/proto 和 src/test/proto的位置。如下项目结构。   
 ![这里写图片描述](https://img-blog.csdn.net/20170716221548102?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)   
 运行package进行项目打包，则会在target 文件会生成java代码。   
 可能会出现如下错误，但是不会有影响。路过大神可以帮忙给出解决办法。

 
```
java.lang.NoSuchMethodError: org.apache.maven.execution.MavenSession.getRepositorySession()Lorg/eclipse/aether/RepositorySystemSession;
    at kr.motd.maven.os.RepositorySessionInjector.injectRepositorySession(RepositorySessionInjector.java:22)
    at kr.motd.maven.os.DetectExtension.injectSession(DetectExtension.java:148)
    at kr.motd.maven.os.DetectExtension.afterProjectsRead(DetectExtension.java:107)
    at org.apache.maven.DefaultMaven.doExecute(DefaultMaven.java:274)
    at org.apache.maven.DefaultMaven.execute(DefaultMaven.java:156)
    at org.apache.maven.cli.MavenCli.execute(MavenCli.java:537)
    at org.apache.maven.cli.MavenCli.doMain(MavenCli.java:196)
    at org.apache.maven.cli.MavenCli.main(MavenCli.java:141)
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
    at java.lang.reflect.Method.invoke(Method.java:498)
    at org.codehaus.plexus.classworlds.launcher.Launcher.launchEnhanced(Launcher.java:290)
    at org.codehaus.plexus.classworlds.launcher.Launcher.launch(Launcher.java:230)
    at org.codehaus.plexus.classworlds.launcher.Launcher.mainWithExitCode(Launcher.java:409)
    at org.codehaus.plexus.classworlds.launcher.Launcher.main(Launcher.java:352)
    at org.codehaus.classworlds.Launcher.main(Launcher.java:47)
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
    at java.lang.reflect.Method.invoke(Method.java:498)
    at com.intellij.rt.execution.application.AppMain.main(AppMain.java:147)
```
 给出service接口的实现

 
```
import com.grpc.demo.HelloServiceGrpc;
import com.grpc.demo.HelloWorldProto;
import io.grpc.stub.StreamObserver;

/**
 * Created by hadoop on 17-7-16.
 */
public class HelloWorldImpl extends HelloServiceGrpc.HelloServiceImplBase {

    @Override
    public void greet(HelloWorldProto.Request request, StreamObserver<HelloWorldProto.Replay> responseObserver) {
        System.out.println("call hello world service ... ");
        HelloWorldProto.Replay replay = HelloWorldProto.Replay.newBuilder().setMes(
                request.getId()+", "+request.getName()+", "+request.getAge()).build();

        responseObserver.onNext(replay);
        responseObserver.onCompleted();
    }
}
```
 server端代码

 
```
import com.grpc.service.HelloWorldImpl;
import io.grpc.Server;
import io.grpc.ServerBuilder;

import java.io.IOException;

/**
 * Created by hadoop on 17-7-16.
 */
public class HelloWorldServer {

    /* The port on which the server should run */
    private int port = 50051;
    private Server server;

    private void start() throws IOException {
        server = ServerBuilder.forPort(port)
                .addService(new HelloWorldImpl())
                .build()
                .start();
        Runtime.getRuntime().addShutdownHook(new Thread() {
            @Override
            public void run() {
                // Use stderr here since the logger may have been reset by its JVM shutdown hook.
                System.err.println("*** shutting down gRPC server since JVM is shutting down");
                HelloWorldServer.this.stop();
                System.err.println("*** server shut down");
            }
        });
    }

    private void stop() {
        if (server != null) {
            server.shutdown();
        }
    }

    /**
     * Await termination on the main thread since the grpc library uses daemon threads.
     */
    private void blockUntilShutdown() throws InterruptedException {
        if (server != null) {
            server.awaitTermination();
        }
    }

    public static void main(String[]args){
        final HelloWorldServer server = new HelloWorldServer();
        try{
            server.start();
            server.blockUntilShutdown();
        }catch (Exception e){
            e.printStackTrace();
        }

    }
}
```
 client端代码

 
```
import com.grpc.demo.HelloServiceGrpc;
import com.grpc.demo.HelloWorldProto;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.StatusRuntimeException;
import java.util.concurrent.TimeUnit;
/**
 * Created by hadoop on 17-7-16.
 */
public class HelloWorldClient {

    private final ManagedChannel channel;
    private final HelloServiceGrpc.HelloServiceBlockingStub blockingStub;

    /** Construct client connecting to HelloWorld server at {@code host:port}. */
    public HelloWorldClient(String host, int port) {

        channel = ManagedChannelBuilder.forAddress(host, port)
                .usePlaintext(true)
                .build();
        blockingStub = HelloServiceGrpc.newBlockingStub(channel);
    }

    public void shutdown() throws InterruptedException {
        channel.shutdown().awaitTermination(5, TimeUnit.SECONDS);
    }

    /** Say hello to server. */
    public void greet() {

        HelloWorldProto.Request request = HelloWorldProto.Request.newBuilder().setName("LiLei").setAge("12").setId(100001).build();
        HelloWorldProto.Replay response;
        try {
            response = blockingStub.greet(request);
        } catch (StatusRuntimeException e) {
            e.printStackTrace();
            return;
        }
        System.out.println("Greeting: " + response.getMes());
    }

    /**
     * Greet server. If provided, the first element of {@code args} is the name to use in the
     * greeting.
     */
    public static void main(String[] args) throws Exception {
        HelloWorldClient client = new HelloWorldClient("localhost", 50051);
        try {
            client.greet();
        } finally {
            client.shutdown();
        }
    }
}
```
 分别运行server端和client端 main函数，在控制台查看运行结果。

   
  