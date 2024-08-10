date

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
