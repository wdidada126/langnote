# 02 高级搜索与查询 DSL（print 第 3 章）

> 内容锚点（✅ 实抓官方仓库）：在线版 054_Query_DSL「Query DSL」、060_Distributed_Search「Distributed Search Execution」、056_Sorting。以下均为 1.x 口径转述 ⚠️，现代替代逐节标注。

## 1. 全书最重要的一次概念切分：查询 vs 过滤

书中把 1.x 的 DSL 归纳为两种节点：

| | Query clause（查询从句） | Filter clause（过滤从句） |
|---|---|---|
| 回答 | 匹配度多少？（相关性评分） | 是否匹配？（二值） |
| 缓存 | 不缓存 | **可缓存**（filter cache） |
| 例子 | full text、函数评分、模糊/邻近 | 范围、term、前缀、exists |

1.x 的语法壳是 `filtered` query（书示范 `{"filtered":{"query":…,"filter":…}}`，还教了 `and/or/not` 组合多个 filtered）——**这个壳 5.0 即删除**。但其"评分/过滤分离"思想原封不动搬进了今天 `bool` 的 `must/should/filter/must_not` 四件套（✅ 现文档 Query DSL 总览：https://www.elastic.co/docs/explore-analyze/query-filter/languages/querydsl ）。书中那句"能用 filter 就别用 query"是**全书第一条性能军规**。

## 2. 全文查询工具箱（print 第 3 章主体）

1.x 口径逐一列出（现代同名可用者多，改名/删除者标注）：

- `match` 家族（match/bool_prefix/phrase/phrase_prefix/match_all）— **现代健在**，书里"match 会先过分析器"的一句是全书被引用最多的排错提示（match 一个 keyword 字段会因分析差异"查不到"）。
- `multi_match`（best_fields / most_fields / cross_fields）— **健在**，书中对 `_all` 的"手工最佳字段 vs 自动 _all"比较随 `_all` 一起失效（替代见 [11 章](11-映射与索引的本质.md)）。
- `query_string` / `simple_query_string` — 健在，书中定位为"给终端用户留的逃生舱"。
- `term` / `range` — 健在，但书中"对分析字段用 term 会怎样"警告升级为现代的"text 字段 term 查询命中倒排词条本身"这一固定坑。
- `span` 家族 — 健在（1.x 尚简陋，书未深入）。
- `more_like_this`、`percolator`（1.x 一代：注册查询、反查文档）— **percolator 在 2.0 重写、5.0 再重写**为"inverted-index percolator"，书中"文档查询翻转"的教学价值保留，配置全变 ⚠️。
- `geo_shape`/`geo_bbox` 1.x 语法 — 已换代，见 [08 章](08-相关性实战与精确值搜索.md)语言处理外的地理内容（本目录未设地理章文件，见 00 映射表说明：在线版地理部内容并入本文件概念层）。

## 3. 复合查询与"布尔=缓存"的工程观

书中讲法（转述，⚠️）：`bool` 的四段 `must/should/must_not/filter`；filter 结果在 1.x 用 RoaringBitmap（**书中用 "rop" 即 roaring bitmap 前史讲法，实际 1.x 已引入**——此句以仓库口径为准 ⚠️ 版本点未逐一核）。要点：
1. 嵌套 bool 的语义：should 在 filter 语境下默认 `minimum_should_match=0`——**这条规则 2026 年仍成立**，书中用整页讲"为什么我的 bool 一个都没过滤掉"。
2. 过滤缓存的失效粒度是"段"级，故 filter 结果集越稳定越划算（"时间窗口别用 now-1m"的现代告诫与此同源）。
3. 1.x 的"或=并集、与=交集"在位图层的代价解释，对照本目录 [12-倒排索引数据结构](12-倒排索引数据结构.md)。

## 4. 分布式搜索执行（print 第 3 章的"inside out"前奏）

1.x `search_type` 三选项（**现代仅剩前两，scan 删除**）：
- `query_then_fetch`（默认）：每分片各算局部 top-N → 协调节点归并。书中公式"召回正确性随 from 深度恶化"由此而来；`dfs_query_then_fetch` 两阶段修正评分，代价多一次网络往返——**现代仍存在同名选项**。
- 1.x 的 `scan` 深遍历 → 书教 scroll；现代栈见 [05 章](05-近实时搜索.md)演进节。

