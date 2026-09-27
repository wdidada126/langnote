# 04 Lucene 入门（print 第 5 章）

> 内容锚点（✅ 实抓官方仓库）：010_Intro/05_What_is_it（"Elasticsearch is an open-source search engine built on top of Apache Lucene"）、075_Inside_a_shard（"Inside a Shard"部）。本章是全书理论地基，转述 ⚠️。

## 1. Lucene 是库，ES 是服务

书中划清三层（2026 年仍然成立，✅ Lucene 官网 https://lucene.apache.org/core/ ）：

| 层 | 负责 | 不负责 |
|---|---|---|
| Lucene | 全文库：分析→倒排→打分→按位取文档 | 分布式、REST、JSON |
| ES | 分布式分片、REST、近实时、聚合 | 底层匹配算法 |
| 分析器（analyzer） | 文本→词条流（tokenizer+filters） | 存储 |

**倒排索引**的定义（书中口径）：正排"文档→词"，倒排"词→文档列表（postings）"；每个词项挂一张有序文档链表，链上可带词频 tf、位置 position、偏移 offset 等负载——**"搜索快"的一切承诺都建立在这张表上**。

🔧 类比实测（非 ES 结论，方法可复跑，脚本在 `D:\develops\tmp\dbwave_estdg\demo_inverted.py`）：SQLite 3.45 FTS5 建 10 万合成文档倒排索引 346ms 后，`MATCH 'inverted index'` 4.9ms，而普通表 `LIKE '%inverted index%'` 全扫 21.2ms；两者命中数一致（56636）。倒排"把查询变成查表"的本质在任意语言栈一致。

## 2. 一个分片 = 一个 Lucene 索引（全书最重要的等式）

书中反复使用这个等式来"翻译"概念：

- ES shard ↔ Lucene Index；ES document ↔ Lucene 32 位 int 文档号 + 存储字段；ES type(1.x) ↔ 同索引内文档前缀+字段级分区（**此映射随 type 删除而失效**，见 00 大对位表 §4-1）；
- 分析字段产生 **term dictionary + postings**；非分析字段产生 **doc_values（列式）/ 正排**；两者是"同数据双结构"，内存预算要分开算。

## 3. 段的微观生命周期（承上启下到 [05 章](05-近实时搜索.md)）

1. 文档先入 in-memory buffer；
2. 每 ~1s **refresh**：buffer 变成一个**不可变 Lucene 段**并打开 searcher → 这一刻起"可搜"（NRT 的由来）；
3. 段只增不改，删除=标记位图（live docs 前身，书中称 delete queue ⚠️ 术语以在线版为准）；
4. **merge** 把小段合成大段，顺带回收删除位图；
5. translog 在两段之间持久化以防丢数据。

书中警句："**段是 append-only 的，这就是 Lucene 并发模型简单到几乎没有锁的原因**"——与 LSM 谱系（书外对照，见 [../设计数据密集型应用/03-存储与检索.md](../设计数据密集型应用/03-存储与检索.md)）同构；本目录用 [../Database_Internals/02-B树基础.md](../Database_Internals/02-B树基础.md) 的 B 树做"可变索引 vs 不可变索引"的对照组。

## 4. 评分最小模型（为 [08 章](08-相关性实战与精确值搜索.md)埋伏笔）

书中用 5 章给出"相关性三要素"直觉：TF（词频）、IDF（稀有度）、字段长度归一（norms）——并明确"Lucene 的评分是**实用的启发式**，不是信息检索教科书的概率模型"。这句免责声明是后 10 年"相关性玄学"讨论的源头之一。

## 5. 为什么 ES 不直接用 Lucene 的全部

- Lucene 无 REST/集群/近实时运维语义；ES 补的是**"活的 Lucene"**：refresh/flush/merge 调度、translog 持久、分片再平衡时段的搬迁（书 15 章）。
- 书中展示 `GET /_cat/indices?v` 与段文件目录（一次真实分片在磁盘上的段列表，⚠️ 转述）来"看见 Lucene"。

