# maven


mvn参考 yum apt，联网下载库文件
分发库文件

mvn dependency:resolve -Dclassifier=sources

mvn dependency:tree

下载源码 maven
idea windows下载jar包源码失败


mvn clean install -s settings.xml -U -DskipTests -Dmaven.repo.local=/tmp/repo


 mirror就是镜像，主要提供一个方便地切换远程仓库地址的途径。比如，上班的时候在公司，用电信的网络，连的是电信的仓库。回到家后，是网通的网络，我想连网通的仓库，就可以通过mirror配置，统一把我工程里的仓库地址都改成联通的，而不用到具体工程配置文件里一个一个地改地址。
mirror的配置在.m2/settings.xml里。如：

  <mirrors>
    <mirror>
      <id>UK</id>
      <name>UK Central</name>
      <url>http://uk.maven.org/maven2</url>
      <mirrorOf>central</mirrorOf>
    </mirror>
  </mirrors>

这样的话，就会给上面id为central的远程仓库做了个镜像。以后向central这个仓库发的请求都会发到http://uk.maven.org/maven2而不是http://repo1.maven.org/maven2了。
<mirrorOf>central</mirrorOf>里是要替代的仓库的id。如果填*，就会替代所有仓库。
    

### verify settings.xml

mvn help:effective-settings

### docker maven

```xml
            <plugin>
                <groupId>com.spotify</groupId>
                <artifactId>docker-maven-plugin</artifactId>
                <version>1.2.0</version>
                <configuration>
                    <!-- 镜像名称 -->
                    <imageName>${docker.image.prefix}/spring-cloud-eureka</imageName>
                    <!-- 依赖java镜像 -->
                    <baseImage>java</baseImage>
                    <imageTags>
                        <imageTag>${project.version}</imageTag>
                        <imageTag>latest</imageTag>
                    </imageTags>
                    <entryPoint>["java", "-jar", "/${project.build.finalName}.jar"]</entryPoint>
                    <dockerHost>http://127.0.0.1:2375</dockerHost>
                    <!--<dockerCertPath>C:\Users\edidada\.docker\machine\machines\default</dockerCertPath>-->
                    <resources>
                        <resource>
                            <targetPath>/</targetPath>
                            <directory>${project.build.directory}</directory>
                            <include>${project.build.finalName}.jar</include>
                        </resource>
                    </resources>
                </configuration>
            </plugin>
```

complie是默认值，表示在build,test,runtime阶段的classpath下都有依赖关系。
test表示只在test阶段有依赖关系，例如junit
provided表示在build,test阶段都有依赖，在runtime时并不输出依赖关系而是由容器提供，例如web war包都不包括servlet-api.jar，而是由tomcat等容器来提供
runtime表示在构建编译阶段不需要，只在test和runtime需要。
https://blog.csdn.net/pengpengzhou/article/details/81743567


`mvn dependency:tree -Dverbose -Dincludes=groupId:artifactIdw`

https://maven.apache.org/pom.html

scope=compile的情况（默认scope)

scope:
This element refers to the classpath of the task at hand (compiling and runtime, testing, etc.) as well as how to limit the transitivity of a dependency. There are five scopes available:
compile - this is the default scope, used if none is specified. Compile dependencies are available in all classpaths. Furthermore, those dependencies are propagated to dependent projects.
provided - this is much like compile, but indicates you expect the JDK or a container to provide it at runtime. It is only available on the compilation and test classpath, and is not transitive.
runtime - this scope indicates that the dependency is not required for compilation, but is for execution. It is in the runtime and test classpaths, but not the compile classpath.
test - this scope indicates that the dependency is not required for normal use of the application, and is only available for the test compilation and execution phases. It is not transitive.
system - this scope is similar to provided except that you have to provide the JAR which contains it explicitly. The artifact is always available and is not looked up in a repository.


