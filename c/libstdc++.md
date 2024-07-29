# libstdc++

libc++/libstdc++
如果你写的是C++代码，这两个库也要非常重视
两个都是C++标准库
libc++是针对clang编译器特别重写的C++标准库
libstdc++自然就是gcc的事儿了
libstdc++与gcc的关系就像clang与libc++

dpkg -L libstdc++-7-doc
libstdcpp7.txt

apt search libstdc++ | grep doc

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

libstdc++-10-doc/focal-updates,focal-security 10.5.0-1ubuntu1~20.04 all
  GNU Standard C++ Library v3 (documentation files)
libstdc++-11-doc/focal 11.4.0-2ubuntu1~20.04 all
  GNU Standard C++ Library v3 (documentation files)
libstdc++-13-doc/focal 13.1.0-8ubuntu1~20.04.2 all
  GNU Standard C++ Library v3 (documentation files)
libstdc++-7-doc/focal 7.5.0-6ubuntu2 all
  GNU Standard C++ Library v3 (documentation files)
libstdc++-8-doc/focal 8.4.0-3ubuntu2 all
  GNU Standard C++ Library v3 (documentation files)
libstdc++-9-doc/focal-updates,focal-security 9.4.0-1ubuntu1~20.04.2 all
  GNU Standard C++ Library v3 (documentation files)


https://gcc.gnu.org/onlinedocs/libstdc++/

Ubuntu 22（通常指的是Ubuntu 22.04 LTS或类似版本）中的C++标准库实现主要由GNU C++库（libstdc++）提供。libstdc++是GNU项目的一部分，是GCC（GNU Compiler Collection）编译器套件中的C++标准库实现。以下是关于Ubuntu 22中C++标准库实现的详细信息：

1. libstdc++概述
功能：libstdc++提供了C++标准库的所有功能，包括容器（如vector、list）、算法、迭代器、输入/输出流、字符串处理、数学函数等。这些功能和工具是C++编程语言的核心组成部分，用于开发各种类型的应用程序。
性能：libstdc++经过优化，具有高效的执行速度和低内存占用，适合在各种规模的项目中使用。
可移植性：作为跨平台的C++标准库实现，libstdc++可以在不同的操作系统和硬件平台上运行，确保了代码的可移植性。
2. 安装与更新
在Ubuntu 22中，libstdc++通常作为GCC编译器套件的一部分自动安装。如果你需要安装或更新GCC和libstdc++，可以使用Ubuntu的包管理器apt。以下是一些基本的命令：

更新软件包列表：sudo apt update
安装GCC和libstdc++：sudo apt install build-essential（这个命令会安装GCC编译器、g++编译器以及一系列构建工具，包括libstdc++）
安装特定版本的GCC和libstdc++：Ubuntu的PPA（Personal Package Archives）可能提供了比默认仓库更新的GCC版本。你可以通过添加PPA源并安装特定版本的GCC来获取最新版本的libstdc++。例如，sudo add-apt-repository ppa:ubuntu-toolchain-r/test 然后 sudo apt install gcc-13 g++-13。
3. 验证安装
安装完成后，你可以通过运行以下命令来验证GCC和g++（以及libstdc++）的版本：

gcc --version
g++ --version
这些命令将显示已安装的GCC和g++编译器的版本信息，从而间接验证libstdc++的版本。

4. 使用C++标准库
在Ubuntu 22中，你可以使用任何支持C++的编辑器或IDE（如VS Code、CLion、Eclipse等）来编写C++程序，并利用libstdc++提供的标准库功能。只需在编译时链接到libstdc++（这通常是自动完成的），你的程序就可以使用C++标准库中的所有功能了。

5. 注意事项
确保你的GCC和g++编译器版本与你的项目需求相匹配。不同版本的编译器可能支持不同版本的C++标准（如C++11、C++14、C++17、C++20等）。
如果你在开发过程中遇到与libstdc++相关的问题，可以查阅GCC和libstdc++的官方文档或搜索相关的社区和论坛以获得帮助。
综上所述，Ubuntu 22中的C++标准库实现主要由libstdc++提供，它是GCC编译器套件的一部分，并提供了丰富的功能和工具来满足C++开发的需求。


## api doc

