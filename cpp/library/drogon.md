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
.\vcpkg.exe install jsoncpp:x64-windows zlib:x64-windows openssl:x64-windows sqlite3:x64-windows libpq:x64-windows libpqxx:x64-windows libmariadb drogon[core,ctl,sqlite3,postgres,mysql,orm]:x64-windows --recurse


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


