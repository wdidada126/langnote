# sqlpp11

## odb vs sqlpp11
SQLpp11 和 ODB 是用于 C++ 的不同类型的数据库库。两者各有特点和适用的场景，下面是对这两者的对比：

### SQLpp11

简介:
- SQLpp11 是一个 C++ 的类型安全的 SQL 查询库，它通过表达式模板生成 SQL 语句，并提供类型安全的查询接口。

特点:
1. 类型安全： 通过使用模板和表达式，SQLpp11 提供了编译时类型检查，减少了运行时错误的可能性。
2. 易用性： 其语法与 SQL 相似，使得编写和理解查询更加直观。
3. 数据库支持： 支持多种数据库后端，如 MySQL、SQLite、PostgreSQL 等。
4. 无 ORM： SQLpp11 不是一个 ORM（对象关系映射），它主要关注生成类型安全的 SQL 查询，而不涉及对象关系映射。

优点:
- 减少 SQL 注入风险。
- 提供编译时的类型检查。
- 灵活且接近 SQL 的查询语法。

缺点:
- 由于没有提供 ORM 功能，开发者需要手动进行对象与关系数据的映射。
- 需要对模板编程有一定的了解。

### ODB

简介:
- ODB 是一个 ORM 库，专为 C++ 设计，它通过编译器生成对象关系映射代码，支持多种数据库。

特点:
1. 对象关系映射： ODB 提供了从 C++ 对象到数据库表的自动映射，大大简化了数据持久化的工作。
2. 数据库支持： 支持多种数据库后端，如 MySQL、SQLite、PostgreSQL、Oracle 等。
3. 编译器支持： 通过 odb 编译器预处理源代码，生成对象关系映射代码。
4. 复杂的查询支持： 支持复杂的查询语法和高级特性，如连接、聚合等。

优点:
- 简化了对象与数据库表之间的映射。
- 提供高级的查询功能，支持复杂的数据库操作。
- 提供编译时生成代码，提高了运行时性能。

缺点:
- 学习曲线较陡，需要掌握 odb 编译器的使用。
- 生成的代码可能会增加编译时间和项目复杂度。

### 选择依据

选择 SQLpp11 的场景：
- 需要类型安全的 SQL 查询。
- 项目不需要 ORM 功能，或者开发者愿意手动进行对象与数据库的映射。
- 希望减少 SQL 注入的风险并进行编译时检查。

选择 ODB 的场景：
- 需要简化对象与数据库之间的映射。
- 需要使用 ORM 提供的高级特性和复杂查询功能。
- 希望通过编译器生成高效的数据库访问代码。

总结来说，SQLpp11 和 ODB 各有优缺点，选择时需要根据项目需求、开发团队的熟悉程度以及具体的应用场景来决定。

## sqlpp11
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

0.64 Oct 8, 2023
0.63 Jun 30, 2023
0.62 Jun 4, 2023
0.61 Dec 18, 2021

https://github.com/rbock/sqlpp11/issues/580

## code

https://github.com/edidada/yishengAttendanceData

## script
find . -name "ddl2cpp"
./.conan2/p/sqlpp36f2f4cec0df9/p/bin/ddl2cpp
./sqlpp11-0.61/scripts/ddl2cpp

/home/wdidada/sqlpp11-0.61/scripts

python ddl2cpp Student.sql ./Student TestProject

ddl2cpp tbl_night_shift.sql ./tbl_night_shift tbl_night_shift
ddl2cpp tbl_single_shift.sql ./tbl_single_shift tbl_single_shift
ddl2cpp articles.sql ./articles articles
ddl2cpp users.sql ./users users
ddl2cpp admins.sql ./admins admins