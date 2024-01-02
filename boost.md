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



b2 工具是 Boost C++ 库的构建工具，它是 Boost 库的一部分。Boost 是一个广泛使用的 C++ 库集合，提供了许多功能强大且经过广泛测试的组件，涵盖了从基本工具到高级功能的各个领域。

b2 工具主要用于构建和安装 Boost 库。它提供了一种简单而灵活的方式来配置、构建和安装 Boost 库，使开发人员能够轻松集成 Boost 到自己的项目中。

以下是 b2 工具的一些主要功能：

1. 构建 Boost 库：b2 工具可以根据你的需求构建特定的 Boost 库。你可以选择要构建的库组件、库类型（静态库或共享库）、目标平台和编译器等配置选项。b2 工具会自动处理依赖关系，并根据你的配置生成所需的库文件。

2. 安装 Boost 库：b2 工具可以将构建好的 Boost 库安装到指定位置，以便你的项目可以使用这些库。安装过程会将库文件和相关的头文件复制到指定的目录中，并生成相应的构建配置文件，以便你的项目可以正确地链接和使用 Boost 库。

3. 自定义配置：b2 工具提供了丰富的配置选项，可以根据你的需求进行自定义配置。你可以指定编译器选项、目标平台、库的版本、调试选项等。

4. 构建变体：b2 工具支持构建不同的 Boost 库变体，如调试版本和发布版本、动态链接库和静态库等。你可以根据需要选择所需的构建变体，以满足特定的项目需求。

5. 依赖管理：b2 工具可以自动处理 Boost 库的依赖关系。当你选择构建特定的 Boost 库时，b2 工具会自动处理该库所依赖的其他 Boost 组件，并确保它们被正确构建和链接。

总之，b2 工具是 Boost C++ 库的构建工具，它简化了 Boost 库的配置、构建和安装过程，使开发人员能够轻松地集成 Boost 库到他们的 C++ 项目中。

希望这个解答能够帮助你理解 b2 工具的作用。如有任何进一步的问题，请随时提问！

## 源代码安装
https://www.boost.org/doc/libs/1_65_0/doc/html/bbv2.html#bbv2.installation

https://www.baeldung.com/linux/boost-install-on-ubuntu

https://www.boost.org/users/history/version_1_65_0.html


https://boostorg.jfrog.io/ui/packages