Maven实战-maven中的可选依赖（optional）
https://blog.csdn.net/lovejj1994/article/details/80283240

optional:
Marks a dependency optional when this project itself is a dependency. For example, imagine a project A that depends upon project B to compile a portion of code that may not be used at runtime, then we may have no need for project B for all project. So if project X adds project A as its own dependency, then Maven does not need to install project B at all. Symbolically, if => represents a required dependency, and --> represents optional, although A=>B may be the case when building A X=>A-->B would be the case when building X.
In the shortest terms, optional lets other projects know that, when you use this project, you do not require this dependency in order to work correctly.


maven_plugin.md

settings.xml
和pom.xml设置jdk版本
两种方式
https://www.cnblogs.com/jiefu/p/10968447.html

```shell
    <resources>
        <resource>
            <filtering>true</filtering>
            <directory>src/main/resources</directory>
        </resource>
        <resource>
            <directory>profiles/${profile.active}</directory>
            <filtering>true</filtering>
        </resource>
    </resources>
    <testResources>
        <testResource>
            <directory>src/test/resources</directory>
            <filtering>true</filtering>
        </testResource>
    </testResources>
    </build>
</project>
```


mvn dependency:copy-dependencies
拷贝项目依赖的jar包到编译目录的lib下面
<plugin>
       <groupId>org.apache.maven.plugins</groupId>
       <artifactId>maven-dependency-plugin</artifactId>
       <version>2.9</version>
       <configuration>
           <outputDirectory>${project.build.directory}/lib</outputDirectory>
           <includeScope>runtime</includeScope>
       </configuration>
</plugin>

mvn dependency:copy-dependencies
maven把依赖包拷贝到lib下


标准web工程在eclipse中利用m2eclipse插件添加依赖管理后，在部署过程中没有将依赖的jar包自动拷贝到/WEB-INF/lib中。
参考了一些朋友的做法手动执行
mvn dependency:copy-dependencies -DoutputDirectory=src/main/webapp/WEB-INF/lib  -DincludeScope=runtime   
命令将jar包拷贝到/WEB-INF/lib目录下。

project节点，设置远程仓库地址
  <repositories>
    <repository>
      <id>repo-mirror</id>
      <url>http://repository.jboss.org/nexus/content/groups/public/</url>
    </repository>
  </repositories>

```shell

[设置Maven的默认jdk编译版本](https://blog.csdn.net/jxchallenger/article/details/90247471)

```
/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/bin/java -Dmaven.multiModuleProjectDirectory=/private/var/folders/ns/qm0ch94j5fbcgfykhrhw4x580000gn/T/archetype1tmp "-Dmaven.home=/Applications/IntelliJ IDEA.app/Contents/plugins/maven/lib/maven3" "-Dclassworlds.conf=/Applications/IntelliJ IDEA.app/Contents/plugins/maven/lib/maven3/bin/m2.conf" "-Dmaven.ext.class.path=/Applications/IntelliJ IDEA.app/Contents/plugins/maven/lib/maven-event-listener.jar" -Dfile.encoding=UTF-8 -classpath "/Applications/IntelliJ IDEA.app/Contents/plugins/maven/lib/maven3/boot/plexus-classworlds-2.6.0.jar" org.codehaus.classworlds.Launcher -Didea.version2019.2.4 -DinteractiveMode=false -DgroupId=cn.wdidada.test -DartifactId=testshorturl-web -Dversion=1.0-SNAPSHOT -DarchetypeGroupId=org.apache.maven.archetypes -DarchetypeArtifactId=maven-archetype-webapp -DarchetypeVersion=RELEASE org.apache.maven.plugins:maven-archetype-plugin:RELEASE:generate
```



问题:maven如何在命令行运行子mudule的main方法？



[使用Maven运行Java main的3种方式](https://www.cnblogs.com/hukaiyang/p/Maven.html)





`mvn exec:java` 不会自动编译



`mvn compile`



`mvn exec:java -Dexec.mainClass="org.apache.shardingsphere.example.orchestration.spring.namespace.ExampleMain"`





```
 Unknown lifecycle phase ".mainClass=org.apache.shardingsphere.example.orchestration.spring.namespace.ExampleMain". You must specify a valid lifecycle phase or a goal in the format <plugin-prefix>:<goal> or <plugin-group-id>:<plugin-artifact-id>[:<plugin-version>]:<goal>. Available lifecycle phases are: validate, initialize, generate-sources, process-sources, generate-resources, process-resources, compile, process-classes, generate-test-sources, process-test-sources, generate-test-resources, process-test-resources, test-compile, process-test-classes, test, prepare-package, package, pre-integration-test, integration-test, post-integration-test, verify, install, deploy, pre-clean, clean, post-clean, pre-site, site, post-site, site-deploy. -> [Help 1]
