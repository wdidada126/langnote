# redis rax

https://github.com/antirez/rax

当然可以！以下是关于 Rax 的简单介绍：

###  Rax 是什么？
Rax 是一个用 ANSI C 编写的 Radix Tree（基数树） 实现，由 Redis 的作者 Salvatore Sanfilippo（@antirez） 开发。

项目地址： [https://github.com/antirez/rax](https://github.com/antirez/rax)

###  简单总结（一句话）

> Rax 是一个轻量、高效、纯 C 语言实现的 Radix Tree（也叫压缩前缀树），用于快速存储和查找字符串前缀相关的键值对。

###  它能做什么？

- 存储键值对，键通常是字符串（如 `"user:1000"`, `"user:1001"`）
- 支持快速的 前缀查找（例如：查找所有以 `"user:"` 开头的键）
- 支持有序遍历（按键的字典序）
- 内存效率高，特别适合有公共前缀的字符串


###  核心特性

| 特性 | 说明 |
|------|------|
|  高性能 | 插入、删除、查找接近 O(m)，m 是键的长度 |
|  内存友好 | 共享前缀，减少重复字符串存储 |
|  纯 ANSI C | 不依赖 C++ 或其他扩展，可移植性强 |
|  单文件实现 | 只有 `rax.h` 和 `rax.c`，易于集成 |
|  支持迭代器 | 可遍历所有键值对，支持前缀扫描 |

###  简单使用示例

```c
#include "rax.h"
#include <stdio.h>

int main() {
    rax *tree = raxNew();  // 创建 radix tree

    // 插入键值对
    raxInsert(tree, (unsigned char*)"hello", 5, "world", NULL);
    raxInsert(tree, (unsigned char*)"help", 4, "me", NULL);

    // 查找
    void *val = raxFind(tree, (unsigned char*)"hello", 5);
    if (val != raxNotFound) {
        printf("Found: %s\n", (char*)val);  // 输出: world
    }

    // 前缀查找（比如找所有 "he" 开头的）
    raxIterator iter;
    raxStart(&iter, tree);
    raxSeek(&iter, "^", (unsigned char*)"he", 2);  // "^" 表示从该前缀开始

    while (raxNext(&iter)) {
        printf("Key: %.*s, Value: %s\n",
               (int)iter.key_len, iter.key, (char*)iter.value);
    }
    raxStop(&iter);

    raxFree(tree);  // 释放
    return 0;
}
```

###  和Redis的关系？

Rax 最初是为 Redis 开发的，用于实现：
- Redis Streams 中的消费者组（consumer groups）
- 高效的键空间扫描

所以它非常稳定、经过生产验证。


###  适用场景

- 需要高效前缀匹配的系统（如路由表、自动补全）
- 嵌入式系统或高性能服务中需要轻量级字典
- 替代 `hash table` 当键有明显前缀特征时


###  总结

| 项目 | 说明 |
|------|------|
| 语言 | ANSI C |
| 作者 | antirez（Redis 作者） |
| 特点 | 轻量、高效、易集成 |
| 用途 | 字符串前缀存储与查找 |
| 是否推荐 | ✅ 非常适合 C 项目中需要前缀匹配的场景 |

