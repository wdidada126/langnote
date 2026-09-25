# 讲 27｜C++ REST SDK：使用现代 C++ 开发网络应用

> **一句话**：网络编程的难点从来不是「把一个 HTTP 请求发过去」，而是**在异步、回调、异常与生命周期之间保持秩序**——C++ REST SDK 正是为了这件事而存在，但它也暴露了 C++ 缺少标准网络库的长期代价。

---

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| C++ REST SDK 是什么 | Casablanca 的后续，`microsoft/cpprestsdk` | 提供 URI 构建、`http_client`/`http_listener`、JSON、流与取消 |
| 异步模型：pplx::task | 任务与延续链、与 `std::future` 的桥接 | Continuation 风格避免「回调地狱」 |
| 错误处理 | `http_exception`、状态码、`error_code` | 网络错误应作为「可预期失败」上报 |
| JSON 与流式数据 | `json::value`、流（文件/内存/upstream） | 大响应要流式处理 |
| 服务端与取消 | `http_listener`、`cancellation_token` | 取消的传播是接口设计的一部分 |
| 现实中的局限 | HTTP/1.x 为主、HTTPS 依赖 OpenSSL、维护状态 | 对现代协议与性能的诉求需要别的方案 |
| 2026 年的替代与补充 | Boost.Beast、Drogon、cpp-httplib、POCO、uWebSockets | 按需求选：协议/性能/易用性各有胜场 |
| 🔧 现代补充 | 标准网络库仍未落地、HTTP/3、TLS 配置 | 「C++ 没有标准网络库」这件事在 2026 年依然成立 |

---

## 核心精讲

> 以下均为**教学示意，不参与构建**。

### 1. 一次异步 HTTP 请求的最小形态

```cpp
// 教学示意：C++ REST SDK 的异步风格（不参与构建）
#include <cpprest/http_client.h>
using namespace web::http;
using namespace web::http::client;

client_configuration cfg;                        // 代理、超时、TLS 选项都在这里
http_client client(U("https://example.com/api"), cfg);
http_request req(methods::GET);
req.set_response_stream(memory_stream());        // 流式接收大响应

client.request(req)
    .then([](http_response response) {           // 延续：拿到响应
        if (response.status_code() != 200) {
            return task_from_exception<VECTOROFBYTE>(http_exception(response.status_code()));
        }
        return response.extract_vector();
    })
    .then([](std::vector<unsigned char> body) {  // 延续：拿到正文
        log_body(body);
    })
    .wait();                                     // 或用 .get() 同步等待（阻塞）
```

三件必须知道的事：

1. **`.then()` 的返回值决定下一步收到什么类型**——这是「延续链」的核心；
2. **`wait()` 与 `get()` 会阻塞**：在 GUI/IO 线程里调用会卡住，应该把同步边界收在某一层；
3. **异常沿延续链传播**：未捕获的异常会让任务进入「已取消/已失败」状态，`.get()` 时重新抛出。

### 2. 错误处理：把网络失败当成「正常分支」

```cpp
// 教学示意：错误分支（不参与构建）
try {
    auto body = client.request(req)
                      .then([](http_response r) { return r.extract_string(); })
                      .get();                    // 网络异常在这里抛出
    use(body);
} catch (const http_exception& e) {
    log("http failed: {} status={}", e.what(), e.error_code().value());
} catch (const std::exception& e) {
    log("unexpected: {}", e.what());
}
```

> 与讲 22 的立场一致：**网络超时、连接拒绝、限流返回 429 都属于「可预期失败」**，应作为返回值/错误码处理；真正的「不可预期」才是异常。

### 3. 服务端的一行示例

```cpp
// 教学示意：http_listener（不参与构建）
http_listener listener(U("http://localhost:8080/api"), cfg);
listener.support(methods::GET, [](http_request request) {
    json::value reply;
    reply["status"] = "ok";
    request.reply(status_codes::OK, reply);        // 异常会自动变成 500
});
listener.open().wait();
```

### 4. 与 `std::future` 的桥接