```





[上述报错是因为在powershell中运行，在cmd中可以运行](https://stackoverflow.com/questions/7576265/maven-exec-plugin-throws-exception-for-no-apparent-reason)



https://stackoverflow.com/questions/19850956/maven-java-the-parameters-mainclass-for-goal-org-codehaus-mojoexec-maven-p



https://www.cnblogs.com/oxspirt/p/7807739.html



pom.xml

project是根节点

```
xmlns="http://maven.apache.org/POM/4.0.0"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
```



### maven setting



- exec-maven-plugin



mirror

mirrorOf 在根据模板创建webapp项目时有用，注释掉会报错







maven是一个程序

它有下列功能：

提供maven resposity，存储jar包信息和描述信息

jar文件的下载，本地maven resposity的管理



打包jar

maven plugin

mybatis maven plugin

grpc maven plugin

spring boot plugin



以前执行一个程序

java --agent --classpath mainclass 之类的

现在

maven run？



以前thrift生成java代码，执行命令行文件

现在，用thrift maven插件，绑定mavenbuild生命周期，一键搞定



maven环境变量

设置jdk版本，文件编码，依赖关系



idea控制台乱码解决方案
https://www.cnblogs.com/jingping/p/10949414.html

-DFile.encode=GB2312


<type>maven-plugin</type>

<dependency>
  <groupId>org.apache.thrift.tools</groupId>
  <artifactId>maven-thrift-plugin</artifactId>
  <version>0.1.11</version>
  <type>maven-plugin</type>
</dependency>

os-maven-plugin在pom.xml中的位置



maven plugin

extension



```
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
            </plugin>
        </plugins>
</build>
```



常用Maven插件介https://cloud.tencent.com/developer/article/1429928



Maven wrapper

The Maven Wrapper is an easy way to ensure a user of your Maven build has everything necessary to run your Maven build.

Gradle
Gradw



maven常用插件总结
https://github.com/takari/maven-wrapper

https://www.cnblogs.com/pixy/p/4977550.html

`mvn clean install -e -X  -DconfigurePath=hello`

```

	<plugin>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-maven-plugin</artifactId>
	</plugin>

```

新开发框架是不是考虑兼容mvaen这种代码管理工具

`mvn help:describe -Dplugin=org.apache.maven.plugins:maven-eclipse-plugin:2.10`

[maven 插件细节](https://blog.csdn.net/tterminator/article/details/81609172)

```

[INFO] org.apache.maven.plugins:maven-install-plugin:2.4

Name: Maven Install Plugin
Description: Copies the project artifacts to the user's local repository.
Group Id: org.apache.maven.plugins
Artifact Id: maven-install-plugin
Version: 2.4
Goal Prefix: install

This plugin has 3 goals:

install:help
  Description: Display help information on maven-install-plugin.
    Call mvn install:help -Ddetail=true -Dgoal=<goal-name> to display parameter
    details.

install:install
  Description: Installs the project's main artifact, and any other artifacts
    attached by other plugins in the lifecycle, to the local repository.

