# sysbench

```shell
sysbench --tables=5 --table_size=100 --mysql-user=root --mysql-password=5Edidada --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-db=sysbench_test oltp_insert prepare
sysbench 1.0.17 (using system LuaJIT 2.0.4)

Creating table 'sbtest1'...
Inserting 100 records into 'sbtest1'
Creating a secondary index on 'sbtest1'...
Creating table 'sbtest2'...
Inserting 100 records into 'sbtest2'
Creating a secondary index on 'sbtest2'...
Creating table 'sbtest3'...
Inserting 100 records into 'sbtest3'
Creating a secondary index on 'sbtest3'...
Creating table 'sbtest4'...
Inserting 100 records into 'sbtest4'
Creating a secondary index on 'sbtest4'...
Creating table 'sbtest5'...
Inserting 100 records into 'sbtest5'
Creating a secondary index on 'sbtest5'...
[root@VM_0_17_centos tests]# sysbench --tables=5 --table_size=100 --mysql-user=root --mysql-password=5Edidada --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-db=sysbench_test oltp_insert run
sysbench 1.0.17 (using system LuaJIT 2.0.4)

Running the test with following options:
Number of threads: 1
Initializing random number generator from current time


Initializing worker threads...

Threads started!

SQL statistics:
    queries performed:
        read:                            0
        write:                           2121
        other:                           0
        total:                           2121
    transactions:                        2121   (211.93 per sec.)
    queries:                             2121   (211.93 per sec.)
    ignored errors:                      0      (0.00 per sec.)
    reconnects:                          0      (0.00 per sec.)

General statistics:
    total time:                          10.0063s
    total number of events:              2121

Latency (ms):
         min:                                    3.04
         avg:                                    4.71
         max:                                   18.34
         95th percentile:                        8.28
         sum:                                 9990.68

Threads fairness:
    events (avg/stddev):           2121.0000/0.00
    execution time (avg/stddev):   9.9907/0.00

```


sysbench
一个模块化，跨平台以及多线程的性能测试工具。
https://github.com/akopytov/sysbench


基准测试（benchmarking）是性能测试的一种类型，强调的是对一类测试对象的某些性能指标进行定量的、可复现、可对比的测试。


 sysbench基准测试
sysbench是一个模块化的、跨平台、多线程基准测试工具，主要用于评估测试各种不同系统参数下的数据库负载情况,它主要包括以下几种方式的测试：

cpu性能

磁盘io性能

调度程序性能

内存分配及传输速度

POSIX线程性能

数据库性能(OLTP基准测试)

目前sysbench主要支持MySQL,pgsql,Oracle这3类数据库

默认支持MySQL，如果需要测试Oracle/PostgreSQL，则在configure时需要加上–with-oracle或者–with-pgsql参数.

通过sysbench工具对数据库开展基准测试最大的亮点在于：可以自动帮你在数据库里构造出来大量的数据，你想要多少数据，就自动给你构造出来多少条数据。同时还可以模拟几千个线程并发的访问数据库，模拟使用各种各样的 SQL 语句，包括模拟出来各种事务提交到你的数据库里去，甚至可以模拟出几十万的 TPS 去压测数据库。


sysbench基本语法
1、在使用前，先要需要安装，建议在Linux下安装sysbench

yum install -y sysbench
2、sysbench的基本语法如下:

sysbench [options]... [testname] [command]

Installed:
  sysbench.x86_64 0:1.0.17-2.el7                                                                                                                                                                                

Dependency Installed:
  ck.x86_64 0:0.5.2-2.el7                                                                              luajit.x86_64 0:2.0.4-3.el7   



sysbench -h
sysbench 1.0.17 (using system LuaJIT 2.0.4)




