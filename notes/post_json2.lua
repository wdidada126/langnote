-- post_json.lua  

request = function()  
    local url = "http://101.43.12.32:8090/blog/list"  
    local body = '{"x":"b", "another_key":123}'  
  
    -- 设置请求方法、URL 和 HTTP 版本  
    wrk.method = "POST"  
    wrk.body = body
    wrk.headers["Content-Type"] = "application/json"  
  
    -- 返回请求体
    return wrk.format(nil, url)
end

