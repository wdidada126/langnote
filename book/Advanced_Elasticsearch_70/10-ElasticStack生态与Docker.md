# Elastic Stack 生态与 Docker（原书 Ch13）

> ⚠️ 主题重构：Ch13 代码含 `docker_create_network`、`docker_pull_image`、`docker_run`、`populate_data` 四个脚本——完整的 Docker Compose 式单文件启动 Elastic Stack 全流程。软件列表：Kibana 7.0.0、Logstash、Filebeat、Docker。

## 1. Elastic Stack 组件图谱

```
Filebeat/Logstash → Elasticsearch ← Kibana
(数据采集)          (存储+搜索)     (可视化)
```

| 组件 | 角色 | 书中版本 |
|---|---|---|
| Elasticsearch | 存储/搜索/分析引擎 | 7.0.0 |
| Logstash | ETL 管道（采集→转换→输出） | 7.0.0 |
| Filebeat | 轻量日志采集器（Beats 家族） | 7.0.0 |
| Kibana | 可视化/仪表盘/Dev Tools | 7.0.0 |

## 2. Docker 部署实战

书中 Ch13 代码按四步脚本化：

1. **创建网络**：`docker network create elastic`——容器间通信隔离
2. **拉取镜像**：`docker pull docker.elastic.co/elasticsearch/elasticsearch:7.0.0`（及 Kibana/Logstash/Filebeat 对应镜像）
3. **启动容器**：`docker run -d --name es01 --net elastic -p 9200:9200 -e "discovery.type=single-node" ...`
4. **填充数据**：`populate_data` 脚本用 `curl -XPOST` 或 ES Python 客户端批量导入 ETF 样例

⚠️ 2026-09-30 本机验证：`docker pull docker.elastic.co/...` 超时不可达——ES 镜像拉取受阻。

## 3. Logstash 管道配置

```ruby
# logstash.conf ⚠️ 转述
input {
  beats { port => 5044 }
}
filter {
  grok { match => { "message" => "%{TIMESTAMP:timestamp} %{IP:clientip} %{NUMBER:response}" } }
  date { match => ["timestamp", "ISO8601"] }
}
output {
  elasticsearch { hosts => ["es01:9200"] index => "etf-logs-%{+YYYY.MM.dd}" }
}
```

- Logstash vs Ingest Pipeline（Ch9）：Logstash 适合"复杂管道+缓冲队列+多路输出"；Ingest Node 适合"ES 侧轻量富化"
- Beats 家族：Filebeat（日志）、Metricbeat（指标）、Packetbeat（网络）、Heartbeat（探活）

## 4. Kibana 可视化

- **Dev Tools Console**：最常用——替代 Postman 的 ES 请求界面
- **Discover**：交互式搜索+过滤——数据探索入口
- **Visualize / Lens**：聚合驱动的图表（柱/饼/折线/热力/地理网格）
- **Dashboard**：多图表组合+时间过滤器联动
- **Timelion**（旧）/ **TSVB**：时间序列高级表达式

书中 `business_analytics.xlsx` 暗示 Kibana 聚合结果导出到 Excel 做二次分析。

## 5. Filebeat 采集配置

```yaml
# filebeat.yml ⚠️ 转述
filebeat.inputs:
  - type: log
    paths: ["/var/log/etf/*.log"]
output.logstash:
  hosts: ["logstash:5044"]
```

- Filebeat 直连 ES 亦可（`output.elasticsearch`）——省去 Logstash 一跳
- 7.0 引入 **Modules**：Nginx/Apache/System/Audit 等预配置采集模板

## 6. 集群内互联（Docker 网络）

书中 `docker_create_network` → `docker_run` 流程：
- ES 容器 `discovery.type=single-node`（开发模式，跳过集群发现）
- Kibana 配置 `ELASTICSEARCH_HOSTS=http://es01:9200`
- Logstash/Filebeat 按 `hosts` 指向 ES 容器名——Docker 内部 DNS 解析

