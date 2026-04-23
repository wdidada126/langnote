# Vintage 引擎简介

# Elasticsearch Vintage 引擎（复古/旧版兼容引擎）简介
你现在用 ES 8.19.x，Kibana 里看到的 Vintage Engine，就是Elastic官方的旧索引兼容引擎，专门用来兼容 ES 7.x、ES 6.x 老索引，不是新车引擎，是兼容引擎。

## 一、一句话定义
Vintage Engine = ES8 内置的 Legacy 旧版Lucene引擎兼容层
ES8 默认用新版 Lucene 9 现代引擎；Vintage 是Lucene 8/7 旧版引擎，用来打开、读取、查询ES7/ES6创建的历史老索引。

## 二、为什么 ES8 要有 Vintage？
ES7 → ES8 底层 Lucene 大版本升级（Lucene8 → Lucene9）：
- ES8 原生新版引擎不兼容 ES7 老索引
- 直接打开会报错、无法查询、无法恢复
- 所以 ES8 内置 Vintage 旧引擎，实现平滑兼容迁移

> Vintage = 复古、经典、旧版兼容模式

## 三、核心作用（你当前环境最相关）
1. 读取/查询 ES6、ES7 创建的历史索引
2. 支持老分词器、老字段类型、老DSL语法
3. 支持老索引合并、重建、迁移到新版引擎
4. Kibana Index Management 里会明确标注：
   - `Engine: vintage`（老索引，兼容引擎）
   - `Engine: default`（ES8新建索引，新版Lucene9引擎）

## 四、Vintage vs Default 引擎对比（面试/工作必懂）
|对比项|Default 现代引擎（ES8默认）|Vintage 复古兼容引擎（ES7/6老索引）|
|---|---|---|
|底层Lucene|Lucene 9.x|Lucene 8.x / 7.x|
|适用索引|ES8新建索引|ES7、ES6历史旧索引|
|性能|更高、优化向量检索、更快|兼容优先、性能略低|
|新特性|支持ES8全部新特性（向量、knn、优化查询）|不支持ES8新特性，只兼容老语法|
|是否可写入|可正常增删改查|只读！只能查，不能写入更新|

### 关键重点：
Vintage 索引是只读！
不能 add/update/delete 文档，只能查询浏览，必须迁移重建到 Default 引擎才能读写。

## 五、你当前Kibana页面怎么看？
打开 Index Management：
- 索引列表里 Engine 列
  - 绿色 `default`：ES8新建、正常读写、新版引擎
  - 灰色 `vintage`：ES7/6迁移过来、只读、旧兼容引擎

## 六、日常操作（vim/命令行可用）
### 1. 查看索引用什么引擎
```bash
curl http://127.0.0.1:9200/_settings?pretty
```
返回里看到
```json
"engine.type" : "vintage"
```
就是复古兼容引擎。

### 2. Vintage老索引迁移到新版Default（必须做）
```json
POST /_reindex
{
  "source": { "index": "你的vintage老索引" },
  "dest": { "index": "new_index_default" }
}
```
重建后新索引就是 default 引擎、可读写。

## 七、总结（极简记忆）
1. Vintage = ES8 内置旧版Lucene兼容引擎
2. 专门跑 ES6/ES7老索引
3. 特点：只读、兼容、不能写入新数据
4. ES8新建索引都是 default 新版引擎
5. Kibana Index Management 里直接可见标识

需要我给你一条一键把所有Vintage只读索引迁移成Default可读写索引的ES命令吗？
