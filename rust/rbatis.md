# rbatis

https://github.com/rbatis/rbatis

cargo doc --open -p rbatis

类似mybatis，可以用xml来动态生成SQL

rbatis = "4.5.33"

```shell
No function or associated item delete_by_id found in the current scope for struct SysDict [E0599] 
// 假设你已经拿到了要删除的 id（String 类型） let id_to_delete = random_id.to_string(); 
// 或从请求中获取 let delete_result = sys_dict::SysDict::delete_by_id(&rb, &id_to_delete).await?; 
tracing::info!("按 id 删除结果: affected rows = {}", delete_result.rows_affected);
```
原因：在你当前的 rbatis 版本（从 crud!(SysDict {}); 这种写法看，大概率是 rbatis 4.x 或更高版本），crud! 宏 不再生成 delete_by_id、select_by_id 等按主键 ID 的专用方法。

旧版本（2.x / 3.x 早期）有 delete_by_id、remove_by_id 等。
新版本（4.x+）简化了 API，只生成少数核心方法：delete_by_map、update_by_map、select_by_map 等。
按 ID 删除现在统一用 delete_by_map + value!{ "id": ... } 来实现（官方推荐方式）。
