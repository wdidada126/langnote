# tidb

SELECT
	T1.USER_ID,
	TCIT.NAME,
	TCIT.JOB_NO,
	TCIT.ID_NO,
	T1.MONTH,
	ESFM.ITEM_VALUES AS SYS_ITEM_VALUES,
	TBCI.ITEM_VALUES AS IMP_ITEM_VALUES
FROM
	(
	SELECT
		A.USER_ID AS USER_ID,
		A.MONTH AS MONTH
	FROM
		(
		SELECT
			*
		FROM
			HRBASE_UAT2.EMPLOYEE_SOCIAL_SUM_MONTH
		WHERE
			ETP_ID = ?
			AND MONTH = ? ) A
	INNER JOIN (
		SELECT
			*
		FROM
			HRBASE_UAT2.T_BILL_COMPARE_TB
		WHERE
			ETP_ID = ?
			AND MONTH = ? ) B ON
		A.USER_ID = B.USER_ID
		AND ( A.COMPANY_AMOUNT != B.COMPANY_AMOUNT
			OR A.PERSON_AMOUNT != B.PERSON_AMOUNT )) T1
LEFT JOIN HRBASE_UAT2.T_CUSTOM_INFO_TD TCIT ON
	T1.USER_ID = TCIT.EMP_ID
LEFT JOIN (
	SELECT
		A.USER_ID,
		A.MONTH,
		CONCAT('[', GROUP_CONCAT(JSON_OBJECT('code', A.CODE, 'companyAmount', IFNULL(A.COMPANY_UPDATE_AMOUNT, ''), 'personAmount', IFNULL(A.PERSON_UPDATE_AMOUNT, ''))), ']') ITEM_VALUES
	FROM
		(
		SELECT
			USER_ID,
			CODE,
			COMPANY_UPDATE_AMOUNT,
			PERSON_UPDATE_AMOUNT,
			MONTH
		FROM
			HRBASE_UAT2.EMPLOYEE_SOCIAL_MONTH
		WHERE
			ETP_ID = ?
			AND MONTH = ?
	UNION ALL
		SELECT
			USER_ID,
			CODE,
			COMPANY_UPDATE_AMOUNT,
			PERSON_UPDATE_AMOUNT,
			MONTH
		FROM
			HRBASE_UAT2.EMPLOYEE_FUND_MONTH
		WHERE
			ETP_ID = ?
			AND MONTH = ?) A
	GROUP BY
		A.USER_ID,
		A.MONTH ) ESFM ON
	T1.USER_ID = ESFM.USER_ID
LEFT JOIN (
	SELECT
		A.USER_ID,
		A.MONTH,
		CONCAT('[', GROUP_CONCAT(JSON_OBJECT('code', A.CODE, 'companyAmount', IFNULL(A.COMPANY_AMOUNT, ''), 'personAmount', IFNULL(A.PERSON_AMOUNT, ''))), ']') ITEM_VALUES
	FROM
		(
		SELECT
			USER_ID,
			CODE,
			COMPANY_AMOUNT,
			PERSON_AMOUNT,
			MONTH
		FROM
			HRBASE_UAT2.T_BILL_COMPARE_INSURANCE_TB
		WHERE
			ETP_ID = ?
			AND MONTH = ?) A
	GROUP BY
		A.USER_ID,
		A.MONTH)TBCI ON
	T1.USER_ID = TBCI.USER_ID


C2311231147301838934081353555974(String), 	(String), C2311231147301838934081353555974(String), 2024-02(String), C2311231147301838934081353555974(String), 2024-02(String), C2311231147301838934081353555974(String), 2024-02(String), C2311231147301838934081353555974(String), 2024-02(String)


在MySQL中，`CONCAT`, `GROUP_CONCAT`, 和 `JSON_OBJECT` 都是字符串处理函数，用于组合、连接和格式化数据。以下是对这三个函数的简要说明，以及它们在您提供的SQL查询中的具体作用：

1. **CONCAT()**

`CONCAT` 函数用于连接两个或多个字符串。例如，`CONCAT('Hello', ' ', 'World')` 会返回字符串 `'Hello World'`。

在您提供的查询中，`CONCAT` 函数用于将一个字符串 `'['` 和 `GROUP_CONCAT` 的结果连接起来，然后再连接一个字符串 `']'`。这是为了构建一个格式化的JSON数组字符串。
2. **GROUP_CONCAT()**

`GROUP_CONCAT` 函数用于将多行数据连接成一个字符串。它经常与 `GROUP BY` 子句一起使用，以将每个组的多行数据连接成一个字符串。

