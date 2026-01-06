# Database_Design_and_Implementation 2

https://www.goodreads.com/book/show/240914702-database-design-and-implementation
https://www.amazon.com/Database-Design-Implementation-Data-Centric-Applications/dp/3030338355

Database Design and Implemehttps://www.amazon.com/Database-Design-Implementation-Data-Centric-Applications/dp/3030338355
ntation Second Edition
https://link.springer.com/book/10.1007/978-3-030-33836-7
Authors:Edward Sciore

D:\develops\git\github\java\simpledb2_mvn\docs

SimpleDB_Chinese_V1_0.pdf
database-design-and-implementation.pdf
Database_Internals.pdf

Product details
Publisher : Springer
Publication date : February 28, 2020
Edition : 1st ed. 2020
Language : English
Print length : 471 pages
ISBN-10 : 3030338355
ISBN-13 : 978-3030338350
Item Weight : 1.69 pounds
Dimensions : 6.1 x 1.07 x 9.25 inches

介绍

版权

## Table of Contents
1. Database Systems. 1
2. JDBC. 15
3. Disk and File Management. 48
4. Memory Management. 79
5. Transaction Management. 105
6. Record Management. 158
7. Metadata Management. 189
8. Query Processing. 213
9. Parsing. 239
10. Planning. 267
11. JDBC Interfaces. 295
12. Indexing. 313
13. Materialization and Sorting. 363
14. Effective Buffer Utilization. 397
15. Query Optimization. 419


### Part 3 SimpleDB内部实现
第12章——磁盘及⽂件管理
第13章——内存管理
第14章——事务管理
第15章——记录管理
第16章——元数据管理
第17章——查询处理
第18章——SQL语句解析
第19章——SQL Planning
第20章——数据库服务
Part 4 ⾼效的查询处理
第21章——索引

## code
https://github.com/wdidada126/simpledb2_mvn


```Java
public class RecordFileTest {
    public static void main(String[] args) throws IOException {
        SimpleDB.init("liuzhian/simpledb");
        Transaction tx = new Transaction();
        Schema schema = new Schema();
        schema.addIntField("A");//有表结构文件的
        TableInfo tableInfo = new TableInfo("junk", schema);

        RecordFile recordFile = new RecordFile(tableInfo, tx);
        for (int i = 0; i < 10000; i++) {
            recordFile.insert();
            int n = (int) Math.round(Math.random() * 200);
            recordFile.setInt("A", n);
        }

        int cnt = 0;
        recordFile.beforeFirst();
        while (recordFile.next()) {
            if (recordFile.getInt("A") < 100) {
                recordFile.delete();
                cnt++;
            }
        }
        System.out.println("删除的记录数：" + cnt);
        // recordFile.close();
        tx.commit();
    }
}
```

## record block的关系
变长
定长

## Schema TableInfo RecordPage
public TableInfo(String tblName, Schema schema)

RecordFile 类提供的抽象级别与到⽬前为⽌我们所看到的其他类有明显不同的。 也就是说， Page ， Buffer ， Transaction 和 RecordPage 这些类的的⽅法都适⽤于特定的块。 ⽽ RecordFile 类向其客户端隐藏掉了块结构的存在。 通常，客户端将不知道（或不在乎）当前正在访问哪个块。 它只需要在完成操作后关闭记录⽂件就OK了。

## lock
s
x
锁的对象是Block

## 算法
Algorithm 14-5 事务T的回滚算法

Algorithm 14-6 恢复算法

Algorithm 14-7 Undo-only恢复下的事务提交算法
1.将事务修改的页中的内容flush到磁盘上。
2.写一条commit log record。
3.将包含日志记录的日志页flush到日志文件上。

Algorithm 14-8 redo-only恢复下的事务回滚算法
对于每个事务修改的缓冲区:
a)将缓冲区标记为未分配的。(在SimpleD中，将缓冲区的块号设置为
b)将缓冲区标记为未修改的。
c)将缓冲区取消固定。

Algorithm 14-9 执行一次静态检查算法
1.停止接受新的事务。
2.等待存在的事务完成。
3.flush所有修改的缓冲区到磁盘
4.追加一条静态检查点日志记录，并且flush到日志文件中。
5.开始接受新的事务。

14-20 锁协议
1.在读某个块前，请求获得该块的共享锁。
2.在写某个块前，请求获得该块的互斥锁。
3.在提交或回滚后释放所有获得的锁。

Algorithm 14-22 wait-die死锁检测策略
假设事务T1请求一个被事务T2持有的锁。
if(T1 is older than T2)
	T1等待该锁;
else if(Tl is newer than T2)
	T1回滚;(即die)

Algorithm 14-23 基于时间限制的死锁检测策略
假设事务T1请求一个被事务T2持有的锁。
1.事务T1等待该锁。
2.如果事务T1待在等待队列上太久，则回滚事务T1.

## 笔记
每个块有2种锁—— 共享锁shared lock(slock) 和 互斥锁exclusive lock(xlock) 。

Remote
Planner
Parse
Query
Metadata
Record
Transaction
Buffer
Log
File

Part 3 SimpleDB内部实现
第12章——磁盘及⽂件管理
第13章——内存管理
第14章——事务管理
第15章——记录管理
第16章——元数据管理
第17章——查询处理
第18章——SQL语句解析
第19章——SQL Planning
第20章——数据库服务
Part 4 ⾼效的查询处理
第21章——索引