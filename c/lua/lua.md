# lua

nginx，动态生成要下载文件的路径，lua

在 Nginx 中使用 Lua（通过 `ngx_lua` 模块，通常由 OpenResty 提供）可以非常灵活地动态生成要下载文件的路径，并交由 Nginx 处理文件下载（如使用 `ngx.exec()` 跳转到静态 location，或直接读取文件发送）。

### 场景说明

你想实现：
- 用户访问一个 URL（如 `/download/123`）
- Lua 脚本根据请求参数、用户身份、时间等动态计算出实际文件路径
- 然后让 Nginx 返回该文件（作为下载）

### 方法一：使用 `ngx.exec()` 跳转到静态 `location`（推荐）

这是最高效、最安全的方式。Lua 只负责“路由”，Nginx 原生处理文件发送。

#### 目录结构示例
```
/usr/local/nginx/
├── html/
│   └── files/
│       └── secret/
│           └── report_2025.pdf
```

#### Nginx 配置（`nginx.conf`）
```nginx
worker_processes  1;

events {
    worker_connections 1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    # 启用 OpenResty 的 Lua 模块
    lua_code_cache on;  # 生产环境可开启，开发时可 off

    server {
        listen 80;
        server_name localhost;

        # 【动态路由入口】
        location /download/ {
            access_by_lua_block {
                -- 示例：从 URL 路径提取 ID
                local id = string.match(ngx.var.uri, "/download/(%d+)")
                if not id then
                    ngx.status = 400
                    ngx.say("Invalid download link")
                    ngx.exit(400)
                end

                --  可加入权限校验（如登录、token、IP等）
                -- local token = ngx.var.arg_token
                -- if not is_valid_token(token) then ... end

                -- 动态生成真实文件路径（相对或绝对）
                local file_path = "/files/secret/report_" .. id .. ".pdf"

                -- 跳转到静态 location（内部重定向）
                ngx.exec("/file", { path = file_path })
            }
        }

        # 【真实文件服务 location】
        location /file {
            internal;  # 仅允许内部跳转访问，禁止外部直接访问

            alias /usr/local/nginx/html;  # 映射到实际目录

            # 强制浏览器下载（而非预览）
            add_header Content-Disposition 'attachment; filename="$uri"';

            # 可选：限制文件类型
            types {
                application/octet-stream pdf;
            }
        }

        # 静态文件根目录
        location / {
            root html;
        }
    }
}
```

### 方法二：Lua 直接读取并发送文件（适合小文件或特殊处理）

适用于需要 Lua 做加密、压缩、记录日志等场景。

```nginx
location /download/ {
    content_by_lua_block {
        local id = string.match(ngx.var.uri, "/download/(%d+)")
        if not id then
            ngx.status = 400
            ngx.say("Invalid ID")
            return
        end

        -- 动态生成文件路径
        local file_path = "/usr/local/nginx/html/files/secret/report_" .. id .. ".pdf"

        -- 使用 Lua 读取文件
        local file = io.open(file_path, "rb")
        if not file then
            ngx.status = 404
            ngx.say("File not found")
            return
        end

        local content = file:read("*all")
        file:close()

        -- 设置响应头（强制下载）
        ngx.header["Content-Type"] = "application/octet-stream"
        ngx.header["Content-Disposition"] = "attachment; filename=\"report_" .. id .. ".pdf\""
        ngx.header["Content-Length"] = string.len(content)

        -- 发送文件内容
        ngx.print(content)
    }
}
```

> 注意：此方式会将文件加载到内存，不适合大文件。推荐使用方法一。

### 方法三：结合 Redis/数据库 动态映射（高级）

```lua
access_by_lua_block {
    local args = ngx.req.get_uri_args()
    local token = args.token

    -- 查询 Redis 获取真实路径
    local redis = require "resty.redis"
    local red = redis:new()
    red:set_timeouts(1000, 1000, 1000)
    red:connect("127.0.0.1", 6379)

    local path = red:get("download_token:" .. token)
    if not path or path == ngx.null then
        ngx.exit(403)
    end

    ngx.exec("/file", { path = path })
}
```
### 关键点总结

| 要点 | 说明 |
|------|------|
| `ngx.exec()` | 推荐用于跳转，让 Nginx 原生处理文件传输 |
| `internal` | 保护 `/file` location，防止直接访问 |
| `alias` vs `root` | `alias` 更适合动态路径映射 |
| `Content-Disposition` | 强制浏览器下载文件 |
| 权限校验 | 在 `access_by_lua_block` 中做 token、IP、登录态验证 |
| 大文件 | 避免 `content_by_lua_block` 读入内存，用 `ngx.exec()` |

### 测试

访问：
```
http://localhost/download/2025?token=abc123
```

Nginx 会动态映射到：
```
/usr/local/nginx/html/files/secret/report_2025.pdf
```
并作为下载文件返回。

### 依赖
确保你使用的是 OpenResty 或 Nginx 编译了 `ngx_http_lua_module`。
> OpenResty 官网：https://openresty.org
通过 Lua + Nginx，你可以实现高度灵活的动态文件下载服务，包括权限控制、路径加密、限速、日志记录等。
