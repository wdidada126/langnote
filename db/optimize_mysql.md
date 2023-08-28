# optimize mysql

mysql not in 优化成 left join 分析



将 MySQL 中的 `NOT IN` 子查询转换为 `LEFT JOIN` 可以是一种优化策略，特别是在处理大型数据集时。通过使用 `LEFT JOIN`，可以避免使用 `NOT IN` 子查询导致的性能问题。

下面是一个示例，演示如何将 `NOT IN` 子查询转换为 `LEFT JOIN`：

假设有两个表格：`table1` 和 `table2`。我们希望从 `table1` 中选择那些在 `table2` 中不存在的记录。

使用 `NOT IN` 子查询的方式：

```sql
SELECT *
FROM table1
WHERE id NOT IN (SELECT id FROM table2);
```

将 `NOT IN` 子查询转换为 `LEFT JOIN` 的方式：

```sql
SELECT table1.*
FROM table1
LEFT JOIN table2 ON table1.id = table2.id
WHERE table2.id IS NULL;
```

在上面的查询中，我们使用了 `LEFT JOIN` 将 `table1` 和 `table2` 进行连接，并根据条件 `table1.id = table2.id` 进行匹配。然后，通过添加 `WHERE table2.id IS NULL` 条件，我们筛选出在 `table2` 中没有匹配的记录。

这种转换的优势在于，使用 `LEFT JOIN` 可以利用数据库的索引和优化器，提供更好的性能。相比之下，`NOT IN` 子查询可能需要对 `table2` 进行多次扫描，并且在处理大型数据集时可能会导致性能下降。

需要注意的是，优化查询的方式取决于具体的数据模型、索引和查询条件。在某些情况下，`NOT IN` 子查询可能更有效率，而在其他情况下，`LEFT JOIN` 可能更适合。因此，根据实际情况进行性能测试和比较是至关重要的。





FREE Trial of Database Performance Analyzer for MySQL from SolarWinds

https://haydenjames.io/mysql-performance-tuning-tips-scripts-tools/
VividCortex

https://www.dnsstuff.com/mysql-tools

https://www.eversql.com/top-5-mysql-monitoring-tools/

