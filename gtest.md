# gtest

vcpkg install gtest

### GTest

- GTEST_API_
- TEST
- EXPECT_EQ
- 

```c
testing::InitGoogleTest(&argc, argv);
```

```c
RUN_ALL_TESTS()
```

### vcpkg安装的库
头文件在vcpkg/installed/x64-linux/include

[wdidada@10-23-29-39 include]$ cd gtest/
[wdidada@10-23-29-39 gtest]$ ls
gtest-death-test.h  gtest-message.h     gtest-printers.h  gtest-test-part.h
gtest.h             gtest-param-test.h  gtest_prod.h      gtest-typed-test.h
gtest-matchers.h    gtest_pred_impl.h   gtest-spi.h       internal
[wdidada@10-23-29-39 gtest]$ pwd


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