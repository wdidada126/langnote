# mysql_8_doc

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

