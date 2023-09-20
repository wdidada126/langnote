# Db2

Windows10 64位安装DB2数据库
https://www.cnblogs.com/luyanjie/p/10423717.html



Db2官网

https://www.ibm.com/analytics/ca/en/technology/db2/db2-linux-unix-windows.html


docker pull ibmcom/db2
docker run -itd --name db2server -e LICENSE=accept -e DB2INST1_PASSWORD=<password> -e DBNAME=<database_name> -p 50000:50000 ibmcom/db2
其中，<password>为您指定的DB2实例管理员（db2inst1）密码，<database_name>为您指定的要创建的数据库名称。另外，-p参数将Docker主机的50000端口映射到容器的50000端口，以便访问DB2服务器。

连接到DB2服务器：使用DB2客户端工具连接到DB2服务器，如Data Studio或命令行工具。

