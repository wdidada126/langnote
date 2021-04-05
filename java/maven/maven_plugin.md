# maven plugin

protoc 插件
thrift插件不好
antlr插件



```shell
D:\Java\jdk1.8.0_231\bin\java.exe -Dmaven.multiModuleProjectDirectory=D:\git\bitbucket\testprotobuf -Dmaven.home=D:\apache-maven-3.6.1 -Dclassworlds.conf=D:\apache-maven-3.6.1\bin\m2.conf "-javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\lib\idea_rt.jar=9096:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\bin" -Dfile.encoding=UTF-8 -classpath D:\apache-maven-3.6.1\boot\plexus-classworlds-2.6.0.jar org.codehaus.classworlds.Launcher -Didea.version=2018.2.5 org.xolstice.maven.plugins:protobuf-maven-plugin:0.6.1:compile
```

maven-surefire-plugin

maven-source-plugin
打包源码到maven本地仓库


```
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-compiler-plugin</artifactId>
				<configuration>
					<source>1.7</source>
					<target>1.7</target>
					<encoding>UTF8</encoding>
				</configuration>
			</plugin>
```