install:install-file
  Description: Installs a file in the local repository.

For more information, run 'mvn help:describe [...] -Ddetail'

```

[maven插件 maven-git-commit-id-plugin](https://blog.csdn.net/shog808/article/details/79404009)

[healthCheck.html变量替换原理](https://segmentfault.com/a/1190000012193745)

如何校验应用存在多版本jar包冲突隐患?
maven plugin
maven-enforcer
http://maven.apache.org/enforcer/enforcer-rules/index.html

`mvn -U clean validate`

```

<plugin>
	<groupId>org.apache.maven.plugins</groupId>
	<artifactId>maven-enforcer-plugin</artifactId>
	<version>3.0.0-M2</version>
	<executions>
		<execution>
			<id>default-cli</id>
			<configuration>
				<rules>
				<dependencyConvergence/>
				</rules>
			</configuration>
			<goals>
				<goal>enforce</goal>
			</goals>
		</execution>
	</executions>
</plugin>

```

[maven-resources-plugin](https://maven.apache.org/plugins/maven-resources-plugin/index.html)


[Maven 内置变量](https://www.cnblogs.com/zz0412/p/3783470.html)

Maven内置变量说明：

${basedir} 项目根目录(即pom.xml文件所在目录)
${project.build.directory} 构建目录，缺省为target目录
${project.build.outputDirectory} 构建过程输出目录，缺省为target/classes
${project.build.finalName} 产出物名称，缺省为${project.artifactId}-${project.version}
${project.packaging} 打包类型，缺省为jar
${project.xxx} 当前pom文件的任意节点的内容
${env.xxx} 获取系统环境变量。例如,"env.PATH"指代了$path环境变量（在Windows上是%PATH%）。
${settings.xxx} 指代了settings.xml中对应元素的值。例如：<settings><offline>false</offline></settings>通过 ${settings.offline}获得offline的值。
Java System Properties: 所有可通过java.lang.System.getProperties()访问的属性都能在POM中使用，例如 ${JAVA_HOME}。

··· 

[INFO] --- autoconfig-maven-plugin:1.2:autoconfig (default) @ isomerization-proxy-web ---
[INFO] -------------------------------------------------
[INFO] Detected system charset encoding: GBK
[INFO] If your can't read the following text, specify correct one like this:
[INFO]
[INFO]   mvn -Dautoconfig.charset=yourcharset
[INFO]
[INFO] Configuring D:\gitlab\isomerization-proxy\target\isomerization-proxy.war, interactiveMode=auto, strict=true
[INFO] -------------------------------------------------
Loading file:/C:/Users/edidada/antx.properties
User-defined properties: file:/C:/Users/edidada/antx.properties

<jar:file:/D:/gitlab/isomerization-proxy/target/isomerization-proxy.war!/>
    Generating META-INF/autoconf/archaius.properties.vm [UTF-8] => WEB-INF/classes/META-INF/conf/config.properties [UTF-8]

<jar:file:/D:/gitlab/isomerization-proxy/target/isomerization-proxy.war!/>
    Generating META-INF/autoconf/dubbo.properties.vm [UTF-8] => WEB-INF/classes/properties/dubbo.properties [UTF-8]

<jar:file:/D:/gitlab/isomerization-proxy/target/isomerization-proxy.war!/>
    Generating META-INF/autoconf/jdbc.properties.vm [UTF-8] => WEB-INF/classes/properties/jdbc.properties [UTF-8]

<jar:file:/D:/gitlab/isomerization-proxy/target/isomerization-proxy.war!/>
    Generating META-INF/autoconf/log4j2.xml.vm [UTF-8] => WEB-INF/classes/log4j2.xml [UTF-8]

<jar:file:/D:/gitlab/isomerization-proxy/target/isomerization-proxy.war!/>
    Generating META-INF/autoconf/micro-service-auth-provider.properties.vm [UTF-8] => WEB-INF/classes/properties/micro-service-auth-provider.properties [UTF-8]

<jar:file:/D:/gitlab/isomerization-proxy/target/isomerization-proxy.war!/>
    Generating META-INF/autoconf/redis-cache.properties.vm [UTF-8] => WEB-INF/classes/properties/redis-cache.properties [UTF-8]

<jar:file:/D:/gitlab/isomerization-proxy/target/isomerization-proxy.war!/>
    Generating META-INF/autoconf/redis-sentinel.properties.vm [UTF-8] => WEB-INF/classes/properties/redis-sentinel.properties [UTF-8]

<jar:file:/D:/gitlab/isomerization-proxy/target/isomerization-proxy.war!/>
    Generating META-INF/autoconf/redis.properties.vm [UTF-8] => WEB-INF/classes/properties/redis.properties [UTF-8]

<jar:file:/D:/gitlab/isomerization-proxy/target/isomerization-proxy.war!/>
    Generating log file: META-INF/autoconf/auto-config.xml.log

···


`“mvn eclipse:eclipse`

`mvn idea:idea`

`mvn -Dverbose dependency:tree`

···
<build>
        <pluginManagement>
            <plugins>
                <plugin>
                    <!--protobuf 插件默认的 Phase 为 GenerateCode-->
                    <groupId>org.xolstice.maven.plugins</groupId>
                    <artifactId>protobuf-maven-plugin</artifactId>
                    <version>0.5.1</version>
                    <executions>
                        <execution>
                            <!--把 Compile mojo和 test compile mojo 绑定到 GenerateCode 阶段。
                            这样，在 GenerateCode 阶段，会执行此插件的两个 mojo。否则，在Maven 默认的 Compile 或 Test 阶段
                            ，不会执行编译动作。-->
                            <goals>
                                <goal>compile</goal>
                                <goal>test-compile</goal>
                            </goals>
                        </execution>
                    </executions>
                </plugin>
            </plugins>
        </pluginManagement>
        <plugins>
            <plugin>
                <groupId>org.xolstice.maven.plugins</groupId>
                <artifactId>protobuf-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>	
···

os-maven-plugin

https://github.com/trustin/os-maven-plugin

maven之pom.xml配置文件详解
https://www.jianshu.com/p/0e3a1f9c9ce7

maven-checkstyle-plugin（执行mvn checkstyle:checkstyle根据规则检查代码）和maven-jxr-plugin （展示错误）插件

maven3超级POM	

Failed to execute goal org.apache.maven.plugins:maven-deploy-plugin:2.7:deploy (default-deploy) on project short-url: Deployment failed: repository element was not specified in the POM inside dis
tributionManagement element or in -DaltDeploymentRepository=id::layout::url parameter -> [Help 1]


[maven跳过单元测试-maven.test.skip和skipTests的区别](https://blog.csdn.net/arkblue/article/details/50974957)

​```java

                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>2.5</version>

