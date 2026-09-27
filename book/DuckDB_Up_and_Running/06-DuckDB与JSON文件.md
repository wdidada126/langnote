# 06 · Using DuckDB with JSON Files（DuckDB 与 JSON 文件）

> 覆盖原书第 6 章。目录来源：✅ 官方示例文件 `Chapter_6.ipynb` 标题实抓。JSON 是"文档世界喂给列存世界"的口岸：本章把**读（三种格式形态）、写（COPY 导出）**两头讲透，是 API 日志、LLM 时代半结构化数据入库的第一站。

## 内容规格（小节地图，✅ 实抓自官方示例 notebook）

- **Loading JSON Files into DuckDB**
  - **Using read_json_auto() Function**：全自动嗅探（列推型、嵌套升 STRUCT）。
  - **Using the read_json() Function**：手动形态，下分四子节 ✅——**Array of JSON Objects**、**Newline-delimited (ND) JSON**、**Nested JSON**、**Custom JSON File**；notebook 原注：`format` 参数可取 `array | newline_delimited(nd) | uns`(unspecified)（✅ 代码注释实抓）。
  - **Loading multiple JSON files**：glob 多文件一枪装。
  - **Using the COPY-FROM Statement**：`COPY t FROM 'x.json'` 批量入表路线。
  - **Exporting Tables to JSON**：`COPY … TO (FORMAT JSON, ARRAY true)` 双形态（数组式/ND 式）。

## 核心技术清单

- 读函数分层：`read_json_auto`（推断）→ `read_json`（给 columns/format 精控）→ 具体 reader（`nd_json`/`array_json` 族糖）。
- 类型映射：JSON object→`STRUCT`、数组→`LIST`、数字默认按值域选 BIGINT/DOUBLE、`UNION BY NAME` 合并异构记录。
- 嵌套访问：`address.zip` 点号链 + `json_extract*` 系函数做"不展开直查"。
- 写侧选项：`FORMAT JSON` + `ARRAY true`（整文档数组）vs 默认 ND（一行一对象）。
- 多文件：glob `*.json` 或显式列表 + `filename=true` 追来源列。
- `COPY … FROM`（半自动入表）与 `CREATE TABLE AS SELECT`（直接落表）两路，后者省一次类型对齐。

## 🔧 实测（1.5.5；示例仓库自带 JSON 文件族）

1. **auto 嗅探嵌套** ✅：`json2.json`（一个 JSON **数组**文档，3 个对象、内含嵌套 `address`）→ `read_json_auto` 得 **3 行**；`DESCRIBE` 显示 `address` 自动成 **`STRUCT(line1 VARCHAR, line2 VARCHAR, state VARCHAR, zip BIGINT)`**——嵌套对象零配置升格结构列。
2. **format 声明防错** ✅：对同一数组文件强行 `read_json(..., format='newline_delimited')` → `Invalid Input Error: Malformed JSON in file … at byte 2`——**格式声明错配直接炸**，反证 `uns`(unspecified)/auto 的价值。
3. **people.json 样本** ✅：3 行，首行 `('Sarah Johnson', 140.5)`（对象数组直落平表）。
4. **导出回环** ✅：`COPY (SELECT * FROM read_json_auto('json2.json')) TO 'out_json2.json' (FORMAT JSON, ARRAY true)` → 544 B 文件，读回 3 行无损。
5. **HTTPS 直读**：`read_json_auto('https://raw.githubusercontent.com/…/json1.json')` 3 行 **1.57 s**（冷 TLS）——JSON 与 httpfs 组合下"远程文档即表"（详见 [08 章](08-用DuckDB访问远程数据.md)）。
6. **json 扩展本体**：1.5.5 中 json 为默认加载扩展（`loaded=True` ✅），`st_read` 之外的 `excel` 类扩展都还要显式 LOAD——JSON 是唯一"开箱即得"的文档格式。
7. **聚合 ND 回环** 🔧：`COPY (SELECT AIRLINE, count(*) n FROM flights GROUP BY 1) TO 'agg_nd.json' (FORMAT JSON)` → **14 行 / 390 B**（默认 ND），`read_json_auto` 读回 14 行、max(n)=1,261,855 与 03 章 WN 计数逐值一致（**0.02 s**）——"SQL 聚合→JSON 报表出口"最小链路。
8. **json_extract_string 嵌套手术刀** 🔧：`json_extract_string('{"a":{"b":42}}', '$.a.b')` → `'42'`（返回 VARCHAR，数值比较前还要 CAST）——不整表展开、单字段直取。

