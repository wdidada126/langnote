javax.sql

CommonDataSource

java.sql
Wrapper

DataSource

DataSource extends CommonDataSource, Wrapper

org.mybatis.spring
SqlSessionFactoryBean


org.mybatis.spring.SqlSessionFactoryBean
private Resource[] mapperLocations;

.xsd

ss自定义xsd元素

org.springframework.jdbc.datasource.DataSourceTransactionManager

http://www.w3school.com.cn/schema/index.asp


org.springframework.context.support.ClassPathXmlApplicationContext

org.springframework.context.support.AbstractRefreshableConfigApplicationContext

protected String[] getConfigLocations() {
	return (this.configLocations != null ? this.configLocations : getDefaultConfigLocations());
}

//            applicationContext.getDefaultConfigLocations();

ss的配置项在包io.shardingsphere.api.config下面

### ShardingDataSourceFactory
工厂方法
创建ShardingDataSource

查看ss javadoc文档