# mysql_8_doc

## show
MySQL 8 支持多种 `SHOW` 语句，这些语句用于查看数据库、表、索引、用户等各种数据库对象和系统状态的信息。以下是一些常见的 `SHOW` 语句及其用途：

### 数据库相关
- `SHOW DATABASES`
    - 用途：显示 MySQL 服务器中所有可用的数据库。
    - 示例：
```sql
SHOW DATABASES;
```
- `SHOW CREATE DATABASE`
    - 用途：显示创建指定数据库的 SQL 语句。
    - 示例：
```sql
SHOW CREATE DATABASE your_database_name;
```

### 表相关
- `SHOW TABLES`
    - 用途：显示当前数据库中的所有表。
    - 示例：
```sql
SHOW TABLES;
```
- `SHOW CREATE TABLE`
    - 用途：显示创建指定表的 SQL 语句，包括表结构、索引等信息。
    - 示例：
```sql
SHOW CREATE TABLE your_table_name;
```
- `SHOW TABLE STATUS`
    - 用途：显示当前数据库中所有表的详细状态信息，如引擎、行数、创建时间等。
    - 示例：
```sql
SHOW TABLE STATUS;
```

### 列相关
- `SHOW COLUMNS FROM`
    - 用途：显示指定表的列信息，包括列名、数据类型、是否允许为空等。
    - 示例：
```sql
SHOW COLUMNS FROM your_table_name;
```

### 索引相关
- `SHOW INDEX FROM`
    - 用途：显示指定表的索引信息，包括索引名、索引类型、索引列等。
    - 示例：
```sql
SHOW INDEX FROM your_table_name;
```

### 用户和权限相关
- `SHOW GRANTS`
    - 用途：显示指定用户的权限信息。
    - 示例：
```sql
SHOW GRANTS FOR 'your_user'@'your_host';
```

### 进程和状态相关
- `SHOW PROCESSLIST`
    - 用途：显示当前 MySQL 服务器中正在运行的所有进程信息，包括进程 ID、用户、主机、执行的 SQL 语句等。
    - 示例：
```sql
SHOW PROCESSLIST;
```
- `SHOW STATUS`
    - 用途：显示 MySQL 服务器的各种状态信息，如连接数、查询次数、缓存命中率等。
    - 示例：
```sql
SHOW STATUS;
```
- `SHOW VARIABLES`
    - 用途：显示 MySQL 服务器的各种系统变量信息，如字符集、缓存大小、日志级别等。
    - 示例：
```sql
SHOW VARIABLES;
```

### 存储引擎相关
- `SHOW ENGINES`
    - 用途：显示 MySQL 服务器支持的所有存储引擎信息，包括引擎名称、描述、是否默认等。
    - 示例：
```sql
SHOW ENGINES;
```

以上只是 MySQL 8 中部分常见的 `SHOW` 语句，实际上还有更多的 `SHOW` 语句可以用于查看不同方面的信息。你可以根据具体需求选择合适的 `SHOW` 语句来查看所需的信息。

## doc

这些函数在MySQL中用于获取日期和时间信息，它们之间的区别如下：
1. NOW():
   - `NOW()`函数返回当前日期和时间，包括年、月、日、时、分和秒。
   - 返回的值是基于当前系统的时区设置。
2. CURDATE():
   - `CURDATE()`函数返回当前日期，仅包括年、月和日部分。
   - 返回的值是基于当前系统的时区设置。
3. CURTIME():
   - `CURTIME()`函数返回当前时间，仅包括时、分和秒部分。
   - 返回的值是基于当前系统的时区设置。
4. UTC_DATE():
   - `UTC_DATE()`函数返回当前的UTC日期，仅包括年、月和日部分。
   - 返回的值不受系统时区设置的影响，始终基于协调世界时（UTC）。
5. UTC_TIME():
   - `UTC_TIME()`函数返回当前的UTC时间，仅包括时、分和秒部分。
   - 返回的值不受系统时区设置的影响，始终基于协调世界时（UTC）。
