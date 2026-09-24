wfrest
linux only http库

# wfrest 学习笔记

## 1. 项目定位

wfrest 是基于 [Sogou C++ Workflow](https://github.com/sogou/workflow) 的 C++ RESTful Web 框架，项目地址为 [wfrest/wfrest](https://github.com/wfrest/wfrest)。它在 Workflow 的异步网络任务、线程池和 HTTP 能力之上，提供更接近 Web 框架使用方式的路由、参数、JSON、静态文件、上传、Cookie、代理、数据库和中间件接口。

可以把两者分工理解为：

```text
业务代码
   |
wfrest: 路由、HTTP 请求/响应、REST API、参数解析
   |
Workflow: 异步任务、HTTP/TLS、连接池、计算任务、串并行/DAG
   |
Linux 网络与线程模型
```

wfrest 不是独立的 HTTP 网络内核，排查网络、连接复用、任务回调和异步并发问题时，需要同时理解 Workflow 的 task 模型。

## 2. 依赖与构建

当前上游 README 要求 Workflow `v0.9.9` 或更高版本，主要面向 Linux；常见依赖包括 CMake、C++ 编译器、OpenSSL、zlib，测试还需要 GoogleTest。

```bash
git clone --recursive https://github.com/wfrest/wfrest.git
cd wfrest
make
sudo make install

# 构建测试和示例
make check
make example
```

也可以使用 CMake、XMake 或仓库提供的 Dockerfile。使用 Git 克隆时要带 `--recursive`，否则 Workflow 子模块缺失会导致头文件或静态库找不到。

注意：仓库早期资料中常见“Linux only”的描述，实际可用性取决于当前 Workflow/wfrest 版本、构建脚本和平台适配情况；生产部署前应在目标操作系统上完成编译和压测，不要只依据旧笔记判断平台支持。

## 3. 最小 HTTP Server

```cpp
#include "wfrest/HttpServer.h"

using namespace wfrest;

int main()
{
    HttpServer server;

    server.GET("/hello", [](const HttpReq *req, HttpResp *resp) {
        resp->String("hello wfrest\n");
    });

    server.POST("/echo", [](const HttpReq *req, HttpResp *resp) {
        resp->String(req->body());
    });

    if (server.start(8888) != 0)
        return 1;

    getchar();
    server.stop();
    return 0;
}
```

测试：

```bash
curl -v http://127.0.0.1:8888/hello
curl -v -X POST http://127.0.0.1:8888/echo -d 'hello'
```

`start()` 成功后服务开始接收请求；退出时调用 `stop()`，不要直接让进程退出而跳过网络线程和任务的收尾。

## 4. 路由与请求数据

常见能力包括：

- `GET`、`POST`、`PUT`、`DELETE` 等 HTTP 方法注册。
- 路径参数，例如 `/users/{id}` 或框架支持的路径参数语法。
- Query String、Header、Cookie、Form、JSON body。
- 文件上传、保存文件和发送文件。
- 静态文件目录、重定向、压缩和 Server-Sent Events。

路径参数、query 参数和 body 的来源不同，不应把它们混在一起解析。对外 API 建议明确内容类型：

```text
Content-Type: application/json -> JSON body
Content-Type: application/x-www-form-urlencoded -> form 参数
multipart/form-data -> 文件和表单字段
```

请求体可能很大时要配置大小上限，并在业务层校验 Content-Type、字符编码、字段长度和文件名。上传文件时不要直接使用用户提供的文件名拼接本地路径，应先做规范化和目录隔离。

## 5. JSON API

wfrest 提供 JSON API 相关能力，适合把 C++ 对象或参数转换成 REST 响应。接口设计建议统一响应格式，例如：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "id": 1
  },
  "request_id": "..."
}
```

HTTP 状态码和业务 `code` 分别表达传输层结果与业务层结果：参数错误使用 4xx，认证失败使用 401/403，资源不存在使用 404，服务内部异常使用 5xx。不要所有情况都返回 200 再依赖业务字段判断。

JSON 解析失败、字段缺失、类型不匹配和未知字段都应有明确错误处理；不要在 handler 中把异常、错误码和原始请求内容直接返回给客户端。

## 6. Handler、计算任务与异步模型

wfrest 的 handler 通常运行在 Workflow 的任务调度模型中。handler 中不应执行无限等待或大规模 CPU 计算，否则会阻塞负责处理其他请求的线程。

需要调用数据库、Redis 或其他 HTTP 服务时，应优先使用 Workflow 对应的异步 task，并用 series/parallel 等组合方式表达依赖关系：

```text
校验请求
   |
   +--> 查询用户
   |
   +--> 查询权限
   |
   +--> 汇总结果 -> 写响应
