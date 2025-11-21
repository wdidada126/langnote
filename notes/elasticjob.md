# elasticjob


Elastic-Job是一个分布式调度解决方案，由两个相互独立的子项目Elastic-Job-Lite和Elastic-Job-Cloud组成。

Elastic-Job-Lite定位为轻量级无中心化解决方案，使用jar包的形式提供分布式任务的协调服务；Elastic-Job-Cloud采用自研Mesos Framework的解决方案，额外提供资源治理、应用分发以及进程隔离等功能。



2.1.5



elasticjob



image-verification-scheduler



http://elasticjob.io/


Elasticsearch本身不直接支持订阅MySQL的binlog（二进制日志）。然而，您可以使用一些工具和技术将MySQL的binlog数据导入到Elasticsearch中。

一种常见的方法是使用Logstash作为中间件，通过其MySQL输入插件（如`logstash-input-jdbc`）连接到MySQL数据库，并订阅binlog事件。该插件可以读取MySQL的binlog，并将其转发到Elasticsearch进行索引。

以下是一个简单的Logstash配置示例：

```plaintext
input {
  jdbc {
    jdbc_driver_library => "/path/to/mysql-connector-java.jar"
    jdbc_driver_class => "com.mysql.jdbc.Driver"
    jdbc_connection_string => "jdbc:mysql://your_mysql_host:your_mysql_port/your_database_name"
    jdbc_user => "your_mysql_username"
    jdbc_password => "your_mysql_password"
    statement => "SHOW BINLOG EVENTS"
  }
}

output {
  elasticsearch {
    hosts => ["your_elasticsearch_host"]
    index => "your_index_name"
    document_id => "%{id}"
  }
}
```

上述配置中，您需要指定MySQL数据库的连接信息，包括主机、端口、数据库名称、用户名和密码。Logstash将使用MySQL的`SHOW BINLOG EVENTS`语句获取binlog事件，并将其发送到Elasticsearch进行索引。

请注意，这只是一个简单的示例，并且可能需要根据您的具体需求进行更多的配置和定制。您可能需要根据实际情况调整字段映射、数据过滤和索引设置等。

另外，还有其他工具和库可以实现MySQL binlog到Elasticsearch的同步，如Debezium、Maxwell等，它们提供更高级的功能和灵活性。您可以根据具体需求选择合适的工具和技术来实现MySQL binlog到Elasticsearch的订阅和同步。