```cpp
// 教学示意：把延续链接回标准库（不参与构建）
std::future<std::string> fetch(std::string url) {
    std::promise<std::string> p;
    http_client client(url);
    client.request(methods::GET)
          .then([p](http_response r) mutable {
              if (r.status_code() == 200) { p.set_value(r.extract_string().get()); }
              else { p.set_value({}); }            // 或 set_exception(http_exception{...})
          })
          .wait();                                 // 注意：这里拿了内部线程
    return p.get_future();
}
```

> 这类桥接代码最容易出的 bug，是**在线程池线程里调 `wait()`** 造成线程饥饿；更稳妥的做法是让框架独占调度，不要把同步等待嵌进延续链。

### 5. 现实位置的评估

| 维度 | cpprestsdk | 备注 |
| --- | --- | --- |
| 协议覆盖 | HTTP/1.x、WebSocket（部分平台） | HTTP/2 与 HTTP/3 缺失 |
| 依赖 | OpenSSL / Windows 平台原生栈 | 打包是部署的额外工作 |
| 异步模型 | `pplx::task` + 延续 | 与现代 `future`/协程仍有互操作成本 |
| 维护状态 | 持续维护但更保守 | 新项目应评估最新的活跃度 |
| 易用性 | 中上：URI/JSON/流都封装好了 | 适合快速搭内部服务与集成脚本 |

```cpp
// 教学示意：其他常见路线的形态（不参与构建）
// Boost.Beast：基于 Asio，接近裸 HTTP/1 与 WebSocket，适合要握 protocol 细节的场景
// Drogon / Crow：现代 C++ 的 Web 框架，路由与中间件齐全
// cpp-httplib：单头文件，做内部工具最省事
// POCO：更完整的框架化解决方案（网络 + 文件系统 + 数据库 + 日志）
```

### 6. 必须处理的几个工程细节

1. **TLS 配置**：证书验证、SNI、代理设置要在 `client_configuration` 里显式给出，不要依赖默认行为；
2. **连接池与超时**：默认超时常常太长或太短，必须按业务设定，并区分「连接超时」与「读取超时」；
3. **重试要幂等**：只对 `GET` 与明确幂等的接口自动重试，并加上退避；
4. **取消**：长时间下载要能被取消，取消必须沿异步链一路传到底层 socket。

---

## 版本演进

| 版本 | 变化 |
| --- | --- |
| 2011 | Casablanca（微软研究项目）发布，C++ REST SDK 的前身 |
| 2015+ | 以 `microsoft/cpprestsdk` 名义开源，跨平台（Windows/Linux/macOS/Android/iOS） |
| C++11/14 | 库本身即基于当时的现代 C++（右值、lambda、RAII）编写 |
| C++17/20 | 使用它的项目逐步迁移到 C++17/20，但库内部的异步模型仍以 `pplx::task` 为主 |
| 2020s | 网络库提案（Networking TS / 标准网络库）反复被推迟，**C++ 至今没有标准网络库** |
| **C++23** | 标准库仍不含网络；`std::expected` 改变了错误处理的写法，但网络层的抽象仍由第三方承担 |
| 2026 | 生态重心转向 Boost.Asio/Beast 与各类现代框架；HTTP/3 生态由_QUIC 实现方主导 |

---

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| RFC 9110 *HTTP Semantics* | **IETF, 2022** | 方法、状态码、缓存语义的现代定义 |
| RFC 6749 *OAuth 2.0* | **IETF, 2012** | 授权流程，几乎所有 HTTP 客户端都要处理的主题 |
| ISO/IEC 14882 | C++ 标准 | 目前**没有**网络库条款——这正是本章所有替代方案的共同背景 |
| `microsoft/cpprestsdk` 官方 Wiki | 仓库文档 | 异步模型、取消令牌与跨平台差异的第一手说明 |
| Williamson, *Network Programming with OpenSSL* / OpenSSL 文档 | **O'Reilly / openssl.org** | TLS 配置细节 |

---

## 近年研究与工业界开源实践（2015–2026）

