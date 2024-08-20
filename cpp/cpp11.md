# cpp11
Youtube-CppNuts的Threading In C++系列视频

https://zhuanlan.zhihu.com/p/556406170
https://zhuanlan.zhihu.com/p/348492524

lock_guard是类模板，在其构造函数中自动给std::mutex加锁，在退出作用域的时候自动解锁，这样就可以保证std::mutex的正确操作，这也是RAII（获取资源便初始化）技术的体现。

C++11中提供了4中互斥量。

std::mutex;                  //非递归的互斥量
std::timed_mutex;            //带超时的非递归互斥量
std::recursive_mutex;        //递归互斥量
std::recursive_timed_mutex;  //带超时的递归互斥量

lock_guard<mutex> 是 C++11 引入的一个智能锁管理类，它用于自动管理互斥锁（mutex）的加锁（lock）和解锁（unlock）操作，以简化线程同步代码的编写，并减少死锁的风险。

当你看到这样的代码：

cpp
lock_guard<mutex> lock(queueMutex);
这行代码的作用是：

自动加锁：当 lock_guard<mutex> 类型的对象 lock 被创建时，它会自动对其构造函数中传入的互斥锁 queueMutex 进行加锁操作。这意味着，从 lock 对象被创建的那一刻起，queueMutex 就被锁定了，任何尝试再次锁定 queueMutex 的线程都会被阻塞，直到 lock 对象被销毁并且 queueMutex 被解锁。
作用域限制：lock_guard<mutex> 对象的生命周期是由它的作用域决定的。一旦 lock 对象离开其所在的作用域（比如函数返回、循环结束、条件语句块结束等），lock 对象就会被销毁。在销毁过程中，lock_guard<mutex> 会自动调用其析构函数，该析构函数负责释放（即解锁）它管理的互斥锁 queueMutex。这种机制确保了互斥锁只在其需要被锁定的代码块内保持锁定状态，减少了死锁的可能性，并简化了锁的管理。
避免忘记解锁：使用 lock_guard<mutex> 可以避免忘记手动解锁互斥锁的问题。在复杂的代码逻辑中，手动管理锁（即使用 mutex.lock() 和 mutex.unlock()）时，很容易因为控制流的变化（如异常抛出、提前返回等）而忘记解锁互斥锁，从而导致死锁或其他同步问题。而 lock_guard<mutex> 通过其自动析构特性，确保了互斥锁总能在合适的时机被解锁。
综上所述，lock_guard<mutex> 通过其自动加锁和解锁的特性，简化了线程同步代码的编写，降低了死锁的风险，是 C++11 及以上版本中推荐使用的线程同步工具之一。

https://en.cppreference.com/w/cpp/11

https://github.com/makelinux/examples/blob/HEAD/cpp/11.cpp


- CO使用的C++11特性:

- - auto
  - std::move
  - std::bind
  - std::function
  - std::unique_ptr
  - std::unordered_map
  - std::unordered_set
  - variadic templates

https://www.bilibili.com/video/BV11x411Z7zk?t=1231&p=2


## auto

当类型明确时：如果变量的类型是明确的，例如int或double，那么没有必要使用auto进行类型推导。直接声明类型可以提高代码的可读性。
API文档和接口：当你正在编写公共API或库时，为了确保接口的清晰性，最好避免使用auto。这样，用户可以清楚地知道函数的返回类型或参数类型。
涉及多态的情况：如果你正在处理涉及多态的代码，例如基类和派生类的关系，使用auto可能会导致类型切割，从而失去多态性。

### 微软auto (C++)
https://learn.microsoft.com/zh-cn/cpp/cpp/auto-cpp?view=msvc-170

可能不需要使用 auto 的转换情况：
你需要一个特定类型，任何其他类型都不行。
例如，在表达式模板帮助程序类型 (valarray+valarray) 中。

### 华为 C++11之啥时候不要用 auto

https://developer.huawei.com/consumer/cn/forum/topic/41599425?fid=26

对于C++11的auto关键字，感觉使用的过程并没有做到得心应手，知其然不知其所以然。
所以系统学习并总结一下，我们什么时候应该使用auto来定义变量。

1）当然是少写N多的字符

// 获取迭代器的类型
typename std::iterator_traits<It>::value_type currValue = *b; //C++98写法
auto currValue = *b; //C++11写法，可以看到简练很多

2）避免未初始化的变量

int x1; // 未初始化
auto x2; // 编译错误！使用auto必须初始化
auto x3 = 0; // 正确！

3）直接持有closure（闭包）

