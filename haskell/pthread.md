# pthread



1.因为pthread不是C标准库，需要链接 

2.在CMakeLists.txt里添加： 

　　FIND_PACKAGE(Threads REQUIRED) 

　　TARGET_LINK_LIBRARIES(${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT})

