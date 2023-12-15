# gflag


读取命令行参数的

https://github.com/edidada/rest_description/tree/mysql_local/unittest

command.flags
配置项

```cpp
#include <gflags/gflags.h>
#include <iostream>
#include <stdio.h>

DEFINE_string(host, "127.0.0.1","the database server host");
DEFINE_string(user, "John","the database server paassword");
DEFINE_string(pwd, "12345678","the database password");
DEFINE_string(db_name, "db_blog","the database name");
DEFINE_string(thread_umber, "2","the server thread number");
DEFINE_int32(server_port, 9081, "the server port");

using namespace std;
int main(int argc, char *argv[]) {
        gflags::ParseCommandLineFlags(&argc, &argv, true);
        cout<<(FLAGS_host)<<endl;
        cout<<(FLAGS_user)<<endl;
        cout<<(FLAGS_pwd)<<endl;
        cout<<(FLAGS_db_name)<<endl;
        cout<<(FLAGS_thread_umber)<<endl;
        cout<<(FLAGS_server_port)<<endl;
}
```