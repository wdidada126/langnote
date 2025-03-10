# drogon

学sprigmvc的，控制器自动发现

testdrogon

    message(FATAL_ERROR "c++17 or higher is required")
有命令行工具

依赖jsoncpp

#include <drogon/orm/DbClient.h>

## 配置项目
    drogon::app().loadConfigFile("config.json");

    app().loadConfigFile("./config.json").run();

## vcpkg
vcpkg search drogon
drogon                   1.9.10           A C++14/17 based HTTP web application framework running on Linux/macOS/Uni...
drogon[ctl]                               Build drogon_ctl tool.
drogon[mysql]                             Support reading and writing from/to MySQL databases.
drogon[orm]                               Build with object-relational mapping support.
drogon[postgres]                          Support reading and writing from/to Postgres databases.
drogon[redis]                             Support reading and writing from/to Redis databases.
drogon[sqlite3]                           Support reading and writing from/to SQLite databases.
drogon[yaml]                              Support YAML Drogon configuration files

vcpkg install jsoncpp:x64-windows zlib:x64-windows openssl:x64-windows sqlite3:x64-windows libpq:x64-windows libpqxx:x64-windows libmariadb drogon[core,ctl,sqlite3,postgres,mysql,orm]:x64-windows --recurse


 .\drogon_ctl.exe version
     _
  __| |_ __ ___   __ _  ___  _ __
 / _` | '__/ _ \ / _` |/ _ \| '_ \
| (_| | | | (_) | (_| | (_) | | | |
 \__,_|_|  \___/ \__, |\___/|_| |_|
                 |___/

A utility for drogon
Version: 1.9.10
Git commit:
Compilation:
  Compiler: cl.exe
  Compiler ID: MSVC
  Compilation flags: /MD /O2 /Oi /Gy /DNDEBUG /Z7  -std=c++20 -ID:/develops/tools/vcpkg/installed/x64-windows/include -ID:/develops/tools/vcpkg/packages/drogon_x64-windows/include
Libraries:
  postgresql: yes  (pipeline mode: yes)
  mariadb: yes
  sqlite3: yes
  ssl/tls backend: OpenSSL
  brotli: yes
  hiredis: no
  c-ares: yes
  yaml-cpp: no


     _
  __| |_ __ ___   __ _  ___  _ __
 / _` | '__/ _ \ / _` |/ _ \| '_ \
| (_| | | | (_) | (_| | (_) | | | |
 \__,_|_|  \___/ \__, |\___/|_| |_|
                 |___/
A utility for drogon
Version: 1.9.10
Git commit: cbf63f8fc4d849bbb82eeb1c83fcf8ff953f19f3
Compilation: 
  Compiler: c++
  Compiler ID: GNU
  Compilation flags: -std=c++17 -I/usr/include/jsoncpp -I/usr/local/include
Libraries: 
  postgresql: yes  (pipeline mode: yes)
  mariadb: yes
  sqlite3: yes
  ssl/tls backend: OpenSSL
  brotli: yes
  hiredis: yes
  c-ares: yes
  yaml-cpp: yes
