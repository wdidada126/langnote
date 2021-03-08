# jboss

WildFly

WildFly, formerly known as JBoss AS, or simply JBoss, is an application server authored by JBoss, now developed by Red Hat. WildFly is written in Java and implements the Java Platform, Enterprise Edition specification. It runs on multiple platforms


WildFly，原名 JBoss AS(JBoss Application Server) 或者 JBoss，是一套应用程序服务器，属于开源的企业级 Java 中间件软件，用于实现基于 SOA 架构的 Web 应用和服务。 WildFly 包含一组可独立运行的软件。
WildFly采用积极的方法进行内存管理。开发基本运行时服务是为了最大程度地减少堆分配。这些服务在重复的完整解析中使用公共的缓存索引元数据，从而减少了堆和对象的流失。模块化类加载的使用可防止重复类和加载超出系统配置要求的类。这不仅减少了基本内存开销，而且还有助于最大程度地减少垃圾收集器的暂停。最后，管理控制台是100％无状态的，并且完全由客户端驱动。它会立即启动，并且需要服务器上的零内存。
WildFly的架构基于可插拔子系统，可以根据需要添加或删除该子系统，可以删除不需要的功能，还可以减少服务器所需的总体磁盘占用空间和内存开销。
这全部由配置成子系统块的配置控制。要删除子系统，只需要删除该简单的配置块即可。例如，如果决定只需要Servlet支持，则可以删除除“undertow”子系统以外的所有子系统。


JBoss Application Server
JBoss AS


https://github.com/wildfly/wildfly

Jakarta EE