## 5. 高亮、建议器与"搜索体验件"

书中第 3 章尾部覆盖：`highlight`（词频/片段拼接原理）、search-as-you-type（edge_ngram 索引时方案 + completion suggester）、did-you-mean（term suggester + 词典）。教学骨架 2026 年仍成立，仅 suggester 在云产品里逐渐让位于 learning-to-rank/语义重排（⚠️ 转述官方文档，未实测）。

## 5.1 facets 专节（print 第 3 章的"另一半天"，3.0 起全灭 ⚠️）

print 版的高级搜索统计仍主用 facets，三类必须认识（读老代码/老帖会撞上）：

- `terms_facet`：词项频次表——"terms 聚合的史前形态"；
- `query_facet`：**把每个查询变成一个桶**（"facet 即查询"），filters 聚合的精神祖先；
- `date_range_facet`/`histogram_facet`：数值分桶，range/date_histogram 的前身。

facets 之死的三条理由（书在线版 301 节总结 ✅ 实抓文件存在）：
1. 挂在独立的 `facets` 请求区，与查询体语法分裂；
2. **不能嵌套**——多维分析直接残废；
3. 实现走的是与查询共用的打分路径，慢且不可组合。

> 本目录把 facets 记作"聚合章的考古层"：读 print 第 4 章时见 [03-聚合](03-聚合.md) §1。

## 5.2 高亮与建议器细节（书代配方）

- `highlight`：`pre_tags/post_tags`、`fragment_size`、`number_of_fragments`、`require_field_match=false`（跨字段高亮）——现代参数同名（⚠️ 转述）；
- 高亮的两条路线：**analyze 现取词位**（默认）vs **require_field_match+offsets 存储**（更准更贵）——这是 [11 章](11-映射与索引的本质.md)类型选择的实例；
- search-as-you-type 配方（书代）：`edge_ngram` 索引分析器 + `keyword` 查询分析器——**非对称分析器**第一教案，完整版见 [07 章](07-词项分析与语言处理.md)；
- did-you-mean 配方：`term_suggester`（词典来自倒排词项+编辑距离）+ 业务词典 `input` 权重 → completion suggester（前缀 FST）。

## 5.3 本章取证与边界

- ✅ 章文件与章名（054_Query_DSL、060_Distributed_Search、056_Sorting、080/100/110/120/130/170 系）实抓官方仓库 1.x 分支 include 清单；
- ⚠️ print 第 3 章正文未实抓；本文件主题按在线版同内容体系重构；
- ⚠️ Roaring 位图进入 ES 的确切小版本未逐一核，仅给"书代已开始位图化"的弱断言；
- ⚠️ span/percolator/geoshape 的 1.x→现代语法差异按"概念存续、配置重写"口径转述，未实测；
- 已验证引用：Query DSL 总览 https://www.elastic.co/docs/explore-analyze/query-filter/languages/querydsl 、深分页 PIT https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-open-point-in-time 。

## 原书要点自测（合上文件能答）

1. 为什么 filter 上下文默认不打分？（二值+可缓存+短路）
2. `should` 在纯 filter 语境下为什么"全过"？——minimum_should_match 默认值题
3. match 一个 keyword 字段会怎样？反过来 term 一个 text 呢？（两侧分析不对称事故）
4. query_then_fetch 与 dfs_query_then_fetch 的往返次数与正确性差异？
5. facets 三条死因各对应今天哪个聚合特性？
6. filtered query 的等价现代写法？（bool.filter + must）
7. scroll 为什么"给 UI 翻页"是错的？（快照语义+深分页不变，[06 章](06-搜索内览.md)）

## 跨代误读备忘（本章专属换算清单）

