# SOFAJRaft

## 代码仓库

https://github.com/sofastack/sofa-jraft

## 编程语言

Java

## 版本version
v1.4.0 Jul 14, 2025
v1.3.15
1.3.13 Apr 10, 2023
1.3.11 Jun 20, 2022

## 编译
git clone https://github.com/sofastack/sofa-jraft.git
cd sofa-jraft
git checkout 1.3.11
mvn clean compile -DskipTests

SOFAJRaft 本身是一个基础的 RAFT 算法库，要实现类似 Nacos（服务发现与配置中心）的功能，通常需要在其基础上构建上层应用。蚂蚁内部的开源项目 SOFARegistry​ 正是基于 SOFAJRaft 实现的高可用服务注册中心。
实现思路参考：
数据模型设计：
将服务注册信息（Service Instance）作为 RAFT 的状态机（State Machine）数据。
当服务注册/注销时，通过 RAFT 协议将操作日志复制到集群多数节点，确保数据一致性。
核心组件：
Meta Server（元数据服务器）：基于 SOFAJRaft 构建的集群，负责存储全局的服务列表和配置数据。
Data Server（数据服务器）：负责接收客户端的服务注册请求，并将变更同步到 Meta Server 集群。
关键特性实现：
服务发现：客户端从 Meta Server 集群拉取最新的服务列表（支持线性一致性读）。
配置管理：将配置项作为 KV 数据存储在 RAFT 状态机中，利用 SOFAJRaft 的日志复制机制保证配置的强一致性