## 7. Docker Compose 编排示例

⚠️ 转述自书中四个 shell 脚本整合为 Compose 文件模式：

```yaml
version: "3.7"
services:
  es01:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.0.0
    environment: [discovery.type=single-node, xpack.security.enabled=false]
    ports: ["9200:9200"]
  kibana:
    image: docker.elastic.co/kibana/kibana:7.0.0
    environment: [ELASTICSEARCH_HOSTS=http://es01:9200]
    ports: ["5601:5601"]
  logstash:
    image: docker.elastic.co/logstash/logstash:7.0.0
    volumes: ["./pipeline:/usr/share/logstash/pipeline"]
```

书中用分步 shell 脚本（`docker_create_network.sh`、`docker_pull_image.sh`、`docker_run.sh`、`populate_data.sh`）教学——比 Compose 文件更透明地展示每步操作。

## 8. 🔧 类比说明

本章为生态工具链——无 FTS5 直接类比点。但：
- **Logstash ≈ SQLite shell 导入脚本**（`sqlite3 .import`）：都是"外部数据 → 转换 → 入库"管道——非 ES 行为
- **Kibana ≈ DuckDB CLI**：交互式查询+结果展示层——非 ES 行为

## 8. 本章要点

- Elastic Stack 是"搜索平台"而非单引擎——ES+Kibana+Logstash+Beats 四件套是标配
- Docker 部署大幅降低入门门槛——书中四步脚本是最佳教学范例
- Logstash 在 7.0+ 面临 Ingest Node + Elastic Agent 的竞争——角色在演进
- TDG 未覆盖 Kibana/Logstash——本章是本册的生态增值部分

## 核心概念速览（中英对照）

1. **Elastic Stack** — Elasticsearch + Kibana + Logstash + Beats 四组件生态
2. **Logstash** — ETL 管道服务器：input→filter→output 三段式
3. **Filebeat** — 轻量日志文件采集器，Go 实现，低资源占用
4. **Beats** — 采集器家族：Filebeat/Metricbeat/Packetbeat/Heartbeat
5. **Kibana** — 可视化前端：Discover/Visualize/Dashboard/Dev Tools
6. **Docker Network** — 容器间网络隔离——书中部署核心手段
7. **Grok Filter** — Logstash 正则模式提取器——非结构化日志解析
8. **Index Pattern** — Kibana 概念：将时间序列索引匹配为可视化数据源
9. **single-node** — ES 开发模式 `discovery.type=single-node`，跳过集群发现
10. **Elastic Agent** — 统一采集器（7.x 后期引入），替代 Beats + Logstash 部分角色
11. **Dev Tools Console** — Kibana 内置 ES 请求编辑器——最常用功能
12. **Time Series Visual Builder (TSVB)** — Kibana 时间序列仪表盘工具

## 最新演进与工业实践

- **8.x/9.x**：Elastic Agent + Fleet 统一采集层——Filebeat/Logstash 角色缩减；Kibana Lens 拖拽可视化成默认体验；8.0 起 ES 安全默认开启（TLS + 认证）——Docker 部署必须配证书
- **Serverless**：Elastic Cloud Serverless 形态（2024 GA）——Kibana + ES + Observability 全托管——Docker 自建部署在非合规场景减少
- **工业实践**：可观测性三支柱（Logs/Metrics/Traces）= Elastic 主打场景——OTel（OpenTelemetry）采集 + ES 存储 + Kibana 展示成 2024–2026 标准栈。书中 2019 的 Logstash → ES 管道被 Elastic Agent → ES 直连简化
- **Elastic 8.x 许可**：SSPL/Elastic License v2——Docker Hub 官方镜像受限，企业自部署需许可证。OpenSearch 分支（https://opensearch.org/ ✅ 200）提供 OpenSearch Dashboards 作为 Kibana 替代品
