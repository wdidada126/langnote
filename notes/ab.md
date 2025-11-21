# ab
## wrk

以下是 AB（Apache Benchmark） 和 wrk 两款HTTP性能测试工具的详细对比，包括共同点和核心区别：

一、共同点

特性 AB 和 wrk 的共同表现

核心功能 都是HTTP负载测试工具，用于测量Web服务器的吞吐量、延迟等性能指标

命令行工具 通过终端命令直接运行，无需GUI界面

开源协议 AB属于Apache License，wrk使用Apache 2.0 License

基础测试指标 均支持统计：请求数/秒（QPS）、延迟分布、错误率等

支持HTTP方法 均可测试GET/POST等基本HTTP方法

二、核心区别

对比维度 AB (Apache Benchmark) wrk

开发背景 Apache软件基金会开发，历史悠久（1996年） 现代高性能工具（2012年），由GitHub工程师开发

多线程支持 单进程，通过并发（-c）模拟用户，但受限于单核性能 多线程架构，天然支持多核CPU利用率

脚本扩展性 仅支持简单参数（如POST数据需通过-p文件指定），无编程能力 支持Lua脚本，可自定义复杂测试逻辑（如动态参数、流程控制）

连接复用 默认短连接（HTTP/1.0），需手动启用长连接（-k） 默认HTTP/1.1长连接，更贴近现代Web实践

性能上限 较低（单进程瓶颈，通常上限约5万QPS） 极高（多线程+事件驱动，可达百万级QPS）

统计报告 提供基础统计（均值、百分比），但无详细分布 提供延迟直方图，更直观展示长尾问题

协议支持 仅HTTP/1.0和1.1 支持HTTP/1.1、2.0（需手动编译）

安装复杂度 通常预装或通过包管理器一键安装（如apt install apache2-utils） 需源码编译（依赖LuaJIT和OpenSSL）

典型使用场景 快速简单测试（如开发环境验证） 生产级压测、极限性能调优

三、选择建议

使用 AB 当：

• 需要快速验证服务器基础性能

• 测试环境资源有限（如单核CPU）

• 无需复杂测试逻辑

使用 wrk 当：

• 需要模拟高并发生产流量

• 测试HTTP/2或需要动态参数

• 需详细分析延迟分布（如P99延迟）

• 多核服务器需充分发挥硬件性能

四、命令对比示例

1. 基础GET测试

# AB
ab -n 10000 -c 100 http://example.com/

# wrk
wrk -t4 -c100 -d10s http://example.com/


2. POST请求测试

# AB（需数据文件）
ab -n 1000 -c 50 -p data.json -T 'application/json' http://example.com/api

# wrk（通过Lua脚本）
wrk -t4 -c100 -d10s -s post.lua http://example.com/api


五、扩展能力

wrk 的 Lua 脚本示例（动态参数）

-- post.lua
request = function()
    local uid = math.random(1, 100000)
    local body = string.format('{"user_id": %d}', uid)
    return wrk.format("POST", "/api", wrk.headers, body)
end

优势：实现参数化请求、动态header、多接口串联测试。

通过以上对比，可根据测试需求灵活选择工具。若需极致性能或现代协议支持，wrk 是更好的选择；若追求简单快捷，AB 仍具实用价值。

## 参数
ab常用参数的介绍：
-n ：总共的请求执行数，缺省是1；
-c： 并发数，缺省是1；
-t：测试所进行的总时间，秒为单位，缺省50000s
-p：POST时的数据文件
-w: 以HTML表的格式输出结果
执行测试用例：ab -n 40000 -c 20 -w  "http://118.182.97.157:8090/blog/getBlogDetail/84"  >> ~/miss.html



ab进行app接口的压测：

 ab -n 400 -c20  "http://www.xxx.com/api.php?sig=......"；
将需要压测的接口，用  " " ;

7.ab进行post传参的压测
 ab -n 400 -c20  -p  parm.txt  -T "application/x-www-form-urlencoded" http://localhost:3000/login
