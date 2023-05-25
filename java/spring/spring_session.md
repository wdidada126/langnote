# spring session

session管理一般在http server上实现，不在gateway上实现


Spring Session是一个用于在分布式系统中管理Web应用会话的框架。它提供了一种简单的方式来管理会话，在不同节点之间共享和存储会话数据。

Spring Session的实现原理基于以下两个核心概念：

1. Session Repository
Session Repository是Spring Session的核心组件之一，它负责存储和管理会话数据。Spring Session支持多种Session Repository实现，包括：

- In-Memory：使用内存存储会话数据，适用于单节点应用场景。
- JDBC：使用数据库存储会话数据，适用于多节点应用场景。
- Redis：使用Redis存储会话数据，适用于多节点应用场景。

在Spring Session中，Session Repository是通过实现`org.springframework.session.SessionRepository`接口来实现的，该接口定义了一组方法，用于存储、读取和删除会话数据。
2. Session ID
Session ID是用于标识会话的唯一标识符。在Spring Session中，Session ID是通过实现`org.springframework.session.SessionIdGenerator`接口来生成的，默认情况下使用UUID来生成Session ID。
Spring Session的实现原理如下：
1. 当用户发起一个HTTP请求时，Spring Framework会拦截这个请求，并创建一个新的Session对象，同时生成一个唯一的Session ID。
2. Spring Session使用Session ID来标识和管理会话。如果Session ID不存在或过期，Spring Framework会创建一个新的Session对象，否则，会从Session Repository中获取相应的会话数据。
3. Spring Session根据配置使用不同的Session Repository来存储和管理会话数据。例如，如果使用JDBC Session Repository，Spring Session会将会话数据存储到数据库中，以便不同节点之间共享和访问。
4. 当用户完成请求并响应完成后，Spring Framework会将Session数据保存回Session Repository中，以便下次请求时可以继续使用。如果Session已经过期，则会在Session Repository中删除相应的会话数据。
总之，Spring Session提供了一种简单的方式来管理会话，在不同节点之间共享和存储会话数据。它通过Session Repository来存储和管理会话数据，并使用Session ID来标识和管理会话。Spring Session支持多种Session Repository实现，包括In-Memory、JDBC和Redis等，可以根据应用场景和需求来选择不同的实现方式。同时，Spring Session还提供了一些扩展功能，如集成Spring Security和OAuth2等，使得管理会话更加方便和灵活。


