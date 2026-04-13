# Gunicorn 是干啥的？
一句话：
Gunicorn = Python 生产环境用的 HTTP 服务器（WSGI Server），用来跑 Flask/Django 这类 Web 应用。

## 1. 它解决什么问题？
你用 Flask/Django 自带的 `runserver`：
- 只能开发用
- 单线程、扛不住并发
- 不安全、不稳定

Gunicorn 就是用来替换它，上生产环境的。

## 2. 核心作用
1. 管理多进程
   自动开多个 worker 进程，同时处理大量请求。

2. 对接 Web 应用
   实现 WSGI 协议，能跑：
   - Flask
   - Django
   - Bottle
   - 其他老式同步 Web 框架

3. 稳定、轻量、生产级
   纯 Python 实现，部署简单，Linux 上标配。

## 3. 典型架构（最常见）
```
用户请求 → Nginx → Gunicorn → Flask/Django
```
- Nginx 负责反向代理、静态文件、负载均衡
- Gunicorn 负责跑 Python 应用、多进程并发

## 4. 最简单使用示例
安装：
```bash
pipx install gunicorn
# 或者项目内
poetry add gunicorn
```

运行 Flask 应用：
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```
- `-w 4`：开 4 个工作进程
- `-b 0.0.0.0:8000`：绑定端口
- `app:app`：模块名:Flask实例

## 5. 和 uvicorn 的区别
- Gunicorn：WSGI → 跑同步框架（Flask/Django）
- Uvicorn：ASGI → 跑异步框架（FastAPI/Starlette/aiohttp）

# 超级总结
Gunicorn = Python Web 项目上线必备的生产级 HTTP 服务器，专门用来稳定、高效地跑 Flask/Django。