将 parm.txt放在和ab.exe相同的文件夹中，parm.txt中存放的是需要post格式传递的参数。
-T ：post请求的head头。

 


ab -n 400 -c20  "http://118.182.97.157:8090/blog/getBlogDetail/84"
ab -n 400 -c20  "http://127.0.0.1:8080/blog/getBlogList"


ab - Apache HTTP server benchmarking tool


This is ApacheBench, Version 2.3 <$Revision: 1430300 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Finished 400 requests


Server Software:        
Server Hostname:        127.0.0.1
Server Port:            8080

Document Path:          /blog/getBlogList
Document Length:        120 bytes

Concurrency Level:      200
Time taken for tests:   0.958 seconds
Complete requests:      400
Failed requests:        0
Write errors:           0
Non-2xx responses:      400
Total transferred:      90000 bytes
HTML transferred:       48000 bytes
Requests per second:    417.43 [#/sec] (mean)
Time per request:       479.117 [ms] (mean)
Time per request:       2.396 [ms] (mean, across all concurrent requests)
Transfer rate:          91.72 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   1.5      0       4
Processing:    18  215 128.4    201     935
Waiting:       17  207 108.0    199     935
Total:         18  216 128.5    201     940

Percentage of the requests served within a certain time (ms)
  50%    201
  66%    236
  75%    259
  80%    270
  90%    321
  95%    382
  98%    663
  99%    915
 100%    940 (longest request)



 Benchmarking 127.0.0.1 (be patient)
Completed 4000 requests
Completed 8000 requests
Completed 12000 requests
Completed 16000 requests
Completed 20000 requests
Completed 24000 requests
Completed 28000 requests
Completed 32000 requests
Completed 36000 requests
Completed 40000 requests
Finished 40000 requests


Server Software:        
Server Hostname:        127.0.0.1
Server Port:            8080

Document Path:          /blog/getBlogList
Document Length:        120 bytes

Concurrency Level:      200
Time taken for tests:   29.294 seconds
Complete requests:      40000
Failed requests:        0
Write errors:           0
Non-2xx responses:      40000
Total transferred:      9000000 bytes
HTML transferred:       4800000 bytes
Requests per second:    1365.49 [#/sec] (mean)
Time per request:       146.468 [ms] (mean)
Time per request:       0.732 [ms] (mean, across all concurrent requests)
Transfer rate:          300.03 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0   57 250.6      2    3051
Processing:     1   86 102.5     63    1825
Waiting:        1   84 101.5     61    1825
Total:          1  143 273.2     67    3148

Percentage of the requests served within a certain time (ms)
  50%     67
  66%     84
  75%     97
  80%    111
  90%    216
  95%   1044
  98%   1106
  99%   1172
 100%   3148 (longest request)
 


 ```shell
 ab -n 400 -c20  "http://118.182.97.157:8090/blog/getBlogDetail/84"
This is ApacheBench, Version 2.3 <$Revision: 1430300 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 118.182.97.157 (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Finished 400 requests


Server Software:        
Server Hostname:        118.182.97.157
Server Port:            8090

Document Path:          /blog/getBlogDetail/84
Document Length:        375 bytes

Concurrency Level:      20
Time taken for tests:   8.152 seconds
Complete requests:      400
Failed requests:        0
Write errors:           0
Total transferred:      203600 bytes
HTML transferred:       150000 bytes
Requests per second:    49.07 [#/sec] (mean)
Time per request:       407.588 [ms] (mean)
Time per request:       20.379 [ms] (mean, across all concurrent requests)
Transfer rate:          24.39 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:       27   36  70.8     31    1036
Processing:   114  333 250.1    254    2306
Waiting:      114  329 246.8    254    2306
Total:        144  369 259.1    285    2339

Percentage of the requests served within a certain time (ms)
  50%    285
  66%    318
  75%    412
  80%    487
  90%    683
  95%    935
  98%   1307
  99%   1407
 100%   2339 (longest request)
```