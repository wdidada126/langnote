# elasticsearch

# 🔥 终极答案：完全可以！而且 90% 场景能直接解决 MySQL JOIN 慢到爆的问题！
我给你用最直白、最实战、你现在就能用的方式讲清楚：

---

# 一、先给你结论（非常重要）
## MySQL 多表 JOIN 慢 = 100% 可以用 ES 解决！
## ES 天生就是为了替代复杂 JOIN、海量数据快速查询而生的！

### 为什么 MySQL JOIN 慢？
- 3张表以上 JOIN → 指数级变慢
- 大数据量（10万以上）→ 直接卡死
- 关联条件复杂 → 优化到死也快不起来
- 模糊查询、多条件组合、排序、分页一起上 → 直接超时

### 为什么 ES 能解决？
ES 不支持 JOIN，但它不需要 JOIN！
ES 存的是 宽表（大文档）
把 MySQL 多张表的数据 合并成一个文档
查的时候 一次查询、0 关联、毫秒级返回

---

# 二、最直白的对比（一看就懂）
## MySQL（你现在的痛点）
```sql
SELECT * FROM order
JOIN user ON order.user_id = user.id
JOIN product ON order.product_id = product.id
JOIN logistics ON order.logistics_id = logistics.id
WHERE order.create_time between ? and ?
AND user.age > 18
AND product.price > 100
ORDER BY order.create_time DESC
LIMIT 100
```
> 4张表JOIN！数据量大一点 → 直接几秒~几十秒！

---

## ES（终极解决方案）
只存 1个索引（相当于1张宽表）
```json
{
  "order_id": 1001,
  "create_time": "2025-01-01",
  "user_id": 100,
  "user_name": "张三",
  "user_age": 25,        ← user表字段
  "product_id": 123,
  "product_name": "手机",
  "product_price": 1999, ← product表字段
  "logistics_no": "SF123",
  "status": "已发货"     ← logistics表字段
}
```

### 查询时
不需要 JOIN！不需要关联！
直接多条件组合查询：
```json
GET /order_index/_search
{
  "query": {
    "bool": {
      "must": [
        { "range": { "create_time": { "gte": "2025-01-01" }}},
        { "range": { "user_age": { "gt": 18 }}},
        { "range": { "product_price": { "gt": 100 }}}
      ]
    }
  },
  "sort": [{ "create_time": "desc" }]
}
```

### 结果
百万、千万数据 → 10 ~ 500 毫秒返回！

# 三、你最关心的 3 个问题
## 1. 什么场景适合从 MySQL 转 ES？
多表关联查询（2张表以上）
查询条件多（组合条件、范围、模糊）
需要排序、分页、统计
数据量大（10万以上）
读多写少（查询多，修改少）
你的银行、订单、用户、风控系统 全部适合！

## 2. 什么场景不适合？
❌ 需要强事务（转账、支付）
❌ 高频实时修改
❌ 数据强一致性要求极高

## 3. 架构怎么做？（最简单方案）
```
MySQL（负责写入、事务、主数据）
  ↓
同步工具（canal / datax / logstash / 代码双写）
  ↓
ES（负责所有复杂查询、列表、搜索、统计）
```

业务接口 → 直接查 ES，不查 MySQL

---

# 四、你的银行示例（完美演示）
## MySQL 里是这样的（3张表）
- user（用户）
- account（账户）
- bank_card（银行卡）

## 查询需要：
```
user JOIN account JOIN bank_card
```
数据量大必然慢！

## ES 里只需要：
一个索引 `bank_user_index`
把三张表字段全部放进去
```json
{
  "user_id": 1,
  "name": "张三",
  "age": 30,
  "account_no": "622202123456",
  "balance": 10000,
  "card_no": "438923729233",
  "city": "北京",
  "state": "BJ"
}
```

查询 0 JOIN，速度提升 10~100 倍！

# 五、最终结论（你可以直接记）
## MySQL 负责：存、写、事务
## ES 负责：查、复杂条件、多表聚合、大数量快速查询

## 多表 JOIN 慢？
## 答案：能！换成 ES 绝对能解决！

如果你愿意，我可以直接给你：
# 【你的业务表 → ES 宽表设计方案】
比如你现在的
- order
- user
- product
- bank

我可以直接帮你设计 最佳 ES mapping 结构
让你 MySQL 多表 JOIN 问题彻底消失！

## ubuntu 24 apt安装

# WSL Ubuntu 安装 Elasticsearch 8.19.14 可执行命令清单
# 适用目标：本地学习、单机、无鉴权联调
# 时间说明：Elastic 官方在 2026-04-08 发布了 8.19.14