## 易错点与陷阱

- **数组 vs ND 是两种文件**：Kibana/logstash 生态产 ND（一行一对象）、API dump 常是数组——`uns` 让 auto 猜，猜错就 byte 2 炸；入库管道里**固定 format 声明**才是可复现工程。
- **数字统一 BIGINT/DOUBLE 的边界**：`zip` 推断成 BIGINT（实测 STRUCT 里 `zip BIGINT`）——邮编、手机号等"数字型标识"要 `columns={zip:'VARCHAR'}` 覆写，否则前导零蒸发。
- **异构行 union**：部分对象缺键 → `union_by_name=true`，否则列错位或报错；键名带点/特殊符时点号访问歧义（用 `json_extract`）。
- **LIST 列再展开**：JSON 数组落 `LIST` 列后不能直接 JOIN，先 `UNNEST`（配合 `generate_subscripts` 保下标）。
- **导出的两种"对"**：`ARRAY true` 出单文档数组（人读友好），默认 ND（流式工具友好）；下游是 Spark/Flink 时**必须 ND**——两形态各存一份是常见防呆。
- **大 JSON 别硬嗅探**：超大 ND 文件 `sample_size=-1` 会全量扫——默认抽样推断即可；复杂类型混排考虑先转 Parquet（02 章往返数据）。
- **json_extract\* 的字符串惯性**：`json_extract_string` 返回 VARCHAR（实测 8 的 `'42'`）——数值比较靠隐转会在 NULL 出现时炸相；显式 CAST 或不走 JSON 直取列。
- **filename 别忘当审计列**：多文件 glob 加载时 `filename=true` 留下来源列——数据血缘是质量要求，不是装饰。

## JSON 函数族速查（句内角色；✅=本目录实测）

| 函数/语法 | 角色 | 注记 |
| --- | --- | --- |
| `read_json_auto(f)` | 推断一切 | ✅ 嵌套→STRUCT（实测 1） |
| `read_json(f, format:=…)` | 形态声明 | ✅ 错配 byte 2 炸（实测 2） |
| `col.subfield` | STRUCT 点号钻取 | ✅ `address.zip` 路线（内容规格） |
| `json_extract_string(j,'$.a.b')` | 单字段直取 | ✅ 返回 VARCHAR（实测 8） |
| `json_valid(j)` | 质量门前置 | ⚠️ 在册未逐测 |
| `to_json(map({'k':col}))` | 关系侧造文档 | ✅ 形态试跑（本目录探针） |
| `unnest(list_col)` | LIST 列→行 | ✅ JSON 数组落库后标配 |
| `COPY … (FORMAT JSON, ARRAY true)` | 数组形态导出 | ✅ 544 B 回环（实测 4） |

## 嵌套 JSON 钻取最小链路（以实测 1 的 json2.json 为题）

```sql
-- 形态①：自动升 STRUCT + 点号钻取（schema 稳定时的日常姿势）
SELECT name, address.city, address.zip FROM read_json_auto('json2.json');
-- 形态②：数组字段展开成行（涉 LIST 才用）
SELECT name, u FROM (SELECT name, unnest(phones) u FROM read_json_auto('p.json'));
-- 形态③：不展开 schema、手术刀直取（异构/冷热字段混杂的救命通道）
SELECT json_extract_string(raw, '$.a.b') FROM nd_logs;
-- 落库定型：钻完就 CTAS，JSON 是入口不是住所
CREATE TABLE t AS SELECT * FROM read_json_auto('json2.json');
```

- 经验法则：**schema 稳走①、数组才②、异构救③**；三形态出口都是同一张 Parquet 入库表（02 章流水线第①步）。

## 关键参数速查（实测注记）

| 用法 | 说明 | 注记 |
| --- | --- | --- |
| `read_json_auto(f)` | 推断一切 | ✅ 嵌套→STRUCT |
| `read_json(f, format:='array'/'newline_delimited')` | 显式形态 | ✅ 错配即炸 |
| `columns={…}` | 类型覆写 | ⚠️ 机制在，未逐测 |
| `union_by_name=true` | 异构合并 | ⚠️ 未逐测 |
| `COPY t FROM f` / `COPY (…) TO f (FORMAT JSON, ARRAY true)` | 入表/导出 | ✅ 544B 回环 |
| glob `read_json_auto('*.json')` | 多文件 | ✅ 本地 glob 可用；HTTP 侧受限（08 章） |

