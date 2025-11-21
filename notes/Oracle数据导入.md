# Oracle数据导入

你当前的需求是：

> 将 Oracle 19c 数据库中，模式（Schema）`zhxc` 下的所有表数据导入到另一个 Oracle 19c 数据库的相同模式 `zhxc` 中。  
> 表结构已经导入完成。

##  前提条件

| 条件 | 是否满足 |
|------|----------|
| 目标数据库已存在 `zhxc` 用户/模式 |  是 |
| 表结构（DDL）已经导入目标库 |  是 |
| 源和目标数据库均为 Oracle 19c |  是 |

#  解决方案：使用 Oracle 数据泵（Data Pump）

推荐使用 Oracle Data Pump（数据泵）工具 的 `expdp` 和 `impdp` 命令来迁移数据。

这种方式速度快、支持并行处理、可精确控制对象类型，且适用于跨库迁移。

##  步骤一：在源数据库上导出 `zhxc` 用户下的所有 表数据

### 1. 创建目录对象（Directory Object）

```sql
-- 在源数据库中执行
CREATE OR REPLACE DIRECTORY data_pump_dir AS '/u01/app/oracle/dpump';
GRANT READ, WRITE ON DIRECTORY data_pump_dir TO zhxc;
```

确保 `/u01/app/oracle/dpump` 路径真实存在，并且 Oracle 用户有读写权限。

### 2. 使用 `expdp` 导出用户下所有表的数据（不导结构）

```bash
expdp zhxc/your_password@source_db \
      DIRECTORY=data_pump_dir \
      DUMPFILE=zhxc_data.dmp \
      LOGFILE=zhxc_data_exp.log \
      CONTENT=DATA_ONLY \
      SCHEMAS=zhxc
```

- `CONTENT=DATA_ONLY`：只导出数据，不导表结构。
- `SCHEMAS=zhxc`：指定要导出的用户模式。


##  步骤二：将 `.dmp` 文件拷贝到目标数据库服务器

```bash
scp /u01/app/oracle/dpump/zhxc_data.dmp target_host:/u01/app/oracle/dpump/
```


##  步骤三：在目标数据库上导入数据

### 1. 创建目录对象（同源库操作）

```sql
-- 在目标数据库中执行
CREATE OR REPLACE DIRECTORY data_pump_dir AS '/u01/app/oracle/dpump';
GRANT READ, WRITE ON DIRECTORY data_pump_dir TO zhxc;
```


### 2. 使用 `impdp` 导入数据

```bash
impdp zhxc/your_password@target_db \
      DIRECTORY=data_pump_dir \
      DUMPFILE=zhxc_data.dmp \
      LOGFILE=zhxc_data_imp.log \
      CONTENT=DATA_ONLY \
      TABLE_EXISTS_ACTION=APPEND
```

- `TABLE_EXISTS_ACTION=APPEND`：表示如果表已存在，就追加数据（不会覆盖或报错）。
  - 可选值：
    - `SKIP`：跳过已有表
    - `TRUNCATE`：清空后插入
    - `REPLACE`：删除表再重建（⚠️ 危险）
    - `APPEND`：默认行为，保留旧数据，新增数据


##  成功标志

- 日志文件中无严重错误（如主键冲突等）
- 所有表数据成功导入
- 查询验证部分表是否导入成功

```sql
SELECT COUNT(*) FROM some_table; -- 源库 vs 目标库对比
```


##  高级选项（可选）

### 并行导出/导入（提升性能）

```bash
expdp ... PARALLEL=4
impdp ... PARALLEL=4
```

### 过滤特定表（例如只导几个大表）

```bash
expdp ... INCLUDE=TABLE:"IN ('TABLE1', 'TABLE2')"
```

##  总结操作命令（快捷参考）

```bash
# 源库导出
expdp zhxc/password@source_db DIRECTORY=data_pump_dir DUMPFILE=zhxc_data.dmp CONTENT=DATA_ONLY SCHEMAS=zhxc

# 拷贝 dump 文件
scp zhxc_data.dmp user@target:/u01/app/oracle/dpump/

# 目标库导入
impdp zhxc/password@target_db DIRECTORY=data_pump_dir DUMPFILE=zhxc_data.dmp CONTENT=DATA_ONLY TABLE_EXISTS_ACTION=APPEND
```

##  其他方法备选（非推荐）

| 方法 | 说明 | 适用场景 |
|------|------|----------|
| SQL*Loader + 导出 CSV | 复杂，效率低 | 小数据量、调试 |
| PL/SQL 脚本逐表插入 | 效率极低 | 极小范围测试 |
| GoldenGate | 实时同步 | 生产环境高可用需求 |
| RMAN | 只能整库恢复 | 不适合单个 schema |

如果你还想了解如何自动化整个流程（脚本化）、记录日志、失败重试机制等，我可以为你提供完整的shell脚本

是否需要我帮你生成一个完整的 Shell 自动化迁移脚本？