# 1. 安装基础工具
sudo apt update
sudo apt install -y curl wget gnupg apt-transport-https ca-certificates

# 2. 导入 Elastic 官方 GPG Key
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg

# 3. 添加 Elastic 8.x APT 仓库
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list

# 4. 安装 Elasticsearch
sudo apt update
sudo apt install -y elasticsearch

# 5. 查看已安装版本
/usr/share/elasticsearch/bin/elasticsearch --version

# 6. 备份配置
sudo cp /etc/elasticsearch/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml.bak

# 7. 写入单机学习配置
sudo tee /etc/elasticsearch/elasticsearch.yml > /dev/null <<'EOF'
cluster.name: es-demo-cluster
node.name: es-demo-node-1
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
network.host: 0.0.0.0
http.port: 9200
discovery.type: single-node
xpack.security.enabled: false
xpack.security.enrollment.enabled: false
EOF

# 8. 设置 Linux 内核参数
echo "vm.max_map_count=262144" | sudo tee /etc/sysctl.d/99-elasticsearch.conf
sudo sysctl --system

# 9. 设置开机自启并启动 ES
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch.service
sudo systemctl restart elasticsearch.service

# 10. 查看状态
sudo systemctl status elasticsearch.service --no-pager

# 11. 查看日志
sudo journalctl -u elasticsearch.service -n 100 --no-pager

# 12. 本机健康检查
curl http://127.0.0.1:9200
curl http://127.0.0.1:9200/_cluster/health?pretty

# 13. 如果你想严格手工安装 8.19.14，也可以用下面这组命令
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.19.14-amd64.deb
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.19.14-amd64.deb.sha512
shasum -a 512 -c elasticsearch-8.19.14-amd64.deb.sha512
sudo dpkg -i elasticsearch-8.19.14-amd64.deb

# 14. Windows 侧验证能否访问 WSL 中的 ES
# 在 Windows PowerShell 执行
# curl http://127.0.0.1:9200


curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch \
  | gpg --dearmor \
  | sudo tee /usr/share/keyrings/elasticsearch-keyring.gpg >/dev/null

echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" \
  | sudo tee /etc/apt/sources.list.d/elastic-8.x.list

sudo apt update
sudo apt install -y elasticsearch

sudo systemctl enable elasticsearch
sudo systemctl start elasticsearch

基于ElasticSearch大宽表存储关键业务数据

## windows操作系统IDEA调试代码
注意下载的jdk是linux操作系统的，坑

https://mirrors.tuna.tsinghua.edu.cn/AdoptOpenJDK/ 404

https://mirrors.huaweicloud.com/elasticsearch/

https://jdk.java.net/archive/

https://www.jianshu.com/p/d218613cbe21
命令行编译
./gradlew localDistro

https://blog.51cto.com/u_15812686/5738580

1、idea导入Elasticsearch 7.10.2源码和编译运行，https://copyfuture.com/blogs-details/20210327133933335M
2、在Windows环境IDEA下编译运行Elasticsearch 7.14.1，https://blog.csdn.net/weixin_43820556/article/details/120165948
3、IDEA 编译 ElasticSearch 7.8.1，https://blog.csdn.net/ShelleyLittlehero/article/details/107642951
4、ElasticSearch-7.8.0 源码编译调试 (详细)，https://zhuanlan.zhihu.com/p/188725714
5、idea源码调试的问题，https://elasticsearch.cn/question/8243

## 架构图
Elasticsearch分布式搜索引擎的总体框架图.png

https://github.com/edidada/elasticsearch-full

## 数据类型
https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html#_multi_fields_2
常用数据类型：
text、keyword、number、array、range、boolean、date、geo_point、ip、nested、object

ElasticSearch基本概念_-yanqi_vip-博客园.mhtml

## 竞品Splunk
Splunk 是一款顶级的日志分析软件,如果你经常用 grep、awk、sed、sort、uniq、tail、head 来分析日志,那么你需要 Splunk。能处理常规的日志格式,比如 apache、squid、系统日志、mail.log 这些

## 讨论组、社区

https://discuss.elastic.co/t/announce-mailing-list/19899

## Slack
https://elasticstack.slack.com/

## 官方文档
doc文档
https://www.elastic.co/guide/en/elasticsearch/reference/6.2/index.html
https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html
es文档
https://www.elastic.co/guide/en/elasticsearch/reference/7.17/index.html

## analysis-ik分词器

ik版本必须跟es版本一致

./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v2.3.0/elasticsearch-analysis-ik-2.3.0.zip

