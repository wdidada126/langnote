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