6. UTC_TIMESTAMP():
   - `UTC_TIMESTAMP()`函数返回当前的UTC日期和时间，包括年、月、日、时、分和秒。
   - 返回的值不受系统时区设置的影响，始终基于协调世界时（UTC）。

通过使用这些函数，您可以根据需要获取当前日期和时间的不同部分，以及在本地时区或UTC时区中获取日期和时间。请注意，这些函数的返回值类型是`DATE`、`TIME`或`DATETIME`，具体取决于函数的用法和上下文。

NO_ZERO_IN_DATE mode.

https://dev.mysql.com/doc/refman/8.0/en/date-and-time-types.html

Data Type	“Zero” Value
DATE	'0000-00-00'
TIME	'00:00:00'
DATETIME	'0000-00-00 00:00:00'
TIMESTAMP	'0000-00-00 00:00:00'
YEAR	0000


分析函数（也叫窗口函数）

mysql 8 doc

Flow Control Functions
Table 14.7 Flow Control Operators

Name	Description
CASE	Case operator
IF()	If/else construct
IFNULL()	Null if/else construct
NULLIF()	Return NULL if expr1 = expr2

"Flow Control Functions" 在编程和计算机网络上下文中通常指的是用于控制数据流动或程序执行流程的函数或机制。将其翻译成中文时，可以根据上下文进行微调，但一个常见的翻译是：

流量控制函数 或 流程控制函数

流量控制 通常与网络通信相关，它确保发送方不会发送超过接收方能够处理的数据量。
流程控制 更广泛地与编程相关，指的是控制代码执行的顺序和条件。

如果你是在特定的编程库、框架或网络协议中遇到 "Flow Control Functions"，那么翻译可能需要更具体地反映其用途。例如，在TCP/IP协议中，"流量控制" 是指确保数据不会丢失或阻塞的机制。而在编程中，"流程控制" 可能包括条件语句（如if-else）、循环（如for、while）以及异常处理等。

Locking Functions

Name	Description
GET_LOCK()	Get a named lock
IS_FREE_LOCK()	Whether the named lock is free
IS_USED_LOCK()	Whether the named lock is in use; return connection identifier if true
RELEASE_ALL_LOCKS()	Release all current named locks
RELEASE_LOCK()	Release the named lock


在MySQL 8中，GET_LOCK()是一个用于获取命名锁的函数。它的作用是在数据库中获取一个命名锁，以防止其他会话获取相同名称的锁。

GET_LOCK()函数的语法如下：

```plaintext
GET_LOCK(str, timeout)
```

参数说明：
- `str`：要获取的锁的名称，为字符串类型。
- `timeout`：获取锁的超时时间，单位为秒。如果设置为0，则函数立即返回，无论是否获取到锁。如果设置为正数，则函数会等待指定的时间，直到获取到锁或超时。

当一个会话成功获取到锁时，它将返回一个值为1的整数。如果获取锁超时或发生错误，将返回0。

GET_LOCK()函数可以用于实现并发控制机制，确保在多个会话同时访问共享资源时的互斥性。例如，您可以在一个会话中使用GET_LOCK()获取某个资源的锁，然后在另一个会话中使用GET_LOCK()尝试获取同样的锁。如果第二个会话无法获取到锁，可以根据返回的结果进行相应的处理，如等待一段时间后重试或执行其他逻辑。

注意事项：
- 获取到的锁只对当前MySQL连接可见，其他连接无法通过GET_LOCK()获取到相同的锁。
- 在使用完锁后，应使用RELEASE_LOCK()函数释放锁，以避免资源泄漏。

请注意，GET_LOCK()函数的使用需要谨慎，过度使用或不正确的使用可能会导致性能问题或死锁情况。建议在设计并发控制方案时，仔细考虑锁的使用方式和范围，确保系统的可靠性和性能。

