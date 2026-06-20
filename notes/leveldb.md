# leveldb

[level source reader](http://www.grakra.com/2017/06/17/Leveldb-RTFSC/)

单机数据库

存在读放大，写放大问题
## rocksdb

leveldb 和 rocksdb 性能对比

https://www.jianshu.com/p/7acdab85c722

单个文件
## demo
cpp写过demo
https://gitee.com/edidada/testleveldb

rocksdb对leveldb做了哪些优化？
https://www.zhihu.com/question/328622742/answer/3177961524

## doc

https://github.com/google/leveldb/tree/main/doc

https://leveldb.readthedocs.io/en/latest/

### class

ibqodeMacBook-Pro:include ibqo$ cd leveldb/
ibqodeMacBook-Pro:leveldb ibqo$ ls
c.h		db.h		export.h	options.h	table.h
cache.h		dumpfile.h	filter_policy.h	slice.h		table_builder.h
comparator.h	env.h		iterator.h	status.h	write_batch.h


level/db.h

Snapshot
Range
DB

  DB() = default;

  DB(const DB&) = delete;
  DB& operator=(const DB&) = delete;

  virtual ~DB();


在LevelDB中，DB类是一个核心的抽象类，用于表示对数据库的操作接口。你提供的代码片段展示了DB类的构造函数、拷贝构造函数、赋值运算符和析构函数的声明方式，这些都是C++类定义中的基本元素。下面我将解释每个部分的作用：

构造函数（Constructor）DB() = default;
这是一个默认构造函数，它被标记为= default;，表示编译器将自动生成一个默认的构造函数，这个构造函数不执行任何特殊的初始化操作，仅仅是将对象实例化。
拷贝构造函数（Copy Constructor）DB(const DB&) = delete;
这个构造函数被声明为= delete;，这意味着它被显式地禁止了。在C++11及以后的版本中，delete关键字可以用于禁止某些特殊成员函数的自动生成。在这个例子中，它防止了DB对象的拷贝构造，这通常是因为DB类管理了一些独特的资源（如文件句柄、内存映射等），这些资源不应该被简单地复制。
赋值运算符（Assignment Operator）DB& operator=(const DB&) = delete;
与拷贝构造函数类似，赋值运算符也被delete了。这同样是为了防止DB对象之间的赋值操作，因为这样的操作可能会导致资源管理的混乱或错误。
析构函数（Destructor）virtual ~DB();
这是一个虚析构函数，它被声明为virtual，但没有给出实现（通常会在类的实现文件中定义）。虚析构函数是多态性的一部分，它允许通过基类指针来删除派生类对象时，能够正确地调用派生类的析构函数，从而确保资源的正确释放。在DB类的上下文中，这意味着如果DB类有派生类，并且这些派生类管理了额外的资源，那么虚析构函数将确保这些资源在对象销毁时被正确清理。
总结来说，这些函数共同定义了DB类的基本行为，特别是关于对象生命周期和资源管理的方面。通过禁止拷贝和赋值操作，DB类确保了其对象的唯一性和资源的独占性，而虚析构函数则支持了多态性，允许通过基类指针安全地管理派生类对象。