https://github.com/medcl/elasticsearch-analysis-ik/releases?page=14

https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.9.2/elasticsearch-analysis-ik-7.9.2.zip

## 应用场景
应用程序搜索
网站搜索
企业搜索
日志处理和分析
基础设施指标和容器监测
应用程序性能监测
地理空间数据分析和可视化
安全分析
业务分析

## 核心概念

index 索引
ideices

文档 document

item

_doc 从6.x开始es慢慢放弃type，并统一默认type为_doc

_type

_search

restful api
java api

PUT
POST

NRT
Near Realtime，近实时，有两个层面的含义，一是从写入一条数据到这条数据可以被搜索，有一段非常小的延迟（大约1秒左右），二是基于Elasticsearch的搜索和分析操作，耗时可以达到秒级。

https://zhuanlan.zhihu.com/p/646455006

Node单独一个Elasticsearch服务器实例称为一个node，node是集群的一部分，每个node有独立的名称，默认是启动时获取一个UUID作为名称，也可以自行配置，node名称特别重要，Elasticsearch集群是通过node名称进行管理和通信的，一个node只能加入一个Elasticsearch集群当中，集群提供完整的数据存储，索引和搜索的功能，它下面的每个node分摊上述功能（每条数据都会索引到node上）。shard分片，是单个Lucene索引，由于单台机器的存储容量是有限的（如1TB），而Elasticsearch索引的数据可能特别大（PB级别，并且30GB/天的写入量），单台机器无法存储全部数据，就需要将索引中的数据切分为多个shard，分布在多台服务器上存储。利用shard可以很好地进行横向扩展，存储更多数据，让搜索和分析等操作分布到多台服务器上去执行，提升集群整体的吞吐量和性能。shard在使用时比较简单，只需要在创建索引时指定shard的数量即可，剩下的都交给Elasticsearch来完成，只是创建索引时一旦指定shard数量，后期就不能再更改了。replica索引副本，完全拷贝shard的内容，shard与replica的关系可以是一对多，同一个shard可以有一个或多个replica，并且同一个shard下的replica数据完全一样，replica作为shard的数据拷贝，承担以下三个任务：shard故障或宕机时，其中一个replica可以升级成shard。replica保证数据不丢失（冗余机制），保证高可用。replica可以分担搜索请求，提升整个集群的吞吐量和性能。shard的全称叫primary shard，replica全称叫replica shard，primary shard数量在创建索引时指定，后期不能修改，replica shard后期可以修改。默认每个索引的primary shard值为5，replica shard值为1，含义是5个primary shard，5个replica shard，共10个shard。因此Elasticsearch最小的高可用配置是2台服务器。

## 查询
其中查询支持多种类型的复杂查询，如match解析查询、排序查询、分页查询、bool查询、fileter查询、多关键字查询、term精确查询、高亮查询

ElasticSearch使用倒排索引与Term Index来提高搜索效率，减少磁盘I/O。
ElasticSearch使用Skip List和Roaring Bitset来合并复杂条件查询的结果集。
https://zhuanlan.zhihu.com/p/646462877
## 客户端
Java High Level REST Client


{
  "_index": "test_index",
  "_type": "test_type",
  "_id": "1",
  "_version": 1,
  "found": true,
  "_source": {
    "test_content": "test test"
  }
}

https://zhuanlan.zhihu.com/p/646647762

_id mysql中存在的唯一id，可以手动指定

## 学习资料
b站 
## books 书籍


Elasticsearch 技术解析与实战 作者: 朱林

