# fast_io

https://gitee.com/edidada/fast_io

https://ewindy.gitee.io/fast_io_rst/index.html


作者：cqwrteur
链接：https://www.zhihu.com/question/485969746/answer/2114579596
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

C with Classes淘汰了。现在流行C with Concepts.请禁用
int
面向对象
iostream
stdio.h
cstdio
fstream
format
charconv
filesystem
locale
friend
private
protected
成员函数
getter/setter
virtual
std::unique_ptr
std::shared_ptr
std::weak_ptr
ranges
异常处理
RTTISFINAE
std::addressof
std::move
std::forward
std::array
std::stringboost
GCC 12淘汰了。现在流行GCC 13
clang 14淘汰了。现在流行clang 15VS 2019淘汰了。现在流行vs 2022用淘汰货的就是卢瑟。算了来个白名单吧。你只能include这些头文件，用这些头文件以外的就是卢瑟。
<cstddef>
<limits>
<cfloat>
<climits>
<version>
<cstdint> 部分的<cstdlib>(只能用std::abort()) <new>
<source_location> <initializer_list> <compare> <coroutine> <cstdarg> <concepts> <type_traits> <bit> <atomic>用这些头文件以外的任何功能都会导致你的代码无法移植。 所以嘛, std::addressof, std::move, std::forward, std::array都是不能用的谢谢。
