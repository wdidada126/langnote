# tbox
https://docs.tboox.org/#/zh-cn/getting_started

tbox win平台，编译安卓的库
cd D:\git\github
git clone https://github.com/tboox/tbox.git
git checkout  v1.7.1
xmake f -m debug  -p android --ndk=C:/Microsoft/AndroidNDK/android-ndk-r23c
xmake -y
xmake package

cd D:\git\github\tbox\build\android\armeabi-v7a\debug

dir


目录: D:\git\github\tbox\build\android\armeabi-v7a\debug


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         2024/8/30     14:13        2078908 demo
-a----         2024/8/30     14:13        2903322 libtbox.a
-a----         2024/8/30     14:11           9318 tbox.config.h


https://github.com/tboox/tbox/

c语言写的

https://docs.tboox.org/

https://docs.tboox.org/#/manual/container

API Manual

Basic
Stream
Memory
Interator
Container
Algorithm
Coroutine
Network
Platform
Zip
XML
Json
Math
Libc
Libm
Hash
Regex
Utils
Object
Charset
Database
## 编译


## api
### 容器

```c
    // init vector
    tb_vector_ref_t vector = tb_vector_init(0, tb_element_str(tb_true));
    if (vector)
    {
        // insert item
        tb_vector_insert_tail(vector, "hello");
        tb_vector_insert_tail(vector, "tbox");

        // dump all items
        tb_for_all (tb_char_t const*, cstr, vector)
        {
            // trace
            tb_trace_i("%s", cstr);
        }

        // exit vector
        tb_vector_exit(vector);
    }
```
## demo官方
https://github.com/tboox/tbox/blob/master/src/demo/demo.h

## 自己的代码

https://github.com/sandisks/ctestttbox


Tbox 是一个轻量级的跨平台 C 库，提供了丰富的数据结构和实用功能。它的设计目标是易于使用和高效。Tbox 包含以下常用的数据结构：

### 1. 动态数组（Vector）
   - 描述：一个自动扩展的数组，支持快速随机访问和动态增删操作。
   - 接口：`tb_vector_t`，`tb_vector_init`，`tb_vector_insert_tail`，`tb_vector_get` 等。

### 2. 链表（List）
   - 描述：双向链表，适合频繁插入和删除操作的场景。
   - 接口：`tb_list_t`，`tb_list_init`，`tb_list_insert_tail`，`tb_list_remove` 等。

### 3. 哈希表（Hash）
   - 描述：基于键值对存储的哈希表，适合快速查找和存储数据。
   - 接口：`tb_hash_map_t`，`tb_hash_map_init`，`tb_hash_map_insert`，`tb_hash_map_get` 等。

### 4. 队列（Queue）
   - 描述：FIFO（先进先出）的队列，适合任务调度等场景。
   - 接口：`tb_queue_t`，`tb_queue_init`，`tb_queue_put`，`tb_queue_get` 等。

### 5. 栈（Stack）
   - 描述：LIFO（后进先出）的栈结构，适合需要回溯的场景。
   - 接口：`tb_stack_t`，`tb_stack_init`，`tb_stack_push`，`tb_stack_pop` 等。

### 6. 红黑树（Red-Black Tree）
   - 描述：平衡二叉树，提供高效的插入、删除和查找操作。
   - 接口：`tb_tree_t`，`tb_tree_init`，`tb_tree_insert`，`tb_tree_remove` 等。

### 7. 链表字典（Hash Dict）
   - 描述：哈希表的链表实现，用于处理大量键值对的存储和查找。
   - 接口：`tb_hash_map_t`，`tb_hash_map_init`，`tb_hash_map_insert`，`tb_hash_map_get` 等。

### 8. 位图（Bitmap）
   - 描述：用于管理位的集合，适合标记和过滤等操作。
   - 接口：`tb_bitmap_t`，`tb_bitmap_init`，`tb_bitmap_set`，`tb_bitmap_clear` 等。

### 9. 双端队列（Deque）
   - 描述：支持在两端进行插入和删除操作的队列。
   - 接口：`tb_deque_t`，`tb_deque_init`，`tb_deque_push_head`，`tb_deque_pop_tail` 等。

### 10. 优先队列（Priority Queue）
   - 描述：基于堆的优先队列，适合需要按优先级处理任务的场景。
   - 接口：`tb_priority_queue_t`，`tb_priority_queue_init`，`tb_priority_queue_put`，`tb_priority_queue_get` 等。

### 11. 环形缓冲区（Circle Buffer）
   - 描述：一种先进先出的缓冲区，适合音频和流媒体数据处理。
   - 接口：`tb_circle_queue_t`，`tb_circle_queue_init`，`tb_circle_queue_put`，`tb_circle_queue_get` 等。

Tbox 还提供了一些其他实用功能和模块，例如内存管理、字符串处理、文件 I/O、线程和同步机制等，非常适合在 C 项目中使用。
