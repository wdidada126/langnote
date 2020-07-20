# 大型网站系统与Java中间件开发实践



[大型网站系统与Java中间件开发实践](https://book.douban.com/subject/25867042/)







读书笔记

bio nio aio

nio开始时回调

aio完成后回调

阿姆达尔定律

amdahls law

http://ifeve.com/amdahls-law/



### 第三章 构建Java中间件



AtomicInteger内部是通过jni调用了特定平台的cas指令

原子类，需要看java标准库源码

https://github.com/edidada/testcasslution

intel cpu的

asm可以直接运行cpu指令

cpu指令有 add move等等

java中间件关键技术

动态代理

反射

字节码技术

asm

ESB SOA

ESB考虑异构系统 提供消息转换等功能

现有SOA，后又ESB

pasox 前提 没有拜占庭将军问题

一致性哈希

把单节点的hash值固定在一个范围

亚马逊 dynamo论文

### 第6章 消息中间件





消息中间件的价值



异步 削峰 解耦