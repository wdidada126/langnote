# cow

cow，是c++ http server
pistache

thread model
并发

http协议的支持情况
http 1.1 1.2 3
request/response
cookie session
head
body
xml json protobuf
context 上下文 没有
有parser，没有handler

c++语法
c++关键字
c++多重继承

#define CROW_ROUTE(app, url) app.template route<crow::black_magic::get_parameter_tag(url)>(url)

命名空间

websocket
cqrs

session

cow版本与asio版本对应关系
截止到我最后的知识更新日期是2023年，Cow是一个C++库，用于处理HTTP客户端和服务器请求，它基于Boost.Asio。Cow的版本与Boost.Asio的版本有一定的对应关系。

以下是一些可能的关系：
* Cow 0.25.0：Boost.Asio 1.75.0
* Cow 0.26.0：Boost.Asio 1.76.0
* Cow 0.27.0：Boost.Asio 1.77.0
请注意，这只是一个大致的对应关系，实际版本可能会有所不同。建议查阅Cow的官方文档或GitHub仓库，以获取最准确和最新的版本对应关系。