// 类比较函数（函数类型【这里应该特指返回值类型，因为参数类型是知道的】仅编译器知道）
auto derefUPLess = [](const std::unique_ptr<Widget>& p1,
                     const std::unique_ptr<Widget>& p2) {
   return *p1 < *p2;
};
// c++14 auto可以用于函数参数，写法将更加简洁
auto derefUPLess = [](const auto& p1,
                     const auto& p2) {
   return *p1 < *p2;
};

《Effective Modern C++》中有提到，auto声明比std::function性能更好（后者会涉及到一些复制操作等，未深究）。

4）避免类型不匹配问题

例1
std::vector<int> v;
…
unsigned sz = v.size();

v.size()的返回值是std::vector<int>::size_type，从官网上的说明可以看到它就是size_t（unsigned integer types）。对于 Intel架构平台，各数据类型实际所占字节如下（引自Integer sizes in C on 32 bit and 64 bit Linux）：

type  executable[1] 32 bit  64 bit
short int 16 bit  16 bit
int 32 bit  32 bit
long int  32 bit  64 bit
long long int 64 bit  64 bit
size_t  32 bit  64 bit
void* [2] 32 bit  64 bit

可以看到，对于 64 位平台，[unsigned ] int与size_t不等，所以上述代码在 64 位平台下可能出现“类型截断”。这时候，使用 auto 就是更好的选择了：

auto sz = v.size(); // sz's type is std::vector<int>::size_type

例2
std::unordered_map<std::string, int> m;
…
for (const std::pair<std::string, int>& p : m)
{
… // do something with p
}

这里有一个陷阱需要注意，就是 map 的 key 是不可变的（map keys are semantically immutable），所以所有对于 map key 的直接操作（譬如解引用迭代器，产生value_type），都会对 key 加上const属性（参考What is difference between const and non const key?）。

也就是说，上面的例子中，map 中的std::pair类型是std::pair<const std::string, int>，而不是std::pair<std::string, int>。 所以将 p 声明为std::pair<std::string, int>后，编译器会尝试将std::pair<std::string, int>转换为std::pair<const std::string, int>。这个过程是这么实现的：对每个 p 想要绑定的 m 中的一员，先将其复制到一个临时对象，然后将 p 绑定到这个临时变量上。在每次循环最后，这个临时对象会被销毁。
上面的过程，其实与你的“初心”是不符的，因为你仅仅只是想将 p 绑定到 m 的所有元素而已。
当然，这时候使用 auto 就能避免这样的“类型不匹配”了：

for (const auto& p : m)
{
… // as before
}

除去类型正确、字符更少的好处，这里还有一点值得提出，就是获取 p 的地址的时候，可以正确的拿到 m 里元素的地址。在不使用 auto 的写法中，获取 p 的地址拿到的是临时对象的地址，而这个临时对象是在循环结束前会被销毁的。

5）利于代码重构
想像一个场景：你定义的一个函数返回int类型，然而随着你的软件使用，int已经不能满足你的需求，你需要将返回值改为long。此时，假如在获取返回值的地方，你是用的是 auto，那么你只需要在函数声明和函数定义处修改。假如你是用的是精确类型定义，那你就需要找出每个调用了此函数并用int类型获取返回值的地方，并全部修改它们。
总结
auto 可以显著减少输入的字符数，可以避免未初始化变量的出现（因为定义 auto 变量必须初始化），也可以防止因为类型不匹配导致的程序错误（例1）及性能问题（例2），对代码重构的工作量也有一定的帮助。
上篇文章总结了为什么需要尽量使用 auto，这篇文章总结一下，我们什么时候不应该使用 auto，或者说什么情况下使用 auto 会导致意料之外的错误。

假设现在有这样一个函数 features，返回 std::vector<bool>。有代码如下：
```c++
#include <iostream>
#include <vector>

// 返回 std::vector<bool>
std::vector<bool> features() {
 return std::vector<bool>{true, false, true};
}

void processWidget(bool p) {
 std::cout << p << std::endl;
}

int main(void) {
 // 这里使用bool获取返回值
 bool highPriority = features()[2];
 processWidget(highPriority);

 return 0;
}
```

上面这段代码可以准确无误的运行。至此，一切都按照我们的意愿在运转，高兴！

~/study/c++/type_deduce on  master! ⌚ 16:56:10
$ g++ -std=c++11 -g 05_not_use_auto.cc

~/study/c++/type_deduce on  master! ⌚ 16:56:10
$ ./a.out
1

