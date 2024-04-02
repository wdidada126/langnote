# gateway

翼支付，大后端应用，不需要走网购，dubbo rpc调用

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
import org.springframework.util.AntPathMatcher;

PathMatcher pathMatcher = new AntPathMatcher(); // Ant匹配器
String method=request.getMethodValue();
String path =request.getURI().getPath();
String restfulPath = method +":"+ path; // Restful接囗权限设计
```



```java

/**
 * Copyright (c) 2020 ShangHai P&C Information Technology Co.,Ltd. All rights reserved.
 * 
 * <p>项目名称	:ares-open-gateway</p>
 * <p>包名称    	:cn.com.yitong.ares.gateway.entity</p>
 * <p>文件名称	:ApiInfo.java</p>
 * <p>创建时间	:2020-7-15 18:24:27 </p>
 */
package cn.com.yitong.ares.gateway.entity;
import java.io.Serializable;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import cn.hutool.json.JSONUtil;

/**
 * <p>
 * API接口信息
 * </p>.
 *
 * @author zwb
 * @since 2020-06-05
 */
@TableName(value = "GW_API_INFO")
public class ApiInfo implements Serializable {

    /**
     * The Constant serialVersionUID.
     */
    private static final long serialVersionUID = 1L;

    /**
     * 接口ID.
     */
    @TableId
    private String apiId;

    /**
     * 分组ID.
     */
    private String groupId;

    /**
     * 接口ID.
     */
    private String docId;

    /**
     * 接口名称.
     */
    private String apiCode;

    /**
     * 接口名称.
     */
    private String apiName;

    /**
     * 接口版本号.
     */
    private String apiVersion;

    /**
     * 报文类型，默认普通报文：1-普通报文、2-文件上传、3-文件下载、4-完全透传.
     */
    private String msgType;

    /**
     * 接口类型：1-产品API、2-SDK-API、3-H5-API.
     */
    private String apiType;

    /**
     * 通配符匹配：0-停用、1-启用.
     */
    private String wildcardMatch;

    /**
     * 请求路径.
     */
    private String apiPath;

    /**
     * 客户端HTTP 请求方法，默认POST
     *             GET
     *             POST
     *             PUT
     *             DELETE
     *             HEAD
     *             OPTION
     *             PATCH.
     */
    private String apiMethod;

    /**
     * 请求报文是否解密
     *             0、不解密
     *             1、需要解密.
     */
    private String isDecode;

    /**
     * 请求报文是否验签：0-否、1-是.
     */
    private String isValidateSign;

    /**
     * 去除路径前缀，默认0，表示不去除，1表示去除1层路径，2表示去除2层路径，依次类推.
     */
    private Integer stripPrefix;

    /**
     * 路由方式：1-路由映射、2-自动路由.
     */
    private String routeType;
    
    
    /**
     * 服务类别.
     */
    private String serviceTypeId;
    
    /**
     * 安全类型：00-保留、01-A1安全级别、02-A2安全级别.
     */
    private String safeType;
    
    /**
     * 是否防重放：0-否、1-是.
     */
    private boolean isCheckReplay=false;
    
    
    /**
     * 是否防重复：0-否、1-是.
     */
    private boolean isCheckRepeat=false;
    
    /**
     * 是否设置cookie
     */
    private boolean isSetCookie = false;
    
    
    /**
     * 入参请求模式：1-参数映射、2-参数透传.
     */
    private String paramForwardType;


    /**
     * 状态:
     *             0-失效、
     *             1-正常.
     */
    private String state;

    /**
     * 是否记录文件日志：0-不记录、1-记录.
     */
    private String isFileLog;

    /**
     * 是否记录数据库日志：0-不记录、1-记录.
     */
    private String isDbLog;

    /**
     * API描述.
     */
    private String apiDesc;

    /**
     * 创建日期，格式：yyyy-MM-dd.
     */
    private String addDate;

    /**
     * 创建时间，格式：yyyy-MM-dd HH:mm:ss.
     */
    private String addDateTime;

    /**
     * 创建人.
     */
    private String addUserId;

    /**
     * 更新日期，格式：yyyy-MM-dd.
     */
    private String modDate;

