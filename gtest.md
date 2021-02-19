# gtest

vcpkg install gtest



```
The package gtest is compatible with built-in CMake targets:

    enable_testing()

    find_package(GTest CONFIG REQUIRED)
    target_link_libraries(main PRIVATE GTest::gtest GTest::gtest_main GTest::gmock GTest::gmock_main)

    add_test(AllTestsInMain main)
```





官方doc

googletest github 仓库

docs文件夹

md文件



支持Linux Mac Windows平台



cmake配置gtest，是另外的可执行文件
类比JUnit，也是另外的main函数

```

The package gtest is compatible with built-in CMake targets:

    enable_testing()

    find_package(GTest CONFIG REQUIRED)
    target_link_libraries(main PRIVATE GTest::gtest GTest::gtest_main GTest::gmock GTest::gmock_main)

    add_test(AllTestsInMain main)

```



```
target_link_libraries(example libgtest.a)
```

```
target_link_libraries(example gtest_main)
```





c 单元测试 gtest

https://blog.csdn.net/u014775175/article/details/65643698