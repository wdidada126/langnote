# 10 · 消息总线库与 SQLite 封装 SmartDB（原书第 12、13 章）

> 覆盖原书第 12 章（12.1 介绍 / 12.2 通用消息定义、注册、分发、设计思想 / 12.3 完整总线 / 12.4 实例）
> 与第 13 章（13.1 sqlite / 13.2 rapidjson / 13.3 SmartDB 各接口 / 13.4 实例）。
> 两章同属"包装第三方库 + 注册分发底座"，合并为一个文件。
> 大纲形态见 [../深入应用C++11.md](../深入应用C++11.md)；返回 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 核心概念速览（中英对照）

- **消息总线** — message bus：按主题解耦的发布/订阅设施，生产者与消费者互不知名。
- **通用消息定义** — generic message：payload 类型擦除（tuple/any）后的统一消息形态，跨模块传值的通行证。
- **注册与分发** — register / dispatch：主题字符串→handler 函数向量的两级 map，分发即查表调用。
- **发布订阅 vs 点对点** — pub/sub vs P2P：广播语义与定向语义的取舍，本书总线以前者为主。
- **SQLite C API** — sqlite3 / sqlite3_stmt / sqlite3_exec：三步句柄协议（open-prepare-step-finalize），裸指针密集区。
- **RAII 事务** — RAII transaction：BEGIN/COMMIT 包进析构协议，异常路径自动 ROLLBACK（ScopeGuard 的近亲应用）。
- **JSON DOM/SAX** — rapidjson Document vs Handler：SmartDB 用 DOM 把行序列化成 JSON 输出。
- **ExecuteTuple** — 书中查询接口：一行 = 一个 tuple，列访问从魔数索引 `get_int(0)` 变成类型化 `std::get<T>`。
- **SQL 注入防线** — prepared statement + 参数绑定：SmartDB 接口设计的第一约束。

## 一、动机：对象间通信与数据落盘是库的地基两件套

第 12 章回答"模块 A 怎么不认识模块 B 地把事件扔出去"；第 13 章回答"怎么把一个以裸指针
和返回码为语言的 C 库（sqlite）改造成 C++11 语言"。前者复用 [09 章](09-AOP库与IoC容器.md)
的注册表+类型擦除底座（cosmos 的 `MessageBus.hpp`），后者复用 [04 章](04-智能指针与内存管理.md)
的删除器协议与 [03 章](03-type_traits与可变参数模板.md) 的 tuple 工具。

## 二、机制

### 2.1 总线：两级 map + 一次擦除
`map<主题, map<订阅者id, function<void(Message)>>>`；消息 payload 用 tuple/any 擦成同构值，
订阅端再按约定还原。要点三条：① 反注册凭 id（[07 章](07-C++11重思设计模式.md) token 协议同款）；
② 分发线程模型（同步直调 or 投递到 [08 章](08-半同步半异步线程池.md) 池）决定库的并发契约——
书版是同步直调，"线程安全留白"是它最容易被误读的点；③ 回调重入（handler 里 publish 同主题）
要快照式遍历。实测的三线程序：publish 一次、两个 lambda 观察者都收到 `order#123`。

### 2.2 SmartDB：C API 的 C++11 化四板斧
```text
句柄   → unique_ptr + 成对删除器（sqlite3*/sqlite3_stmt*）
错误码 → 检查点转异常（或 expected，见演进节）
查询行 → tuple + 递归列读取器（实测 11 档：1| sqlite-row|3.5|）
事务   → RAII 包装 BEGIN/COMMIT/ROLLBACK，异常即回滚
```
13.3.6 的 JSON 接口把行序列化成 rapidjson 文档：`Document d(kObjectType); d.AddMember(...)`
逐列写入——SmartDB 因此同时是 ORM 雏形与"行即文档"的早期中文实践。rapidjson 的
`alloc` 生命周期绑定 Document 是当年踩坑点（拷贝 Document 深拷、跨 allocator 引用悬垂）。

### 2.3 tuple 行的类型学
`std::tuple<int,string,double>` 行 vs `vector<Column>`：编译期列类型已知 → `get<T>` 按**类型**取列
（重复列类型退化按序取）；运行期 schema 未知 → 只能 Variant/any 列。书选前者，代价是 SELECT *
的列序耦合——14 年后这题由结构化绑定 + 反射提案继续作答（见演进节）。

### 2.4 分发的生命周期协议（总线最容易埋雷的一层）
① **注册即拷贝**：handler 进 `function` 时闭包按值切片，捕获的 `this` 是否仍有效总线无权知道——
悬垂纪律与 [07 章](07-C++11重思设计模式.md) 观察者完全同款，token 反注册或 weak 升锁二选一。
② **分发期重入**：handler 内 `subscribe/unsubscribe` 同一表 = 遍历中修改容器；工程解是
"分发持快照，变更走延迟队列"——书版同步直调把这层留白，复刻时不要连留白一起抄。
③ **消息序≠因果序**：多主题交叉时总线只保证"同 handler 串行收到"，跨主题顺序要显式收敛
（单队列串行分发是书版事实上的保护伞，换线程池分发即失去它——08 章自死锁纪律一并生效）。

## 三、权衡与实战提示