- **C++ 标准网络库仍未落地**：这是 C++ 长期被吐槽的结构性缺口；实践上，Boost.Asio 是异步 I/O 的准标准。
- **HTTP/2 与 HTTP/3 的生态错位**：cpprestsdk 停留在 HTTP/1.x，而新服务普遍要 HTTP/2；工业项目要么上 Beast，要么直接用 Go/Rust 侧网关。
- **异步与生命周期**：回调里捕获 `this`、捕获引用是内存安全事故的主要来源；2026 年的推荐做法是「捕获值或 `weak_ptr`，并在回调入口校验」。
- **协程时代的接口重构**：当项目引入 C++20 协程后，异步 HTTP 调用可以写成同步的样子，这反过来要求库提供 `awaitable` 接口——这是第三方网络库下一步的演进方向。
- 🔧 **没有标准网络库的代价被反复计价**：跨语言互操作（ABI）、TLS 配置差异、打包（OpenSSL 版本）是三层隐性成本，选型时应把它们算进去。
- 🔧 **`std::expected` 与网络错误**：第三方库开始提供「返回 `expected<Response, http_error>`」的路线，避免异常穿越线程与 C ABI 边界。

| 仓库 | star | 说明 |
| --- | --- | --- |
| `microsoft/cpprestsdk` | **8.2k★** | 讲 27 的主角 |
| `boostorg/asio` | **1.6k★** | 异步 I/O 的准标准，多数网络库的底座 |
| `fmtlib/fmt` | **25.8k★** | 日志与错误信息的格式化 |
| `microsoft/vcpkg` | **27.5k★** | 引入 TLS/OpenSSL 等依赖的跨平台方案 |
| `google/benchmark` | **10.4k★** | 给 HTTP 客户端写吞吐基准 |

---

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「`.get()` 只是 convenience，没关系」 | 在 IO 线程或线程池里 `.get()`/`.wait()` 会造成线程饥饿与卡顿；同步边界要收在一处 |
| 2 | 「网络异常就该往上抛」 | 超时、限流、连接拒绝是可预期失败；应作为返回值处理或转成业务错误码 |
| 3 | 「默认值够用了」 | 超时、代理、TLS 校验、重试策略都必须显式配置，且要区分连接超时与读取超时 |
| 4 | 「回调里捕获 `this` 最方便」 | 对象可能先于回调完成被销毁；用值捕获或 `weak_ptr`，并在入口校验 |
| 5 | 「HTTP/1.1 永远够用」 | 现代服务普遍要 HTTP/2/3、连接池与流水线；选型时要确认协议支持 |
| 6 | 🔧 本讲只覆盖了一个特定的第三方库 | 2026 年的做法是先确定「要不要框架」，再在 Boost.Beast / Drogon / httplib / POCO 之间按需求选，而不是默认沿用旧栈 |
| 7 | 🔧 未提 C++20 协程与异步接口的融合 | 协程落地后，异步 HTTP 调用可以写成 `co_await`，但前提是库提供 `awaitable` 接口——这是选择网络库的新标准 |
| 8 | 🔧 缺少「安全」视角 | 证书校验必须开启、回调与 URL 要防注入、不要把请求体原样打进日志（与讲 26 的脱敏要求一致） |

---

## 与其他章 / 其他书的联系

- **`09-函数对象lambda与函数式编程.md`**：延续链（`then`）就是函数式组合子在异步场景的应用。
- **`02-自己动手实现智能指针.md`**：回调捕获 `shared_ptr`/`weak_ptr` 的生命周期问题。
- **`05-异常与错误处理的现代化.md`**：`http_exception` 与 `std::error_code` 的取舍。
- **`11-thread与future及内存模型.md`**：取消令牌与线程协作。
- **`13-数字计算与Boost.md`**：Boost.Asio/Beast 是同族方案，可对照。
- **`16-未来篇Concepts-Ranges-协程.md`**：协程与 executors 将直接影响异步网络代码的写法。
- **`book/C++服务器开发精髓.md`**、**`book/Linux后端开发工程实践.md`**：服务端工程视角的延伸。