    /**
     * 更新时间，格式：yyyy-MM-dd HH:mm:ss.
     */
    private String modDateTime;

    /**
     * 更新人.
     */
    private String modUserId;

    /**
     * 审核时间，格式：yyyy-MM-dd.
     */
    private String authDate;

    /**
     * 审核时间，格式：yyyy-MM-dd HH:mm:ss.
     */
    private String authDateTime;

    /**
     * 审核操作员.
     */
    private String authUserId;

    /**
     * 数据删除标记：0-未删除、1-已删除.
     */
    private String delFlag;

    /**
     * Gets the api id.
     *
     * @return the api id
     */
    public String getApiId() {
        return apiId;
    }

    /**
     * Sets the api id.
     *
     * @param apiId the new api id
     */
    public void setApiId(String apiId) {
        this.apiId = apiId;
    }

    /**
     * Gets the group id.
     *
     * @return the group id
     */
    public String getGroupId() {
        return groupId;
    }

    /**
     * Sets the group id.
     *
     * @param groupId the new group id
     */
    public void setGroupId(String groupId) {
        this.groupId = groupId;
    }

    /**
     * Gets the doc id.
     *
     * @return the doc id
     */
    public String getDocId() {
        return docId;
    }

    /**
     * Sets the doc id.
     *
     * @param docId the new doc id
     */
    public void setDocId(String docId) {
        this.docId = docId;
    }

    /**
     * Gets the api code.
     *
     * @return the api code
     */
    public String getApiCode() {
        return apiCode;
    }

    /**
     * Sets the api code.
     *
     * @param apiCode the new api code
     */
    public void setApiCode(String apiCode) {
        this.apiCode = apiCode;
    }

    /**
     * Gets the api name.
     *
     * @return the api name
     */
    public String getApiName() {
        return apiName;
    }

    /**
     * Sets the api name.
     *
     * @param apiName the new api name
     */
    public void setApiName(String apiName) {
        this.apiName = apiName;
    }

    /**
     * Gets the api version.
     *
     * @return the api version
     */
    public String getApiVersion() {
        return apiVersion;
    }

    /**
     * Sets the api version.
     *
     * @param apiVersion the new api version
     */
    public void setApiVersion(String apiVersion) {
        this.apiVersion = apiVersion;
    }

    /**
     * Gets the msg type.
     *
     * @return the msg type
     */
    public String getMsgType() {
        return msgType;
    }

    /**
     * Sets the msg type.
     *
     * @param msgType the new msg type
     */
    public void setMsgType(String msgType) {
        this.msgType = msgType;
    }

    /**
     * Gets the api type.
     *
     * @return the api type
     */
    public String getApiType() {
        return apiType;
    }

    /**
     * Sets the api type.
     *
     * @param apiType the new api type
     */
    public void setApiType(String apiType) {
        this.apiType = apiType;
    }

    /**
     * Gets the wildcard match.
     *
     * @return the wildcard match
     */
    public String getWildcardMatch() {
        return wildcardMatch;
    }

    /**
     * Sets the wildcard match.
     *
     * @param wildcardMatch the new wildcard match
     */
    public void setWildcardMatch(String wildcardMatch) {
        this.wildcardMatch = wildcardMatch;
    }

    /**
     * Gets the api path.
     *
     * @return the api path
     */
    public String getApiPath() {
        return apiPath;
    }

    /**
     * Sets the api path.
     *
     * @param apiPath the new api path
     */
    public void setApiPath(String apiPath) {
        this.apiPath = apiPath;
    }

    /**
     * Gets the api method.
     *
     * @return the api method
     */
    public String getApiMethod() {
        return apiMethod;
    }

    /**
     * Sets the api method.
     *
     * @param apiMethod the new api method
     */
    public void setApiMethod(String apiMethod) {
        this.apiMethod = apiMethod;
    }

    /**
     * Gets the 是否 decode.
     *
     * @return the 是否 decode
     */
    public String getIsDecode() {
        return isDecode;
    }

