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

Sonar 可以集成不同的测试工具，代码分析工具，以及持续集成工具，比如pmd-cpd、checkstyle、findbugs、Jenkins。sonar最大的特点就是插件化，可以根据不同的场景需求进行插件化安装，以Java代码检测为，但同时可以检测Python、C++等多种语言。