这时候的我，灵机一动，想到上篇文章中使用 auto 的诸多好处，决定将 bool 直接替换为 auto，即：
```c++
#include <iostream>
#include <vector>

// 返回 std::vector<bool>
std::vector<bool> features() {
 return std::vector<bool>{true, false, true};
}

void processWidget(bool p) {
 std::cout << p << std::endl;
}

int main(void) {
 // 这里使用auto替换bool，获取返回值
 auto highPriority = features()[2];
 processWidget(highPriority);// 此时运行结果是未定义行为

 return 0;
}
```

再编译一把，正常通过，大功告成。

接着运行，应该是没有问题：

$ ./a.out
0 #结果却出乎意料！

结果却与想象的不太一样，这是为何？

接下来探究其中缘由（这里涉及的底层原理很复杂，下面只是简略版本，其实我自己理解的也不是很好）。

在使用 auto 获取返回结果的版本中，highPriority 的类型已经不再是 bool了。std::vector<bool> 的 [] 操作符并不返回容器中一个对象的引用（除了容器中的对象是bool类型外，[] 操作符都是返回容器中一个对象的引用），而是返回一个 std::vector<bool>::reference 类型（嵌套在 std::vector<bool> 中的一个类）的对象。

std::vector<bool>::reference 的存在是因为 std::vector<bool> 使用一种压缩的方式来存储它的“bools”对象，使用一个 bit 存储一个 bool。这就导致了 [] 操作符的返回值问题， [] 操作符按理来说应该返回一个 T&，但是 C++ 禁止对 bit 进行引用。不能返回一个 bool&，所以只能返回一个行为类似 bool& 的对象std::vector<bool>::reference。

这个时候我们再来理解上面两段代码的不同之处：

bool highPriority = features()[2];在这里，features 函数返回一个 std::vector<bool>  对象，然后调用[] 操作符。[] 操作符返回一个 std::vector<bool>::reference 对象，然后通过显示转换成 bool 类型，对 highPriority 进行初始化。这时候 highPriority 的值就是 std::vector<bool> 中的 bit 2。

auto highPriority = features()[2];相同的是，features 函数返回一个 std::vector<bool> 对象，然后调用[] 操作符。[] 操作符返回一个 std::vector<bool>::reference 对象。事情到了这里有了一点不同，因为 highPriority 的类型是通过 auto 来自动推导的。这时候 highPriority 的值是什么，取决于 std::vector<bool>::reference 的实现，这导致了 highPriority 的值具体是什么，这是一个未定义的行为。

可以使用所谓显示指定类型初始化规则（the explicitly typed initializer idiom）来避免这个错误：

auto highPriority = static_cast<bool>(features()[2]);

这时候你可能又有疑问，直接使用 bool 不就好了吗？为啥还要使用 auto，再经过一个强制转换来定义？

好处在于，可以明确的告诉读代码的人，这里我特意做了某个特殊处理。

譬如，计算方差函数返回double类型：

double calcEpsilon(); // return tolerance value

假设你在使用的时候明确知道float已经满足需求了，并且你就是想用float来存储计算结果，当然你可以用如下代码：

float ep = calcEpsilon(); // impliclitly convert double → float

但是这个会很难表明“我故意减小函数返回值的精度”，使用显示指定类型初始化规则，则代码如下：

auto ep = static_cast<float>(calcEpsilon());


## move
在C++11中，std::move是一个非常有用的函数模板，它位于<utility>头文件中。std::move本身并不移动任何东西，它的主要作用是将其参数转换为右值引用（rvalue reference），从而允许我们利用移动语义（move semantics）来优化资源管理和性能。移动语义允许对象通过“窃取”资源（如动态分配的内存、文件句柄等）的方式被高效地转移，而不是通过复制。

代码例子
以下是一个使用std::move的示例，展示了如何在自定义类型中实现移动构造函数和移动赋值运算符，并演示了std::move的使用。

cpp
#include <iostream>  
#include <utility> // 包含std::move  
  
class Buffer {  
public:  
    char* data;  
    size_t size;  
  
    // 构造函数  
    Buffer(size_t s) : size(s) {  
        data = new char[s];  
        std::cout << "Buffer allocated: " << data << std::endl;  
    }  
  
    // 析构函数  
    ~Buffer() {  
        delete[] data;  
        std::cout << "Buffer deallocated: " << data << std::endl;  
    }  
  
    // 禁用拷贝构造函数和拷贝赋值运算符（为了简单起见）  
    Buffer(const Buffer&) = delete;  
    Buffer& operator=(const Buffer&) = delete;  
  
    // 移动构造函数  
    Buffer(Buffer&& other) noexcept : data(other.data), size(other.size) {  
        other.data = nullptr; // 将源对象的指针置为空，避免删除同一内存  
        other.size = 0;  
    }  
  
