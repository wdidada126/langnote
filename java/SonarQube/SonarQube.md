# Sonar


1. 默认支持代码文本格式全为 UTF-8，其他编码可能会产生乱码；
2. 目前支持 C#、C++、Go、Groovy、Java、JavaScript、Lua、PHP、Python、Ruby、TypeScript、Web、XML；
3. 仅保存最近一次分析结果；
4. Pull Request 合并或关闭后将会移除分析结果。



SonarQube是管理代码质量一个开放平台,可以快速的定位代码中潜在的或者明显的错误

https://docs.sonarqube.org/latest/setup/get-started-2-minutes/

https://docs.sonarqube.org/pages/viewpage.action?pageId=7996665


[代码质量管理平台SonarQube的安装、配置与使用](https://www.cnblogs.com/qiumingcheng/p/7253917.html)





travis 结合?

[代码质量管理平台SonarQube的安装、配置与使用](https://www.cnblogs.com/qiumingcheng/p/7253917.html)

![sonar架构图](../../imgs/sonar架构图.jpg)

Sonar可以集成不同的测试工具，代码分析工具，以及持续集成工具，比如pmd-cpd、checkstyle、findbugs、Jenkins。sonar最大的特点就是插件化，可以根据不同的场景需求进行插件化安装，以Java代码检测为，但同时可以检测Python、C++等多种语言。


sonarqube-9

./bin/linux-x86-64/sonar.sh  start
Starting SonarQube...
Failed to start SonarQube.


Unrecognized option: --add-exports=java.base/jdk.internal.ref=ALL-UNNAMED


sonar启动报错 （sonarqube-9.1.0.47736 跟 java 8 不兼容）


wget https://download.java.net/openjdk/jdk11/ri/openjdk-11+28_linux-x64_bin.tar.gz
tar -xzvf jdk-11.0.14_linux-x64_bin.tar.gz

二、环境变量配置
1、修改环境配置文件

vim /etc/profile
根据需要的Java版本把下面代码加入到配置文件内容中

# Java11环境变量配置
JAVA_HOME=/devtools/java/java11/jdk-11.0.14
PATH=$JAVA_HOME/bin:$PATH
CLASSPATH=$JAVA_HOME/lib
export JAVA_HOME CLASSPATH PATH
 
# Java8环境变量配置
JAVA_HOME=/devtools/java/java8/jdk1.8.0_321
PATH=$PATH:$JAVA_HOME/bin
CLASSPATH=.:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export JAVA_HOME PATH CLASSPATH
2、刷新配置文件使之生效

source /etc/profile


yum install java-11



https://blog.csdn.net/wawa8899/article/details/118027710

sonar支持的数据库
pg
oracle
sqlserver
h2默认

106.75.209.6:9000

admin 5Edidada


#### sonar与jenkins的集成

### SonarScanner进行扫描
版本兼容
4.7

https://docs.sonarqube.org/8.9/analysis/scan/sonarscanner/


https://blog.csdn.net/nikeylee/article/details/117367744


sonarqube与IDEA

idea sonalint插件
	https://blog.csdn.net/zengmingen/article/details/106473012

pom.xml增加

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
            <plugin>
                <groupId>org.sonarsource.scanner.maven</groupId>
                <artifactId>sonar-maven-plugin</artifactId>
                <version>3.7.0.1746</version>
            </plugin>
        </plugins>
    </build>


idea maven插件 sonar执行

Downloading analyzer 'php'
Downloading analyzer 'ruby'
Downloading analyzer 'javascript'
Downloading analyzer 'kotlin'
Downloading analyzer 'python'



Plugin 'secrets' embeds dependencies. This will be deprecated soon. Plugin should be updated.


[SYNC] Downloading plugin 'sonar-scala-plugin-1.9.0.3429.jar'
Downloaded 'sonarscala' in 125036ms
[SYNC] Downloading plugin 'sonar-xml-plugin-2.5.0.3376.jar'
Downloaded 'xml' in 20056ms
[SYNC] Synchronizing analyzer configuration for project 'dsfasdfasd'
Downloaded settings in 602ms
[SYNC] Fetching rule set for language 'java' from profile 'AYCZOR_MC86mYA7mcuyI'
[SYNC] Fetching rule set for language 'js' from profile 'AYCZORi3C86mYA7mcuK1'
[SYNC] Fetching rule set for language 'kotlin' from profile 'AYCZORDxC86mYA7mcuCD'
[SYNC] Fetching rule set for language 'php' from profile 'AYCZOSUvC86mYA7mcvDs'
[SYNC] Fetching rule set for language 'py' from profile 'AYCZORsQC86mYA7mcuTB'
[SYNC] Fetching rule set for language 'ruby' from profile 'AYCZORxTC86mYA7mcuWl'
[SYNC] Fetching rule set for language 'scala' from profile 'AYCZORADC86mYA7mct-w'
[SYNC] Fetching rule set for language 'ts' from profile 'AYCZOSvBC86mYA7mcvYH'
[SYNC] Fetching rule set for language 'web' from profile 'AYCZOSHUC86mYA7mcu6U'
[SYNC] Fetching rule set for language 'xml' from profile 'AYCZOSL5C86mYA7mcu7k'
[SYNC] Synchronizing project branches for project 'dsfasdfasd'
Plugin 'secrets' embeds dependencies. This will be deprecated soon. Plugin should be updated.
Clearing all issues because binding was updated
Using connection '106.75.209.6' for project 'dsfasdfasd'
Analysing 3 files...
Found 0 issues
Using connection '106.75.209.6' for project 'dsfasdfasd'
Analysing 'A.java'...
Found 0 issues