```

https://maven.apache.org/surefire/maven-surefire-plugin/

Goals Overview
The Surefire Plugin has only one goal:

surefire:test runs the unit tests of an application.

生成文件
file:///D:/github/testresilience4j/resilience4j-web/target/surefire-reports/index.html

maven pom.xml配置plugins
···

            <!--配置生成Javadoc包-->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-javadoc-plugin</artifactId>
                <version>2.10.4</version>
                <configuration>
                    <encoding>UTF-8</encoding>
                    <aggregate>true</aggregate>
                    <charset>UTF-8</charset>
                    <docencoding>UTF-8</docencoding>
                </configuration>
                <executions>
                    <execution>
                        <id>attach-javadocs</id>
                        <goals>
                            <goal>jar</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
            <!--配置生成源码包-->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-source-plugin</artifactId>
                <version>3.0.1</version>
                <executions>
                    <execution>
                        <id>attach-sources</id>
                        <goals>
                            <goal>jar</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
···		


```java



```

这样，Maven搜索jar包依赖的顺序就是：
1）搜索本地仓库，没有找到，就去第2步，否则退出
2）搜索中央仓库【配置镜像】，没有找到，就去第3步，否则退出
3）去java.net远程仓库获取，没有找到，就报错，否则退出

[maven仓库调用顺序](https://blog.csdn.net/win7system/article/details/51272367)



maven jar包重复依赖时，引用的顺序

树的深度有限遍历



## 私服上传jar包
可以考虑上传jar包到maven官方镜像

如果有搭建自己公司的maven私服，公司内部会把自己的公司的公共jar包上传到maven私服中。
如果私服配置了上传权限，servers标签需要给出授权信息。

使用方法
1.在maven的工程中，pom中使用ditributionManagement标签私服地址。

<distributionManagement>
    <repository>
        <id>release-repository</id>
        <name>Release Repository</name>
        <url>http://www.myrepository.com/repositories/releases</url>
    </repository>
    <snapshotRepository>
        <id>snapshot-repository</id>
        <name>Snapshot Repository</name>
        <url>http://www.myrepository.com/repositories/snapshots</url>
    </snapshotRepository></distributionManagement>
上面的例子，我们公司的私服地址是http://www.myrepository.com，配置了SNAPSHOT包的上传路径和RELEASE包的上传路径。

2.在maven的settings.xml中配置servers。

```
<servers>
    <server>
        <id>snapshot-repository</id>
        <username>snapshot</username>
        <password>123456</password>
    </server>
    <server>
        <id>release-repository</id>
        <username>release</username>
        <password>123456</password>
    </server>
