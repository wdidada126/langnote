# 文档操作 API（原书 Ch3）

> ⚠️ 主题重构：Ch3 代码目录 `document_api`，含 `acwf.json`（账户/持仓数据）与 `acwi.json` 示例。

## 1. CRUD 操作全谱

ES 文档生命周期四个核心操作：

| 操作 | 端点 | 语义 | 幂等性 |
|---|---|---|---|
| Index | `PUT /idx/_doc/1` | 创建/覆盖，指定 ID | ✅ 幂等 |
| Create | `POST /idx/_create/1` | 仅创建，已存在则 409 | 非幂等 |
| Update | `POST /idx/_update/1` | 部分更新（doc/脚本） | 非幂等 |
| Get | `GET /idx/_doc/1` | 读取 `_source` | 只读 |
| Delete | `DELETE /idx/_doc/1` | 标记删除 | ✅ 幂等 |

官方文档：https://www.elastic.co/guide/en/elasticsearch/reference/7.17/docs.html ✅ 200

## 2. 乐观并发控制（OCC）

- `if_seq_no` + `if_primary_term`：条件写入，冲突则 409
- `version_type=external`：外部版本号（如数据库时间戳），ES 信任客户端版本
- `_seq_no`（序列号）和 `_primary_term`（主代次）在 7.0 取代旧 `version` 字段作为内部 OCC

⚠️ ES 转述。7.0 的 seq_no 模型是 6.x `version` 方案的改进——与 TDG [../Elasticsearch_The_Definitive_Guide/09-单节点索引与搜索.md](../Elasticsearch_The_Definitive_Guide/09-单节点索引与搜索.md) 中 1.x 时代 `version` 字段对照阅读。

## 3. Bulk API 批量写入

```json
{"index": {"_index": "cf_etf", "_id": "SPY"}}
{"symbol":"SPY","name":"S&P 500 ETF","price":330.5}
{"index": {"_index": "cf_etf", "_id": "QQQ"}}
{"symbol":"QQQ","name":"Nasdaq ETF","price":200.1}
```

- 单个 HTTP 请求打包多条操作，`NDJSON`（`application/x-ndjson`）格式
- 默认 chunk：5MB–15MB 为最佳吞吐区间（官方建议）
- 每条操作独立执行——Bulk 不提供原子性保证

官方文档：https://www.elastic.co/guide/en/elasticsearch/reference/7.17/docs-bulk.html（⚠️ 推定 URL，7.17 未验证路径）

## 4. Update by Query 与 Delete by Query

- `POST /idx/_update_by_query` + `POST /idx/_delete_by_query`
- 本质：scroll 读取 → 逐条执行 → 可能产生 `version_conflicts` 参数处理
- 7.0 引入 `conflicts=proceed` 跳过冲突文档继续执行

官方文档：https://www.elastic.co/guide/en/elasticsearch/reference/7.17/docs-update-by-query.html ✅ 200；https://www.elastic.co/guide/en/elasticsearch/reference/7.17/docs-delete-by-query.html ✅ 200

## 5. MGET / 多文档读取

`POST /_mget` 一次取多个文档（跨索引亦可）：
```json
{"docs":[{"_index":"cf_etf","_id":"SPY"},{"_index":"cf_etf","_id":"QQQ"}]}
```

`mget` 比多次 `get` 高效：单次 HTTP 请求 → 协调节点并行分发到各分片 → 归并结果。但注意：若文档在不同分片上，协调节点仍需多路 fan-out——网络 RTT 决定延迟下界。

## 6. GET 读一致性语义

ES 7.0 的 `GET /idx/_doc/1` **不保证强一致**（与 TDG 时代口径一致）：
- 默认经协调节点轮询分片——可能读到未刷新的内存 buffer 之外的数据
- `preference=_primary`：强制读主分片——一致性最强但负载不均
- `realtime=true`（默认）：GET 读 translog 保证 NRT 语义——与 `_search` 的"仅搜已刷新段"不同

⚠️ ES 转述。官方文档：https://www.elastic.co/guide/en/elasticsearch/reference/7.17/docs.html ✅ 200

## 8. 🔧 类比演示（非 ES 行为）

**G4：FTS5 rebuild ≈ ES reindex 类比**（SQLite 3.45.3）

