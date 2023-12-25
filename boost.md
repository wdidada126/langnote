# boost

要在Ubuntu 20上安装特定版本的libboost-dev（例如1.65版本），你可以考虑使用第三方APT源，因为Ubuntu官方仓库可能不提供旧版本。以下是一些推荐的第三方APT源：

阿里云开源镜像站：阿里云提供了广泛的开源软件镜像，包括Boost。你可以尝试添加阿里云的源到你的系统中。
清华大学开源软件镜像站：清华大学也提供了许多开源软件的镜像，包括Boost。
中科大开源镜像站：中国科学技术大学开源软件镜像站也是一个可靠的选择。
添加这些源之后，你可以使用类似以下的命令来安装特定版本的libboost-dev：

bash
sudo apt-get update  
sudo apt-get install libboost-dev=1.65.1-1
请注意，你需要将上述命令中的版本号替换为你想要安装的确切版本。此外，由于使用第三方源可能会带来一些风险，如软件包的完整性和安全性，建议在使用之前仔细检查和验证源的可靠性。

支持Aix平台

模板
元编程

boost.test
https://blog.csdn.net/Betterc5/article/details/86291109





https://blog.csdn.net/weixin_33656634/article/details/86133362



Boost库系列：基于boost::asio的http、https serve实现方式总结

https://www.boost.org/doc/libs/1_67_0/doc/html/boost_asio/examples/cpp03_examples.html

1、http::server，简单的单线程服务器，只有一个主线程；
2、 http::server2  多个io_contex响应socket连接
3、 http::server3 一个io_context多个线程run()
4、 http::server4 单线程的协程



  boost.x86_64 0:1.53.0-28.el7                                          
  boost-atomic.x86_64 0:1.53.0-28.el7                                   
  boost-chrono.x86_64 0:1.53.0-28.el7                                   
  boost-context.x86_64 0:1.53.0-28.el7                                  
  boost-filesystem.x86_64 0:1.53.0-28.el7                               
  boost-graph.x86_64 0:1.53.0-28.el7                                    
  boost-iostreams.x86_64 0:1.53.0-28.el7                                
  boost-locale.x86_64 0:1.53.0-28.el7                                   
  boost-math.x86_64 0:1.53.0-28.el7                                     
  boost-program-options.x86_64 0:1.53.0-28.el7                          
  boost-python.x86_64 0:1.53.0-28.el7                                   
  boost-random.x86_64 0:1.53.0-28.el7                                   
  boost-regex.x86_64 0:1.53.0-28.el7                                    
  boost-serialization.x86_64 0:1.53.0-28.el7                            
  boost-signals.x86_64 0:1.53.0-28.el7                                  
  boost-test.x86_64 0:1.53.0-28.el7                                     
  boost-timer.x86_64 0:1.53.0-28.el7                                    
  boost-wave.x86_64 0:1.53.0-28.el7                                     

## boost版本
1.71
1.53
1.66

## ubuntu 20 gcc9编译boost 1.65失败

```shell
gcc.compile.c++ bin.v2/libs/python/build/gcc-9/release/threading-multi/converter/builtin_converters.o
libs/python/src/converter/builtin_converters.cpp: In function ‘void* boost::python::converter::{anonymous}::convert_to_cstring(PyObject*)’:
libs/python/src/converter/builtin_converters.cpp:51:35: error: invalid conversion from ‘const void*’ to ‘void*’ [-fpermissive]
   51 |       return PyUnicode_Check(obj) ? _PyUnicode_AsString(obj) : 0;

    "g++"   -O3 -finline-functions -Wno-inline -Wall -pthread -fPIC -m64  -DBOOST_ALL_NO_LIB=1 -DBOOST_PYTHON_SOURCE -DNDEBUG  -I"." -I"/usr/include/python3.8" -c -o "bin.v2/libs/python/build/gcc-9/release/threading-multi/converter/builtin_converters.o" "libs/python/src/converter/builtin_converters.cpp"

...failed gcc.compile.c++ bin.v2/libs/python/build/gcc-9/release/threading-multi/converter/builtin_converters.o...
```
