# doxygen c cpp doc
https://www.doxygen.nl/index.html
mac 2025
Doxygen version 1.9.5

Doxygen完全支持C语言的代码文档生成。

## 简介：什么是 Doxygen？
https://github.com/doxygen/doxygen/blob/master/BUILD.txt

git clone https://github.com/doxygen/doxygen.git
cd doxygen
git checkout Release_1_14_0
cmake -B build
cmake --build build

[Doxygen](https://www.doxygen.nl/index.html) 是一个开源的、跨平台的文档生成工具，支持多种编程语言，包括：

- C
- C++
- Java
- Python
- C#
- Objective-C
- PHP
- Go
- ……等等

它通过解析源代码中的注释，自动生成结构化的API文档（HTML、PDF、LaTeX、XML 等格式）。

##  Doxygen 对 C 语言的支持情况

| 支持内容 | 是否支持 |
|----------|----------|
| 函数文档 |  支持 |
| 结构体（struct） |  支持 |
| 枚举（enum） |  支持 |
| 联合体（union） |  支持 |
| 全局变量 |  支持 |
| 宏定义（#define） |  支持 |
| 类型定义（typedef） |  支持 |
| 模块化分组（@defgroup / @addtogroup） |  支持 |
| 图形化调用关系图（Call graph） |  支持（依赖 Graphviz） |


##  示例：C 语言 + Doxygen 注释

### 示例头文件 `example.h`

```c
/
 * @file example.h
 * @brief 示例头文件，演示如何使用 Doxygen 注释 C 语言代码
 */

#ifndef EXAMPLE_H
#define EXAMPLE_H

/
 * @brief 计算两个整数的最大值
 *
 * 此函数返回传入的两个整数中较大的那个。
 *
 * @param a 第一个整数
 * @param b 第二个整数
 * @return 返回较大的整数
 */
int max(int a, int b);

/
 * @brief 表示颜色的枚举类型
 */
typedef enum {
    COLOR_RED,   /< 红色 */
    COLOR_GREEN, /< 绿色 */
    COLOR_BLUE   /< 蓝色 */
} Color;

#endif // EXAMPLE_H
```


##  如何生成文档
1. 安装 Doxygen
   macOS（Homebrew）：
   ```bash
   brew install doxygen
   ```

   Linux（Ubuntu/Debian）：
   ```bash
   sudo apt-get install doxygen
   ```

2. 创建配置文件

   在项目根目录运行：

   ```bash
   doxygen -g
   ```

   会生成一个默认的 `Doxyfile` 配置文件。

3. 修改配置文件（可选）

   打开 `Doxyfile`，设置以下关键项：

   ```ini
   INPUT                  = ./src ./include
   FILE_PATTERNS          = *.c *.h
   RECURSIVE              = YES
   GENERATE_HTML          = YES
   GENERATE_LATEX         = NO
   HAVE_DOT               = YES
   UML_LOOK               = YES
   CALL_GRAPH             = YES
   CALLER_GRAPH           = YES
   ```

4. 生成文档

   ```bash
   doxygen Doxyfile
   ```

5. 查看结果

   默认输出在 `html/index.html`，可以用浏览器打开查看。



##  常用 Doxygen 注释标签（C 语言常用）

| 标签 | 用途 |
|------|------|
| `@file` | 描述当前文件 |
| `@brief` | 简要描述 |
| `@details` | 详细描述 |
| `@param` | 参数说明 |
| `@return` | 返回值说明 |
| `@typedef` | 自定义类型说明 |
| `@enum` | 枚举值说明 |
| `@struct` | 结构体字段说明 |
| `@var` | 变量说明 |
| `@defgroup` / `@addtogroup` | 分组模块 |
| `@code` / `@endcode` | 插入代码示例 |



##  示例：结构体和 typedef 的注释

```c
/
 * @struct Person
 * @brief 表示一个人的基本信息
 */
typedef struct {
    char name[64]; /< 姓名 */
    int age;        /< 年龄 */
} Person;
```



##  进阶技巧

- 使用 `@internal` 和 `@endinternal` 来隐藏内部实现
- 使用 `@ingroup` 将多个函数归为一组
- 使用 `@ref` 引用其他符号
- 使用 `@see` 添加参考链接
- 使用 `@todo` 标记待办事项
- 使用 `@warning` 或 `@note` 添加提示



##  总结

| 内容 | 说明 |
|------|------|
| 是否支持 C |  完全支持 |
| 支持的特性 | 函数、结构体、枚举、宏定义、调用图等 |
| 输出格式 | HTML、PDF、XML、Markdown 等 |
| 推荐搭配 | Graphviz（用于图形化文档） |
| 推荐场景 | 开发 C 语言库、嵌入式系统、驱动开发等需要文档的项目 |

如果你希望我帮你写一个完整的 C 语言项目 + Doxygen 注释模板，或者帮你配置 Doxygen 生成漂亮的文档页面，请告诉我！
是否需要我提供一个完整 CMake + Doxygen 的自动化文档生成流程？欢迎继续提问！

## 特色
可以生成cpp的类继承关系图
## 官网
https://www.doxygen.org/index.html
## 版本
### 版本version
Version 1.15.0 is now available! Release date: 22 October 2025

## 安装

### win
choco install doxygen.install

## example

http://www.wangafu.net/~nickm/libevent-2.1/doxygen/html/event_8h.html

Data Structures
struct  	event

Macros
#define 	_EVENT_LOG_DEBUG   EVENT_LOG_DEBUG

event type flag
Flags to pass to event_base_get_num_events() to specify the kinds of events we want to aggregate counts for
#define 	EVENT_BASE_COUNT_ACTIVE   1U

Log severities
#define 	EVENT_LOG_DEBUG   0

Loop flags
These flags control the behavior of event_base_loop().

Typedefs

typedef void(* 	event_log_cb) (int severity, const char *msg)

Enumerations

enum event_base_config_flag

Functions
EVENT2_EXPORT_SYMBOL void 	event_active (struct event *ev, int res, short ncalls)


## 下载安装
https://www.doxygen.nl/download.html
Doxygen 用于生成文档

clang用了doxygen
grpc用doxygen
执行xxx脚本
./tools/doxygen/runxxx.sh

muduo据说可以用 Doxygen
sudo apt-get install -y doxygen doxygen-gui graphviz

sudo yum install doxygen -y
GENERATE_LATEX 是否输出latex

doxygen -g <config-file>

直接运行doxygen -g，生成Doxyfile

第二步运行
doxygen Doxyfile
生成html latex

GENERATE_LATEX改成 NO

### 实验1
https://github.com/edidada/testconan
### 实验2 pistache支持doxygen
下载pistache源码
Doxygen生成文档时报"sh: dot: not found"
sudo apt-get install graphviz

https://cedar-renjun.github.io/2014/03/21/learn-doxygen-in-10-minutes/
https://zhuanlan.zhihu.com/p/122523174
### 例子
Doxyfile

### 实验3 trantor drogon