    /**
     * Sets the 是否 decode.
     *
     * @param isDecode the new 是否 decode
     */
    public void setIsDecode(String isDecode) {
        this.isDecode = isDecode;
    }

    /**
     * Gets the 是否 validate sign.
     *
     * @return the 是否 validate sign
     */
    public String getIsValidateSign() {
        return isValidateSign;
    }

    /**
     * Sets the 是否 validate sign.
     *
     * @param isValidateSign the new 是否 validate sign
     */
    public void setIsValidateSign(String isValidateSign) {
        this.isValidateSign = isValidateSign;
    }

    /**
     * Gets the strip prefix.
     *
     * @return the strip prefix
     */
    public Integer getStripPrefix() {
        return stripPrefix;
    }

    /**
     * Sets the strip prefix.
     *
     * @param stripPrefix the new strip prefix
     */
    public void setStripPrefix(Integer stripPrefix) {
        this.stripPrefix = stripPrefix;
    }

    /**
     * Gets the route type.
     *
     * @return the route type
     */
    public String getRouteType() {
        return routeType;
    }

    /**
     * Sets the route type.
     *
     * @param routeType the new route type
     */
    public void setRouteType(String routeType) {
        this.routeType = routeType;
    }

    /**
     * Gets the state.
     *
     * @return the state
     */
    public String getState() {
        return state;
    }

    /**
     * Sets the state.
     *
     * @param state the new state
     */
    public void setState(String state) {
        this.state = state;
    }

    /**
     * Gets the 是否 file log.
     *
     * @return the 是否 file log
     */
    public String getIsFileLog() {
        return isFileLog;
    }

    /**
     * Sets the 是否 file log.
     *
     * @param isFileLog the new 是否 file log
     */
    public void setIsFileLog(String isFileLog) {
        this.isFileLog = isFileLog;
    }

    /**
     * Gets the 是否 db log.
     *
     * @return the 是否 db log
     */
    public String getIsDbLog() {
        return isDbLog;
    }

    /**
     * Sets the 是否 db log.
     *
     * @param isDbLog the new 是否 db log
     */
    public void setIsDbLog(String isDbLog) {
        this.isDbLog = isDbLog;
    }
    

    /**
     * Gets the service type id.
     *
     * @return the serviceTypeId
     */
	public String getServiceTypeId() {
		return serviceTypeId;
	}

	/**
	 * Sets the service type id.
	 *
	 * @param serviceTypeId the serviceTypeId to set
	 */
	public void setServiceTypeId(String serviceTypeId) {
		this.serviceTypeId = serviceTypeId;
	}

	/**
	 * Gets the safe type.
	 *
	 * @return the safeType
	 */
	public String getSafeType() {
		return safeType;
	}

	/**
	 * Sets the safe type.
	 *
	 * @param safeType the safeType to set
	 */
	public void setSafeType(String safeType) {
		this.safeType = safeType;
	}

	/**
	 * Gets the 是否 check replay.
	 *
	 * @return the isCheckReplay
	 */
	public boolean getIsCheckReplay() {
		return isCheckReplay;
	}

	/**
	 * Sets the 是否 check replay.
	 *
	 * @param isCheckReplay the isCheckReplay to set
	 */
	public void setIsCheckReplay(boolean isCheckReplay) {
		this.isCheckReplay = isCheckReplay;
	}

	/**
	 * Gets the 是否 check repeat.
	 *
	 * @return the isCheckRepeat
	 */
	public boolean getIsCheckRepeat() {
		return isCheckRepeat;
	}

	/**
	 * Sets the 是否 check repeat.
	 *
	 * @param isCheckRepeat the isCheckRepeat to set
	 */
	public void setIsCheckRepeat(boolean isCheckRepeat) {
		this.isCheckRepeat = isCheckRepeat;
	}
	
	
	/**
	 * Checks if is 设置 cookie.
	 *
	 * @return true, if is 设置 cookie
	 */
	public boolean isSetCookie() {
		return isSetCookie;
	}

	/**
	 * Sets the 设置 cookie.
	 *
	 * @param isSetCookie the new 设置 cookie
	 */
	public void setSetCookie(boolean isSetCookie) {
		this.isSetCookie = isSetCookie;
	}

