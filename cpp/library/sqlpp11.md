# sqlpp11

SQLPP11确实是一个头文件(header-only)库。这意味着它不需要编译成静态或动态链接库,而是通过包含相应的头文件即可在您的项目中使用。

## doc
https://github.com/rbock/sqlpp11/blob/main/docs/Home.md

## windows
vcpkg install sqlpp11

sqlpp11 provides CMake targets:
    # this is heuristically generated, and may not be correct
    find_package(Sqlpp11 CONFIG REQUIRED)
    target_link_libraries(main PRIVATE sqlpp11::sqlpp11)

0.61
