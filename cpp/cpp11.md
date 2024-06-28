# cpp11

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