在您的查询中，`GROUP_CONCAT` 函数用于将每个 `USER_ID` 和 `MONTH` 组合的多行数据（即多个 `CODE`, `COMPANY_AMOUNT`, 和 `PERSON_AMOUNT`）连接成一个字符串。
3. **JSON_OBJECT()**

`JSON_OBJECT` 函数用于创建一个JSON对象。它接受偶数个参数，其中每对参数构成一个键值对。

在您的查询中，`JSON_OBJECT` 函数用于创建一个JSON对象，其中 `code` 是键，`A.CODE` 是值；`companyAmount` 是键，`IFNULL(A.COMPANY_AMOUNT, '')` 是值；`personAmount` 是键，`IFNULL(A.PERSON_AMOUNT, '')` 是值。这样，每个 `CODE` 和对应的 `COMPANY_AMOUNT` 和 `PERSON_AMOUNT` 都被封装成一个JSON对象。

将这些函数结合起来，您的查询将为每个 `USER_ID` 和 `MONTH` 组合生成一个JSON数组字符串，其中包含多个JSON对象，每个对象代表一个 `CODE` 和对应的 `COMPANY_AMOUNT` 和 `PERSON_AMOUNT`。

例如，如果查询结果的一个组是：


```yaml
USER_ID: 1
MONTH: 1
CODE: A
COMPANY_AMOUNT: 100
PERSON_AMOUNT: 50
CODE: B
COMPANY_AMOUNT: 200
PERSON_AMOUNT: NULL
```
那么，`GROUP_CONCAT` 和 `JSON_OBJECT` 会生成以下字符串：


```json
"[{\"code\":\"A\",\"companyAmount\":\"100\",\"personAmount\":\"50\"},{\"code\":\"B\",\"companyAmount\":\"200\",\"personAmount\":\"\"}]"
```
这个字符串是一个有效的JSON数组，其中包含两个JSON对象。

`JSON_OBJECT` 函数在 MySQL 中是在 MySQL 5.7.8 版本中引入的。从该版本开始，MySQL 提供了对 JSON 数据类型的原生支持，包括一系列用于处理 JSON 数据的函数。`JSON_OBJECT` 函数是其中之一，它允许用户轻松地创建 JSON 对象。

在 MySQL 5.7.8 及更高版本中，你可以使用 `JSON_OBJECT` 函数来构建 JSON 对象，就像你在问题中描述的那样。这为用户提供了在 SQL 查询中直接生成 JSON 数据的能力，而无需在应用程序级别进行额外的处理。


tidb oracle语法差异对照表
https://docs.pingcap.com/zh/tidb/stable/oracle-functions-to-tidb

屹tong
5.7.25-TiDB-v4.0.16

tidb解决的是容量问题

PingCAP 团队的论文《TiDB: A Raft-based HTAP Database 》入选 VLDB 2020 ，成为业界第一篇 Real-time HTAP 分布式数据库工业实现的论文。
https://blog.csdn.net/tidb_pingcap/article/details/108401113

infra底层类开源是大势所趋，除了star数，团队的布局也很厉害，无论是湾区设office，发VLDB提高reputation，用Rust写存储层做网红，D轮融资不断推进，同时做TP/AP甚至融合成一个HTAP（虽然说Hybrid现在更多是一个学术上的噱头，但是解决方案确实很新，学术上我认为是超过了Google那篇的），开源周边工具（其实这些轮子大公司都在造，但是PingCAP有开源的优势，比较新的比如TiCDC和Chaos Mesh），注重社区技术布道提升话语权和影响力，都让这个公司变得像一个综合性数据库公司。对比其他做infra开源的，你会发现PingCAP真的做得很好。甚至你以后说TiDB开始做分布式Cache或者Stream Service或者networking library我都不奇怪。更不用说中美脱钩的大环境下，保证自主知识产权的基础软件有多难得了。

硬件要求

16核心32G

https://pingcap.com/docs-cn/stable/hardware-and-software-requirements/#tidb-

TiDB 悲观锁 吴雪莲

tcc
tcc_cap
tcc_ord
tcc_red自带数据库

tidb客户端访问兼容myql协议

TiDB Slack

部署 TiDB 集群（包括 PD、TiDB、TiKV 等组件和监控组件） 

[CentOS6 x64下编译TiDB](https://www.cnblogs.com/blogzcan/p/8283883.html)

tidb耗硬件

pd（placement driver，提供时间戳服务和系统拓扑维护）

tidb 在线试用

无
## tikv
https://github.com/tikv/tikv

tidb 翼支付
https://www.infoq.cn/article/dhwGsHXsoIcsF5kPsWoO