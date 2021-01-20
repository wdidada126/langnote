# ofbiz

erp开源电商系统

### github repo
以前ant编译，拷贝jar包
现在 gradle
在build.gradle上添加jar包引用

https://github.com/apache/ofbiz-framework

```powershell
./init-gradle-wrapper
./gradlew cleanAll loadAll
./gradlew ofbiz
```

local mysql
如何查看mysql运行的sql语句
打开xx日志

1.进入Mysql
2.启用Log功能(general_log=ON) SHOW VARIABLES LIKE "general_log%"; SET GLOBAL general_log = 'ON';
3.设置Log文件地址(所有Sql语句都会在general_log_file里) SET GLOBAL general_log_file = 'c:\mysql.log';

http://localhost:8080/catalog/


D:\Mysql\mysql-5.7.31-winx64\data\chengwu2.log


https://cwiki.apache.org/confluence/display/OFBIZ/How+to+migrate+OFBiz+from+Derby+to+MySQL+database


https://localhost:8443/catalog/control/main

登陆 用户名/密码  admin ofbiz(一样的)

https://blog.csdn.net/qq_38802742/article/details/89397510