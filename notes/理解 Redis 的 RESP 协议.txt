# Redis RESP

+OK
*2
$4
AUTH
$7
5%Redis
*2
$4
AUTH
$7
5%Redis
*3
$6
CLIENT
$7
setname
$16
fancy_jedis_name
*3
$6
CLIENT
$7
setname
$6
string
*2
$6
CLIENT
$7
getname
$6
string



For Simple Strings the first byte of the reply is "+"
For Errors the first byte of the reply is "-"
For Integers the first byte of the reply is ":"
For Bulk Strings the first byte of the reply is "$"
For Arrays the first byte of the reply is "*"

理解 Redis 的 RESP 协议


单行回复：回复的第一个字节是 “+”
错误信息：回复的第一个字节是 “-”
整形数字：回复的第一个字节是 “:”
多行字符串：回复的第一个字节是 “\$”
数组：回复的第一个字节是 “*”


BGSAVE 在后台异步(Asynchronously)保存当前数据库的数据到磁盘。
SAVE 命令执行一个同步保存操作，将当前 Redis 实例的所有数据快照(snapshot)以 RDB 文件的形式保存到硬盘。



