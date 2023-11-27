# apifox
20231124 apifox丢数据

比postman好用

apifox，指定pqs去调用http接口

Apifox可以很容易地为你的测试生成各种不同的参数化查询字符串(PQs)。

具体操作如下:
1. 首先你需要拥有Apifox账号,然后创建一个新项目。
2. 添加需要测试的HTTP接口。Apifox支持直接输入URL或上传接口定义。
3. 然后选择要调用这个接口的测试用例。Apifox有丰富的内置测试用例,也支持自定义测试用例。
4. 在“Parameters”下,可以为这个测试用例定义多种参数,包括路径参数、查询参数、头部参数、 Body 参数等。
5. Apifox支持高级的参数化,可以为参数定义不同的分布式值。
6. 你可以指定查询字符串中的一个或多个参数需要参数化。Apifox支持多种参数类型,如整数、浮点数、字符串等。
7. 然后运行这个测试用例,Apifox就会根据你的分布式值,自动为这个接口生成大量参数化的查询字符串,并调用这个接口。
8. 你还可以指定调用频率和并发数,对接口做压力测试。
9. 测试结束后,Apifox会给你一个详细的报告,包含各种分布式值下接口的响应情况和运行指标。
10. 通过分析报告,你就可以找到接口存在的各种缺陷和问题。

举个例子,你可以为接口:

```
http://example.com/products?limit=10&category=books
```

指定`limit`参数需要参数化,为其指定1-1000的整数分布。

Apifox就会调用接口:

```
http://example.com/products?limit=1
http://example.com/products?limit=2
......
http://example.com/products?limit=1000
```

希望这对你有帮助!如有其他问题欢迎随时留言。