[Elasticsearch源码解析与优化实战](https://book.douban.com/subject/30386800/)
张超 / 电子工业出版社 / 2019-1 /

[Elasticsearch实战与原理解析](https://book.douban.com/subject/35001679/)
牛冬 / 电子工业出版社 / 2020-3

[Elasticsearch搜索引擎构建入门与实战](https://book.douban.com/subject/35658411/)
高印会 / 机械工业出版社 / 2021-10

[Elasticsearch全面解析与实践](https://book.douban.com/subject/35702743/)
张文亮 / 机械工业出版社 / 2021-12-14 / 79.00

## Rust写的竞品 meilisearch
全文搜索

倒排索引

elasticsearch

https://book.douban.com/subject/25868239/

es其分布式设计理念和其他分布式Nosql数据库的设计理念都差不多
nosql

搜索，es

wukong搜索

订单表 优化

一共有20个field，分布在5个表中，现在要查询出完整的订单信息，如何做到接近实时查询

大公司的思路用ES建立索引，查询ES

例如，广州机房到北京机房，正常情况下 RTT 大约是 50 毫秒左右，遇到网络波动之类的情况，RTT 可能飙升到 500 毫秒甚至 1 秒，更不用说经常发生的线路丢包问题，那延迟可能就是几秒几十秒了。

nosql


## 源代码

### java doc
https://javadoc.io/doc/org.elasticsearch/elasticsearch/latest/index.html

elasticsearch-7.17.13-javadoc.jar

https://javadoc.io/doc/org.elasticsearch/elasticsearch/7.17.13/index.html

github.com/elastic/elasticsearch
gradle组织的

```powshell
$env:JAVA_HOME = "D:\Java\jdk-13.0.2+8"
$env:Path = "D:\Java\jdk-13.0.2+8\bin;$env:Path"
.\bin\elasticsearch.bat
.\gradlew.bat build
```

## Windows电脑安装启动Elasticsearch

windows电脑安装了

cd D:\dev_tools\elasticsearch-7.3.2
$env:JAVA_HOME = "D:\dev_tools\elasticsearch-7.3.2\jdk"
$env:Path = "D:\dev_tools\elasticsearch-7.3.2\jdk\bin;$env:Path"
.\bin\elasticsearch.bat
D:\dev_tools\elasticsearch-7.3.2\bin\elasticsearch.bat

需要java11

往索引里面插入数据 报错
{
    "error": {
        "root_cause": [
            {
                "type": "cluster_block_exception",
                "reason": "index [json_index] blocked by: [FORBIDDEN/12/index read-only / allow delete (api)];"
            }
        ],
        "type": "cluster_block_exception",
        "reason": "index [json_index] blocked by: [FORBIDDEN/12/index read-only / allow delete (api)];"
    },
    "status": 403
}
当Elasticsearch检测到磁盘空间不足时，也会进入read-only mode。
https://www.elastic.co/cn/downloads/past-releases
https://www.elastic.co/cn/downloads/past-releases/elasticsearch-7-3-2

你遇到的问题与Elasticsearch相关。错误信息“index [json_index] blocked by: [FORBIDDEN/12/index read-only / allow delete (api)]”表明你试图在Elasticsearch中创建名为"json_index"的索引，但系统当前处于只读模式，不能执行写操作。

Elasticsearch有一个内置的read-only mode，它会在以下情况下触发：
默认情况下，Elasticsearch启动时会进入read-only mode，这是为了防止在启动过程中进行写操作导致数据不一致。
当你进行一些特定操作，如删除所有索引、关闭所有节点、或者执行一些可能破坏数据的操作时，Elasticsearch会进入read-only mode。
当Elasticsearch检测到磁盘空间不足时，也会进入read-only mode。
要解决这个问题，你可以采取以下几种方法：

等待一段时间后再次尝试。Elasticsearch在启动后会自动退出read-only mode。
如果你需要立即进行写操作，可以尝试关闭Elasticsearch，然后重新启动。但请注意，这可能会导致数据丢失或损坏，所以只有在你确定这样做不会导致问题的情况下才应该这样做。
如果是因为磁盘空间不足导致的read-only mode，你可以清理一些空间后再次尝试。
如果这些方法都不能解决问题，可能需要检查你的Elasticsearch配置，或者考虑增加磁盘空间。
希望这些信息能帮助你解决问题。如果你还有其他问题，欢迎随时提问。



http://127.0.0.1:9200/

http://127.0.0.1:9200/

{
  "name" : "DESKTOP-DAF8ST0",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "IgkMeZyXQk2bmv4wbvgNpg",
  "version" : {
    "number" : "7.3.2",
    "build_flavor" : "default",
    "build_type" : "zip",
    "build_hash" : "1c1faf1",
    "build_date" : "2019-09-06T14:40:30.409026Z",
    "build_snapshot" : false,
    "lucene_version" : "8.1.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}

https://blog.csdn.net/qq_34383510/article/details/128132503



db-engines

search engine中排名



https://db-engines.com/en/ranking/search+engine



## Elasticsearch课程
Elasticsearch 核心技术与实战

https://time.geekbang.org/course/intro/100030501



快速构建分布式搜索和分析引擎

阮一鸣  eBay Pronto 平台技术负责人

Pronto 平台目前管理了 eBay 内部上百个 Elasticsearch 集群，包含了 4000 多个数据节点。这些集群目前被广泛使用在 eBay 的生产环境之中。涵盖了网站搜索，商品推荐，日志管理，风险控制，IT 运维，安全监控等多个领域。



![es学习路线](imgs/es_study.jpg)
