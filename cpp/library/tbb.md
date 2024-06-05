# tbb

使用Intel TBB实现可串行化冲突
首先，你需要安装Intel TBB库。如果你还没有安装，可以通过以下方式安装：

- 在Linux上，你可以使用包管理器安装，比如`apt-get`：
```bash
sudo apt-get install libtbb-dev
```

- 在Windows上，你可以从Intel官网下载安装包。
接下来，是示例代码：

```cpp
#include <iostream>
#include <vector>
#include <tbb/tbb.h>

// 共享资源
int shared_resource = 0;

// 一个线程执行的函数
void increment(int thread_id) {
    tbb::mutex::scoped_lock lock(mtx);  // 锁定互斥锁
    
    // 访问和修改共享资源
    std::cout << "Thread " << thread_id << " is incrementing the shared resource." << std::endl;
    shared_resource++;
    std::cout << "Shared resource after increment: " << shared_resource << std::endl;
}

int main() {
    const int num_threads = 10;
    std::vector<std::thread> threads;

    // 使用tbb::parallel_for并行执行线程
    tbb::parallel_for(0, num_threads, [](int i) {
        increment(i);
    });

    std::cout << "Final value of shared resource: " << shared_resource << std::endl;
    return 0;
}
```

### 代码解释：

1. 共享资源：`shared_resource`是所有线程访问和修改的共享变量。
2. TBB库：包括头文件`tbb/tbb.h`来使用TBB库中的功能。
3. 互斥锁：使用`tbb::mutex`来保护共享资源的访问。
4. 线程函数：`increment`函数在访问和修改共享资源前锁定互斥锁。
5. 主函数：
    - 使用`tbb::parallel_for`并行执行线程，避免了手动管理线程的创建和同步。
    - 打印最终的共享资源值。
TBB库提供了更高层次的抽象，使并行编程更加简洁和高效。通过使用`tbb::parallel_for`，我们可以轻松地并行执行多个线程，并保证线程安全。
