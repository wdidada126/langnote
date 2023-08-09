# tomcat_code

```xml
    <dependency>
      <groupId>org.apache.tomcat.embed</groupId>
      <artifactId>tomcat-embed-core</artifactId>
      <version>9.0.38</version>
      <scope>compile</scope>
    </dependency>
```




```xml
    <dependency>
      <groupId>org.apache.tomcat.embed</groupId>
      <artifactId>tomcat-embed-core-websocket</artifactId>
      <version>9.0.38</version>
      <scope>compile</scope>
    </dependency>
```
## 源代码分包解析 9.0

tomcat-embed-core  9.0 java api doc网址

https://tomcat.apache.org/tomcat-9.0-doc/api/index.html


org.apache.catalina
org.apache.catalina.ant
org.apache.catalina.ant.jmx
org.apache.catalina.authenticator
org.apache.catalina.authenticator.jaspic
org.apache.catalina.connector
org.apache.catalina.core
org.apache.catalina.deploy
org.apache.catalina.filters
org.apache.catalina.ha
org.apache.catalina.ha.authenticator
org.apache.catalina.ha.backend
org.apache.catalina.ha.context
org.apache.catalina.ha.deploy
org.apache.catalina.ha.session
org.apache.catalina.ha.tcp
org.apache.catalina.loader
org.apache.catalina.manager
org.apache.catalina.manager.host
org.apache.catalina.manager.util
org.apache.catalina.mapper
org.apache.catalina.mbeans
org.apache.catalina.realm
org.apache.catalina.security
org.apache.catalina.servlets
org.apache.catalina.session
org.apache.catalina.ssi
org.apache.catalina.startup
org.apache.catalina.storeconfig
org.apache.catalina.tribes
org.apache.catalina.tribes.group
org.apache.catalina.tribes.group.interceptors
org.apache.catalina.tribes.io
org.apache.catalina.tribes.jmx
org.apache.catalina.tribes.membership
org.apache.catalina.tribes.membership.cloud
org.apache.catalina.tribes.tipis
org.apache.catalina.tribes.transport
org.apache.catalina.tribes.transport.bio
org.apache.catalina.tribes.transport.nio
org.apache.catalina.tribes.util
org.apache.catalina.users
org.apache.catalina.util
org.apache.catalina.valves
org.apache.catalina.valves.rewrite
org.apache.catalina.webresources
org.apache.catalina.webresources.war
org.apache.coyote
org.apache.coyote.ajp
org.apache.coyote.http11
org.apache.coyote.http11.filters
org.apache.coyote.http11.upgrade
org.apache.coyote.http2
org.apache.el
org.apache.el.lang
org.apache.el.stream
org.apache.el.util
org.apache.jasper
org.apache.jasper.compiler
org.apache.jasper.compiler.tagplugin
org.apache.jasper.el
org.apache.jasper.optimizations
org.apache.jasper.runtime
org.apache.jasper.security
org.apache.jasper.servlet
org.apache.jasper.tagplugins.jstl
org.apache.jasper.tagplugins.jstl.core
org.apache.jasper.util
org.apache.juli
org.apache.juli.logging
org.apache.naming
org.apache.naming.factory
org.apache.naming.factory.webservices
org.apache.naming.java
org.apache.tomcat
org.apache.tomcat.buildutil
org.apache.tomcat.buildutil.translate
org.apache.tomcat.dbcp.dbcp2
org.apache.tomcat.dbcp.dbcp2.cpdsadapter
org.apache.tomcat.dbcp.dbcp2.datasources
org.apache.tomcat.dbcp.dbcp2.managed
org.apache.tomcat.dbcp.pool2
org.apache.tomcat.dbcp.pool2.impl
org.apache.tomcat.jdbc.naming
org.apache.tomcat.jdbc.pool
org.apache.tomcat.jdbc.pool.interceptor
org.apache.tomcat.jdbc.pool.jmx
org.apache.tomcat.jni
org.apache.tomcat.util
org.apache.tomcat.util.bcel
org.apache.tomcat.util.bcel.classfile
org.apache.tomcat.util.buf
org.apache.tomcat.util.codec.binary
org.apache.tomcat.util.collections
org.apache.tomcat.util.compat
org.apache.tomcat.util.descriptor
org.apache.tomcat.util.descriptor.tagplugin
org.apache.tomcat.util.descriptor.tld
org.apache.tomcat.util.descriptor.web
org.apache.tomcat.util.digester
org.apache.tomcat.util.file
org.apache.tomcat.util.http
org.apache.tomcat.util.http.fileupload
org.apache.tomcat.util.http.fileupload.disk
org.apache.tomcat.util.http.fileupload.impl
org.apache.tomcat.util.http.fileupload.servlet
org.apache.tomcat.util.http.fileupload.util
org.apache.tomcat.util.http.fileupload.util.mime
org.apache.tomcat.util.http.parser
org.apache.tomcat.util.log
org.apache.tomcat.util.modeler
org.apache.tomcat.util.modeler.modules
org.apache.tomcat.util.net
org.apache.tomcat.util.net.jsse
org.apache.tomcat.util.net.openssl
org.apache.tomcat.util.net.openssl.ciphers
org.apache.tomcat.util.res
org.apache.tomcat.util.scan
org.apache.tomcat.util.security
org.apache.tomcat.util.threads
org.apache.tomcat.util.xreflection
org.apache.tomcat.websocket
org.apache.tomcat.websocket.pojo
org.apache.tomcat.websocket.server