</servers>
```

需要注意的是两处的id需要相互匹配。
帐号的权限都是私服配置的。上传到SNAPSHOT还是RELEASE是由项目的version决定的。
也可以使用ssh key的方式配置servers。

Maven对settings.xml配置的官方说明文档。http://maven.apache.org/settings.html#Servers
Maven对password进行加密配置的说明文档。http://maven.apache.org/guides/mini/guide-encryption.html

[maven跳过单元测试-maven.test.skip和skipTests的区别](https://blog.csdn.net/arkblue/article/details/50974957)
mvn package -Dmaven.test.skip=true

## plugin

- maven-source-plugin

[maven-source-plugin](https://maven.apache.org/plugins/maven-source-plugin/)

[Maven之（七）pom.xml配置文件详解](https://blog.csdn.net/u012152619/article/details/51485297)

maven modules项目打包，直接在主目录mvn install就行，不用在子module进行打包


maven 安装jar到电脑磁盘上

```java

mvn install:install-file -DgroupId=org.csource -DartifactId=fastdfs-client-java -Dversion=1.25 -Dpackaging=jar -Dfile=D:/x/fastdfs_client.jar 

```

设置war文件名称projectName.war
默认是${artifactId}-${version}

```
    <build>
        <finalName>projectName</finalName>
    </build>

<build>
  <defaultGoal>install</defaultGoal>
  <directory>${basedir}/target</directory>
  <finalName>${artifactId}-${version}</finalName>
  <filters>
    <filter>filters/filter1.properties</filter>
  </filters>
  ...
</build>

```


http://maven.apache.org/pom.html#BaseBuild_Element


[maven jdk配置](http://www.blogjava.net/fancydeepin/archive/2015/06/23/maven-jdk.html)

```shell
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
```



[maven version RELEASE](https://codeday.me/bug/20170313/1432.html)

```shell
	<dependency>
		<groupId>junit</groupId>
		<artifactId>junit</artifactId>
		<version>RELEASE</version>
		<scope>test</scope>
	</dependency>
