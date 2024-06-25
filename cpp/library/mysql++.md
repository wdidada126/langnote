# mysql++

http://www.tangentsoft.net/mysql++/doc/html/userman/


安装MySQL++之前需要先安装MySQL：

[root@localhost zhxilin]# yum install mysql-devel
[root@localhost zhxilin]# 
紧接着下载MySQL++源码并解压，我们把压缩包解压到/usr/mysql++下：

[root@localhost zhxilin]# cd 下载
[root@localhost 下载]# wget http://www.tangentsoft.net/mysql++/releases/mysql++-3.2.2.tar.gz
[root@localhost 下载]# tar -zxvf mysql++-3.2.2.tar.gz -C /usr/
[root@localhost usr]# mv mysql++-3.2.2 mysql++
进入mysql++目录下，开始编译，先执行./configure生成makefile文件，之后再make，编译出libmysqlpp.so库文件：

[root@localhost mysql++]# ./configure --enable-thread-check 
[root@localhost mysql++]# make
[root@localhost mysql++]# make install


```cpp
  #include <mysql++.h>
  #include <iostream>
  
  using namespace std;
 int main()
  {
      const char* db = 0, *server = 0, *user = 0, *password = "";
      db = "test";
     server = "localhost";
     user = "zhxilin";
     password = "";
     
     mysqlpp::Connection conn(false);
     if (conn.connect(db, server, user, password)) {
         cout << "connect db succeed. " << endl;
         mysqlpp::Query query = conn.query("SELECT * FROM Student");
         if (mysqlpp::StoreQueryResult res = query.store()) {
             cout.setf(ios::left);
             cout << setw(31) << "Sid" <<
                 setw(10) << "Sname" <<
                 setw(10) << "Sage" <<
                 setw(10) << "Sgender" <<                 
                 setw(10) << "SDepartment" << endl;
 
             mysqlpp::StoreQueryResult::const_iterator it;
             for (it = res.begin(); it != res.end(); ++it) {
                 mysqlpp::Row row = *it;
                 cout << setw(30) << row[0] << ' ' <<
                         setw(9) << row[1] << ' ' <<
                         setw(9) << row[2] << ' ' <<
                         setw(9) << row[3] << ' ' <<
                         setw(9) << row[4] << ' ' <<
                         endl;
             }
         }
     } else {
         cout << "connect db fail. " << endl;
     }
     return 0;
 }

```