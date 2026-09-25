# 第 8 章 基于 Netty 单体 IM 系统的开发实战（卷1）

> 用 Netty 搭单体 IM：私聊/群聊、心跳检测（`IdleStateHandler`）、登录鉴权、消息广播、`ChannelGroup` 管理连接。本书把前 7 章串成可运行 IM，是「理论→实战」第一座桥。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| 连接管理 | `ChannelGroup` / `ChannelId`→用户 |
| 心跳 | `IdleStateHandler` 读空闲检测 |
| 私聊/群聊 | 单发 / 广播 |
| 鉴权 | 登录帧校验，未登录拒业务 |

## 二、核心精讲

### 2.1 🔧 心跳与假死
- 客户端定时发 ping，服务端 `IdleStateHandler` 触发 `userEventTriggered` 关闭空闲连接（🔧 防「假死连接」占 fd；TCP `SO_KEEPALIVE` 间隔太长（默认 2h），应用层心跳更可控）。

### 2.2 连接→用户映射
- 登录后建 `userId ↔ ChannelId` 索引（🔧 用 `ConcurrentHashMap` 或 Redis 集中存；单体用本地 Map，集群需 Redis 路由，见 15 章）。

### 2.3 群聊广播
- `ChannelGroup.writeAndFlush` 广播（🔧 大群广播用「写缓冲 + 限流」防单慢连接拖垮；Netty `Channel.isWritable` 背压）。

## 三、版本演进 / 论文 / 前沿

- 论文/规范：WebSocket RFC 6455（IM 推送替代长轮询）；XMPP（早期 IM 协议）。
- 工业界：Netty（IM 底座）、t-io（国产 IM 框架）、OpenIM、RocketMQ（Netty 通信）。
- 开源 stars（2026-09）：netty 34k / rocketmq 22k / dubbo 41k。

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "靠 TCP keepalive" | 间隔太长，用应用心跳 |
| 2 | "群聊无背压" | isWritable 限流 |
| 3 | "单体 Map 存连接" | 集群需 Redis 路由 |
| 4 | "未登录能发消息" | 鉴权前置 |
