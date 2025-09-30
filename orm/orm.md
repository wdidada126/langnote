# orm

java模板，java.sql里面有异常，需要try catch 用模板替换调

以前数据库是按照cpu核心和连接数收费的，数据库网络连接是重要资源，连接需要复用。数据库连接数又上限，不能无限制扩容，连接池

hibernate，直接根据java bean直接新建表

数据库类型和java类型不完全一样，需要转换，mybatis一堆数据类型处理器 handler

mybatis，根据谓词动态生成sql，但是还要写sql
https://www.zhihu.com/question/345039462/answer/822447793

我也用过 mysql++ 很久。可以通过宏等方式绑定结构体(struct)什么的，但有几个坑 ，包括连接池有线程问题，我自己就提交过两个fix（其一被采纳，后因沟通不是太畅，所以就放弃提交）。
后来自己撸了一个结构化绑定，但感觉用宏用得太多，弃用。终于改用 sqlpp11。它的思路是你创建好数据库或表，然后导出DDL，用它提供的py工具，生成一C++代码。很是方便。然后基本就脱离 手写SQL（包括字段字称，表名称）的 过往了，在IDE里，基本完全靠IDE提示各类字段。比如，先来看一段简单的：

```cpp

    d2v2::Article t;  //表
    unsigned long long uid = std::stoull(id);
    auto rows = db(select(t.id, t.title
                          , t.author, t.ctime, t.utime
                          , t.summary, t.content)
                   .from(t)
                   .where(t.id == uid));
    one = d2db::ConvertOne<Content>(rows);

```

当你在编辑器输入 “t.”，IDE就会自动提示该表实际存在的 id, title, author等字段名。

其实我并不喜欢完全的ORM，因一张表有许多字段，但并不是每次select都需要全部字段的。

ConverOne<T>（）是我简单写的一个函数模板。用来快速将rows转换成std::vector<T>一类的，基于STL的数据。

sqlpp11支持挺全面的标准SQL语法（当然，并不完全支持，但平常我们直接写sql，也不会用全）。以查询为例，支持连接查询，子查询等。

来一个带有稍微复杂条件，以及结果排序的查询：

```cpp

    d2v2::Department t;
     
    auto rows = db(select(t.id, t.name, t.title, t.category
                          , t.dependence, t.video, t.summary, t.content
                          , t.courseCount, t.publicedCount, t.finishedCount, t.topview
                          , t.ctime, t.utime)                  
                    .from(t)
                    .where(t.topview > 0)
                  .order_by(t.ctime.asc())
                    .limit(10u));

    mr = d2db::ConvertMulti<Department>(rows);

```

带join的例子，顺便演示如何先生成“Statement/语句”，再执行：

```cpp

    d2v2::Article a;   //表1
    d2v2::TopArticles ta;   //表2

    auto stat = sqlpp::select().columns(a.id, a.title,
                                        a.course, a.category,
                                        a.author, a.video, a.vminutes, a.minutes,
                                        a.summary, a.preface,
                                        a.ctime, a.utime)
                .from(ta.join(a).on(ta.article == a.id and ta.module == "one_minute"))
                .unconditionally()
.order_by(ta.topi.desc())
.limit(3U);

    auto rows = db(stat);
    mr = d2db::ConvertMulti<article::Summary>(rows);

```

以上是Select，来个插入：

```cpp

d2db::InsertResult Insert(da4qi4::Context ctx, Course const& course)
{
    d2db::ScopedConnection sc(model::DBC(ctx));
    sqlpp::mysql::connection& db(*sc);

    d2db::InsertResult ir;

    db_try

    d2v2::Course t;
    ir.insert_id = db(insert_into(t).set(
                                  t.name = course.name,
                                  t.title = course.title,
                                  t.category = course.category,
                                  t.gradelevelTip = sqlpp::tvin(course.gradelevel_tip),
                                  t.dependence = sqlpp::tvin(course.dependence),
                                  t.achievement = sqlpp::tvin(course.achievement),
                                  t.summary = course.summary,
                                  t.shortSummary = sqlpp::tvin(course.short_summary),
                                  t.content = sqlpp::tvin(course.content),
                                  t.listIndex = course.list_index,
                                  t.video = sqlpp::tvin(course.video)));
    db_catch(ir.exception)

    if (ir.HasError())
    {
        ctx->Logger()->error("Insert course fail. {}. {}.", course.name, ir.exception);
    }

    return ir;
}

```

其中间的“tvin”等函数，用于处理SQL中 有NULL，C++没有原生该类型的处理。所有c++对sql的封装都一样要面对这些，但在sqlpp11，也可以在定义表时设置某个非“NOT NULL”的字段，如果其插入值是空串，就直接将它当数据库中的NULL处理；说这些细节，是为了表明这些坑sqlpp11都已经填了。事实上我自己在写orm时，也埋过，想想还是直接用别人的成果更好。

jdbctemplate

mybatis
