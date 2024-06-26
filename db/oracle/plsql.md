# pl/sql

https://docs.oracle.com/en/database/oracle/oracle-database/19/lnpls/index.html

json pljson框架

https://www.jianshu.com/p/936e7068b019

了解了您的问题是关于PL/SQL的库，以下是一些常用的PL/SQL库和包，这些库和包可以帮助简化开发、提高效率并增强功能：
1. DBMS_STANDARD：
   - 简介：这是Oracle提供的一个基本包，包含了一些标准的PL/SQL功能，如错误处理、输出信息等。
   - 功能：例如`RAISE_APPLICATION_ERROR`用于生成自定义错误消息，`DBMS_OUTPUT.PUT_LINE`用于输出调试信息。
2. DBMS_SQL：
   - 简介：这是一个用于动态SQL处理的包，允许在运行时构建和执行SQL语句。
   - 功能：支持动态构建和执行SQL语句，查询结果集处理等。
3. DBMS_JOB：
   - 简介：这是一个用于作业调度的包，允许在数据库中调度和管理作业。
   - 功能：创建、运行和管理定时作业。
4. DBMS_SCHEDULER：
   - 简介：这是一个更现代的作业调度包，提供了比DBMS_JOB更强大的功能。
   - 功能：支持复杂的调度规则、窗口管理、资源管理等。
5. DBMS_LOB：
   - 简介：这是一个用于处理大对象（LOB，如CLOB和BLOB）的包。
   - 功能：提供了对LOB的读写操作、剪切、拼接、比较等功能。
6. DBMS_STATS：
   - 简介：这是一个用于收集数据库统计信息的包，有助于优化查询性能。
   - 功能：收集和管理表、索引等对象的统计信息，分析数据分布，支持优化器。
7. UTL_FILE：
   - 简介：这是一个用于文件操作的包，允许PL/SQL程序读写操作系统文件。
   - 功能：提供了文件的打开、读取、写入和关闭等功能。
8. HTP 和 HTF：
   - 简介：这是两个用于生成HTML输出的包，通常用于构建Web应用程序。
   - 功能：提供生成HTML元素的方法，如表格、链接、表单等。
9. OWA_UTIL：
   - 简介：这是一个常用的实用工具包，提供了一些辅助功能。
   - 功能：如生成唯一标识符、格式化日期和数字、获取环境变量等。
10. DBMS_CRYPTO：
    - 简介：这是一个用于加密和解密数据的包。
    - 功能：支持数据加密、解密、哈希等操作。

这些库和包提供了丰富的功能，帮助开发人员在PL/SQL中实现复杂的业务逻辑、优化性能和增强应用程序的功能。

Oracle 工具

面向过程的(可以加入业务需要的逻辑)

增强SQL

既可以单独执行，也可以Java代码调用执行

plsql跟sql对比
sql面向结果集
不能单独执行

[如何配置PL/SQL Developer，以及连接Oracle数据库](https://zhuanlan.zhihu.com/p/85631865)

https://www.oracle.com/database/technologies/appdev/plsql.html

在PL/SQL开发中，一些常用的框架和工具可以帮助提高开发效率、代码质量和项目管理。以下是一些常见的PL/SQL框架和工具：

1. Oracle APEX（Application Express）：
   - 简介：Oracle APEX是一个基于Web的开发环境，允许开发人员快速构建和部署数据驱动的应用程序。
   - 特点：支持快速应用开发、内置数据报表和图表、用户友好、易于使用、与Oracle数据库无缝集成。
2. PL/SQL Developer：
   - 简介：PL/SQL Developer是Allround Automations公司开发的一个集成开发环境（IDE），专门用于PL/SQL的开发。
   - 特点：提供代码编辑器、调试器、测试工具、SQL窗口和命令窗口，支持代码模板、版本控制、代码分析等功能。
3. SQL*Plus：
   - 简介：SQL*Plus是Oracle数据库提供的一个命令行工具，用于运行SQL和PL/SQL命令。
   - 特点：适合脚本编写和批处理任务，可以与其他工具和脚本语言集成，执行SQL和PL/SQL语句。
4. TOAD for Oracle：
   - 简介：TOAD（Tool for Oracle Application Developers）是Quest Software开发的一个综合性开发工具。
   - 特点：提供强大的SQL和PL/SQL编辑功能、调试工具、代码分析、数据库管理、数据建模等功能，适合大型项目开发和数据库管理。
5. SQL Developer：
   - 简介：SQL Developer是Oracle公司提供的一个免费的集成开发环境，用于数据库开发和管理。
   - 特点：支持SQL和PL/SQL编辑、调试、数据库设计、数据迁移、报表生成、版本控制等功能，用户界面友好。
6. utPLSQL：
   - 简介：utPLSQL是一个用于PL/SQL单元测试的开源框架，类似于JUnit用于Java单元测试。
   - 特点：提供自动化测试功能，支持测试用例编写、测试结果报告、集成CI/CD（持续集成/持续交付）流程，有助于提高代码质量和可靠性。
7. ODC（Oracle Data Cartridge）：
   - 简介：Oracle Data Cartridge框架允许开发人员创建定制的数据类型和索引。
   - 特点：适合处理复杂数据类型和大数据量应用，增强了Oracle数据库的扩展性和灵活性。

通过使用这些框架和工具，PL/SQL开发人员可以提高开发效率、增强代码质量、简化项目管理，并更好地集成和管理数据库应用程序。

table function

PL/SQL（Procedural Language/Structured Query Language）比SQL（Structured Query Language）更高明的地方主要在于它增加了程序化特性和更强大的功能。以下是几方面的对比：
1. 程序化特性：
   - 控制结构：PL/SQL支持循环（如`FOR`、`WHILE`循环）和条件判断（如`IF-THEN-ELSE`），使得编写复杂逻辑变得可能。而SQL本身只支持基本的查询、插入、更新和删除操作，没有程序化的控制结构。
   - 异常处理：PL/SQL提供了异常处理机制，可以捕获和处理运行时错误，提高了程序的鲁棒性。SQL不具备这种能力。
   - 变量和常量：PL/SQL允许在程序中声明变量和常量，可以存储和操作数据，而SQL不支持直接的变量声明。
2. 模块化编程：
   - 过程和函数：PL/SQL支持创建存储过程和函数，方便代码重用和模块化管理。一个复杂的业务逻辑可以分解为多个小的过程和函数，提高了代码的可读性和可维护性。
   - 包（Packages）：PL/SQL中的包允许将相关的过程、函数、变量和游标等组合在一起进行管理，增强了代码组织和封装。
3. 性能和效率：
   - 批量处理：PL/SQL支持批量处理数据，减少了SQL和数据库之间的通信开销，提高了执行效率。例如，使用PL/SQL的批量插入可以显著快于单条SQL语句逐条插入。
   - 触发器：PL/SQL支持触发器，可以在特定事件（如插入、更新、删除）发生时自动执行定义好的PL/SQL代码，增强了数据的自动化管理能力。
4. 集成性：
   - 与数据库的集成：PL/SQL是Oracle数据库专有的扩展语言，深度集成在Oracle数据库中，利用Oracle的优化器和其他特性，提供了高效的执行性能。

总之，PL/SQL通过引入程序化特性和模块化管理，增强了SQL的功能，使得开发者可以编写更加复杂和高效的数据库应用程序。