## 与其他章/书的互链

- 文件 IO 全景（CSV/Parquet 对照）→ [02-数据导入DuckDB.md](02-数据导入DuckDB.md)；远程 JSON → [08-用DuckDB访问远程数据.md](08-用DuckDB访问远程数据.md)
- DIA 侧的 JSON/Excel/SQLite 直查叙事与 `json_` 函数族细节 → [../DuckDB_in_Action/05-无持久化的数据探索.md](../DuckDB_in_Action/05-无持久化的数据探索.md)
- 湖仓里的半结构化标准（Iceberg 侧 VARIANT/宽表）→ [../Apache_Iceberg活用入門/00-总览与阅读地图.md](../Apache_Iceberg活用入門/00-总览与阅读地图.md)

## 思考题（合上笔记再答）

1. 三种 format 取值分别在什么文件上会失败？给出你见过的报错原文。（ND 声明打到数组文件：Malformed JSON at byte 2——本目录实证）
2. JSON 的 zip 字段为什么是本章最重要的类型警示？（BIGINT 推断吃前导零；覆写 VARCHAR）
3. 写出"3 个对象+嵌套 address"文件的一入一出最小链路。（read_json_auto → COPY TO (FORMAT JSON, ARRAY true)，实测回环无损）
4. `json_extract_string('$.a.b')` 返回什么类型？三种钻取形态怎么选？（VARCHAR（实测 8）；schema 稳走 STRUCT 点号、数组才 UNNEST、异构救手术刀——钻取节口诀）

## 2026 视角补注

- 1.3.0 起 **VARIANT** 类型（GitHub releases ✅ 1.3.0 "Ossivalis"，2025-05）给"每行 schema 都不同"的日志/事件数据一个不拍平的家——本书成书时点（1.1.x）还没有它，是 UAR→现状的最大增量点之一。
- JSON 与 Arrow/Parquet 的互转（`to_arrow_table` + pyarrow.compute）与"LATERAL FLATTEN 一代"的对比在 2024–2026 博客中反复出现；DuckDB 的答案始终是"SQL 直查 + 一次 CTAS"。
- LLM 评测集即 JSONL（=ND 一行一对象）：`read_json_auto('eval/*.jsonl')` 是 2025–2026 agent 开发的日常词汇——本章 format/dtype 教训全额复用（定性口径）。

## 核心概念速览（中英对照）

- **ND JSON** — Newline-delimited JSON：一行一对象的事实日志格式。
- **数组 JSON** — Array of objects：整文档一次性 JSON 数组。
- **uns 形态** — Unspecified：交给推断器的 format 档。
- **结构列** — STRUCT：JSON 对象自动映射的命名字段列。
- **列表列** — LIST：JSON 数组映射，UNNEST 展开。
- **类型覆写** — columns 参数：防邮编/ID 误推断。
- **按名合并** — union_by_name：异构记录对齐列。
- **导出双形态** — ARRAY true vs ND：人读与流读的取舍。
- **嗅探抽样** — sample_size：推断器的成本旋钮。
- **VARIANT** — 1.3+ 的半结构化兜底类型（本书后时代增量）。
- **手术刀直取** — json_extract_string + JSONPath：不展开 schema 的单字段通道。

## 最新演进与工业实践

- **版本演进**：JSON 函数族在 1.x 线持续加料（`json_merge_patch`、`map_keys` 配套等，具体以文档为准 ⚠️ 未逐一实测）；VARIANT（1.3.0 ✅）是 2025–2026 半结构化讨论的主角，与 Iceberg/Parquet 的 VARIANT 提案同代。
- **工业实践**：API 日志 → ND → DuckDB `read_json_auto` glob 摄取 → Parquet 落库，是"零平台单机数据湖"的标准三步；LLM 工具链（评测集/数据集卡片）同样以 JSON 为交换格式，本章的 format 错配教训在 HF 数据集直读时复用（08 章）。
- **互读**：DIA 附录侧的批量导入姿势 → [../DuckDB_in_Action/12-附录A-客户端API.md](../DuckDB_in_Action/12-附录A-客户端API.md)。