## 分包解析

### org.apache.catalina



| Interface Summary                    |                                                              |      |
| ------------------------------------ | ------------------------------------------------------------ | ---- |
| Interface                            | Description                                                  |      |
| AccessLog                            | Intended for use by a Valve to indicate that the Valve provides access logging. |      |
| AsyncDispatcher                      |                                                              |      |
| Authenticator                        | An Authenticator is a component (usually a Valve or Container) that provides some sort of authentication service. |      |
| Cluster                              | A Cluster works as a Cluster client/server for the local host Different Cluster implementations can be used to support different ways to communicate within the Cluster. |      |
| Contained                            | Decoupling interface which specifies that an implementing class is associated with at most one Container instance. |      |
| Container                            | A Container is an object that can execute requests received from a client, and return responses based on those requests. |      |
| ContainerListener                    | Interface defining a listener for significant Container generated events. |      |
| ContainerServlet                     | A ContainerServlet is a servlet that has access to Catalina internal functionality, and is loaded from the Catalina class loader instead of the web application class loader. |      |
| Context                              | A Context is a Container that represents a servlet context, and therefore an individual web application, in the Catalina servlet engine. |      |
| CredentialHandler                    | This interface is used by the Realm to compare the user provided credentials with the credentials stored in the Realm for that user. |      |
| DistributedManager                   | Interface implemented by session managers that do not keep a complete copy of all sessions in memory but do know where every session is. |      |
| Engine                               | An Engine is a Container that represents the entire Catalina servlet engine. |      |
| Executor                             |                                                              |      |
| Group                                | Abstract representation of a group of Users in a UserDatabase. |      |
| Host                                 | A Host is a Container that represents a virtual host in the Catalina servlet engine. |      |
| JmxEnabled                           | This interface is implemented by components that will be registered with an MBean server when they are created and unregistered when they are destroyed. |      |
| Lifecycle                            | Common interface for component life cycle methods.           |      |
| Lifecycle.SingleUse                  | Marker interface used to indicate that the instance should only be used once. |      |
| LifecycleListener                    | Interface defining a listener for significant events (including "component start" and "component stop" generated by a component that implements the Lifecycle interface. |      |
| Loader                               | A Loader represents a Java ClassLoader implementation that can be used by a Container to load class files (within a repository associated with the Loader) that are designed to be reloaded upon request, as well as a mechanism to detect whether changes have occurred in the underlying repository. |      |
| Manager                              | A Manager manages the pool of Sessions that are associated with a particular Context. |      |
| Pipeline                             | Interface describing a collection of Valves that should be executed in sequence when the invoke() method is invoked. |      |
| Realm                                | A Realm is a read-only facade for an underlying security realm used to authenticate individual users, and identify the security roles associated with those users. |      |
| Role                                 | Abstract representation of a security role, suitable for use in environments like JAAS that want to deal with Principals. |      |
| Server                               | A Server element represents the entire Catalina servlet container. |      |
| Service                              | A Service is a group of one or more Connectors that share a single Container to process their incoming requests. |      |
| Session                              | A Session is the Catalina-internal facade for an HttpSession that is used to maintain state information between requests for a particular user of a web application. |      |
| SessionIdGenerator                   |                                                              |      |
| SessionListener                      | Interface defining a listener for significant Session generated events. |      |
| Store                                | A Store is the abstraction of a Catalina component that provides persistent storage and loading of Sessions and their associated user data. |      |
| StoreManager                         | PersistentManager would have been a better name but that would have clashed with the implementation name. |      |
| ThreadBindingListener                | Callback for establishing naming association when entering the application scope. |      |
| TomcatPrincipal                      | [Defines additional methods implemented by Principals created by Tomcat's standard Realm implementations.](https://tomcat.apache.org/tomcat-9.0-doc/api/org/apache/catalina/Realm.html) |      |
| TrackedWebResource                   |                                                              |      |
| User                                 | [Abstract representation of a user in a UserDatabase.](https://tomcat.apache.org/tomcat-9.0-doc/api/org/apache/catalina/UserDatabase.html) |      |
| UserDatabase                         | Abstract representation of a database of Users and Groups that can be maintained by an application, along with definitions of corresponding Roles, and referenced by a Realm for authentication and access control. |      |
| Valve                                | A Valve is a request processing component associated with a particular Container. |      |
| WebResource                          | Represents a file or directory within a web application.     |      |
| WebResourceRoot                      | Represents the complete set of resources for a web application. |      |
| WebResourceRoot.CacheStrategy        | Provides a mechanism to modify the caching behaviour.        |      |
| WebResourceSet                       | Represents a set of resources that are part of a web application. |      |
| Wrapper                              | A Wrapper is a Container that represents an individual servlet definition from the deployment descriptor of the web application. |      |
| Class Summary                        |                                                              |      |
| Class                                | Description                                                  |      |
| ContainerEvent                       | General event for notifying listeners of significant changes on a Container. |      |
| Globals                              | Global constants that are applicable to multiple packages within Catalina. |      |
| LifecycleEvent                       | General event for notifying listeners of significant changes on a component that implements the Lifecycle interface. |      |
| SessionEvent                         | General event for notifying listeners of significant changes on a Session. |      |
| Enum Summary                         |                                                              |      |
| Enum                                 | Description                                                  |      |
| LifecycleState                       | [The list of valid states for components that implement Lifecycle.](https://tomcat.apache.org/tomcat-9.0-doc/api/org/apache/catalina/Lifecycle.html) |      |
| WebResourceRoot.ArchiveIndexStrategy |                                                              |      |
| WebResourceRoot.ResourceSetType      |                                                              |      |
| Exception Summary                    |                                                              |      |
| Exception                            | Description                                                  |      |
| LifecycleException                   | General purpose exception that is thrown to indicate a lifecycle related problem. |      |



org.apache.catalina.ant
org.apache.catalina.ant.jmx
org.apache.catalina.authenticator
org.apache.catalina.authenticator.jaspic
org.apache.catalina.connector
org.apache.catalina.core
org.apache.catalina.deploy
org.apache.catalina.filters
org.apache.catalina.ha
org.apache.catalina.ha.authenticator
org.apache.catalina.ha.backend
org.apache.catalina.ha.context
org.apache.catalina.ha.deploy
org.apache.catalina.ha.session
org.apache.catalina.ha.tcp
org.apache.catalina.loader
org.apache.catalina.manager
org.apache.catalina.manager.host
org.apache.catalina.manager.util
org.apache.catalina.mapper
org.apache.catalina.mbeans
org.apache.catalina.realm
org.apache.catalina.security
org.apache.catalina.servlets
org.apache.catalina.session
org.apache.catalina.ssi
org.apache.catalina.startup
org.apache.catalina.storeconfig
org.apache.catalina.tribes
org.apache.catalina.tribes.group
org.apache.catalina.tribes.group.interceptors
org.apache.catalina.tribes.io
org.apache.catalina.tribes.jmx
org.apache.catalina.tribes.membership
org.apache.catalina.tribes.membership.cloud
org.apache.catalina.tribes.tipis
org.apache.catalina.tribes.transport
org.apache.catalina.tribes.transport.bio
org.apache.catalina.tribes.transport.nio
org.apache.catalina.tribes.util
org.apache.catalina.users
org.apache.catalina.util
org.apache.catalina.valves
org.apache.catalina.valves.rewrite
org.apache.catalina.webresources
org.apache.catalina.webresources.war
### org.apache.coyote
org.apache.coyote.ajp
org.apache.coyote.http11
org.apache.coyote.http11.filters
org.apache.coyote.http11.upgrade
org.apache.coyote.http2
org.apache.el
org.apache.el.lang
org.apache.el.stream
org.apache.el.util
org.apache.jasper
org.apache.jasper.compiler
org.apache.jasper.compiler.tagplugin
org.apache.jasper.el
org.apache.jasper.optimizations
org.apache.jasper.runtime
org.apache.jasper.security
org.apache.jasper.servlet
org.apache.jasper.tagplugins.jstl
org.apache.jasper.tagplugins.jstl.core
org.apache.jasper.util
### org.apache.juli
### org.apache.juli.logging
### org.apache.naming
### org.apache.naming.factory
org.apache.naming.factory.webservices
### org.apache.naming.java
### org.apache.tomcat
### org.apache.tomcat.buildutil
org.apache.tomcat.buildutil.translate
org.apache.tomcat.dbcp.dbcp2
org.apache.tomcat.dbcp.dbcp2.cpdsadapter
org.apache.tomcat.dbcp.dbcp2.datasources
org.apache.tomcat.dbcp.dbcp2.managed
org.apache.tomcat.dbcp.pool2
org.apache.tomcat.dbcp.pool2.impl
### org.apache.tomcat.jdbc.naming
org.apache.tomcat.jdbc.pool
org.apache.tomcat.jdbc.pool.interceptor
org.apache.tomcat.jdbc.pool.jmx
### org.apache.tomcat.jni
### org.apache.tomcat.util
org.apache.tomcat.util.bcel
org.apache.tomcat.util.bcel.classfile
org.apache.tomcat.util.buf
org.apache.tomcat.util.codec.binary
org.apache.tomcat.util.collections
org.apache.tomcat.util.compat
org.apache.tomcat.util.descriptor
org.apache.tomcat.util.descriptor.tagplugin
org.apache.tomcat.util.descriptor.tld
org.apache.tomcat.util.descriptor.web
org.apache.tomcat.util.digester
org.apache.tomcat.util.file
org.apache.tomcat.util.http
org.apache.tomcat.util.http.fileupload
org.apache.tomcat.util.http.fileupload.disk
org.apache.tomcat.util.http.fileupload.impl
org.apache.tomcat.util.http.fileupload.servlet
org.apache.tomcat.util.http.fileupload.util
org.apache.tomcat.util.http.fileupload.util.mime
org.apache.tomcat.util.http.parser
org.apache.tomcat.util.log
org.apache.tomcat.util.modeler
org.apache.tomcat.util.modeler.modules
org.apache.tomcat.util.net
org.apache.tomcat.util.net.jsse
org.apache.tomcat.util.net.openssl
org.apache.tomcat.util.net.openssl.ciphers
org.apache.tomcat.util.res
org.apache.tomcat.util.scan
org.apache.tomcat.util.security
org.apache.tomcat.util.threads
org.apache.tomcat.util.xreflection
### org.apache.tomcat.websocket
org.apache.tomcat.websocket.pojo
org.apache.tomcat.websocket.server