# SQLAdvisor


有同学已经编译了docker镜像，启动一个容器
docker run -d --name=sqladvisor ppabc/sqladvisor

在容器里执行sqladvisor即可，不报错
docker exec -it sqladvisor bash
sqladvisor -h 172.17.10.84 -P 3306 -u root -p 密码 -d test -q "select * from t4 where tcol04=1;" -v 1



4年之前更新的代码

cmake的
源码安装

SQLAdvisor是由美团点评公司技术工程部DBA团队（北京）开发维护的一个分析SQL给出索引优化建议的工具。

https://github.com/Meituan-Dianping/SQLAdvisor/