```

[maven-source-plugin](https://maven.apache.org/plugins/maven-source-plugin/)


maven plugin

增加指令

[Maven的Java插件开发指南](http://ifeve.com/maven-java-pluging/)



<packaging>pom</packaging> //不会打jar包
默认值是jar
http://maven.apache.org/pom.html#Maven_Coordinates


IDEA 插件 maven runner

[maven github](https://github.com/apache/maven)
maven是jiava开发的

[Maven实战](https://book.douban.com/subject/5345682/)


Maven权威指南 电纸书

[Maven权威指南](https://book.douban.com/subject/5345682/)


[maven指令](https://blog.csdn.net/moshenglv/article/details/52027106)

nexus Maven私服开源软件

配置maven

M2_HOME
编辑PATH变量，添加Maven bin文件夹到PATH的最后，如：%M2_HOME%\bin，这样就可以在命令中的任何目录下运行Maven命令了

`C:\Users\edidada\.m2`

[maven新建多module](https://blog.csdn.net/ruanjian1111ban/article/details/80890539)


[maven dependency机制 官方文档](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html)


dependencies与dependencyManagement的区别
dependencies即使在子项目中不写该依赖项，那么子项目仍然会从父项目中继承该依赖项（全部继承）
dependencyManagement里只是声明依赖，并不实现引入，因此子项目需要显示的声明需要用的依赖。如果不在子项目中声明依赖，是不会从父项目中继承下来的；只有在子项目中写了该依赖项，并且没有指定具体版本，才会从父项目中继承该项，并且version和scope都读取自父pom;另外如果子项目中指定了版本号，那么会使用子项目中指定的jar版本。

```

maven项目打包成tar.gz格式

```

使用mvn命令行查看maven依赖

`

mvn dependency:tree

`

```shell

Unresolveable build extension: Plugin kr.motd.maven:os-maven-plugin

```

[maven修改版本号](https://www.cnblogs.com/chn58/p/6554742.html)



#### 1 设置新的版本号

`mvn versions:set -DnewVersion=1.1.3`

#### 2 当新版本号设置不正确时可以撤销新版本号的设置

`mvn versions:revert`

#### 3 确认新版本号无误后提交新版本号的设置

`mvn versions:commit`


IDEA
execute maven goal

clean install

[MAVEN-命令行创建工程](https://www.jianshu.com/p/1e2e263da088)


```shell

mvn archetype:generate -DgroupId=com.zetcode -DartifactId=propertyplaceholder -Dversion=1.0-SNAPSHOT -Dpackage=com.zetcode

```

[skip test](https://maven.apache.org/plugins-archives/maven-surefire-plugin-2.12.4/examples/skipping-test.html)



spring-boot 2017年使用的还是maven

https://my.oschina.net/hzchenyh/blog/678369





Maven查看哪些插件生效



mvn tree list



depedenceManager 错

pluginManager



Maven中的DependencyManagement和Dependencies

https://www.iteye.com/blog/liugang594-1687781



Maven parent作用？

**maven项目pom.xml中parent标签的使用**



使用maven是为了更好的帮项目管理包依赖，maven的核心就是pom.xml。当我们需要引入一个jar包时，在pom文件中加上<dependency></dependency>就可以从仓库中依赖到相应的jar包。



现在有这样一个场景，有两个web项目A、B，一个java项目C，它们都需要用到同一个jar包：common.jar。如果分别在三个项目的pom文件中定义各自对common.jar的依赖，那么当common.jar的版本发生变化时，三个项目的pom文件都要改，项目越多要改的地方就越多，很麻烦。这时候就需要用到parent标签, 我们创建一个parent项目，打包类型为pom，parent项目中不存放任何代码，只是管理多个项目之间公共的依赖。在parent项目的pom文件中定义对common.jar的依赖，ABC三个子项目中只需要定义<parent></parent>，parent标签中写上parent项目的pom坐标就可以引用到common.jar了。



上面的问题解决了，我们在切换一个场景，有一个springmvc.jar，只有AB两个web项目需要，C项目是java项目不需要，那么又要怎么去依赖。如果AB中分别定义对springmvc.jar的依赖，当springmvc.jar版本变化时修改起来又会很麻烦。解决办法是在parent项目的pom文件中使用<dependencyManagement></dependencyManagement>将springmvc.jar管理起来，如果有哪个子项目要用，那么子项目在自己的pom文件中使用



```java
<dependency>
​    <groupId></groupId>
​      <artifactId></artifactId>
</dependency>
```



标签中写上springmvc.jar的坐标，不需要写版本号，可以依赖到这个jar包了。这样springmvc.jar的版本发生变化时只需要修改parent中的版本就可以了。



```shell
maven-compiler-plugin


  <build>
  	<plugins>
  		<plugin>
  			<groupId>org.apache.maven.plugins</groupId>
  			<artifactId>maven-compiler-plugin</artifactId>
  			<configuration>
  				<source>1.8</source>
  				<target>1.8</target>
  				<encoding>UTF-8</encoding>
  			</configuration>
  		</plugin>
  	</plugins>
  </build>
