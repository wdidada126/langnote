# Db2


主要是国内很多金融企业，因为使用的IBM的硬件设备，而DB2和WebSphere中间件是免费送的，免费送的，免费送的……另外，在超大数据量处理方面，DB2并非是一无是处，so，未来很长一段时间内，还会被广大图便宜的用户使用。

服务器z系列p系列，以及ds8000，v7000这些高低端存储

政府和国企全面要求国产化设备，能跟华为竞争的只有H3C

目前警用集群市场，重点还是放在PDT上

推荐牛新庄博士的三本书《循序渐进DB2》《深入解析DB2》《DB2性能调整与优化》还有IBM官方的DB2文档

Windows10 64位安装DB2数据库
https://www.cnblogs.com/luyanjie/p/10423717.html



Db2官网

https://www.ibm.com/analytics/ca/en/technology/db2/db2-linux-unix-windows.html


docker pull ibmcom/db2
docker run -itd --name db2server -e LICENSE=accept -e DB2INST1_PASSWORD=<password> -e DBNAME=<database_name> -p 50000:50000 ibmcom/db2
其中，<password>为您指定的DB2实例管理员（db2inst1）密码，<database_name>为您指定的要创建的数据库名称。另外，-p参数将Docker主机的50000端口映射到容器的50000端口，以便访问DB2服务器。

连接到DB2服务器：使用DB2客户端工具连接到DB2服务器，如Data Studio或命令行工具。

