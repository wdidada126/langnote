**UPSERT** = UPDATE + INSERT：如果记录存在就更新，不存在就插入。

**例子（MySQL）：**
```sql
INSERT INTO users (id, name, age)
VALUES (1, '张三', 25)
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    age = VALUES(age);
```
- `id=1` 已存在 → 更新 `name`、`age`
- `id=1` 不存在 → 插入新记录

**其他数据库写法：**
- PostgreSQL：`INSERT ... ON CONFLICT (id) DO UPDATE SET ...`
- SQLite：`INSERT ... ON CONFLICT(id) DO UPDATE SET ...`
- SQL Server / Oracle：用 `MERGE` 语句实现