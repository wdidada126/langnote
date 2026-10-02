# 概念专篇：协程与 asyncio 迁移（条目 60–63）

> 把「线程做阻塞 I/O」的代码改写成「单线程协程高并发」。本篇独立于章节正文，深入条目 60–63。

## 一、核心区别

| 维度 | 线程（条目 53/59） | 协程（条目 60） |
|---|---|---|
| 调度 | 操作系统抢占式 | 事件循环协作式（await 让出） |
| 并发上限 | 受 GIL/线程数限制 | 单线程可挂上万协程 |
| 阻塞代价 | 阻塞线程 → 占一个 OS 线程 | 阻塞协程 → 卡整个事件循环（🔴） |

## 二、从线程 I/O 改写到 asyncio（条目 61）

```python
# 教学示意，不参与构建
# 线程版
import threading
def fetch_all(urls):
    results = {}
    def work(u):
        results[u] = blocking_get(u)
    ts = [threading.Thread(target=work, args=(u,)) for u in urls]
    for t in ts: t.start()
    for t in ts: t.join()
    return results

# asyncio 版（条目 61/60）
import asyncio, aiohttp
async def fetch_one(session, url):
    async with session.get(url) as resp:
        return await resp.text()
async def fetch_all_async(urls):
    async with aiohttp.ClientSession() as s:
        return await asyncio.gather(*[fetch_one(s, u) for u in urls])
```

## 三、桥接阻塞调用（条目 62/63）

协程里不能跑阻塞函数，否则卡住循环。用 `asyncio.to_thread`（3.9+）把阻塞调用卸到线程池：

```python
async def bridge():
    data = await asyncio.to_thread(blocking_read, path)
```

多协程统一取消/异常传播，用 `asyncio.TaskGroup`（3.12+，PEP 654 关联）：

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(fetch_one(s, u)) for u in urls
```

## 四、保持事件循环畅通（条目 63）

- 协程内禁止 `time.sleep`/`requests.get`/重 CPU 循环。
- CPU 密集用 `asyncio.to_thread` 或 [../08-稳定与性能.md](../08-稳定与性能.md) 条目 64 的 `ProcessPoolExecutor`。
- 长循环内定期 `await asyncio.sleep(0)` 让出（旧式写法，现代用 `to_thread` 更干净）。

## 五、3.13+ 注意事项

🔧 PEP 703 free-threading 开启 `--disable-gil` 后，线程并行 CPU 限制解除，但 asyncio 协作模型不变。

## 六、常见误区

| 误区 | 修正 |
|---|---|
| 协程里调 `requests.get` | 用 `aiohttp`/`httpx.AsyncClient`，或 `to_thread` 包住 |
| 忘记 `await` | 协程不 await 就不执行；容易静默漏跑 |
| `gather` 不捕获异常 | 一个任务抛异常会取消其余；用 `TaskGroup` 或 `return_exceptions=True` |
| 把 asyncio 当多线程用 | 协作式并发，阻塞一个点全崩（条目 63） |

## 与其他章的联系

- 并发总览：[../07-并发与并行.md](../07-并发与并行.md) 条目 52–64。
- 惰性/生成器：[../04-推导与生成.md](../04-推导与生成.md)。
- 异常链：[../10-协作开发.md](../10-协作开发.md) 条目 88（PEP 654 `ExceptionGroup`）。
