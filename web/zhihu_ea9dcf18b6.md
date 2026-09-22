# 网络博文/教程

- 来源：zhihu.com
- 链接：https://www.zhihu.com/search?q=%E4%B8%AD%E9%97%B4%E8%A1%A8&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A1747208349%7D

## 笔记（聚合自 2020–2026 日常笔记，2026-09-23 整理）

### 2023-09
> 结论：能避免跨库查询尽量避免，能在SQL里面join尽量在SQL里面执行JOIN。如果上面两种都不可行，就创建[中间表](https://www.zhihu.com/search?q=%E4%B8%AD%E9%97%B4%E8%A1%A8&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A1747208349%7D)来保存聚合数据。下下策才是在Java代码里面做Join，如果一定要用stream api做join的话，建议开启并行。