```shell
sysbench --help
Usage:
  sysbench [options]... [testname] [command]

Commands implemented by most tests: prepare run cleanup help

General options:
  --threads=N                     number of threads to use [1]
  --events=N                      limit for total number of events [0]
  --time=N                        limit for total execution time in seconds [10]
  --forced-shutdown=STRING        number of seconds to wait after the --time limit before forcing shutdown, or 'off' to disable [off]
  --thread-stack-size=SIZE        size of stack per thread [64K]
  --rate=N                        average transactions rate. 0 for unlimited rate [0]
  --report-interval=N             periodically report intermediate statistics with a specified interval in seconds. 0 disables intermediate reports [0]
  --report-checkpoints=[LIST,...] dump full statistics and reset all counters at specified points in time. The argument is a list of comma-separated values representing the amount of time in seconds elapsed from start of test when report checkpoint(s) must be performed. Report checkpoints are off by default. []
  --debug[=on|off]                print more debugging info [off]
  --validate[=on|off]             perform validation checks where possible [off]
  --help[=on|off]                 print help and exit [off]
  --version[=on|off]              print version and exit [off]
  --config-file=FILENAME          File containing command line options
  --tx-rate=N                     deprecated alias for --rate [0]
  --max-requests=N                deprecated alias for --events [0]
  --max-time=N                    deprecated alias for --time [0]
  --num-threads=N                 deprecated alias for --threads [1]

Pseudo-Random Numbers Generator options:
  --rand-type=STRING random numbers distribution {uniform,gaussian,special,pareto} [special]
  --rand-spec-iter=N number of iterations used for numbers generation [12]
  --rand-spec-pct=N  percentage of values to be treated as 'special' (for special distribution) [1]
  --rand-spec-res=N  percentage of 'special' values to use (for special distribution) [75]
  --rand-seed=N      seed for random number generator. When 0, the current time is used as a RNG seed. [0]
  --rand-pareto-h=N  parameter h for pareto distribution [0.2]

Log options:
  --verbosity=N verbosity level {5 - debug, 0 - only critical messages} [3]

  --percentile=N       percentile to calculate in latency statistics (1-100). Use the special value of 0 to disable percentile calculations [95]
  --histogram[=on|off] print latency histogram in report [off]

General database options:

  --db-driver=STRING  specifies database driver to use ('help' to get list of available drivers) [mysql]
  --db-ps-mode=STRING prepared statements usage mode {auto, disable} [auto]
  --db-debug[=on|off] print database-specific debug information [off]


Compiled-in database drivers:
  mysql - MySQL driver
  pgsql - PostgreSQL driver

mysql options:
  --mysql-host=[LIST,...]          MySQL server host [localhost]
  --mysql-port=[LIST,...]          MySQL server port [3306]
  --mysql-socket=[LIST,...]        MySQL socket
  --mysql-user=STRING              MySQL user [sbtest]
  --mysql-password=STRING          MySQL password []
  --mysql-db=STRING                MySQL database name [sbtest]
  --mysql-ssl[=on|off]             use SSL connections, if available in the client library [off]
  --mysql-ssl-cipher=STRING        use specific cipher for SSL connections []
  --mysql-compression[=on|off]     use compression, if available in the client library [off]
  --mysql-debug[=on|off]           trace all client library calls [off]
  --mysql-ignore-errors=[LIST,...] list of errors to ignore, or "all" [1213,1020,1205]
  --mysql-dry-run[=on|off]         Dry run, pretend that all MySQL client API calls are successful without executing them [off]

pgsql options:
  --pgsql-host=STRING     PostgreSQL server host [localhost]
  --pgsql-port=N          PostgreSQL server port [5432]
  --pgsql-user=STRING     PostgreSQL user [sbtest]
  --pgsql-password=STRING PostgreSQL password []
  --pgsql-db=STRING       PostgreSQL database name [sbtest]

Compiled-in tests:
  fileio - File I/O test
  cpu - CPU performance test
  memory - Memory functions speed test
  threads - Threads subsystem performance test
  mutex - Mutex performance test

See 'sysbench <testname> help' for a list of options for each test.
```


create database sysbench_test; 

sysbench /usr/share/sysbench/oltp_read_write.lua --tables=5 --table_size=100000 --mysql-user=root --mysql-password=5Edidada --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-db=sysbench_test cleanup


sysbench --tables=5 --table_size=100000 --mysql-user=root --mysql-password=5Edidada --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-db=sysbench_test oltp_insert run



sysbench --tables=5 --table_size=100 --mysql-user=root --mysql-password=5Edidada --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-db=sysbench_test oltp_insert
sysbench 1.0.17 (using system LuaJIT 2.0.4)