```python
conn.execute("CREATE VIRTUAL TABLE old_idx USING fts5(name, text)")
for i in range(300):
    conn.execute("INSERT INTO old_idx VALUES(?,?)", (f"doc{i}", f"legacy content about search {i}"))
# 300 行 rebuild：0.34ms — 类比 ES 小索引 _reindex 操作
conn.execute("INSERT INTO old_idx(old_idx) VALUES('rebuild')")
# 验证 rebuild 后仍可搜索
r = conn.execute("SELECT count(*) FROM old_idx WHERE old_idx MATCH 'search'").fetchone()  # 300
```

- FTS5 `rebuild` 重建倒排索引——类比 ES `_reindex`（源索引→目标索引全量重写）
- ES reindex 涉及：新主分片分配、版本递增、别名切换；FTS5 rebuild 仅重建 B-tree 索引——**机制根本不同，非 ES 行为**

## 9. 写入路径内部机制

```
HTTP PUT/POST → Coordinating Node → Primary Shard
                                       ↓
                               Index Buffer (in-memory segment)
                                       ↓ (每 5s 或 buffer 满)
                               Disk Segment (Lucene, 不可变)
                                       ↑
                               Translog (持久化日志, 每写 fsync)
                                       ↓ (commit, 默认 30min)
                               Disk Segment (searchable)
```

- `refresh`（默认 1s）：将 in-memory buffer → 新段 → 打开 searcher → 可搜
- `flush`：translog 清空 + 段落盘 commit——重启不丢
- `fsync`：translog 每次写同步到磁盘——ES 7.0 默认 `index.translog.durability=request`（每请求 fsync）

⚠️ ES 集群行为转述；与 TDG [../Elasticsearch_The_Definitive_Guide/05-近实时搜索.md](../Elasticsearch_The_Definitive_Guide/05-近实时搜索.md) 对照——概念一致，7.0 参数名微调。

## 10. 本章要点

- 文档 API 是 ES 最基础操作层——应用开发日常 80% 在此
- OCC 的 seq_no/primary_term 模型与 TDG 时代 version 字段对比——7.0 改进
- Bulk API 是性能关键：单条 vs Bulk 差 10x+ 吞吐
- reindex 是运维日常（mapping 变更、分片数变更触发）
- `_source` 关闭（`enabled:false`）省磁盘——但 update/reindex/script 依赖它，需权衡

## 核心概念速览（中英对照）

1. **文档** — Document：ES 最小存储单元，JSON 格式，等同于关系数据库的行
2. **Index API** — 创建/覆盖文档，指定 `_id` 或自动生成
3. **乐观并发控制** — OCC (Optimistic Concurrency Control)：`_seq_no` + `_primary_term` 检测冲突
4. **Bulk API** — 批量 NDJSON 提交，提升写入吞吐
5. **_source** — 文档原始 JSON，7.0 默认常开，更新/搜索脚本可访问
6. **translog** — Transaction Log：持久化写入日志，防止段未 flush 前丢失
7. **Update by Query** — 按查询条件批量更新，内部 scroll+index
8. **Delete by Query** — 按查询条件批量删除，7.0 引入 conflicts=proceed
9. **MGET** — Multi-get：一次读取多个文档
10. **Reindex** — 从源索引全量拷贝到目标索引，常因 mapping/shard 变更触发
11. **refresh_interval** — 写入到可搜的间隔（默认 1s），影响 NRT 语义
12. **NDJSON** — Newline-Delimited JSON：Bulk API 请求体格式

## 最新演进与工业实践

- **ES 8.x/9.x**：Update by Query / Delete by Query 保留，但官方推荐 **reindex + 别名切换** 做大规模变更——避免协调节点内存压力。delete-by-query 操作 API：https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-delete-by-query ✅ 200
- **ES|QL（9.0 GA）**：管道式 `FROM idx | WHERE ... | KEEP ...` 查询语言（https://www.elastic.co/docs/reference/query-languages/esql ✅ 200），但文档操作仍走 REST API
- **Serverless 形态**：Elastic Cloud Serverless 自动管理 reindex/shard split（2024 GA）——本书 7.0 时代的"手工 reindex"运维技能在 Serverless 下大幅简化
- **社区实践**：Bulk 最佳实践（5–15MB 分块、refresh_interval=-1 导入期关闭）在 ES 9.x 仍适用；`_source` 可关闭（`enabled:false`）省磁盘——但 update 和 reindex 依赖 `_source`，需权衡
- **7.0 → 8.x 断点**：`_doc` 替代 `/{index}/{type}` 路径——全书 API 示例的 URL 翻译入口；`version_type=external` 语义微调（外部版本号类型约束更严格）
- **Update by Query 改进**：8.x 引入 `search_slice` 参数——支持切片并行执行 ubq；`requests_per_second` 参数限流——书中简单版需升级为生产安全版
