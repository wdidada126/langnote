# wrk

## 编程语言
c语言写的
## 使用方式

wrk -c 1000 -t 8 -d 30 --latency 'http://127.0.0.1:19999/qps?id=1'
Running 30s test @ http://127.0.0.1:19999/qps?id=1

https://github.com/wg/wrk

零声教育 wrk

wrk是一款针对HTTP协议的基准测试工具，它能够在单机多核CPU的条件下，使用系统自带的高性能I/O机制，如epoll，kqueue等，通过多线程和事件模式，对目标机器产生大量的负载。wrk支持Lua脚本来创建复杂的测试场景（这一点与OpenResty支持Lua脚本相同），也可以输出详细的响应时间统计信息。wrk的优点有以下几点：

高性能：wrk可以利用多核CPU的并行计算能力，同时使用多个线程和连接来发送请求，并且使用高效的I/O模型来处理响应。这样wrk可以在单机上产生高达数十万甚至数百万级别的QPS（每秒请求数），远超过其他常见的压测工具，如ab、siege、jmeter等。
灵活：wrk支持使用Lua脚本来定制压测场景，例如自定义HTTP方法、动态生成请求参数、修改请求头等。这样我们可以模拟各种复杂和真实的用户行为和业务逻辑，使得压测结果更加贴近实际情况。
简洁：wrk的安装和使用都非常简单，只需要几条命令就可以完成。wrk的输出也非常清晰和直观，可以显示每个线程和总体的响应时间和每秒请求数，并且可以打印出响应时间的分布情况，方便我们分析系统的性能瓶颈。

### 发送post带json参数的例子
post_json.lua


```lua
-- post_json.lua  
  
request = function()  
    local url = "http://101.43.12.32:8090/user/list"  
    local body = '{"x":"b", "another_key":123}'  
  
    -- 设置请求方法、URL 和 HTTP 版本  
    wrk.method = "POST"  
    wrk.url = url  
    wrk.headers["Content-Type"] = "application/json"  
  
    -- 返回请求体  
    return body  
end
```

wrk -t12 -c400 -d30s --header "Content-Type: application/json" --body '{"x":"b"}' http://101.43.12.32:8090/user/list

## 安装
wget https://github.com/wg/wrk/archive/refs/tags/4.2.0.tar.gz
tar -zxvf 4.2.0.tar.gz
rm -rf 4.2.0.tar.gz
cd wrk-4.2.0/
make -j5

wrk  -t12 -c400 -d30s  -s post_json2.lua http://101.43.12.32:8090/blog/list

post_json2.lua