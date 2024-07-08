# pthread

https://www.man7.org/linux/man-pages/man3/pthread_rwlock_init.3p.html

1.因为pthread不是C标准库，需要链接 
2.在CMakeLists.txt里添加： 

　　FIND_PACKAGE(Threads REQUIRED) 
　　TARGET_LINK_LIBRARIES(${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT})


https://gitee.com/edidada/cpp11thread
https://www.runoob.com/w3cnote/cpp-std-thread.html

cpp11才有线程类 之前用linux c api提供的线程类
https://blog.csdn.net/qq_44861043/article/details/119643641

- pthread_rwlock_init
- pthread_rwlock_destroy
- pthread_rwlock_rdlock
- pthread_rwlock_tryrdlock
- pthread_rwlock_timedrdlock
- pthread_rwlock_wrlock
- pthread_rwlock_trywrlock
- pthread_rwlock_timedwrlock
- pthread_rwlock_unlock
- pthread_rwlockattr_init
- pthread_rwlockattr_destroy
- pthread_rwlockattr_getpshared
- pthread_rwlockattr_setpshared
- pthread_rwlockattr_getkind_np
- pthread_rwlockattr_setkind_np



- pthread_cond_init
- pthread_cond_destroy
- pthread_cond_signal
- pthread_cond_broadcast
- pthread_cond_wait
- pthread_cond_timedwait
- pthread_condattr_init
- pthread_condattr_destroy
- pthread_condattr_setpshared
- pthread_condattr_getclock
- pthread_condattr_setclock



- pthread_spin_init
- pthread_spin_destroy
- pthread_spin_lock
- pthread_spin_trylock
- pthread_spin_unlock


- pthread_barrier_init
- pthread_barrier_destroy
- pthread_barrier_wait
- pthread_barrierattr_init
- pthread_barrierattr_destroy
- pthread_barrierattr_getpshared
- pthread_barrierattr_setpshared


- pthread_key_create
- pthread_key_delete
- pthread_getspecific
- pthread_setspecific

注意跟java比较
