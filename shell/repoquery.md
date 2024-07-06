# repoquery

https://www.cnblogs.com/JMLiu/p/7692784.html

repoquery是yum扩展工具包yum-utils中的一个工具，所有如果你没有repoquery命令的话，可以先 sudo yum install yum-utils 安装yum-utils包。是为了加强和补充yum功能的工具，重点是查询包的关系。repoquery的官方说明是：query information from Yum repositories，故名意思，它只能查看信息，并不能执行安装卸载更新等实质性的操作。而且要和Yum库配合使用。

    repoquery的命令格式和yum很像，但是又有不同，yum 的命令格式是yun [options] [command] [package ...]， repoquery的命令格式是repoquery [options] [item ...]，当然，也可以是repoquery -a [options]，没有item，表示所有。从命令格式的不同，也可以反映出repoquery只能做查询而不支持实质性的操作。

    repoquery的操作分为5类，分别是常规操作、包查询、包选择、组查询和组选择


centos系统命令repoquery
dpkg -l
```shell
[root@leryltdllllwew9a ~]# repoquery -ql spdlog-devel
/usr/include/spdlog
/usr/include/spdlog/async_logger.h
/usr/include/spdlog/common.h
/usr/include/spdlog/details
/usr/include/spdlog/details/async_log_helper.h
/usr/include/spdlog/details/async_logger_impl.h
/usr/include/spdlog/details/file_helper.h
/usr/include/spdlog/details/log_msg.h
/usr/include/spdlog/details/logger_impl.h
/usr/include/spdlog/details/mpmc_bounded_q.h
/usr/include/spdlog/details/null_mutex.h
/usr/include/spdlog/details/os.h
/usr/include/spdlog/details/pattern_formatter_impl.h
/usr/include/spdlog/details/registry.h
/usr/include/spdlog/details/spdlog_impl.h
/usr/include/spdlog/fmt
/usr/include/spdlog/fmt/bundled
/usr/include/spdlog/fmt/bundled/format.cc
/usr/include/spdlog/fmt/bundled/format.h
/usr/include/spdlog/fmt/bundled/ostream.cc
/usr/include/spdlog/fmt/bundled/ostream.h
/usr/include/spdlog/fmt/bundled/printf.h
/usr/include/spdlog/fmt/fmt.h
/usr/include/spdlog/fmt/ostr.h
/usr/include/spdlog/formatter.h
/usr/include/spdlog/logger.h
/usr/include/spdlog/sinks
/usr/include/spdlog/sinks/android_sink.h
/usr/include/spdlog/sinks/ansicolor_sink.h
/usr/include/spdlog/sinks/base_sink.h
/usr/include/spdlog/sinks/dist_sink.h
/usr/include/spdlog/sinks/file_sinks.h
/usr/include/spdlog/sinks/msvc_sink.h
/usr/include/spdlog/sinks/null_sink.h
/usr/include/spdlog/sinks/ostream_sink.h
/usr/include/spdlog/sinks/sink.h
/usr/include/spdlog/sinks/stdout_sinks.h
/usr/include/spdlog/sinks/syslog_sink.h
/usr/include/spdlog/spdlog.h
/usr/include/spdlog/tweakme.h
/usr/share/doc/spdlog-devel-0.10.0
/usr/share/doc/spdlog-devel-0.10.0/README.md
/usr/share/doc/spdlog-devel-0.10.0/example
/usr/share/doc/spdlog-devel-0.10.0/example/CMakeLists.txt
/usr/share/doc/spdlog-devel-0.10.0/example/Makefile
/usr/share/doc/spdlog-devel-0.10.0/example/Makefile.clang
/usr/share/doc/spdlog-devel-0.10.0/example/Makefile.mingw
/usr/share/doc/spdlog-devel-0.10.0/example/bench.cpp
/usr/share/doc/spdlog-devel-0.10.0/example/example.cpp
/usr/share/doc/spdlog-devel-0.10.0/example/example.sln
/usr/share/doc/spdlog-devel-0.10.0/example/example.vcxproj
/usr/share/doc/spdlog-devel-0.10.0/example/logs
/usr/share/doc/spdlog-devel-0.10.0/example/utils.h
/usr/share/licenses/spdlog-devel-0.10.0
/usr/share/licenses/spdlog-devel-0.10.0/LICENSE
```
