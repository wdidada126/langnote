
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