I. Introduction
1. Status
Implementation Status
C++ 1998/2003
Implementation Status
Implementation Specific Behavior
C++ 2011
Implementation Specific Behavior
C++ 2014
Implementation Specific Behavior
Filesystem TS
C++ 2017
Implementation Specific Behavior
Parallelism 2 TS
C++ 2020
C++ 2023
C++ TR1
Implementation Specific Behavior
C++ TR 24733
C++ IS 29124
Implementation Specific Behavior
License
The Code: GPL
The Documentation: GPL, FDL
Bugs
Implementation Bugs
Standard Bugs
2. Setup
Prerequisites
Configure
Make
3. Using
Command Options
Headers
Header Files
Mixing Headers
The C Headers and namespace std
Precompiled Headers
Macros
Dual ABI
Troubleshooting
Namespaces
Available Namespaces
namespace std
Using Namespace Composition
Linking
Almost Nothing
Finding Dynamic or Shared Libraries
Experimental Library Extensions
Concurrency
Prerequisites
Thread Safety
Atomics
IO
Structure
Defaults
Future
Alternatives
Containers
Exceptions
Exception Safety
Exception Neutrality
Memory allocation
Doing without
Compatibility
With C
With POSIX thread cancellation
Debugging Support
Using g++
Debug Mode
Tracking uncaught exceptions
Memory Leak Hunting
Non-memory leaks in Pool and MT allocators
Data Race Hunting
Using gdb
Debug Versions of Library Binary Files
Compile Time Checking
II. Standard Contents
4. Support
Types
Fundamental Types
Numeric Properties
NULL
Dynamic Memory
Additional Notes
Termination
Termination Handlers
Verbose Terminate Handler
5. Diagnostics
Exceptions
API Reference
Adding Data to exception
Use of errno by the library
Concept Checking
6. Utilities
Functors
Pairs
Memory
Allocators
Requirements
Design Issues
Implementation
Interface Design
Selecting Default Allocation Policy
Disabling Memory Caching
Using a Specific Allocator
Custom Allocators
Extension Allocators
auto_ptr
Limitations
Use in Containers
shared_ptr
Requirements
Design Issues
Implementation
Class Hierarchy
Thread Safety
Selecting Lock Policy
Related functions and classes
Use
Examples
Unresolved Issues
Acknowledgments
Traits
7. Strings
String Classes
Simple Transformations
Case Sensitivity
Arbitrary Character Types
Tokenizing
Shrink to Fit
CString (MFC)
8. Localization
Locales
locale
Requirements
Design
Implementation
Interacting with "C" locales
Future
Facets
ctype
Implementation
Specializations
Future
codecvt
Requirements
Design
wchar_t Size
Support for Unicode
Other Issues
Implementation
Use
Future
messages
Requirements
Design
Implementation
Models
The GNU Model
Use
Future
9. Containers
Sequences
list
list::size() is O(n)
Associative
Insertion Hints
bitset
Size Variable
Type String
Unordered Associative
Insertion Hints
Hash Code
Hash Code Caching Policy
Interacting with C
Containers vs. Arrays
10. Iterators
Predefined
Iterators vs. Pointers
One Past the End
11. Algorithms
Mutating
swap
Specializations
12. Numerics
Complex
complex Processing
Generalized Operations
Interacting with C
Numerics vs. Arrays
C99
13. Input and Output
Iostream Objects
Stream Buffers
Derived streambuf Classes
Buffering
Memory Based Streams
Compatibility With strstream
File Based Streams
Copying a File
Binary Input and Output
Interacting with C
Using FILE* and file descriptors
Performance
14. Atomics
API Reference
15. Concurrency
API Reference
III. Extensions
16. Compile Time Checks
17. Debug Mode
Intro
Semantics
Using
Using the Debug Mode
Using a Specific Debug Container
Design
Goals
Methods
The Wrapper Model
Safe Iterators
Safe Sequences (Containers)
Precondition Checking
Release- and debug-mode coexistence
Compile-time coexistence of release- and debug-mode components
Link- and run-time coexistence of release- and debug-mode components
Alternatives for Coexistence
Other Implementations
18. Parallel Mode
Intro
Semantics
Using
Prerequisite Compiler Flags
Using Parallel Mode
Using Specific Parallel Components
Design
Interface Basics
Configuration and Tuning
Setting up the OpenMP Environment
Compile Time Switches
Run Time Settings and Defaults
Implementation Namespaces
Testing
Bibliography
19. The mt_allocator
Intro
Design Issues
Overview
Implementation
Tunable Parameters
Initialization
Deallocation Notes
Single Thread Example
Multiple Thread Example
20. The bitmap_allocator
Design
Implementation
Free List Store
Super Block
Super Block Data Layout
Maximum Wasted Percentage
allocate
deallocate
Questions
1
2
3
Locality
Overhead and Grow Policy
21. Policy-Based Data Structures
Intro
Performance Issues
Associative
Priority Que
Goals
Associative
Policy Choices
Underlying Data Structures
Iterators
Functional
Priority Queues
Policy Choices
Underlying Data Structures
Binary Heaps
Using
Prerequisites
Organization
Tutorial
Basic Use
Configuring via Template Parameters
Querying Container Attributes
Point and Range Iteration
Examples
Intermediate Use
Querying with container_traits
By Container Method
Hash-Based
Branch-Based
Priority Queues
Design
Concepts
Null Policy Classes
Map and Set Semantics
Distinguishing Between Maps and Sets
Alternatives to std::multiset and std::multimap
Iterator Semantics
Point and Range Iterators
Distinguishing Point and Range Iterators
Invalidation Guarantees
Genericity
Tag
Traits
By Container
hash
Interface
Details
tree
Interface
Details
Trie
Interface
Details
List
Interface
Details
Priority Queue
Interface
Details
Testing
Regression
Performance
Hash-Based
Text find
Integer find
Integer Subscript find
Integer Subscript insert
Integer find with Skewed-Distribution
Erase Memory Use
Branch-Based
Text insert
Text find
Text find with Locality-of-Reference
split and join
Order-Statistics
Multimap
Text find with Small Secondary-to-Primary Key Ratios
Text find with Large Secondary-to-Primary Key Ratios
Text insert with Small Secondary-to-Primary Key Ratios
Text insert with Small Secondary-to-Primary Key Ratios
Text insert with Small Secondary-to-Primary Key Ratios Memory Use
Text insert with Small Secondary-to-Primary Key Ratios Memory Use
Priority Queue
Text push
Text push and pop
Integer push
Integer push
Text pop Memory Use
Text join
Text modify Up
Text modify Down
Observations
Associative
Priority_Queue
Acknowledgments
Bibliography
22. HP/SGI Extensions
Backwards Compatibility
Deprecated
23. Utilities
24. Algorithms
25. Numerics
26. Iterators
27. Input and Output
Derived filebufs
28. Demangling
29. Concurrency
Design
Interface to Locks and Mutexes
Interface to Atomic Functions
Implementation
Using Built-in Atomic Functions
Thread Abstraction
Use
IV. Appendices
A. Contributing
Contributor Checklist
Reading
Assignment
Getting Sources
Submitting Patches
Directory Layout and Source Conventions
Coding Style
Bad Identifiers
By Example
Design Notes
B. Porting and Maintenance
Configure and Build Hacking
Prerequisites
Overview
General Process
What Comes from Where
Configure
Storing Information in non-AC files (like configure.host)
Coding and Commenting Conventions
The acinclude.m4 layout
GLIBCXX_ENABLE, the --enable maker
Shared Library Versioning
Make
Generated files
Writing and Generating Documentation
Introduction
Generating Documentation
Doxygen
Prerequisites
Generating the Doxygen Files
Debugging Generation
Markup
Docbook
Prerequisites
Generating the DocBook Files
Debugging Generation
Editing and Validation
File Organization and Basics
Markup By Example
Porting to New Hardware or Operating Systems
Operating System
CPU
Character Types
Thread Safety
Numeric Limits
Libtool
Testing
Test Organization
Directory Layout
Naming Conventions
Running the Testsuite
Basic
Variations
Permutations
Writing a new test case
Examples of Test Directives
Directives Specific to Libstdc++ Tests
Test Harness and Utilities
DejaGnu Harness Details
Utilities
Special Topics
Qualifying Exception Safety Guarantees
Overview
Existing tests
C++11 Requirements Test Sequence Descriptions
ABI Policy and Guidelines
The C++ Interface
Versioning
Goals
History
Prerequisites
Configuring
Checking Active
Allowed Changes
Prohibited Changes
Implementation
Testing
Single ABI Testing
Multiple ABI Testing
Outstanding Issues
API Evolution and Deprecation History
3.0
3.1
3.2
3.3
3.4
4.0
4.1
4.2
4.3
4.4
4.5
4.6
4.7
4.8
4.9
5
5.3
6
7
7.2
7.3
8
9
10
11
12
12.3
13
13.3
14
Backwards Compatibility
First
Second
Third
Pre-ISO headers removed
Extension headers hash_map, hash_set moved to ext or backwards
No ios::nocreate/ios::noreplace.
No stream::attach(int fd)
Support for C++98 dialect.
Support for C++TR1 dialect.
Support for C++11 dialect.
Container::iterator_type is not necessarily Container::value_type*
C. Free Software Needs Free Documentation
D. GNU General Public License version 3
E. GNU Free Documentation License

https://gcc.gnu.org/onlinedocs/libstdc++/index.html

下载
https://gcc.gnu.org/pub/gcc/libstdc++/doxygen/