1. `{"filtered":{...}}`、`{"and":{...}}`、`{"or":{...}}`、`{"not":{...}}`、顶层 `fquery` ——五个语法化石，现代一律 `bool` 四件套；
2. 书中 filter 写法的 `"cache":{...}` 参数与"每 filter 单独缓存"心智：现代 filter 上下文自动缓存、粒度=段，**手工 cache 参数已消失**；
3. 书中 `text` 查询（全文多词自动 bool）与 `match` 的代际纠缠：2.x 合并为 match 系，遇到 `text` 直读 `match` ⚠️；
4. facets 请求块（`"facets":{}`）出现在 print 示例里——一律翻译成顶层 `"aggs"` 再读；
5. `more_like_this` 书代靠 `like_field` 配置，现代以 `mlt`+多字段/向量替代，语义相近参数全换；
6. 在线版已见的 percolate 注册格式（1.x 文档式查询注册）**不是**现代格式——现代 percolator 是"query 存进 `percolator_query` 类型字段"（⚠️ 转述），读本章配 percolator 例子时直接看新文档。

### 本章深读互链
- 位图与集合运算的成本底层 → [12-倒排索引数据结构](12-倒排索引数据结构.md)
- 打分与降权实战 → [08-相关性实战与精确值搜索](08-相关性实战与精确值搜索.md)
- SQL 侧对照（谓词下推/缓存的类比）→ [../高性能mysql.md](../高性能mysql.md)
- 检索语言通论 → [../设计数据密集型应用/02-数据模型与查询语言.md](../设计数据密集型应用/02-数据模型与查询语言.md)

## 核心概念速览（中英对照）

- **查询 DSL** — Query DSL：JSON 声明式检索语言，书的核心语法层（现代健在）
- **查询/过滤二分** — Query vs Filter：打分 vs 二值+缓存；演化为 bool 四件套
- **bool 复合查询** — Boolean query：must/should/must_not/filter 组合
- **minimum_should_match** — 最少匹配数：should 语义的开关，书中大坑
- **filtered query** — Filtered query：1.x 的"查询+过滤"壳，**5.0 已删** ⚠️
- **match 会分析** — Match analyzes：全文查询先过分析器再查倒排
- **multi_match** — Multi-match：best_fields/most_fields/cross_fields 三种字段策略（健在）
- **span 邻近查询** — Span queries：位置约束匹配（书浅讲，现代丰富）
- **percolator 一代** — Percolate v1：反转为"文档流查询"，已两度重写 ⚠️
- **search_type** — Search type：query_then_fetch / dfs_ 两阶段修正评分
- **段级过滤缓存** — Per-segment filter cache：位图缓存，稳定谓词才值钱
- **高亮** — Highlighting：基于词位与片段评分的后处理
- **补全建议器** — Completion suggester：专字段+前缀 FST，书时代前沿件

## 最新演进与工业实践

1. **删除的壳，保留的魂**：`filtered/and/or/not` 全删，等价写法是 `bool.filter`；书中"评分与过滤分离"的教学反而因 8.x Query Rules、ES|QL 的 `WHERE`（https://www.elastic.co/docs/reference/query-languages/esql ✅）而成为通用直觉。
2. **深分页三件套**（现代标准答案，✅ 文档可达）：scroll（导出）、**PIT + search_after**（https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-open-point-in-time ✅）、ES|QL cursor——1.x 的"search_type 选型"题变成"按场景选游标"。
3. **重新索引与别名**：书里 reindex 靠插件/logstash（⚠️），现代有原生 `_reindex`（https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex ✅）；1.x 的 update-mapping 限制（改 analyzer 必须重建）今天依旧成立。
4. **k-NN 与混合检索**：2026 的"高级查询"清单加了 `knn` 子句、RRF 混合（向量+词法）与 `semantic_text` 检索（https://www.elastic.co/docs/solutions/search/vector/knn 、https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/semantic-text ✅）——它们仍挂在同一套 bool 语法上，书中 DSL 骨架没白学。
5. **对照阅读**：过滤位图/跳表代价 → 本目录 [12-倒排索引数据结构](12-倒排索引数据结构.md)；排序与 fielddata → [06-搜索内览](06-搜索内览.md)；DDIA 视角的检索层 → [../设计数据密集型应用/03-存储与检索.md](../设计数据密集型应用/03-存储与检索.md)。
