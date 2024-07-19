# crow
## conan

https://conan.io/center/recipes/crowcpp-crow?version=1.2.0

## vcpkg
vcpkg list crow
crow:x64-windows                                  1.0-5               Very fast and easy to use C++ micro web framework

https://github.com/CrowCpp/Crow

https://github.com/CrowCpp/Crow/tags

https://crowcpp.org/

## 例子

D:\git\github\cppcrow_v1_0_5_examples

https://github.com/edidada/cppcrow_v1_0_5_examples

vcpkg.json

{
    "name": "crow",
    "version-string": "master",
    "dependencies": [
        "asio",
        "openssl",
        "zlib"
    ]
}

https://github.com/CrowCpp/Crow/blob/master/Doxyfile

Crow
v1.0+5

maven是可以制定依赖库的版本的，甚至根据os来判断是否需要某个库
Crow是使用cmake构建的，没有安装boost报错

```cmake
CMake Error at /usr/local/share/cmake-3.30/Modules/FindPackageHandleStandardArgs.cmake:233 (message):
  Could NOT find Boost (missing: Boost_INCLUDE_DIR system date_time)
-- Configuring incomplete, errors occurred!
  (Required is at least version "1.64")
```



安装
libboost-atomic1.74.0 libboost-chrono-dev libboost-chrono1.74-dev

Crow/include/crow/routing.h:431:29: error: no match for ‘operator=’ (operand types are ‘std::function<bool(const crow::request&)>’ and ‘C_A_T_C_H_T_E_S_T_112()::<lambda(const crow::request&, void**)>’) 报错



-- Found Boost: /usr/lib/x86_64-linux-gnu/cmake/Boost-1.71.0/BoostConfig.cmake (found suitable version "1.71.0", minimum required is "1.64") found components: system date_time
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Failed
-- Looking for pthread_create in pthreads
-- Looking for pthread_create in pthreads - not found
-- Looking for pthread_create in pthread
-- Looking for pthread_create in pthread - found
-- Found Threads: TRUE
-- The C compiler identification is GNU 9.4.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- example_compression example deactivated
-- example_ssl example deactivated
-- Compression tests are omitted. (Configure with CROW_ENABLE_COMPRESSION=ON to enable them)
-- SSL tests are omitted. (Configure with CROW_ENABLE_SSL=ON to enable them)
-- Configuring done (1.5s)
-- Generating done (0.0s)



