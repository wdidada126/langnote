# jsch

https://central.sonatype.com/artifact/com.jcraft/jsch/overview

对于Java中实现SSH登录协议的库，以下是几个推荐：

#### JSch
- 简介：JSch是一个纯Java实现的SSH2客户端库，提供SSH连接、远程命令执行、文件传输（SFTP、SCP）等功能。
- 特点：
    - 支持多种加密算法和认证方式（密码、公私钥等）。
    - 易于集成，文档齐全，社区活跃。
- Maven依赖：

```xml
<dependency>
    <groupId>com.jcraft</groupId>
    <artifactId>jsch</artifactId>
    <version>0.1.55</version>
</dependency>
```

#### Ganymed SSH-2
- 简介：Ganymed SSH-2是一个高性能的SSH2客户端库，支持SSH连接、端口转发、SFTP等功能。
- 特点：
    - 速度快，资源消耗低。
    - 提供详细的API文档和示例。
- Maven依赖：

```xml
<dependency>
    <groupId>ch.ethz.ganymed</groupId>
    <artifactId>ganymed-ssh2</artifactId>
    <version>build210</version>
</dependency>
```

#### SSHJ
- 简介：SSHJ是一个纯Java实现的SSH客户端库，支持SSH连接、远程命令执行、文件传输（SFTP）等功能。
- 特点：
    - 支持异步操作，易于使用。
    - 提供丰富的API和示例。
- Maven依赖：

```xml
<dependency>
    <groupId>com.hierynomus</groupId>
    <artifactId>sshj</artifactId>
    <version>0.33.1</version>
</dependency>
```

#### Trilead SSH-2
- 简介：Trilead SSH-2是一个轻量级的SSH2客户端库，支持SSH连接、端口转发、SFTP等功能。
- 特点：
    - 代码简洁，易于集成。
    - 提供基本的SSH功能。
- Maven依赖：

```xml
<dependency>
    <groupId>com.trilead</groupId>
    <artifactId>trilead-ssh2</artifactId>
    <version>1.0.0-build221</version>
</dependency>
```

这些库都提供了丰富的功能和良好的文档支持，您可以根据项目需求选择合适的库来实现SSH登录协议。
