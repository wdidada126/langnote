# sphinx

综合考虑了下，不用mysql的全文检索了，用sphinx开源全文检索引擎来实现

## 源代码
Sphinx是一个全文检索引擎，它使用SQL语言进行查询。它的源代码托管在GitHub上，地址为
https://github.com/sphinxsearch/sphinx
您可以在该页面上找到有关Sphinx的更多信息和文档。

Sphinx是一个全文检索引擎，主要为其他应用提供高速、低空间占用、高结果相关度的全文搜索功能。Sphinx可以非常容易地与SQL数据库和脚本语言集成。当前系统内置MySQL和PostgreSQL数据库数据源的支持，也支持从标准输入读取特定格式的XML数据。通过修改源代码，用户可以自行增加新的数据源（例如：其他类型的DBMS的原生支持）。Sphinx还为一些脚本语言设计搜索API接口，如PHP,Python,Perl,Ruby等，同时为MySQL也设计了一个存储引擎插件。

Sphinx的特性包括：
索引：通过索引，Sphinx可以高效地搜索包含在文本中的词汇。
搜索：Sphinx提供了精确搜索、模糊搜索和部分匹配搜索等多种搜索方式。
排序：Sphinx支持根据相关性、时间、权重等因素对搜索结果进行排序。
过滤：Sphinx支持根据一些特定的条件过滤搜索结果。
语法分析：Sphinx内置了词法分析器，能够对输入的文本进行语法分析。
文本预处理：Sphinx支持对文本进行预处理，例如去除停用词、词干提取等。
插件支持：Sphinx支持插件，可以扩展其功能。
总体来说，Sphinx是一个功能强大的全文检索引擎，适用于各种需要全文搜索功能的应用场景。

## 其他全文搜索引擎
1.Apache Lucene Java全文搜索框架
https://www.oschina.net/p/lucene
2.Apache Solr全文搜索服务器
https://www.oschina.net/p/solr
3.Nutch搜索引擎
https://www.oschina.net/p/nutch
4.RediSearch高性能全文搜索引擎
https://redis.io/docs/stack/search/
RediSearch是一个高性能的全文搜索引擎，可作为一个Redis Module运行在 Redis 上，是由 RedisLabs 团队开发的。实现了Redis的查询、二级索引和全文搜索。这些功能在文本查询的基础上实现了多字段查询、聚合、精确短语匹配、数字过滤、地理过滤和矢量相似性语义搜索。
项目地址：https://www.oschina.net/p/redisearch
5.Xapian C++检索引擎
https://www.oschina.net/p/xapian
6.Manticore Search C++ 开发的高性能搜索引擎
C/C++ 官网：https://manticoresearch.com/

Manticore Search 是一个使用 C++ 开发的高性能搜索引擎，创建于 2017 年，其前身是 Sphinx Search 。Manticore Search 充分利用了 Sphinx，显着改进了它的功能，修复了数百个错误，几乎完全重写了代码并保持开源！这一切使 Manticore Search 成为一个现代，快速，轻量级和功能齐全的数据库，具有出色的全文搜索功能。
来自 MS 官方的测试表明 Manticore Search 性能比 ElasticSearch 有很大的提升。
项目地址：https://www.oschina.net/p/manticoresearch

7.Tantivy全文搜索引擎库
Rust
Tantivy是一个用Rust编写的搜索引擎库，其灵感来自于Lucene。得益于Rust语言加持，Tantivy性能比Lucene要好得多。
https://www.oschina.net/p/tantivy