- 总线的字符串主题=无类型协议：拼写错误运行期才炸；项目上建议枚举/强类型主题包装。
- 同步总线里的慢 handler = 全链路延迟传染；要隔离就上队列（即"从库模式"改"异步模式"）。
- SmartDB 的删除器必须与 sqlite 的分配协议成对：`sqlite3_free` 释放 `errmsg` 等 API 约定要逐条对表。
- 主题命名建议带版本号（`order.created.v1`）：总线无 schema 检查，消费者演进只能靠命名自保——
  这是工业消息系统（如各类 service bus）用血换来的约定，书版留白处恰是工程必答题。

## 四、相邻概念对比

| 对比 | 差异一句话 |
| --- | --- |
| 消息总线 vs 观察者模式 | 模式是类协作，总线是模块协作加进程内寻址（主题路由）；总线常以观察者实现 |
| any payload vs tuple payload | 完全开放类型 vs 封闭列集；SmartDB 选 tuple，总线选"结构 + function" |
| rapidjson vs 手写序列化 | DOM 便捷 + allocator 纪律 vs 零依赖但重码 |
| RAII 事务 vs ScopeGuard | 同一思想的两实现：析构即退出协议 |
| prepared 绑定 vs 字符串拼 SQL | 前者把"数据"与"代码"在协议层分开（注入防线 + 计划缓存），后者两层事故都要付 |

## 五、实测（🔧 三档：g++ 15.2，gnu++11/17/23，`ch10.cpp`）

```text
gnu++11: OK  mailer: order#123 / audit : order#123 / C++11 recursive row: 1| sqlite-row|3.5|
gnu++17: OK  追加 bindings: 1  sqlite-row 3.5 / 1  sqlite-row 3.5 via apply
gnu++23: OK  同 17
```

- C++11 档的递归模板 `print_row`（enable_if 双版本）与 C++17 档的一行 `std::apply + 折叠` 输出等价——
  书 13.3.5 的实现今天可以删掉三页代码。
- sqlite/rapidjson 属第三方 C 库，本次按机制复刻（tuple 行/分发树）而未链接真实库——
  接口协议层结论不受影响，真实链接验证 ⚠️ 未做。
- 两个观察者（mailer/audit）同一次 publish 均收到 `order#123`：同步总线"逐 handler 串行调用"的
  分发语义实测成立——这也是 2.4 节"快 handler 传染全链路"警告的另一面。

## 六、最新演进与工业实践

- **C++17**：`std::any` 成为 payload 标准形态（03 章）；`string_view` 让主题路由零拷贝；
  `std::apply/get<I>` 全面接管 tuple 行。
- **C++20/23**：`std::expected<T, E>`（P0792R14 实测解析）为 SmartDB 类 API 给出"返回码→类型化错误"
  的当代答案（SQLite 错误码 + 消息可编进 `expected<Row, SqliteError>`）；ranges 让 handler 遍历协议化。
- **反射远景**：C++ 静态反射仍在提案路上（std::reflect 系，Einar Schäfer 等推进，目标 C++26/29 ⚠️
  提案号未逐一实测），列类型自动映射这题 2026 年仍靠宏/代码生成（magic_enum、SQLpp 等）。
- **案例库现状对账（本次实测）**：
  - **SQLite**：官方 sqlite.org 当前版本 **3.53.4**（2026-09 实测页面），API 向后兼容策略未变——
    书 13.1 的代码今天仍可编译，SmartDB 的教训依旧有效。
  - **rapidjson**：[Tencent/rapidjson](https://github.com/tencent/rapidjson) 实测最新 release 停在
    v1.1.0（2016-08），最后一次 push 2025-02、未归档——**事实上的维护模式**；社区主流转向
    [nlohmann/json](https://github.com/nlohmann/json)（实测 2026-09：约 5 万 star，当周仍有 push）
    与 SIMD 系解析器。书中 13.2 的 API 细节今天多需换写法。
  - **嵌入式存储对照**：Google leveldb 经 API 实测最新 release 1.23（2021-02），基本冻结；
    其精神续接收束于 RocksDB 与 abseil 工具链——本书读者若按 [../精通LevelDB.md](../精通LevelDB.md)
    的路径读源码，注意版本代际。
- **消息总线的工业化**：进程内总线在 2026 年的标准形态是各类 `EventBus`/中间件链
  （Qt 信号槽、Godot 信号、EnTT 事件），核心三件（主题路由/类型擦除/反注册）与本章设计一一对应。

## 七、交叉互链

- 大纲：[../深入应用C++11.md](../深入应用C++11.md)；总索引：[../C++系列·总索引.md](../C++系列·总索引.md)
- 上游章：[09 章注册表底座](09-AOP库与IoC容器.md)、[04 章删除器托管](04-智能指针与内存管理.md)、[03 章 tuple/ScopeGuard](03-type_traits与可变参数模板.md)
- 并发衔接：[08 章线程池（异步分发器）](08-半同步半异步线程池.md)
- 教程线：[../现代C++实战30讲/15-REST-SDK与网络应用.md](../现代C++实战30讲/15-REST-SDK与网络应用.md)（序列化/落盘的同题现代解）、[../C++标准库/08-特殊容器与字符串.md](../C++标准库/08-特殊容器与字符串.md)
- 对象模型：[../深度探索C++对象模型/03-Data语意学.md](../深度探索C++对象模型/03-Data语意学.md)（tuple 布局的机制解释）
- 辨析：[../C++实战.md](../C++实战.md)