    // 移动赋值运算符  
    Buffer& operator=(Buffer&& other) noexcept {  
        if (this != &other) {  
            delete[] data; // 释放当前对象的资源  
            data = other.data;  
            size = other.size;  
            other.data = nullptr; // 将源对象的指针置为空  
            other.size = 0;  
        }  
        return *this;  
    }  
  
    // 为了示例，我们添加一个函数来打印数据地址  
    void printAddress() const {  
        std::cout << "Buffer address: " << data << std::endl;  
    }  
};  
  
int main() {  
    Buffer buf1(100); // 分配100字节  
    buf1.printAddress();  
  
    // 使用std::move来触发移动构造函数  
    Buffer buf2 = std::move(buf1);  
  
    // 注意：此时buf1处于有效但未定义的状态，因为我们重写了它的指针  
    // 在实际应用中，你应该避免使用buf1，直到它被重新赋值或销毁  
  
    // buf2现在拥有原buf1的资源  
    buf2.printAddress(); // 应该与buf1之前打印的地址相同  
  
    // 销毁buf2，这将释放内存  
    // 注意：buf1的析构函数不会被自动调用，因为buf1的指针已经被我们设置为nullptr  
    // 如果你尝试销毁buf1，它将尝试删除nullptr，这是安全的但无用  
}
注意：

在上面的例子中，我们禁用了拷贝构造函数和拷贝赋值运算符，这是为了避免不必要的复制，并强制使用移动语义。
当我们调用std::move(buf1)时，我们并没有真正移动buf1的内容；我们只是获得了一个可以被当作右值引用的buf1的引用。然后，这个右值引用被用于调用移动构造函数或移动赋值运算符。
移动操作后，源对象（在这个例子中是buf1）处于有效但未定义的状态。这意味着它的析构函数仍然可以安全地被调用，但你不能假设它的任何成员变量（在这个例子中是data和size）有特定的值。在实际应用中，你可能需要在移动后重置或重新赋值源对象。
noexcept关键字用于指示函数不会抛出异常，这可以优化某些情况下的代码生成。如果你的移动构造函数或移动赋值运算符确实不会抛出异常，你应该使用它。

## mutex

mutex头文件是c++哪个版本开始支持的？ api列表，代码例子
mutex头文件是C++11版本开始支持的。在C++11中，<mutex>是C++标准程序库中的一个头文件，它定义了C++11标准中的一些互斥访问的类与方法等，用于多线程编程中保护共享数据不被同时访问。

mutex API列表
<mutex>头文件中定义的与mutex相关的类和函数主要包括：

std::mutex：最基本的互斥锁类，不能被递归使用。
std::recursive_mutex：递归互斥锁类，允许同一个线程多次对同一个互斥锁进行加锁。
std::timed_mutex：定时互斥锁类，提供了try_lock_for和try_lock_until成员函数，允许线程在一定时间内尝试获取锁。
std::recursive_timed_mutex：带定时的递归互斥锁类，结合了std::recursive_mutex和std::timed_mutex的特性。
std::lock_guard：与Mutex RAII（Resource Acquisition Is Initialization）相关的类模板，用于自动管理互斥锁的加锁和解锁。
std::unique_lock：与Mutex RAII相关，但提供了更灵活的上锁和解锁控制。
代码例子
以下是一个使用std::mutex的简单代码例子，展示了如何在多线程环境中保护共享数据：

cpp
#include <iostream>  
#include <thread>  
#include <mutex>  
  
std::mutex mtx; // 定义一个互斥锁  
int shared_data = 0; // 定义一个共享数据  
  
void increment_shared_data() {  
    mtx.lock(); // 加锁  
    ++shared_data; // 修改共享数据  
    mtx.unlock(); // 解锁  
}  
  
int main() {  
    std::thread t1(increment_shared_data); // 创建第一个线程  
    std::thread t2(increment_shared_data); // 创建第二个线程  
  
    t1.join(); // 等待第一个线程完成  
    t2.join(); // 等待第二个线程完成  
  
    std::cout << "Shared data: " << shared_data << std::endl; // 输出共享数据  
    return 0;  
}
在这个例子中，std::mutex mtx;定义了一个互斥锁对象mtx，用于保护共享数据shared_data。在increment_shared_data函数中，通过调用mtx.lock();对互斥锁进行加锁，确保在修改共享数据时不会有其他线程同时访问它。修改完成后，通过调用mtx.unlock();释放互斥锁，允许其他线程访问共享数据。

请注意，为了简化代码和避免死锁等问题，C++11还提供了std::lock_guard等RAII工具来自动管理互斥锁的加锁和解锁过程。在实际编程中，推荐使用这些工具来提高代码的安全性和可读性。