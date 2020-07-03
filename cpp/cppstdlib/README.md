<<<<<<< HEAD
# cppstdlib

cppstdlib 随书源码

[cppstdlib](http://www.cppstdlib.com/)


https://book.douban.com/subject/26419721/


Chap. 6

```c++
vector
#include <vector>
void push_back(const value_type& __x)
int size()
vectorVariableName[i]
```


double ended queue

```c++
deque
#include <deque>
void push_front(value_type&& __x)
int size()
dequeVariableName[i]
```


```shell
g++ array1.cpp -o array1
In file included from /usr/include/c++/5/array:35:0,
                 from array1.cpp:11:
/usr/include/c++/5/bits/c++0x_warning.h:32:2: error: #error This file requires compiler and library support for the ISO C++ 2011 standard. This support must be enabled with the -std=c++11 or-std=gnu++11 compiler options.
 #error This file requires compiler and library support \
  ^
array1.cpp: In function ‘int main()’:
array1.cpp:19:5: error: ‘array’ was not declared in this scope
     array<string,5> coll = { "hello", "world" };
     ^
array1.cpp:19:17: error: expected primary-expression before ‘,’ token
     array<string,5> coll = { "hello", "world" };
                 ^
array1.cpp:19:21: error: ‘coll’ was not declared in this scope
     array<string,5> coll = { "hello", "world" };
                     ^
array1.cpp:19:47: warning: extended initializer lists only available with -std=c++11 or -std=gnu++11
     array<string,5> coll = { "hello", "world" };
```


list
c++ 11
两个不同的list

- lists<>
- forward_list<>


=======
# cppstdlib

cppstdlib 随书源码

[cppstdlib](http://www.cppstdlib.com/)


https://book.douban.com/subject/26419721/


Chap. 6

```c++
vector
#include <vector>
void push_back(const value_type& __x)
int size()
vectorVariableName[i]
```


double ended queue

```c++
deque
#include <deque>
void push_front(value_type&& __x)
int size()
dequeVariableName[i]
```


```shell
g++ array1.cpp -o array1
In file included from /usr/include/c++/5/array:35:0,
                 from array1.cpp:11:
/usr/include/c++/5/bits/c++0x_warning.h:32:2: error: #error This file requires compiler and library support for the ISO C++ 2011 standard. This support must be enabled with the -std=c++11 or-std=gnu++11 compiler options.
 #error This file requires compiler and library support \
  ^
array1.cpp: In function ‘int main()’:
array1.cpp:19:5: error: ‘array’ was not declared in this scope
     array<string,5> coll = { "hello", "world" };
     ^
array1.cpp:19:17: error: expected primary-expression before ‘,’ token
     array<string,5> coll = { "hello", "world" };
                 ^
array1.cpp:19:21: error: ‘coll’ was not declared in this scope
     array<string,5> coll = { "hello", "world" };
                     ^
array1.cpp:19:47: warning: extended initializer lists only available with -std=c++11 or -std=gnu++11
     array<string,5> coll = { "hello", "world" };
```


list
c++ 11
两个不同的list

- lists<>
- forward_list<>


>>>>>>> afe522da082020e5ece0b75c43067644b2edb768
