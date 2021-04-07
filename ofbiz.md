# ofbiz



cd /root/apache-ofbiz-17.12.05/

java -jar build/libs/ofbiz.jar & > ofbiz.log 2>&1 &



```sql
SELECT JOB_ID, JOB_NAME, RUN_TIME, POOL_ID, STATUS_ID, PARENT_JOB_ID, PREVIOUS_JOB_ID, SERVICE_NAME, LOADER_NAME, MAX_RETRY, CURRENT_RETRY_COUNT, AUTH_USER_LOGIN_ID, RUN_AS_USER, RUNTIME_DATA_ID, RECURRENCE_INFO_ID, TEMP_EXPR_ID, CURRENT_RECURRENCE_COUNT, MAX_RECURRENCE_COUNT, RUN_BY_INSTANCE_ID, START_DATE_TIME, FINISH_DATE_TIME, CANCEL_DATE_TIME, JOB_RESULT, LAST_UPDATED_STAMP, LAST_UPDATED_TX_STAMP, CREATED_STAMP, CREATED_TX_STAMP FROM JOB_SANDBOX WHERE ((RUN_BY_INSTANCE_ID = 'ofbiz1' AND ((CANCEL_DATE_TIME IS NOT NULL AND CANCEL_DATE_TIME < '2021-04-03 10:09:36.777') OR (FINISH_DATE_TIME IS NOT NULL AND FINISH_DATE_TIME < '2021-04-03 10:09:36.777')))) ORDER BY JOB_ID ASC
```





一集菜单

会计
应付账户
应收账户
资产维护
目录
内容
设备
人力资源
制造

新建产品
应付账户 里面操作需要产品






erp开源电商系统

github repo
以前ant编译，拷贝jar包
现在 gradle
在build.gradle上添加jar包引用

https://github.com/apache/ofbiz-framework



\framework\entity\config\entityengine.xml中更改为本地mysql配置



`vim framework/entity/config/entityengine.xml`





四个数据库

ofbiz
ofbiz_odbc
ofbizolap
ofbiztenant



```powershell
./init-gradle-wrapper
./gradlew cleanAll loadAll
./gradlew ofbiz
```



./gradlew cleanAll "ofbiz --load-data readers=seed,seed-initial" loadAdminUserLogin -PuserLoginId=admin



local mysql
如何查看mysql运行的sql语句
打开xx日志

1.进入Mysql
2.启用Log功能(general_log=ON) 
SHOW VARIABLES LIKE "general_log%";
SET GLOBAL general_log = 'ON';
3.设置Log文件地址(所有Sql语句都会在general_log_file里)
SET GLOBAL general_log_file = 'c:\mysql.log';

http://localhost:8080/catalog/


D:\Mysql\mysql-5.7.31-winx64\data\chengwu2.log


https://cwiki.apache.org/confluence/display/OFBIZ/How+to+migrate+OFBiz+from+Derby+to+MySQL+database


https://localhost:8443/catalog/control/main

登陆 用户名/密码  admin ofbiz  密码改了 5%Edidada

https://blog.csdn.net/qq_38802742/article/details/89397510


社区
https://ofbiz.apache.org/mailing-lists.html

表结构设计
大量的外键 触发器



```sql
INSERT INTO SERVER_HIT (VISIT_ID, CONTENT_ID, HIT_START_DATE_TIME, HIT_TYPE_ID, NUM_OF_BYTES, RUNNING_TIME_MILLIS, USER_LOGIN_ID, STATUS_ID, REQUEST_URL, REFERRER_URL, SERVER_IP_ADDRESS, SERVER_HOST_NAME, INTERNAL_CONTENT_ID, PARTY_ID, ID_BY_IP_CONTACT_MECH_ID, REF_BY_WEB_CONTACT_MECH_ID) VALUES ('10707', 'accounting.LookupBillingAccount', '2021-04-07 12:55:05.271', 'REQUEST', null, 437, 'admin', null, 'https://106.75.209.6:8443/accounting/control/LookupBillingAccount', 'https://106.75.209.6:8443/accounting/control/createInvoice', '127.0.0.1', '10-23-29-39', null, null, null, null)



INSERT INTO SERVER_HIT (VISIT_ID, CONTENT_ID, HIT_START_DATE_TIME, HIT_TYPE_ID, NUM_OF_BYTES, RUNNING_TIME_MILLIS, USER_LOGIN_ID, STATUS_ID, REQUEST_URL, REFERRER_URL, SERVER_IP_ADDRESS, SERVER_HOST_NAME, INTERNAL_CONTENT_ID, PARTY_ID, ID_BY_IP_CONTACT_MECH_ID, REF_BY_WEB_CONTACT_MECH_ID) VALUES ('10707', 'accounting.LookupBillingAccount', '2021-04-07 12:55:05.271', 'REQUEST', null, 437, 'admin', null, 'https://106.75.209.6:8443/accounting/control/LookupBillingAccount', 'https://106.75.209.6:8443/accounting/control/createInvoice', '127.0.0.1', '10-23-29-39', null, null, null, null) 

SELECT COUNT(1)  FROM JOB_MANAGER_LOCK WHERE ((((THRU_DATE IS NULL OR THRU_DATE > '2021-04-07 12:55:19.607') AND (FROM_DATE IS NULL OR FROM_DATE <= '2021-04-07 12:55:19.607')) AND (INSTANCE_ID = 'ofbiz1' OR INSTANCE_ID = '_NA_')));

SELECT JOB_ID, JOB_NAME, RUN_TIME, POOL_ID, STATUS_ID, PARENT_JOB_ID, PREVIOUS_JOB_ID, SERVICE_NAME, LOADER_NAME, MAX_RETRY, CURRENT_RETRY_COUNT, AUTH_USER_LOGIN_ID, RUN_AS_USER, RUNTIME_DATA_ID, RECURRENCE_INFO_ID, TEMP_EXPR_ID, CURRENT_RECURRENCE_COUNT, MAX_RECURRENCE_COUNT, RUN_BY_INSTANCE_ID, START_DATE_TIME, FINISH_DATE_TIME, CANCEL_DATE_TIME, JOB_RESULT, LAST_UPDATED_STAMP, LAST_UPDATED_TX_STAMP, CREATED_STAMP, CREATED_TX_STAMP FROM JOB_SANDBOX WHERE ((RUN_BY_INSTANCE_ID = 'ofbiz1' AND ((CANCEL_DATE_TIME IS NOT NULL AND CANCEL_DATE_TIME < '2021-04-03 12:55:20.153') OR (FINISH_DATE_TIME IS NOT NULL AND FINISH_DATE_TIME < '2021-04-03 12:55:20.153')))) ORDER BY JOB_ID ASC;
```



mysql查询缓存

https://www.cnblogs.com/coshaho/p/7192343.html





Of biz Mac idea 命令行编译失败



