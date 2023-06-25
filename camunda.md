# camunda

### camunda跟activiti的关系 
Camunda和Activiti是两个流程引擎框架，它们有一定的关系。
Activiti是一个开源的BPM（Business Process Management）引擎，最初由Alfresco软件公司开发，后来由于Alfresco将其捐赠给了Apache软件基金会，成为Apache项目之一。Activiti提供了流程定义、执行和管理的功能，可以用于构建和执行业务流程。
Camunda是一个基于Activiti流程引擎的开源项目，它是在Activiti的基础上进行扩展和改进的。Camunda提供了更广泛的功能和工具，包括工作流引擎、决策引擎和案例管理等，以支持更复杂的业务流程管理需求。Camunda也提供了更丰富的API和集成选项，使其更加灵活和可扩展。
可以说，Camunda是在Activiti的基础上进行了进一步的发展和完善，提供了更多功能和扩展性。尽管如此，Activiti仍然是一个成熟且广泛使用的流程引擎，而Camunda则是在Activiti基础上的一种选择，可以根据具体需求选择使用其中之一。


基于camunda开发的工作流web系统--中享思途

http://www.situedu.com/news/uid/2950.html

https://www.cnblogs.com/yscec/p/11562064.html


camunda-modeler
画流程图的工具

https://camunda.com/download/modeler/?__hstc=12929896.eb7fddd2cb015af811484bcc48f563df.1687671971326.1687671971326.1687671971326.1&__hssc=12929896.1.1687671971326&__hsfp=3766048905

Open Source Desktop Modeler
Supports: BPMN, DMN, Forms
Version: 5.12.0
Release Date: June 13, 2023
Platform: Camunda 7 and 8

全亿健康用了

```xml
        <dependency>
            <groupId>org.camunda.bpm.springboot</groupId>
            <artifactId>camunda-bpm-spring-boot-starter-rest</artifactId>
            <version>7.15.0</version>
        </dependency>

        <dependency>
            <groupId>org.camunda.bpm.springboot</groupId>
            <artifactId>camunda-bpm-spring-boot-starter-webapp</artifactId>
            <version>7.15.0</version>
        </dependency>
```