FATAL: /usr/share/sysbench/oltp_common.lua:28: Command is required. Supported commands: prepare, prewarm, run, cleanup, help
[root@VM_0_17_centos ~]# sysbench --tables=5 --table_size=100 --mysql-user=root --mysql-password=5Edidada --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-db=sysbench_test oltp_insert help
sysbench 1.0.17 (using system LuaJIT 2.0.4)

oltp_insert options:
  --auto_inc[=on|off]           Use AUTO_INCREMENT column as Primary Key (for MySQL), or its alternatives in other DBMS. When disabled, use client-generated IDs [on]
  --create_secondary[=on|off]   Create a secondary index in addition to the PRIMARY KEY [on]
  --delete_inserts=N            Number of DELETE/INSERT combinations per transaction [1]
  --distinct_ranges=N           Number of SELECT DISTINCT queries per transaction [1]
  --index_updates=N             Number of UPDATE index queries per transaction [1]
  --mysql_storage_engine=STRING Storage engine, if MySQL is used [innodb]
  --non_index_updates=N         Number of UPDATE non-index queries per transaction [1]
  --order_ranges=N              Number of SELECT ORDER BY queries per transaction [1]
  --pgsql_variant=STRING        Use this PostgreSQL variant when running with the PostgreSQL driver. The only currently supported variant is 'redshift'. When enabled, create_secondary is automatically disabled, and delete_inserts is set to 0
  --point_selects=N             Number of point SELECT queries per transaction [10]
  --range_selects[=on|off]      Enable/disable all range SELECT queries [on]
  --range_size=N                Range size for range SELECT queries [100]
  --secondary[=on|off]          Use a secondary index in place of the PRIMARY KEY [off]
  --simple_ranges=N             Number of simple range SELECT queries per transaction [1]
  --skip_trx[=on|off]           Don't start explicit transactions and execute all queries in the AUTOCOMMIT mode [off]
  --sum_ranges=N                Number of SELECT SUM() queries per transaction [1]
  --table_size=N                Number of rows per table [10000]
  --tables=N                    Number of tables [1]




show variables like '%stmt%';
+----------------------------+----------------------+
| Variable_name              | Value                |
+----------------------------+----------------------+
| binlog_stmt_cache_size     | 32768                |
| max_binlog_stmt_cache_size | 18446744073709547520 |
| max_prepared_stmt_count    | 16382                |
+----------------------------+----------------------+
3 rows in set (0.04 sec)



```shell
cd /usr/share/sysbench
[root@VM_0_17_centos sysbench]# ;;
-bash: syntax error near unexpected token `;;'
[root@VM_0_17_centos sysbench]# ll
total 64
-rwxr-xr-x 1 root root  1452 Mar 16  2019 bulk_insert.lua
-rw-r--r-- 1 root root 14369 Mar 16  2019 oltp_common.lua
-rwxr-xr-x 1 root root  1290 Mar 16  2019 oltp_delete.lua
-rwxr-xr-x 1 root root  2415 Mar 16  2019 oltp_insert.lua
-rwxr-xr-x 1 root root  1265 Mar 16  2019 oltp_point_select.lua
-rwxr-xr-x 1 root root  1649 Mar 16  2019 oltp_read_only.lua
-rwxr-xr-x 1 root root  1824 Mar 16  2019 oltp_read_write.lua
-rwxr-xr-x 1 root root  1118 Mar 16  2019 oltp_update_index.lua
-rwxr-xr-x 1 root root  1127 Mar 16  2019 oltp_update_non_index.lua
-rwxr-xr-x 1 root root  1440 Mar 16  2019 oltp_write_only.lua
-rwxr-xr-x 1 root root  1919 Mar 16  2019 select_random_points.lua
-rwxr-xr-x 1 root root  2118 Mar 16  2019 select_random_ranges.lua
drwxr-xr-x 4 root root  4096 Feb  7 16:44 tests
[root@VM_0_17_centos sysbench]# cd tests/
[root@VM_0_17_centos tests]# ll
total 12
drwxr-xr-x 3 root root 4096 Feb  7 16:44 include
drwxr-xr-x 2 root root 4096 Feb  7 16:44 t
-rwxr-xr-x 1 root root 2536 Mar 16  2019 test_run.sh
```