```



maven 安装本地的jar包到本地仓库



[使用maven命令安装jar包到本地仓库](https://www.cnblogs.com/yadongliang/p/9829760.html)



```
安装指定文件到本地仓库命令：mvn install:install-file

-DgroupId=<groupId>       : 设置上传到仓库的包名

-DartifactId=<artifactId> : 设置该包所属的模块名

-Dversion=1.0.0           : 设置该包的版本号

-Dpackaging=jar           : 设置该包的类型(很显然jar包)

-Dfile=<myfile.jar>       : 设置该jar包文件所在的路径与文件名

mvn install:install-file -DgroupId=com.zebra -DartifactId=ZSDK_API -Dversion=v2.12.3782 -Dpackaging=jar -Dfile=E:\perslib\ZSDK_API.jar

mvn install:install-file -DgroupId=com.zebra -DartifactId=ZSDK_CARD_API -Dversion=v2.12.3782 -Dpackaging=jar -Dfile=E:\perslib\ZSDK_CARD_API.jar
```



cmd not pwoershell

`mvn clean install -Dmaven.test.skip=true -Dmaven.javadoc.skip=true -Dcheckstyle.skip=true`





cd D:\git\github\shardingsphere\examples\sharding-jdbc-example\orchestration-example\orchestration-raw-jdbc-example



```shell
mvn install:install-file -DgroupId=org.apache.shardingsphere.example -DartifactId=config-utility -Dversion=5.0.0-RC1-SNAPSHOT -Dpackaging=jar -Dfile=D:\git\github\shardingsphere\examples\example-core\config-utility\target\config-utility-5.0.0-RC1-SNAPSHOT.jar
```





```shell
mvn install:install-file -DgroupId=org.apache.shardingsphere.example -DartifactId=example-spring-mybatis -Dversion=5.0.0-RC1-SNAPSHOT -Dpackaging=jar -Dfile=D:\git\github\shardingsphere\examples\example-core\example-spring-mybatis\target\example-spring-mybatis-5.0.0-RC1-SNAPSHOT.jar
```



```
mvn install:install-file -DgroupId=org.apache.shardingsphere.example -DartifactId=example-raw-jdbc -Dversion=5.0.0-RC1-SNAPSHOT -Dpackaging=jar -Dfile=D:\git\github\shardingsphere\examples\example-core\example-raw-jdbc\target\example-raw-jdbc-5.0.0-RC1-SNAPSHOT.jar
```





```
mvn -f pom.xml compile exec:java -Dexec.classpathScope=compile  -Dexec.mainClass="org.apache.shardingsphere.example.orchestration.spring.namespace.ExampleMain"
```


mvn 设置jvm参数
在系统的环境变量中，设置M2_OPTS，用以存放JVM的参数，具体设置的步骤，参数示例如下：
MAVEN_OPTS=-Xms256m -Xmx768m -XX:PermSize=128m -XX:MaxPermSize=256M

