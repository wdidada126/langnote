# spdlog


## 支持的平台
Linux, FreeBSD, OpenBSD, Solaris, AIX
Windows (msvc 2013+, cygwin)
macOS (clang 3.5+)
Android

head only

[C++日志库spdlog]( https://blog.csdn.net/jacky128256/article/details/103769794 )



[spdlog]( https://github.com/gabime/spdlog)


## 安装

## centos安装
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

### ubuntu安装

sudo apt install libspdlog-dev -y

testspdlog.md