```

两个查询相互独立时可以并行，结果汇总时再进入后续步骤；有先后依赖时使用串行流程。每个出站任务都应设置超时、失败处理和取消/终止路径。

不要把请求级状态写入全局可变变量。多个请求可能并发执行，共享缓存、连接池和统计数据需要明确线程安全边界；局部变量、请求对象和响应对象的生命周期也不能跨异步回调悬挂引用。

## 7. 数据库、Redis 和代理

上游示例覆盖 MySQL、Redis、HTTP 代理和定时器等能力。使用时重点注意：

- 数据库连接和 Redis 连接应复用连接池，不要每个请求创建新连接。
- 事务、连接上下文和任务回调必须明确由哪个线程/任务拥有。
- 数据库超时、连接断开、重试和幂等不能只依赖框架默认值。
- HTTP 代理要区分目标 URL、代理 URL、Host 和 SNI；HTTPS 代理链路要单独验证证书和 CONNECT 行为。
- 出站请求必须限制重定向次数、响应体大小和总耗时，避免 SSRF、无限重定向和资源耗尽。

Workflow 支持 HTTP、Redis、MySQL、Kafka 等异步客户端能力；wfrest 负责 Web 接口层时，后端任务仍应按照 Workflow 的异步模型组织。

## 8. BluePrint、静态文件与切面

BluePrint 可用于把一组路由按模块组织，再挂载到主服务，例如按 `/api/v1/user`、`/api/v1/order` 拆分业务模块。这样可以降低单个 `main()` 中的路由注册密度，并便于测试和复用。

静态文件服务要特别处理：

- 目录穿越：拒绝 `..` 和规范化后越出根目录的路径。
- MIME 类型：不要仅由用户提供的扩展名决定安全策略。
- 缓存头：区分带 hash 的静态资源和不可缓存的动态内容。
- 大文件：使用流式/文件发送接口，避免一次性读入内存。
- 访问控制：管理文件、配置文件和日志目录不能暴露在静态根目录下。

切面（Aspect-oriented programming）适合统一处理日志、鉴权、请求 ID、耗时统计和异常边界，但切面中的逻辑应保持轻量。鉴权失败要尽早返回，日志不要记录密码、Token、完整 Cookie 或敏感 body。

## 9. HTTPS、Cookie 与代理

HTTPS 服务至少需要配置证书、私钥和证书链，并验证：

- 客户端是否强制使用 HTTPS。
- 证书 SAN 是否覆盖访问域名。
- TLS 版本和密码套件是否符合组织要求。
- 反向代理终止 TLS 后，应用是否正确识别可信的 `X-Forwarded-Proto`、`X-Forwarded-For`。
- Cookie 是否设置 `Secure`、`HttpOnly`、合适的 `SameSite` 和过期时间。

不能无条件信任客户端提交的 `X-Forwarded-*` 头；只有来自受信任代理的请求才应读取这些头，并在边界层覆盖而不是追加伪造值。

## 10. 错误处理与可观测性

建议为每个请求建立 request ID，并在访问日志、业务日志、下游任务和响应 Header 中传递。至少记录：method、path、状态码、耗时、请求 ID、客户端地址、下游错误和响应大小。

生产环境要区分：

- 客户端可见的安全错误信息。
- 供开发者排障的内部错误和堆栈。
- 结构化访问日志和指标。

关注以下指标：请求量、P50/P95/P99 延迟、4xx/5xx、活动连接、线程池队列、下游超时、连接池耗尽、上传大小和内存使用。异步框架中“线程没有阻塞”不代表系统没有背压，仍要对队列长度和下游容量设置上限。

## 11. 常见坑

1. 没有递归拉取 Workflow 子模块，导致编译失败。
2. 在 handler 中执行同步磁盘、数据库或网络操作，导致事件处理线程被阻塞。
3. 异步回调捕获局部变量引用，回调执行时变量已经销毁。
4. 响应已经结束后仍继续写响应，或多个并发分支同时修改同一个响应对象。
5. 只设置连接超时，没有设置请求总超时、读取超时和下游超时。
6. 把上传文件名直接拼入路径，造成路径穿越或文件覆盖。
7. 通过 `X-Forwarded-For` 直接获得“真实 IP”，导致审计和限流被伪造。
8. 只返回 HTTP 200，调用方无法区分参数错误、未授权和服务故障。
9. 把静态文件服务根目录指向项目根目录，意外暴露配置、密钥和源码。
10. 只压测单个 handler，没有压测连接复用、慢下游、慢客户端和大请求体。

## 12. 参考资料

- [wfrest GitHub](https://github.com/wfrest/wfrest)
- [wfrest Releases](https://github.com/wfrest/wfrest/releases)
- [Sogou Workflow GitHub](https://github.com/sogou/workflow)
- [Workflow 中文 README](https://github.com/sogou/workflow/blob/master/README_cn.md)