	/**
	 * Gets the param forward type.
	 *
	 * @return the paramForwardType
	 */
	public String getParamForwardType() {
		return paramForwardType;
	}

	/**
	 * Sets the param forward type.
	 *
	 * @param paramForwardType the paramForwardType to set
	 */
	public void setParamForwardType(String paramForwardType) {
		this.paramForwardType = paramForwardType;
	}

	/**
	 * Gets the api desc.
	 *
	 * @return the api desc
	 */
	public String getApiDesc() {
        return apiDesc;
    }

    /**
     * Sets the api desc.
     *
     * @param apiDesc the new api desc
     */
    public void setApiDesc(String apiDesc) {
        this.apiDesc = apiDesc;
    }

    /**
     * Gets the 新增 date.
     *
     * @return the 新增 date
     */
    public String getAddDate() {
        return addDate;
    }

    /**
     * Sets the 新增 date.
     *
     * @param addDate the new 新增 date
     */
    public void setAddDate(String addDate) {
        this.addDate = addDate;
    }

    /**
     * Gets the 新增 date time.
     *
     * @return the 新增 date time
     */
    public String getAddDateTime() {
        return addDateTime;
    }

    /**
     * Sets the 新增 date time.
     *
     * @param addDateTime the new 新增 date time
     */
    public void setAddDateTime(String addDateTime) {
        this.addDateTime = addDateTime;
    }

    /**
     * Gets the 新增 user id.
     *
     * @return the 新增 user id
     */
    public String getAddUserId() {
        return addUserId;
    }

    /**
     * Sets the 新增 user id.
     *
     * @param addUserId the new 新增 user id
     */
    public void setAddUserId(String addUserId) {
        this.addUserId = addUserId;
    }

    /**
     * Gets the mod date.
     *
     * @return the mod date
     */
    public String getModDate() {
        return modDate;
    }

    /**
     * Sets the mod date.
     *
     * @param modDate the new mod date
     */
    public void setModDate(String modDate) {
        this.modDate = modDate;
    }

    /**
     * Gets the mod date time.
     *
     * @return the mod date time
     */
    public String getModDateTime() {
        return modDateTime;
    }

    /**
     * Sets the mod date time.
     *
     * @param modDateTime the new mod date time
     */
    public void setModDateTime(String modDateTime) {
        this.modDateTime = modDateTime;
    }

    /**
     * Gets the mod user id.
     *
     * @return the mod user id
     */
    public String getModUserId() {
        return modUserId;
    }

    /**
     * Sets the mod user id.
     *
     * @param modUserId the new mod user id
     */
    public void setModUserId(String modUserId) {
        this.modUserId = modUserId;
    }

    /**
     * Gets the auth date.
     *
     * @return the auth date
     */
    public String getAuthDate() {
        return authDate;
    }

    /**
     * Sets the auth date.
     *
     * @param authDate the new auth date
     */
    public void setAuthDate(String authDate) {
        this.authDate = authDate;
    }

    /**
     * Gets the auth date time.
     *
     * @return the auth date time
     */
    public String getAuthDateTime() {
        return authDateTime;
    }

    /**
     * Sets the auth date time.
     *
     * @param authDateTime the new auth date time
     */
    public void setAuthDateTime(String authDateTime) {
        this.authDateTime = authDateTime;
    }

    /**
     * Gets the auth user id.
     *
     * @return the auth user id
     */
    public String getAuthUserId() {
        return authUserId;
    }

    /**
     * Sets the auth user id.
     *
     * @param authUserId the new auth user id
     */
    public void setAuthUserId(String authUserId) {
        this.authUserId = authUserId;
    }

    /**
     * Gets the del flag.
     *
     * @return the del flag
     */
    public String getDelFlag() {
        return delFlag;
    }

    /**
     * Sets the del flag.
     *
     * @param delFlag the new del flag
     */
    public void setDelFlag(String delFlag) {
        this.delFlag = delFlag;
    }

    /**
     * To string.
     *
     * @return the string
     */
    @Override
    public String toString() {
        return JSONUtil.toJsonStr(this);
    }
}

```