## 5.1 一条文档的入册流水线（书中"使文本可搜"的分步拆解）

以 `{"title":"Quick brown foxes","body":"the quick brown fox jumps…"}` 索引进 title/body 为例（⚠️ 转述示意）：

1. 解析 JSON → 文档对象（[09 章](09-单节点索引与搜索.md)）；
2. 逐字段走分析器：`Quick brown foxes` → `[quick, brown, fox]`（词干化后）；
3. 每个词项查/建 term dictionary 条目；
4. 在词项的 postings 追加 `docID=新段内序号`，带 tf/position/norm 负载；
5. `_source` 原文另存一份；
6. 文档号进"新增位图"，live docs 保持全 1；
7. 上述全部发生在**内存 buffer**，refresh 时才具象为段。

> 这条链解释了本章三个"为什么"：为什么 term 精确匹配要 not_analyzed（第 2 步会改词）；为什么删除便宜（第 6 步位图）；为什么段合并会回收空间（第 4 步的 docID 只在段内有效，合并即重排）。

## 5.2 词项字典与 postings 的"书代形态"小考

- 字典：书代以 **trie（前缀树）家族**为主角——"有序 + 共享前缀 + 可前缀扫描"三性质即 10 章所有 prefix/regex 性能的来源；现代 FST 保留三性质并压缩到近磁盘；
- postings：`[3,7,8,14,…]` → delta `[3,4,1,6,…]` → 位打包——书中手算演示"100 万次 +1 增量用 1 bit 存"；
- **norm 是打分用的字段长度指纹**（存 1 字节），不是原文长度——书特意辟谣的坑；
- 位置信息：短语、邻近、高亮三者共享 positions 负载——**关 positions 省空间废短语**（现代 `_index_options` 同源 ⚠️）。

## 5.3 本章取证与边界

- ✅ "built on top of Apache Lucene"、分析器分层、段/合并/refresh/translog 叙事与 075_Inside_a_shard 部文件结构实抓自官方仓库；
- ✅ Lucene 项目主页可达：https://lucene.apache.org/core/ ；
- 🔧 FTS5/DuckDB 类比数字见 [12 章实测节](12-倒排索引数据结构.md)，仅证结构直觉不证 ES 性能；
- ⚠️ print 第 5 章正文未实抓；"rop/位图/trie→FST"的演进时间点按"书代 trie 讲解、后继 FST"弱断言，未逐一核对版本；
- ⚠️ delete queue→live docs 的术语代际按在线版口径（仓库文件 75_Inside_a_shard 部）。

## 原书要点自测（合上文件能答）

1. "一个分片 = 一个 Lucene 索引"能翻译哪些运维现象？（段数、合并、缓存、每分片文档数整型上限 ⚠️ 具体数值口径随版本有出入）
2. 倒排为什么天然有序？有序带来哪些查询红利？（跳表/前缀/归并）
3. 删除一个文档在 Lucene 层实际发生了什么？
4. refresh 与 commit 分别让什么"可见/持久"？
5. norms/positions/payloads 各服务什么特性？
6. 段不可变给并发模型省了什么？（近无锁）与 LSM 的分歧点在哪？（重写的动机：检索 vs 写放大，[../设计数据密集型应用/03-存储与检索.md](../设计数据密集型应用/03-存储与检索.md)）
7. 写出一个"看见 Lucene"的端点。（`_cat/segments`）

## 跨代误读备忘（本章专属换算清单）

