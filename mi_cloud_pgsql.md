# mi cloud




psql COPY指令 

COPY table_name form local_system_file

失败

考虑是不是psql9

pg sql server 10，考虑是否是版本不兼容









psql







\copy { ***table\*** [ ( ***column_list\*** ) ] | ( ***query\*** ) } { from | to } { ***'filename'\*** | program ***'command'\*** | stdin | stdout | pstdin | pstdout } [ [ with ] ( ***option\*** [, ...] ) ]



Performs a frontend (client) copy. This is an operation that runs an SQL COPY command, but instead of the server reading or writing the specified file, psql reads or writes the file and routes the data between the server and the local file system. This means that file accessibility and privileges are those of the local user, not the server, and no SQL superuser privileges are required.

When program is specified, ***command\*** is executed by psql and the data passed from or to ***command\*** is routed between the server and the client. Again, the execution privileges are those of the local user, not the server, and no SQL superuser privileges are required.

For \copy ... from stdin, data rows are read from the same source that issued the command, continuing until \. is read or the stream reaches EOF. This option is useful for populating tables in-line within a SQL script file. For \copy ... to stdout, output is sent to the same place as psql command output, and the COPY ***count\*** command status is not printed (since it might be confused with a data row). To read/write psql's standard input or output regardless of the current command source or \o option, write from pstdin or to pstdout.

The syntax of this command is similar to that of the SQL COPY command. All options other than the data source/destination are as specified for COPY. Because of this, special parsing rules apply to the \copy meta-command. Unlike most other meta-commands, the entire remainder of the line is always taken to be the arguments of \copy, and neither variable interpolation nor backquote expansion are performed in the arguments.







编程



函数式兴起

cpu的计算能力

函数式>面向对象





拍拍贷 架构师



杨波 波波老师

https://www.bilibili.com/video/BV13D4y1Q7AY

拍拍贷大学 讲师






腾讯 c++ 多进程

跨进程通信比跨线程通信容易

单机 多机



Navicate

导入导出sql

pg

列名不加 双引号




一致性hash

https://github.com/Jaskey/ConsistentHash





pg vs mysql

netbsd 高贵 不响应工业界需求



