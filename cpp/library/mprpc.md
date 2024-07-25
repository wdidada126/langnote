# mprpc

## zk c client

https://github.com/apache/zookeeper/tree/release-3.4.2/src/c

### conan2 zk 3.8.1

```
/usr/bin/cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_MAKE_PROGRAM=/usr/bin/make -DCMAKE_C_COMPILER=/usr/bin/gcc -DCMAKE_CXX_COMPILER=/usr/bin/g++ -DCMAKE_PROJECT_TOP_LEVEL_INCLUDES=conan_provider.cmake -DCONAN_COMMAND=D:\dev_tools\Conan\conan\conan.exe -G "CodeBlocks - Unix Makefiles" -S /home/wdidada/testzookeeperclientc -B /home/wdidada/testzookeeperclientc/cmake-build-debug-ubuntu22
```

```
/usr/bin/cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_MAKE_PROGRAM=/usr/bin/make -DCMAKE_C_COMPILER=/usr/bin/gcc -DCMAKE_CXX_COMPILER=/usr/bin/g++ -DCMAKE_PROJECT_TOP_LEVEL_INCLUDES="conan_provider.cmake" -DCONAN_COMMAND="/home/wdidada/.local/bin/conan" -G "CodeBlocks - Unix Makefiles" -S /home/wdidada/testzookeeperclientc -B /home/wdidada/testzookeeperclientc/cmake-build-debug-ubuntu22
```

/home/wdidada/.conan2/p/b/zookecf49b8b0d7f3e/p/lib

C:\Users\edida\.conan2\p\zooke736c622ee4b2a\s\src\zookeeper-client