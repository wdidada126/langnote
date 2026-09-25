# ch2_http_server —— 多线程 HTTP GET 服务器 + 简易路由

## 对应章节

- 教材：§2.2（Web 与 HTTP：请求/响应格式、条件 GET、状态码）、§2.1（协议与 C/S）、§2.4（socket 编程）
- 笔记：`notes/ch2-02-http.md`（第 5 讲）、`notes/ch2-04-sockets.md`（第 7 讲）

## 协议要点

1. 请求行解析：`METHOD SP TARGET SP VERSION`；头部按 `k: v` 逐行读，读到 `\r\n\r\n` 为止——
   TCP 是字节流、无消息边界，"读满框架"必须由应用自己做（笔记第 4/7 讲的粘包条目）。
2. 响应：状态行 + `Content-Type/Content-Length/Date/Server` + 空行 + 体；304 不带体。
3. 路由表：`/`（首页）、`/hello?name=`（查询参数）、`/time`、`/count`（共享状态+锁，演示并发）、
   `/static/<file>`（MIME 猜测 + 简化版 `If-Modified-Since` 协商缓存）。
4. 并发：每连接一线程（`threading.Thread`），`SO_REUSEADDR`+`listen(16)`。
5. 教学简化：不实现持久连接复用循环（发完即关）；不解析 POST 体。

## 运行

```
# 启动服务器
python http_server.py            # 或 ./run.sh

# 另开终端验证
curl -i http://127.0.0.1:8000/
curl -i http://127.0.0.1:8000/hello?name=kurose
curl -i http://127.0.0.1:8000/count        # 重复访问，计数增长=线程共享状态
curl -i http://127.0.0.1:8000/static/index.html
curl -i -H 'If-Modified-Since: <上次响应的 Last-Modified>' http://127.0.0.1:8000/static/index.html  # 期望 304
curl -i -X POST http://127.0.0.1:8000/     # 期望 405
python -m http.server 对比观察亦可
```

run.sh / run.bat 会先 `python -m py_compile http_server.py` 做语法自检再启动。

## 实验建议

- 用 Wireshark 过滤 `http.request`，对照笔记 §5 的字段表逐行核对。
- 把 `threading` 换成 `selectors` 事件循环重写（思考题：慢客户端/10k 连接谁赢？）。
