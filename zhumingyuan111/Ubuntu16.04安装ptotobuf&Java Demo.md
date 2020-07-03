---
title: Ubuntu16.04安装ptotobuf&Java Demo
date: 2017-07-15 16:11:58
tags: CSDN迁移
---
  ### protobuf 安装

 下载protobuf 源码，可以选择不同的版本本人选择的3.3.0版本   
 [https://github.com/google/protobuf/releases/tag/](https://github.com/google/protobuf/releases/tag/)   
 解压文件，并进入protobuf目录，会发现autogen.sh文件。   
 执行 `./autogen.sh`  生成configure文件   
 如果出现错误信息可能是因为缺少C++ lib包导致，则进行相关的错误信息查询和安装即可。   
 之后分别执行以下命令进行安装

 
```
./configure
./make
./make check
./make install
```
 注意：configure 时可以指定安装位置，若没有指明，默认安装在/usr/local/lib下面。

 安装完成之后，进行检查

 
```
protoc --version 
```
 若出现proto版本号则安装成功！

 
### Java demo

 
#### idea 建立maven工程

 pom.xml

 
```
<dependencies>
        <dependency>
            <groupId>com.google.protobuf</groupId>
            <artifactId>protobuf-java</artifactId>
            <version>3.3.0</version>
        </dependency>
    </dependencies>
```
 MessageProto.proto文件内容

 
```
package proto;
option java_package="com.protobuf.bean";
option java_outer_classname="MessageProto";

message Message{
   required int64 id =1;
   required string title=2;
   required string content=3;

   enum Type{
     SUPER=0;
     COMMON=1;
   }
   required Type type=4;
}
```
 生成java文件

 
```
protoc --java_out=../java/ ./MessageProto.proto
```
 –java_out=../java/ 代表生成的java文件所放位置   
 后面的路径是proto文件位置   
 更多protoc命令请自行网上查询。

 
#### 测试类

 将生成的代码拷贝进工程，编写测试main函数

 
```

import com.protobuf.bean.MessageProto;

/**
 * Created by hadoop on 17-7-15.
 */
public class MessageProtoTest {

    public static void main(String[]args){
        MessageProto.Message.Builder builder = MessageProto.Message.newBuilder();
        builder.setContent("message content ....");
        builder.setId(1001);
        builder.setTitle("title 1");
        builder.setType(MessageProto.Message.Type.SUPER);
        System.out.println("original message is : "+builder.build());
        byte[]data = builder.build().toByteArray();
        try{
            MessageProto.Message cloneMes = MessageProto.Message.parseFrom(data);
            System.out.println("clone message is : "+cloneMes);
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
```
 输出结果如下：

 
```
original message is : id: 1001
title: "title 1"
content: "message content ...."
type: SUPER

clone message is : id: 1001
title: "title 1"
content: "message content ...."
type: SUPER


Process finished with exit code 0
```
   
  