# gateway
apisix
四大开源网关的对比分析（OpenResty/Kong/Zuul2/SpringCloudGateway 等）

gateway的作用是？

流量过滤？
后端项目有多个，映射到多个后端项目，前端同意url

后端微服务，有多个应用
前端http入参 head
X-Gw-App-Id
TEST_APPS_MARKET_OPRMGT
PC_MP_HUMAN

TEST_APPS_MARKET_APP
MP-CONSOLE
9999
TEST_APPS_MARKET_OPRMGT
TEST_APPS_MARKET_POC
1000
TEST_PC_OPERATE
SMART-SALARY-PC
OPEN_PLATFORM
UNIFY-MESSAGE-CENTER
PC_MP_HUMAN

前端调用的url写在这里
gw_api_info

后端api写在这里
gw_back_api_info


映射
gw_api_route_mapping


CREATE TABLE `gw_api_info` (
  `API_ID` varchar(50) NOT NULL COMMENT '接口ID',
  `APP_ID` varchar(50) DEFAULT NULL COMMENT '应用ID',
  `SAFE_TYPE` varchar(2) NOT NULL DEFAULT '00' COMMENT '安全类型：00-保留、01-A1安全级别、02-A2安全级别',
  `API_CODE` varchar(100) DEFAULT NULL COMMENT '接口名称',
  `API_NAME` varchar(128) NOT NULL COMMENT '接口名称',
  `API_VERSION` varchar(32) DEFAULT NULL COMMENT '接口版本号',
  `MSG_TYPE` varchar(1) NOT NULL DEFAULT '1' COMMENT '报文类型，默认普通报文：1-普通报文、2-文件上传、3-文件下载、4-完全透传',
  `API_TYPE` varchar(1) NOT NULL DEFAULT '1' COMMENT '接口类型：1-产品API、2-SDK-API、3-H5-API',
  `WILDCARD_MATCH` varchar(1) NOT NULL DEFAULT '0' COMMENT '通配符匹配：0-停用、1-启用',
  `API_PATH` varchar(512) NOT NULL COMMENT '请求路径',
  `API_METHOD` varchar(32) NOT NULL DEFAULT 'POST' COMMENT '客户端HTTP 请求方法，默认POST\r\n            GET\r\n            POST\r\n            PUT\r\n            DELETE\r\n            HEAD\r\n            OPTION\r\n            PATCH',
  `IS_DECODE` varchar(1) NOT NULL DEFAULT '0' COMMENT '请求报文是否解密\r\n            0、不解密\r\n            1、需要解密',
  `IS_VALIDATE_SIGN` varchar(1) NOT NULL DEFAULT '1' COMMENT '请求报文是否验签：0-否、1-是',
  `IS_CHECK_REPLAY` varchar(1) DEFAULT '0' COMMENT '是否防重放：0-否、1-是',
  `IS_CHECK_REPEAT` varchar(1) DEFAULT '0' COMMENT '是否防重复：0-否、1-是',
  `REPEAT_TIME` int(8) NOT NULL COMMENT '防重复提交时间,单位ms',
  `IS_SET_COOKIE` varchar(1) NOT NULL COMMENT '是否开启SET_COOKIE:0-否、1-是',
  `STRIP_PREFIX` int(11) NOT NULL DEFAULT '0' COMMENT '去除路径前缀，默认0，表示不去除，1表示去除1层路径，2表示去除2层路径，依次类推',
  `ROUTE_TYPE` varchar(1) DEFAULT '1' COMMENT '路由方式：1-路由映射、2-自动路由',
  `PARAM_FORWARD_TYPE` varchar(1) DEFAULT '1' COMMENT '入参请求模式：1-参数映射、2-参数透传',
  `STATE` varchar(1) NOT NULL DEFAULT '1' COMMENT '状态:\r\n            0-失效、\r\n            1-正常',
  `IS_FILE_LOG` varchar(1) NOT NULL DEFAULT '1' COMMENT '是否记录文件日志：0-不记录、1-记录',
  `IS_DB_LOG` varchar(1) NOT NULL DEFAULT '1' COMMENT '是否记录数据库日志：0-不记录、1-记录，同步记录、2-记录，异步记录',
  `API_DESC` varchar(200) DEFAULT NULL COMMENT 'API描述',
  `ADD_DATE` varchar(10) DEFAULT NULL COMMENT '创建日期，格式：yyyy-MM-dd',
  `ADD_DATE_TIME` varchar(20) DEFAULT NULL COMMENT '创建时间，格式：yyyy-MM-dd HH:mm:ss',
  `ADD_USER_ID` varchar(50) DEFAULT NULL COMMENT '创建人',
  `MOD_DATE` varchar(10) DEFAULT NULL COMMENT '更新日期，格式：yyyy-MM-dd',
  `MOD_DATE_TIME` varchar(20) DEFAULT NULL COMMENT '更新时间，格式：yyyy-MM-dd HH:mm:ss',
  `MOD_USER_ID` varchar(50) DEFAULT NULL COMMENT '更新人',
  `AUTH_DATE` varchar(10) DEFAULT NULL COMMENT '审核时间，格式：yyyy-MM-dd',
  `AUTH_DATE_TIME` varchar(20) DEFAULT NULL COMMENT '审核时间，格式：yyyy-MM-dd HH:mm:ss',
  `AUTH_USER_ID` varchar(50) DEFAULT NULL COMMENT '审核操作员',
  `DEL_FLAG` varchar(1) NOT NULL DEFAULT '0' COMMENT '数据删除标记：0-未删除、1-已删除',
  PRIMARY KEY (`API_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='API接口信息';

CREATE TABLE `gw_back_api_info` (
  `BACK_API_ID` varchar(50) NOT NULL COMMENT '接口ID',
  `BACK_GROUP_ID` varchar(50) DEFAULT NULL COMMENT '分组ID',
  `BACK_SYS_ID` varchar(50) DEFAULT NULL COMMENT '系统ID',
  `BACK_API_CODE` varchar(50) DEFAULT NULL COMMENT 'API编号',
  `BACK_API_NAME` varchar(128) NOT NULL COMMENT '接口名称',
  `BACK_API_VERSION` varchar(32) DEFAULT '' COMMENT '接口版本号',
  `BACK_PATH` varchar(512) DEFAULT NULL COMMENT '后端服务地址',
  `BACK_METHOD` varchar(32) NOT NULL DEFAULT 'POST' COMMENT '后端服务HTTP 请求方法，默认POST\r\n            GET\r\n            POST\r\n            PUT\r\n            DELETE\r\n            HEAD\r\n            OPTION\r\n            PATCH',
  `CONTENT_TYPE` varchar(256) DEFAULT '' COMMENT '请求数据类型，常用格式：application/json;charset=UTF-8、application/xml;charset=UTF-8、text/html;charset=UTF-8、application/x-www-form-urlencoded;charset=utf-8、multipart/form-data、text/plain',
  `BACK_TIMEOUT` int(11) NOT NULL DEFAULT '10000' COMMENT '后端超时，默认10000，单位毫秒',
  `ERR_CODE_NAME` varchar(50) DEFAULT NULL COMMENT '错误码名称',
  `ERR_MSG_NAME` varchar(50) DEFAULT NULL COMMENT '错误描述名称',
  `SUCC_CODE_VALUE` varchar(50) DEFAULT '1' COMMENT '指后端系统响应成功状态码的值，默认1',
  `SESS_ID_NAME` varchar(50) DEFAULT NULL COMMENT '会话ID名称',
  `RST_DEMO` varchar(1024) DEFAULT NULL COMMENT '返回结果示例',
  `RST_ERR_DEMO` varchar(512) DEFAULT NULL COMMENT '返回错误结果示例',
  `STATE` varchar(1) NOT NULL DEFAULT '1' COMMENT '状态：\r\n            0-停用、\r\n            1-启用',
  `ADD_DATE` varchar(10) DEFAULT NULL COMMENT '创建日期，格式：yyyy-MM-dd',
  `ADD_DATE_TIME` varchar(20) DEFAULT NULL COMMENT '创建时间，格式：yyyy-MM-dd HH:mm:ss',
  `ADD_USER_ID` varchar(50) DEFAULT NULL COMMENT '创建人',
  `MOD_DATE` varchar(10) DEFAULT NULL COMMENT '更新日期，格式：yyyy-MM-dd',
  `MOD_DATE_TIME` varchar(20) DEFAULT NULL COMMENT '更新时间，格式：yyyy-MM-dd HH:mm:ss',
  `MOD_USER_ID` varchar(50) DEFAULT NULL COMMENT '更新人',
  `AUTH_DATE` varchar(10) DEFAULT NULL COMMENT '审核时间，格式：yyyy-MM-dd',
  `AUTH_DATE_TIME` varchar(20) DEFAULT NULL COMMENT '审核时间，格式：yyyy-MM-dd HH:mm:ss',
  `AUTH_USER_ID` varchar(50) DEFAULT NULL COMMENT '审核操作员',
  `DEL_FLAG` varchar(1) NOT NULL DEFAULT '0' COMMENT '数据删除标记：0-未删除、1-已删除',
  PRIMARY KEY (`BACK_API_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='后端API接口信息';


CREATE TABLE `gw_api_route_mapping` (
  `API_ID` varchar(50) NOT NULL COMMENT '接口ID',
  `BACK_API_ID` varchar(50) NOT NULL COMMENT '接口ID',
  `ADD_DATE` varchar(10) DEFAULT NULL COMMENT '创建日期，格式：yyyy-MM-dd',
  `ADD_DATE_TIME` varchar(20) DEFAULT NULL COMMENT '创建时间，格式：yyyy-MM-dd HH:mm:ss',
  `ADD_USER_ID` varchar(50) DEFAULT NULL COMMENT '创建人',
  `MOD_DATE` varchar(10) DEFAULT NULL COMMENT '更新日期，格式：yyyy-MM-dd',
  `MOD_DATE_TIME` varchar(20) DEFAULT NULL COMMENT '更新时间，格式：yyyy-MM-dd HH:mm:ss',
  `MOD_USER_ID` varchar(50) DEFAULT NULL COMMENT '更新人',
  `AUTH_DATE` varchar(10) DEFAULT NULL COMMENT '审核时间，格式：yyyy-MM-dd',
  `AUTH_DATE_TIME` varchar(20) DEFAULT NULL COMMENT '审核时间，格式：yyyy-MM-dd HH:mm:ss',
  `AUTH_USER_ID` varchar(50) DEFAULT NULL COMMENT '审核操作员',
  `DEL_FLAG` varchar(1) NOT NULL DEFAULT '0' COMMENT '数据删除标记：0-未删除、1-已删除',
  PRIMARY KEY (`API_ID`,`BACK_API_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='API路由映射表';


薪酬
文件上传
文件下载
普通报文

INSERT INTO `cloud_gateway_console`.`gw_back_api_info`(`BACK_API_ID`, `BACK_GROUP_ID`, `BACK_SYS_ID`, `BACK_API_CODE`, `BACK_API_NAME`, `BACK_API_VERSION`, `BACK_PATH`, `BACK_METHOD`, `CONTENT_TYPE`, `BACK_TIMEOUT`, `ERR_CODE_NAME`, `ERR_MSG_NAME`, `SUCC_CODE_VALUE`, `SESS_ID_NAME`, `RST_DEMO`, `RST_ERR_DEMO`, `STATE`, `ADD_DATE`, `ADD_DATE_TIME`, `ADD_USER_ID`, `MOD_DATE`, `MOD_DATE_TIME`, `MOD_USER_ID`, `AUTH_DATE`, `AUTH_DATE_TIME`, `AUTH_USER_ID`, `DEL_FLAG`) VALUES ('42b8bbe99952b850', 'b8b7998ab350e950', '508ae9b7b84f9952', NULL, '智能薪酬文件透传', '', '/api/salary/smartRouter.do', 'POST', '5', 10000, '', '', '', '', '', '', '1', '2024-03-01', '2024-03-01 19:13:05', '系统管理员', NULL, NULL, NULL, NULL, NULL, NULL, '0');
INSERT INTO `cloud_gateway_console`.`gw_back_api_info`(`BACK_API_ID`, `BACK_GROUP_ID`, `BACK_SYS_ID`, `BACK_API_CODE`, `BACK_API_NAME`, `BACK_API_VERSION`, `BACK_PATH`, `BACK_METHOD`, `CONTENT_TYPE`, `BACK_TIMEOUT`, `ERR_CODE_NAME`, `ERR_MSG_NAME`, `SUCC_CODE_VALUE`, `SESS_ID_NAME`, `RST_DEMO`, `RST_ERR_DEMO`, `STATE`, `ADD_DATE`, `ADD_DATE_TIME`, `ADD_USER_ID`, `MOD_DATE`, `MOD_DATE_TIME`, `MOD_USER_ID`, `AUTH_DATE`, `AUTH_DATE_TIME`, `AUTH_USER_ID`, `DEL_FLAG`) VALUES ('ac2265c8b9921945', 'a5fd480ea960eacf', '1c485eddb93360ad', NULL, '智能薪酬服务透传', '1.0.0', '/api/salary/smartRouter.do', 'POST', '1', 60000, '', '', '', '', '', '', '1', '2024-01-31', '2024-01-31 10:12:28', '系统管理员', '2024-01-31', '2024-01-31 10:13:06', '系统管理员', NULL, NULL, NULL, '0');


```java
PathMatcher pathMatcher = new AntPathMatcher(); // Ant匹配器
String method=request.getMethodValue();
String path =request.getURI().getPath();
String restfulPath = method +":"+ path; // Restful接囗权限设计
```



