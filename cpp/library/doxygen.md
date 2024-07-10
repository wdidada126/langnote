# doxygen cpp doc

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

enum  	event_base_config_flag

Functions
EVENT2_EXPORT_SYMBOL void 	event_active (struct event *ev, int res, short ncalls)


## dd

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