1. 书中 Lucene 为 4.x；今天的 Lucene 9/10 已重写字典/ postings 编码并加入 HNSW 图索引——**"段+倒排+位图"三件套不变，其余都可能变**；
2. "ES 用 Lucene 但不用其分布式能力"一句要更新：Lucene 本身从未分布式，分布是 ES 的全部工作；分叉的 OpenSearch 同样骑在 Lucene 上（谱系见 [00 §4-20](00-总览与阅读地图.md)）；
3. 书中"delete queue"术语 → 现代 live docs/软删除（soft deletes）两代改名；
4. 书代 type→Lucene 字段前缀的映射说明（`_type` 当特殊字段索引）**整段作废**，现代一个文档就是干净的一条链；
5. 本章的"一个倒排词项挂多长链"的心算例题，量级建议 ×(10–100)：现代单索引文档数普遍远超 2014 年；
6. `norms` 在纯 keyword 时代存在感下降，但打分链里仍在（[08 章](08-相关性实战与精确值搜索.md)）。

### 本章深读互链
- 写入侧的同一套段生命周期 → [05-近实时搜索](05-近实时搜索.md)
- 数据结构细节与 🔧 类比实验 → [12-倒排索引数据结构](12-倒排索引数据结构.md)
- 不可变索引谱系（LSM 对照）→ [../设计数据密集型应用/03-存储与检索.md](../设计数据密集型应用/03-存储与检索.md)、[../cassandra实战.md](../cassandra实战.md)
- 论文/历史线 → [../../db/db.md](../../db/db.md)

## 核心概念速览（中英对照）

- **Lucene** — Lucene：Java 全文检索库；ES 的存储/匹配/打分内核
- **倒排索引** — Inverted index：词项→(docID,tf,pos…) 的有序 postings
- **词条** — Term：分析后的最小匹配单位（"running"→"run" 取决于分析链）
- **词项字典** — Term dictionary：有序词表（书时代 trie，后演化为 FST 系 ⚠️ 对位见 12 章）
- **postings 列表** — Postings list：某词项的文档链，可带 tf/位置/偏移负载
- **段** — Segment：append-only 的 Lucene 微索引；不可变是并发策略的根
- **live docs / 删除位图** — Live docs：标记删除，merge 时回收
- **merge** — Segment merging：小段合并，控段数上限换查询/索引速度
- **refresh** — Refresh：buffer→新段+开 searcher，秒级可搜
- **translog** — Transaction log：段间持久化与重放（书 5/6 章联合引入）
- **分片=Lucene 索引** — Shard as Lucene Index：全书概念翻译总枢纽
- **doc_values（前身正排）** — Forward/columnar：与倒排并存的双结构，排序/聚合用

## 最新演进与工业实践

1. **内核换代**：书时代 Lucene 4 → ES 7=Lucene 8 → ES 8=Lucene 9（块树 BP 格式）→ **ES 9=Lucene 10**（2024 末 GA，✅ 官网可达；具体小版本点 ⚠️ 未逐一核）。倒排+位图+段模型的**抽象从未变**，变的只是编码（For/PFOR/BitPack、跳表、WAND 类剪枝）。
2. **向量化是新增结构**：HNSW 图作为"段内第二索引"嵌入 Lucene 9（kNN）——2026 年 dense_vector/k-NN 是官方一等公民（✅ https://www.elastic.co/docs/solutions/search/vector/knn ）；书的词法世界观与向量世界观并存互补。
3. **概念复用范本**：中文原创的讲解（含图）见 [../从Lucene到Elasticsearch.md](../从Lucene到Elasticsearch.md)，与本目录互为中英对照（辨析见 00 §5）。
4. **跨栈类比**：段/合并→ LSM→ [../cassandra实战.md](../cassandra实战.md)、[../设计数据密集型应用/03-存储与检索.md](../设计数据密集型应用/03-存储与检索.md)；不可变文件块→ [../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)。
5. **工业实践**：读放大诊断（_cat/segments）、merge 线程池调优、以及"为什么大量更新会喂养 merge 而饿死搜索线程"等 2026 年运维帖，源头都是本章模型；书中 `refresh_interval` 的写法今天仍可在索引设置里找到（⚠️ 转述，未实测）。
