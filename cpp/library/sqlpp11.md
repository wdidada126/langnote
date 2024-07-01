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

## version
https://github.com/rbock/sqlpp11/tags

0.61
Dec 18, 2021

0.64
Oct 8, 2023

0.63
Jun 30, 2023

0.62
Jun 4, 2023


https://github.com/rbock/sqlpp11/issues/580

## code

https://github.com/edidada/yishengAttendanceData

