# date

## 备注
date 3.0.1 要求c++17，否则time_zone报错
cmakelistx.txt里面有
conan date页面我没找到相关要求

maven 库要求java11，如果用java8编译，如何报错？

## dd

https://github.com/HowardHinnant/date

git clone https://github.com/HowardHinnant/date.git
cd date
git checkout v3.0.1
mkdir build
cd build
cmake -DENABLE_DATE_TESTING=ON -DBUILD_TZ_LIB=ON ../
cmake --build .
cmake --install .

cmake --install .
-- Install configuration: ""
-- Installing: /usr/local/include/date/date.h
-- Installing: /usr/local/lib/libdate-tz.a
-- Installing: /usr/local/include/date/tz.h
-- Installing: /usr/local/lib/cmake/date/dateTargets.cmake
-- Installing: /usr/local/lib/cmake/date/dateTargets-noconfig.cmake
-- Installing: /usr/local/lib/cmake/date/dateConfig.cmake
-- Installing: /usr/local/lib/cmake/date/dateConfigVersion.cmake


编译选项：
date: USE_SYSTEM_TZ_DB OFF
date: MANUAL_TZ_DB OFF
date: USE_TZ_DB_IN_DOT OFF
date: BUILD_SHARED_LIBS OFF
date: ENABLE_DATE_TESTING ON
date: DISABLE_STRING_VIEW OFF. 

在C++中，date库（也被称为 "Howard Hinnant's date/time library"）是一个第三方库，它基于C++11（以及之后的版本）的 <chrono> 库，但提供了更为方便和强大的日期和时间处理能力。这个库并不直接包含在C++标准库中，但你可以通过下载源码或者通过包管理器（如vcpkg, Conan, 或者Homebrew等）来安装它。

