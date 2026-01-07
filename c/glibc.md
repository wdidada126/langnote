# glibc

在Ubuntu系统中，查看glibc（GNU C Library）的版本信息可以通过终端使用命令行工具完成。glibc是Linux系统中C语言的标准库，几乎所有的Linux系统都会用到它。下面是一些常用的方法：

1. 使用ldd命令

ldd命令主要用于打印共享库的依赖关系，但它同样可以显示glibc的版本信息。你可以简单地运行：

ldd --version

这将显示ldd工具的版本，其中包括了使用的glibc版本。

2. 使用libc.so.6

在Ubuntu系统中，glibc的主要库文件通常位于/lib/x86_64-linux-gnu/libc.so.6（对于64位系统）或/lib/i386-linux-gnu/libc.so.6（对于32位系统）。你可以通过查看这个文件的链接信息来找到其版本信息：

ls -l /lib/x86_64-linux-gnu/libc.so.6

这将显示文件的信息，包括版本号。例如，如果你看到类似libc.so.6 => /lib/x86_64-linux-gnu/libc-2.31.so，则表示你的glibc版本是2.31。

3. 使用getconf命令

getconf命令可以用来查询系统的配置变量，其中包括glibc的版本信息。要查看glibc的版本，可以使用：

getconf GNU_LIBC_VERSION

这会直接显示glibc的版本号，例如glibc 2.31。

4. 使用strings命令

你还可以使用strings命令来查看glibc的版本信息。首先，找到glibc的主要库文件：

find /lib -name libc.so.* | head -n 1

然后，使用strings命令查看其中的内容：

strings /path/to/libc.so | grep GLIBC_

这将列出与glibc相关的所有版本字符串，你可以从中找到具体的版本号。

5. 使用update-alternatives命令（对于多版本安装情况）

如果你的系统上安装了多个版本的glibc，可以使用update-alternatives命令来查看当前使用的glibc版本：

update-alternatives --display libc

这个命令将显示所有可用的glibc版本以及当前使用的版本。

以上方法中的任何一种都可以帮助你查看Ubuntu系统上的glibc版本。

## version版本

https://sourceware.org/glibc/manual/
2.41 (latest)
2.40
2.39
2.38
2.37
2.36
2.35
2.34
2.33
2.32
2.31
2.30
2.29
2.28
2.27
2.26
2.25
2.24
2.23
2.22

关注glibc版本更新日志

centos7   glibc-devel   centos7_glibc-devel.txt 
ubuntu20  libc6-dev     ubuntu20_libc6-dev.txt

## 源代码

glibc-doc/focal-updates,focal-security,now 2.31-0ubuntu9.16 all [installed]
  GNU C Library: Documentation
glibc-doc-reference/focal,now 2.30-1ubuntu1 all [installed,automatic]
  GNU C Library: Documentation
glibc-source/focal-updates,focal-security 2.31-0ubuntu9.16 all
  GNU C Library: sources

sudo apt install -y glibc-source

ftp的
https://www.gnu.org/software/libc/

https://mirrors.ustc.edu.cn/gnu/glibc/


glibc确实实现了C标准库。glibc，全称为GNU C Library，是GNU项目的一部分，为C语言程序提供了一套丰富的函数库实现。它不仅实现了ISO C标准中的函数，还遵循POSIX（可移植操作系统接口）标准，并扩展了许多与Linux特定功能相关的函数。这使得glibc成为Linux系统中最常用的C函数库之一。
https://sourceware.org/glibc/documentation.html

## 版本

2024-07-22: glibc 2.40 released.
2024-01-31: glibc 2.39 released.
2023-07-31: glibc 2.38 released.
2023-02-01: glibc 2.37 released.
2022-08-01: glibc 2.36 released.
2022-02-03: glibc 2.35 released.
2021-08-01: glibc 2.34 released.
2021-02-01: glibc 2.33 released.

glibc确实实现了C标准库。glibc，全称为GNU C Library，是GNU项目的一部分，为C语言程序提供了一套丰富的函数库实现。它不仅实现了ISO C标准中的函数，还遵循POSIX（可移植操作系统接口）标准，并扩展了许多与Linux特定功能相关的函数。这使得glibc成为Linux系统中最常用的C函数库之一。

具体来说，glibc的功能包括但不限于：

文件操作：提供了一系列用于文件读写、打开、关闭等操作的函数。
内存管理：包括内存分配、释放等函数，支持程序的内存使用需求。
字符串处理：提供了丰富的字符串操作函数，如字符串复制、比较、查找等。
数学运算：实现了数学运算相关的函数，支持基本的数学计算和高级的数学运算功能。
线程安全：glibc是线程安全的，支持多线程环境下的并发操作。
本地化支持：glibc支持多种语言和文化习惯，能够处理不同语言的字符编码和排序规则。
此外，glibc还提供了许多实用的工具和程序，如ldd（用于查看程序依赖的共享库）、locale（用于设置和查询本地化信息）等，这些工具可以帮助开发者更好地管理和调试C程序。

由于glibc的广泛兼容性和稳定性，它成为了大多数Unix和类Unix系统（如Linux）上的标准C库。glibc得到了大量的测试和优化，以确保在各种Linux发行版上的稳定性和性能。同时，glibc还提供了丰富的文档和社区支持，使得开发者在使用过程中能够得到及时的帮助。

因此，glibc确实实现了C标准库，并为C语言程序提供了必要的函数和工具，以处理各种常见的任务。

ldd --version

ldd (Ubuntu GLIBC 2.35-0ubuntu3.8) 2.35
Copyright (C) 2022 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
Written by Roland McGrath and Ulrich Drepper.

https://github.com/edidada/testlinuxlibcrypt/actions

## doc

在Ubuntu 22.04（或任何基于Debian的Linux发行版）上安装glibc（GNU C Library）及其头文件和库文件是一个相对直接的过程。glibc是Linux系统中非常重要的一个库，它提供了标准C库的实现，包括常用的函数、数据类型等。

安装glibc
通常情况下，Ubuntu系统已经预装了glibc。但是，如果你需要安装特定版本的glibc或者确认glibc已安装，可以使用以下命令：

bash
sudo apt update  
sudo apt install libc6 libc6-dbg libc6-dev libc6-dev-i386 libc6-doc libc6-i386 libc6-locales
libc6 是glibc的主要库文件。
libc6-dbg 包含调试符号。
libc6-dev 包含用于开发所需的头文件和静态库。
libc6-dev-i386 是为32位开发环境提供的头文件和静态库（如果你的系统支持多架构）。
libc6-doc 包含文档。
libc6-i386 是32位版本的glibc库（如果你的系统支持多架构）。
libc6-locales 提供额外的本地化支持。
查看glibc的头文件
glibc的头文件通常安装在/usr/include目录下。你可以使用find命令来查找所有与glibc相关的头文件：

bash
sudo find /usr/include -name "*glibc*"
但请注意，glibc的头文件可能不会直接包含glibc这个字符串在文件名中。更常见的做法是查找sys、stdio.h、stdlib.h等标准C库的头文件，它们都是glibc的一部分。

为了查看glibc特有的头文件（如扩展的API或特定于glibc的宏），你可能需要直接查看/usr/include下的相关目录，如/usr/include/x86_64-linux-gnu（对于64位系统）或/usr/include/i386-linux-gnu（对于32位系统）。

查看glibc的库文件
glibc的库文件（动态链接库和静态库）通常安装在/lib、/usr/lib或/usr/lib/x86_64-linux-gnu（对于64位系统）等目录下。要查看glibc的库文件，可以使用ls命令结合通配符：

bash
ls /lib/x86_64-linux-gnu/libc*.so*  # 对于64位系统  
ls /lib/i386-linux-gnu/libc*.so*    # 对于32位系统（如果你的系统支持）
这些命令会列出所有以libc开头并以.so（共享对象，即动态库）结尾的文件。

总结
通过以上步骤，你可以在Ubuntu 22.04上安装glibc及其开发文件，并查看其头文件和库文件的位置。这对于开发依赖于glibc的应用程序或库至关重要。

https://sourceware.org/glibc/manual/2.37/html_mono/libc.html

1 Introduction
1.1 Getting Started
1.2 Standards and Portability
1.2.1 ISO C
1.2.2 POSIX (The Portable Operating System Interface)
1.2.2.1 POSIX Safety Concepts
1.2.2.2 Unsafe Features
1.2.2.3 Conditionally Safe Features
1.2.2.4 Other Safety Remarks
1.2.3 Berkeley Unix
1.2.4 SVID (The System V Interface Description)
1.2.5 XPG (The X/Open Portability Guide)
1.3 Using the Library
1.3.1 Header Files
1.3.2 Macro Definitions of Functions
1.3.3 Reserved Names
1.3.4 Feature Test Macros
1.4 Roadmap to the Manual
2 Error Reporting
2.1 Checking for Errors
2.2 Error Codes
2.3 Error Messages
3 Virtual Memory Allocation And Paging
3.1 Process Memory Concepts
3.2 Allocating Storage For Program Data
3.2.1 Memory Allocation in C Programs
3.2.1.1 Dynamic Memory Allocation
3.2.2 The GNU Allocator
3.2.3 Unconstrained Allocation
3.2.3.1 Basic Memory Allocation
3.2.3.2 Examples of malloc
3.2.3.3 Freeing Memory Allocated with malloc
3.2.3.4 Changing the Size of a Block
3.2.3.5 Allocating Cleared Space
3.2.3.6 Allocating Aligned Memory Blocks
3.2.3.7 Malloc Tunable Parameters
3.2.3.8 Heap Consistency Checking
3.2.3.9 Statistics for Memory Allocation with malloc
3.2.3.10 Summary of malloc-Related Functions
3.2.4 Allocation Debugging
3.2.4.1 How to install the tracing functionality
3.2.4.2 Example program excerpts
3.2.4.3 Some more or less clever ideas
3.2.4.4 Interpreting the traces
3.2.5 Replacing malloc
3.2.6 Obstacks
3.2.6.1 Creating Obstacks
3.2.6.2 Preparing for Using Obstacks
3.2.6.3 Allocation in an Obstack
3.2.6.4 Freeing Objects in an Obstack
3.2.6.5 Obstack Functions and Macros
3.2.6.6 Growing Objects
3.2.6.7 Extra Fast Growing Objects
3.2.6.8 Status of an Obstack
3.2.6.9 Alignment of Data in Obstacks
3.2.6.10 Obstack Chunks
3.2.6.11 Summary of Obstack Functions
3.2.7 Automatic Storage with Variable Size
3.2.7.1 alloca Example
3.2.7.2 Advantages of alloca
3.2.7.3 Disadvantages of alloca
3.2.7.4 GNU C Variable-Size Arrays
3.3 Resizing the Data Segment
3.4 Memory Protection
3.4.1 Memory Protection Keys
3.5 Locking Pages
3.5.1 Why Lock Pages
3.5.2 Locked Memory Details
3.5.3 Functions To Lock And Unlock Pages
4 Character Handling
4.1 Classification of Characters
4.2 Case Conversion
4.3 Character class determination for wide characters
4.4 Notes on using the wide character classes
4.5 Mapping of wide characters.
5 String and Array Utilities
5.1 Representation of Strings
5.2 String and Array Conventions
5.3 String Length
5.4 Copying Strings and Arrays
5.5 Concatenating Strings
5.6 Truncating Strings while Copying
5.7 String/Array Comparison
5.8 Collation Functions
5.9 Search Functions
5.9.1 Compatibility String Search Functions
5.10 Finding Tokens in a String
5.11 Erasing Sensitive Data
5.12 Shuffling Bytes
5.13 Obfuscating Data
5.14 Encode Binary Data
5.15 Argz and Envz Vectors
5.15.1 Argz Functions
5.15.2 Envz Functions
6 Character Set Handling
6.1 Introduction to Extended Characters
6.2 Overview about Character Handling Functions
6.3 Restartable Multibyte Conversion Functions
6.3.1 Selecting the conversion and its properties
6.3.2 Representing the state of the conversion
6.3.3 Converting Single Characters
6.3.4 Converting Multibyte and Wide Character Strings
6.3.5 A Complete Multibyte Conversion Example
6.4 Non-reentrant Conversion Function
6.4.1 Non-reentrant Conversion of Single Characters
6.4.2 Non-reentrant Conversion of Strings
6.4.3 States in Non-reentrant Functions
6.5 Generic Charset Conversion
6.5.1 Generic Character Set Conversion Interface
6.5.2 A complete iconv example
6.5.3 Some Details about other iconv Implementations
6.5.4 The iconv Implementation in the GNU C Library
6.5.4.1 Format of gconv-modules files
6.5.4.2 Finding the conversion path in iconv
6.5.4.3 iconv module data structures
6.5.4.4 iconv module interfaces
7 Locales and Internationalization
7.1 What Effects a Locale Has
7.2 Choosing a Locale
7.3 Locale Categories
7.4 How Programs Set the Locale
7.5 Standard Locales
7.6 Locale Names
7.7 Accessing Locale Information
7.7.1 localeconv: It is portable but …
7.7.1.1 Generic Numeric Formatting Parameters
7.7.1.2 Printing the Currency Symbol
7.7.1.3 Printing the Sign of a Monetary Amount
7.7.2 Pinpoint Access to Locale Data
7.8 A dedicated function to format numbers
7.9 Yes-or-No Questions
8 Message Translation
8.1 X/Open Message Catalog Handling
8.1.1 The catgets function family
8.1.2 Format of the message catalog files
8.1.3 Generate Message Catalogs files
8.1.4 How to use the catgets interface
8.1.4.1 Not using symbolic names
8.1.4.2 Using symbolic names
8.1.4.3 How does to this allow to develop
8.2 The Uniforum approach to Message Translation
8.2.1 The gettext family of functions
8.2.1.1 What has to be done to translate a message?
8.2.1.2 How to determine which catalog to be used
8.2.1.3 Additional functions for more complicated situations
8.2.1.4 How to specify the output character set gettext uses
8.2.1.5 How to use gettext in GUI programs
8.2.1.6 User influence on gettext
8.2.2 Programs to handle message catalogs for gettext
9 Searching and Sorting
9.1 Defining the Comparison Function
9.2 Array Search Function
9.3 Array Sort Function
9.4 Searching and Sorting Example
9.5 The hsearch function.
9.6 The tsearch function.
10 Pattern Matching
10.1 Wildcard Matching
10.2 Globbing
10.2.1 Calling glob
10.2.2 Flags for Globbing
10.2.3 More Flags for Globbing
10.3 Regular Expression Matching
10.3.1 POSIX Regular Expression Compilation
10.3.2 Flags for POSIX Regular Expressions
10.3.3 Matching a Compiled POSIX Regular Expression
10.3.4 Match Results with Subexpressions
10.3.5 Complications in Subexpression Matching
10.3.6 POSIX Regexp Matching Cleanup
10.4 Shell-Style Word Expansion
10.4.1 The Stages of Word Expansion
10.4.2 Calling wordexp
10.4.3 Flags for Word Expansion
10.4.4 wordexp Example
10.4.5 Details of Tilde Expansion
10.4.6 Details of Variable Substitution
11 Input/Output Overview
11.1 Input/Output Concepts
11.1.1 Streams and File Descriptors
11.1.2 File Position
11.2 File Names
11.2.1 Directories
11.2.2 File Name Resolution
11.2.3 File Name Errors
11.2.4 Portability of File Names
12 Input/Output on Streams
12.1 Streams
12.2 Standard Streams
12.3 Opening Streams
12.4 Closing Streams
12.5 Streams and Threads
12.6 Streams in Internationalized Applications
12.7 Simple Output by Characters or Lines
12.8 Character Input
12.9 Line-Oriented Input
12.10 Unreading
12.10.1 What Unreading Means
12.10.2 Using ungetc To Do Unreading
12.11 Block Input/Output
12.12 Formatted Output
12.12.1 Formatted Output Basics
12.12.2 Output Conversion Syntax
12.12.3 Table of Output Conversions
12.12.4 Integer Conversions
12.12.5 Floating-Point Conversions
12.12.6 Other Output Conversions
12.12.7 Formatted Output Functions
12.12.8 Dynamically Allocating Formatted Output
12.12.9 Variable Arguments Output Functions
12.12.10 Parsing a Template String
12.12.11 Example of Parsing a Template String
12.13 Customizing printf
12.13.1 Registering New Conversions
12.13.2 Conversion Specifier Options
12.13.3 Defining the Output Handler
12.13.4 printf Extension Example
12.13.5 Predefined printf Handlers
12.14 Formatted Input
12.14.1 Formatted Input Basics
12.14.2 Input Conversion Syntax
12.14.3 Table of Input Conversions
12.14.4 Numeric Input Conversions
12.14.5 String Input Conversions
12.14.6 Dynamically Allocating String Conversions
12.14.7 Other Input Conversions
12.14.8 Formatted Input Functions
12.14.9 Variable Arguments Input Functions
12.15 End-Of-File and Errors
12.16 Recovering from errors
12.17 Text and Binary Streams
12.18 File Positioning
12.19 Portable File-Position Functions
12.20 Stream Buffering
12.20.1 Buffering Concepts
12.20.2 Flushing Buffers
12.20.3 Controlling Which Kind of Buffering
12.21 Other Kinds of Streams
12.21.1 String Streams
12.21.2 Programming Your Own Custom Streams
12.21.2.1 Custom Streams and Cookies
12.21.2.2 Custom Stream Hook Functions
12.22 Formatted Messages
12.22.1 Printing Formatted Messages
12.22.2 Adding Severity Classes
12.22.3 How to use fmtmsg and addseverity
13 Low-Level Input/Output
13.1 Opening and Closing Files
13.2 Input and Output Primitives
13.3 Setting the File Position of a Descriptor
13.4 Descriptors and Streams
13.5 Dangers of Mixing Streams and Descriptors
13.5.1 Linked Channels
13.5.2 Independent Channels
13.5.3 Cleaning Streams
13.6 Fast Scatter-Gather I/O
13.7 Copying data between two files
13.8 Memory-mapped I/O
13.9 Waiting for Input or Output
13.10 Synchronizing I/O operations
13.11 Perform I/O Operations in Parallel
13.11.1 Asynchronous Read and Write Operations
13.11.2 Getting the Status of AIO Operations
13.11.3 Getting into a Consistent State
13.11.4 Cancellation of AIO Operations
13.11.5 How to optimize the AIO implementation
13.12 Control Operations on Files
13.13 Duplicating Descriptors
13.14 File Descriptor Flags
13.15 File Status Flags
13.15.1 File Access Modes
13.15.2 Open-time Flags
13.15.3 I/O Operating Modes
13.15.4 Getting and Setting File Status Flags
13.16 File Locks
13.17 Open File Description Locks
13.18 Open File Description Locks Example
13.19 Interrupt-Driven Input
13.20 Generic I/O Control operations
14 File System Interface
14.1 Working Directory
14.2 Accessing Directories
14.2.1 Format of a Directory Entry
14.2.2 Opening a Directory Stream
14.2.3 Reading and Closing a Directory Stream
14.2.4 Simple Program to List a Directory
14.2.5 Random Access in a Directory Stream
14.2.6 Scanning the Content of a Directory
14.2.7 Simple Program to List a Directory, Mark II
14.2.8 Low-level Directory Access
14.3 Working with Directory Trees
14.4 Hard Links
14.5 Symbolic Links
14.6 Deleting Files
14.7 Renaming Files
14.8 Creating Directories
14.9 File Attributes
14.9.1 The meaning of the File Attributes
14.9.2 Reading the Attributes of a File
14.9.3 Testing the Type of a File
14.9.4 File Owner
14.9.5 The Mode Bits for Access Permission
14.9.6 How Your Access to a File is Decided
14.9.7 Assigning File Permissions
14.9.8 Testing Permission to Access a File
14.9.9 File Times
14.9.10 File Size
14.9.11 Storage Allocation
14.10 Making Special Files
14.11 Temporary Files
15 Pipes and FIFOs
15.1 Creating a Pipe
15.2 Pipe to a Subprocess
15.3 FIFO Special Files
15.4 Atomicity of Pipe I/O
16 Sockets
16.1 Socket Concepts
16.2 Communication Styles
16.3 Socket Addresses
16.3.1 Address Formats
16.3.2 Setting the Address of a Socket
16.3.3 Reading the Address of a Socket
16.4 Interface Naming
16.5 The Local Namespace
16.5.1 Local Namespace Concepts
16.5.2 Details of Local Namespace
16.5.3 Example of Local-Namespace Sockets
16.6 The Internet Namespace
16.6.1 Internet Socket Address Formats
16.6.2 Host Addresses
16.6.2.1 Internet Host Addresses
16.6.2.2 Host Address Data Type
16.6.2.3 Host Address Functions
16.6.2.4 Host Names
16.6.3 Internet Ports
16.6.4 The Services Database
16.6.5 Byte Order Conversion
16.6.6 Protocols Database
16.6.7 Internet Socket Example
16.7 Other Namespaces
16.8 Opening and Closing Sockets
16.8.1 Creating a Socket
16.8.2 Closing a Socket
16.8.3 Socket Pairs
16.9 Using Sockets with Connections
16.9.1 Making a Connection
16.9.2 Listening for Connections
16.9.3 Accepting Connections
16.9.4 Who is Connected to Me?
16.9.5 Transferring Data
16.9.5.1 Sending Data
16.9.5.2 Receiving Data
16.9.5.3 Socket Data Options
16.9.6 Byte Stream Socket Example
16.9.7 Byte Stream Connection Server Example
16.9.8 Out-of-Band Data
16.10 Datagram Socket Operations
16.10.1 Sending Datagrams
16.10.2 Receiving Datagrams
16.10.3 Datagram Socket Example
16.10.4 Example of Reading Datagrams
16.11 The inetd Daemon
16.11.1 inetd Servers
16.11.2 Configuring inetd
16.12 Socket Options
16.12.1 Socket Option Functions
16.12.2 Socket-Level Options
16.13 Networks Database
17 Low-Level Terminal Interface
17.1 Identifying Terminals
17.2 I/O Queues
17.3 Two Styles of Input: Canonical or Not
17.4 Terminal Modes
17.4.1 Terminal Mode Data Types
17.4.2 Terminal Mode Functions
17.4.3 Setting Terminal Modes Properly
17.4.4 Input Modes
17.4.5 Output Modes
17.4.6 Control Modes
17.4.7 Local Modes
17.4.8 Line Speed
17.4.9 Special Characters
17.4.9.1 Characters for Input Editing
17.4.9.2 Characters that Cause Signals
17.4.9.3 Special Characters for Flow Control
17.4.9.4 Other Special Characters
17.4.10 Noncanonical Input
17.5 BSD Terminal Modes
17.6 Line Control Functions
17.7 Noncanonical Mode Example
17.8 Reading Passphrases
17.9 Pseudo-Terminals
17.9.1 Allocating Pseudo-Terminals
17.9.2 Opening a Pseudo-Terminal Pair
18 Syslog
18.1 Overview of Syslog
18.2 Submitting Syslog Messages
18.2.1 openlog
18.2.2 syslog, vsyslog
18.2.3 closelog
18.2.4 setlogmask
18.2.5 Syslog Example
19 Mathematics
19.1 Predefined Mathematical Constants
19.2 Trigonometric Functions
19.3 Inverse Trigonometric Functions
19.4 Exponentiation and Logarithms
19.5 Hyperbolic Functions
19.6 Special Functions
19.7 Known Maximum Errors in Math Functions
19.8 Pseudo-Random Numbers
19.8.1 ISO C Random Number Functions
19.8.2 BSD Random Number Functions
19.8.3 SVID Random Number Function
19.8.4 High Quality Random Number Functions
19.9 Is Fast Code or Small Code preferred?
20 Arithmetic Functions
20.1 Integers
20.2 Integer Division
20.3 Floating Point Numbers
20.4 Floating-Point Number Classification Functions
20.5 Errors in Floating-Point Calculations
20.5.1 FP Exceptions
20.5.2 Infinity and NaN
20.5.3 Examining the FPU status word
20.5.4 Error Reporting by Mathematical Functions
20.6 Rounding Modes
20.7 Floating-Point Control Functions
20.8 Arithmetic Functions
20.8.1 Absolute Value
20.8.2 Normalization Functions
20.8.3 Rounding Functions
20.8.4 Remainder Functions
20.8.5 Setting and modifying single bits of FP values
20.8.6 Floating-Point Comparison Functions
20.8.7 Miscellaneous FP arithmetic functions
20.9 Complex Numbers
20.10 Projections, Conjugates, and Decomposing of Complex Numbers
20.11 Parsing of Numbers
20.11.1 Parsing of Integers
20.11.2 Parsing of Floats
20.12 Printing of Floats
20.13 Old-fashioned System V number-to-string functions
21 Date and Time
21.1 Time Basics
21.2 Time Types
21.3 Calculating Elapsed Time
21.4 Processor And CPU Time
21.4.1 CPU Time Inquiry
21.4.2 Processor Time Inquiry
21.5 Calendar Time
21.5.1 Getting the Time
21.5.2 Setting and Adjusting the Time
21.5.3 Broken-down Time
21.5.4 Formatting Calendar Time
21.5.5 Convert textual time and date information back
21.5.5.1 Interpret string according to given format
21.5.5.2 A More User-friendly Way to Parse Times and Dates
21.5.6 Specifying the Time Zone with TZ
21.5.7 Functions and Variables for Time Zones
21.5.8 Time Functions Example
21.6 Setting an Alarm
21.7 Sleeping
22 Resource Usage And Limitation
22.1 Resource Usage
22.2 Limiting Resource Usage
22.3 Process CPU Priority And Scheduling
22.3.1 Absolute Priority
22.3.1.1 Using Absolute Priority
22.3.2 Realtime Scheduling
22.3.3 Basic Scheduling Functions
22.3.4 Traditional Scheduling
22.3.4.1 Introduction To Traditional Scheduling
22.3.4.2 Functions For Traditional Scheduling
22.3.5 Limiting execution to certain CPUs
22.4 Querying memory available resources
22.4.1 Overview about traditional Unix memory handling
22.4.2 How to get information about the memory subsystem?
22.5 Learn about the processors available
23 Non-Local Exits
23.1 Introduction to Non-Local Exits
23.2 Details of Non-Local Exits
23.3 Non-Local Exits and Signals
23.4 Complete Context Control
24 Signal Handling
24.1 Basic Concepts of Signals
24.1.1 Some Kinds of Signals
24.1.2 Concepts of Signal Generation
24.1.3 How Signals Are Delivered
24.2 Standard Signals
24.2.1 Program Error Signals
24.2.2 Termination Signals
24.2.3 Alarm Signals
24.2.4 Asynchronous I/O Signals
24.2.5 Job Control Signals
24.2.6 Operation Error Signals
24.2.7 Miscellaneous Signals
24.2.8 Signal Messages
24.3 Specifying Signal Actions
24.3.1 Basic Signal Handling
24.3.2 Advanced Signal Handling
24.3.3 Interaction of signal and sigaction
24.3.4 sigaction Function Example
24.3.5 Flags for sigaction
24.3.6 Initial Signal Actions
24.4 Defining Signal Handlers
24.4.1 Signal Handlers that Return
24.4.2 Handlers That Terminate the Process
24.4.3 Nonlocal Control Transfer in Handlers
24.4.4 Signals Arriving While a Handler Runs
24.4.5 Signals Close Together Merge into One
24.4.6 Signal Handling and Nonreentrant Functions
24.4.7 Atomic Data Access and Signal Handling
24.4.7.1 Problems with Non-Atomic Access
24.4.7.2 Atomic Types
24.4.7.3 Atomic Usage Patterns
24.5 Primitives Interrupted by Signals
24.6 Generating Signals
24.6.1 Signaling Yourself
24.6.2 Signaling Another Process
24.6.3 Permission for using kill
24.6.4 Using kill for Communication
24.7 Blocking Signals
24.7.1 Why Blocking Signals is Useful
24.7.2 Signal Sets
24.7.3 Process Signal Mask
24.7.4 Blocking to Test for Delivery of a Signal
24.7.5 Blocking Signals for a Handler
24.7.6 Checking for Pending Signals
24.7.7 Remembering a Signal to Act On Later
24.8 Waiting for a Signal
24.8.1 Using pause
24.8.2 Problems with pause
24.8.3 Using sigsuspend
24.9 Using a Separate Signal Stack
24.10 BSD Signal Handling
25 The Basic Program/System Interface
25.1 Program Arguments
25.1.1 Program Argument Syntax Conventions
25.1.2 Parsing Program Arguments
25.2 Parsing program options using getopt
25.2.1 Using the getopt function
25.2.2 Example of Parsing Arguments with getopt
25.2.3 Parsing Long Options with getopt_long
25.2.4 Example of Parsing Long Options with getopt_long
25.3 Parsing Program Options with Argp
25.3.1 The argp_parse Function
25.3.2 Argp Global Variables
25.3.3 Specifying Argp Parsers
25.3.4 Specifying Options in an Argp Parser
25.3.4.1 Flags for Argp Options
25.3.5 Argp Parser Functions
25.3.5.1 Special Keys for Argp Parser Functions
25.3.5.2 Argp Parsing State
25.3.5.3 Functions For Use in Argp Parsers
25.3.6 Combining Multiple Argp Parsers
25.3.7 Flags for argp_parse
25.3.8 Customizing Argp Help Output
25.3.8.1 Special Keys for Argp Help Filter Functions
25.3.9 The argp_help Function
25.3.10 Flags for the argp_help Function
25.3.11 Argp Examples
25.3.11.1 A Minimal Program Using Argp
25.3.11.2 A Program Using Argp with Only Default Options
25.3.11.3 A Program Using Argp with User Options
25.3.11.4 A Program Using Multiple Combined Argp Parsers
25.3.12 Argp User Customization
25.3.12.1 Parsing of Suboptions
25.3.13 Parsing of Suboptions Example
25.4 Environment Variables
25.4.1 Environment Access
25.4.2 Standard Environment Variables
25.5 Auxiliary Vector
25.5.1 Definition of getauxval
25.6 System Calls
25.7 Program Termination
25.7.1 Normal Termination
25.7.2 Exit Status
25.7.3 Cleanups on Exit
25.7.4 Aborting a Program
25.7.5 Termination Internals
26 Processes
26.1 Running a Command
26.2 Process Creation Concepts
26.3 Process Identification
26.4 Creating a Process
26.5 Executing a File
26.6 Process Completion
26.7 Process Completion Status
26.8 BSD Process Wait Function
26.9 Process Creation Example
27 Inter-Process Communication
27.1 Semaphores
27.1.1 System V Semaphores
27.1.2 POSIX Semaphores
28 Job Control
28.1 Concepts of Job Control
28.2 Controlling Terminal of a Process
28.3 Access to the Controlling Terminal
28.4 Orphaned Process Groups
28.5 Implementing a Job Control Shell
28.5.1 Data Structures for the Shell
28.5.2 Initializing the Shell
28.5.3 Launching Jobs
28.5.4 Foreground and Background
28.5.5 Stopped and Terminated Jobs
28.5.6 Continuing Stopped Jobs
28.5.7 The Missing Pieces
28.6 Functions for Job Control
28.6.1 Identifying the Controlling Terminal
28.6.2 Process Group Functions
28.6.3 Functions for Controlling Terminal Access
29 System Databases and Name Service Switch
29.1 NSS Basics
29.2 The NSS Configuration File
29.2.1 Services in the NSS configuration File
29.2.2 Actions in the NSS configuration
29.2.3 Notes on the NSS Configuration File
29.3 NSS Module Internals
29.3.1 The Naming Scheme of the NSS Modules
29.3.2 The Interface of the Function in NSS Modules
29.4 Extending NSS
29.4.1 Adding another Service to NSS
29.4.2 Internals of the NSS Module Functions
30 Users and Groups
30.1 User and Group IDs
30.2 The Persona of a Process
30.3 Why Change the Persona of a Process?
30.4 How an Application Can Change Persona
30.5 Reading the Persona of a Process
30.6 Setting the User ID
30.7 Setting the Group IDs
30.8 Enabling and Disabling Setuid Access
30.9 Setuid Program Example
30.10 Tips for Writing Setuid Programs
30.11 Identifying Who Logged In
30.12 The User Accounting Database
30.12.1 Manipulating the User Accounting Database
30.12.2 XPG User Accounting Database Functions
30.12.3 Logging In and Out
30.13 User Database
30.13.1 The Data Structure that Describes a User
30.13.2 Looking Up One User
30.13.3 Scanning the List of All Users
30.13.4 Writing a User Entry
30.14 Group Database
30.14.1 The Data Structure for a Group
30.14.2 Looking Up One Group
30.14.3 Scanning the List of All Groups
30.15 User and Group Database Example
30.16 Netgroup Database
30.16.1 Netgroup Data
30.16.2 Looking up one Netgroup
30.16.3 Testing for Netgroup Membership
31 System Management
31.1 Host Identification
31.2 Platform Type Identification
31.3 Controlling and Querying Mounts
31.3.1 Mount Information
31.3.1.1 The fstab file
31.3.1.2 The mtab file
31.3.1.3 Other (Non-libc) Sources of Mount Information
31.3.2 Mount, Unmount, Remount
32 System Configuration Parameters
32.1 General Capacity Limits
32.2 Overall System Options
32.3 Which Version of POSIX is Supported
32.4 Using sysconf
32.4.1 Definition of sysconf
32.4.2 Constants for sysconf Parameters
32.4.3 Examples of sysconf
32.5 Minimum Values for General Capacity Limits
32.6 Limits on File System Capacity
32.7 Optional Features in File Support
32.8 Minimum Values for File System Limits
32.9 Using pathconf
32.10 Utility Program Capacity Limits
32.11 Minimum Values for Utility Limits
32.12 String-Valued Parameters
33 Cryptographic Functions
33.1 Passphrase Storage
33.2 Generating Unpredictable Bytes
34 Debugging support
34.1 Backtraces
35 Threads
35.1 ISO C Threads
35.1.1 Return Values
35.1.2 Creation and Control
35.1.3 Call Once
35.1.4 Mutexes
35.1.5 Condition Variables
35.1.6 Thread-local Storage
35.2 POSIX Threads
35.2.1 Thread-specific Data
35.2.2 Non-POSIX Extensions
35.2.2.1 Setting Process-wide defaults for thread attributes
35.2.2.2 Controlling the Initial Signal Mask of a New Thread
35.2.2.3 Functions for Waiting According to a Specific Clock
35.2.2.4 Detecting Single-Threaded Execution
35.2.2.5 Restartable Sequences
36 Dynamic Linker
36.1 Dynamic Linker Introspection
37 Internal probes
37.1 Memory Allocation Probes
37.2 Non-local Goto Probes
38 Tunables
38.1 Tunable names
38.2 Memory Allocation Tunables
38.3 Dynamic Linking Tunables
38.4 Elision Tunables
38.5 POSIX Thread Tunables
38.6 Hardware Capability Tunables
38.7 Memory Related Tunables
Appendix A C Language Facilities in the Library
A.1 Explicitly Checking Internal Consistency
A.2 Variadic Functions
A.2.1 Why Variadic Functions are Used
A.2.2 How Variadic Functions are Defined and Used
A.2.2.1 Syntax for Variable Arguments
A.2.2.2 Receiving the Argument Values
A.2.2.3 How Many Arguments Were Supplied
A.2.2.4 Calling Variadic Functions
A.2.2.5 Argument Access Macros
A.2.3 Example of a Variadic Function
A.3 Null Pointer Constant
A.4 Important Data Types
A.5 Data Type Measurements
A.5.1 Width of an Integer Type
A.5.2 Range of an Integer Type
A.5.3 Floating Type Macros
A.5.3.1 Floating Point Representation Concepts
A.5.3.2 Floating Point Parameters
A.5.3.3 IEEE Floating Point
A.5.4 Structure Field Offset Measurement
Appendix B Summary of Library Facilities
Appendix C Installing the GNU C Library
C.1 Configuring and compiling the GNU C Library
C.2 Installing the C Library
C.3 Recommended Tools for Compilation
C.4 Specific advice for GNU/Linux systems
C.5 Reporting Bugs
Appendix D Library Maintenance
D.1 Adding New Functions
D.1.1 Platform-specific types, macros and functions
D.2 Fortification of function calls
D.3 Symbol handling in the GNU C Library
D.3.1 64-bit time symbol handling in the GNU C Library
D.4 Porting the GNU C Library
D.4.1 Layout of the sysdeps Directory Hierarchy
D.4.2 Porting the GNU C Library to Unix Systems
Appendix E Platform-specific facilities
E.1 PowerPC-specific Facilities
E.2 RISC-V-specific Facilities
E.3 X86-specific Facilities
Appendix F Contributors to the GNU C Library
Appendix G Free Software Needs Free Documentation
Appendix H GNU Lesser General Public License
Appendix I GNU Free Documentation License
Concept Index
Type Index
Function and Macro Index
Variable and Constant Macro Index
Program and File Index



Short Table of Contents
1 Introduction
2 Error Reporting
3 Virtual Memory Allocation And Paging
4 Character Handling
5 String and Array Utilities
6 Character Set Handling
7 Locales and Internationalization
8 Message Translation
9 Searching and Sorting
10 Pattern Matching
11 Input/Output Overview
12 Input/Output on Streams
13 Low-Level Input/Output
14 File System Interface
15 Pipes and FIFOs
16 Sockets
17 Low-Level Terminal Interface
18 Syslog
19 Mathematics
20 Arithmetic Functions
21 Date and Time
22 Resource Usage And Limitation
23 Non-Local Exits
24 Signal Handling
25 The Basic Program/System Interface
26 Processes
27 Inter-Process Communication
28 Job Control
29 System Databases and Name Service Switch
30 Users and Groups
31 System Management
32 System Configuration Parameters
33 Cryptographic Functions
34 Debugging support
35 Threads
36 Dynamic Linker
37 Internal probes
38 Tunables
Appendix A C Language Facilities in the Library
Appendix B Summary of Library Facilities
Appendix C Installing the GNU C Library
Appendix D Library Maintenance
Appendix E Platform-specific facilities
Appendix F Contributors to the GNU C Library
Appendix G Free Software Needs Free Documentation
Appendix H GNU Lesser General Public License
Appendix I GNU Free Documentation License
Concept Index
Type Index
Function and Macro Index
Variable and Constant Macro Index
Program and File Index

## 头文件
14.6 Deleting Files
unistd.h
14.7 Renaming Files

14.8 Creating Directories
sys/stat.h
14.9.1 The meaning of the File Attributes
sys/stat.h
14.9.2 Reading the Attributes of a File
sys/stat.h
14.9.3 Testing the Type of a File
sys/stat.h
14.9.4 File Owner
unistd.h
14.9.5 The Mode Bits for Access Permission
sys/stat.h
14.9.7 Assigning File Permissions
sys/stat.h
14.9.8 Testing Permission to Access a File
unistd.h
14.9.9 File Times
sys/time.h
utime.h

14.10 Making Special Files
sys/stat.h
14.11 Temporary Files
stdio.h
15.1 Creating a Pipe
unistd.h
15.3 FIFO Special Files
sys/stat.h
16.3.3 Reading the Address of a Socket
sys/socket.h
16.4 Interface Naming
net/if.h

## 库文件
GNU C Library (glibc) 是 GNU 操作系统和许多类 Unix 系统（包括 Linux）上的标准 C 库实现。除了 `libm.so` 提供的数学库，glibc 还包含许多其他关键库，涵盖了各种功能。以下是一些常用的 glibc 提供的库：

1. libc.so: 标准 C 库，提供基本的系统调用和 C 标准库函数，如输入/输出、字符串操作、内存管理等。
2. libpthread.so: POSIX 线程库，提供多线程编程支持。
3. libdl.so: 动态链接库，允许程序在运行时加载和卸载动态库。
4. librt.so: 实时扩展库，提供实时编程接口，如高精度定时器和信号。
5. libnsl.so: 网络服务库，用于网络服务（如 NIS）的支持。
6. libresolv.so: 解析库，提供域名解析功能。
7. libcrypt.so: 加密库，提供密码加密和解密功能。
8. libutil.so: 系统实用库，提供一些常用的系统实用函数，如获取用户信息等。
9. libanl.so: 异步网络库，用于异步网络编程。

### 简要描述每个库的功能

1. libc.so
   - 功能: 提供 C 语言的基本功能，如标准输入输出、字符串处理、内存管理、文件操作、时间日期处理等。
   - 示例代码:
     ```c
     #include <stdio.h>
     #include <stdlib.h>

     int main() {
         printf("Hello, World!\n");
         return 0;
     }
     ```
   - 编译命令:
     ```sh
     gcc -o hello hello.c
     ```

2. libpthread.so
   - 功能: 提供 POSIX 线程 API，用于多线程编程。
   - 示例代码:
     ```c
     #include <pthread.h>
     #include <stdio.h>

     void* print_message(void* ptr) {
         char* message = (char*)ptr;
         printf("%s\n", message);
         return NULL;
     }

     int main() {
         pthread_t thread;
         char* message = "Hello, Thread!";
         pthread_create(&thread, NULL, print_message, (void*)message);
         pthread_join(thread, NULL);
         return 0;
     }
     ```
   - 编译命令:
     ```sh
     gcc -o thread_example thread_example.c -lpthread
     ```

3. libdl.so
   - 功能: 提供动态加载共享库的函数，如 `dlopen`、`dlsym`、`dlclose` 等。
   - 示例代码:
     ```c
     #include <stdio.h>
     #include <dlfcn.h>

     int main() {
         void* handle = dlopen("libm.so", RTLD_LAZY);
         if (!handle) {
             fprintf(stderr, "%s\n", dlerror());
             return 1;
         }
         dlclose(handle);
         return 0;
     }
     ```
   - 编译命令:
     ```sh
     gcc -o dl_example dl_example.c -ldl
     ```

4. librt.so
   - 功能: 提供实时编程的扩展功能，如高精度定时器、信号和消息队列等。
   - 示例代码:
     ```c
     #include <stdio.h>
     #include <time.h>

     int main() {
         struct timespec ts;
         clock_gettime(CLOCK_REALTIME, &ts);
         printf("Current time: %ld.%09ld\n", ts.tv_sec, ts.tv_nsec);
         return 0;
     }
     ```
   - 编译命令:
     ```sh
     gcc -o rt_example rt_example.c -lrt
     ```

5. libnsl.so
   - 功能: 提供网络服务库，用于网络信息服务（NIS）和 RPC 等。
   - 示例代码:
     ```c
     #include <netdb.h>
     #include <stdio.h>

     int main() {
         struct hostent *host = gethostbyname("example.com");
         if (host) {
             printf("Host name: %s\n", host->h_name);
         }
         return 0;
     }
     ```
   - 编译命令:
     ```sh
     gcc -o nsl_example nsl_example.c -lnsl
     ```

6. libresolv.so
   - 功能: 提供域名解析的函数，如 `res_query`、`res_search` 等。
   - 示例代码:
     ```c
     #include <resolv.h>
     #include <stdio.h>

     int main() {
         unsigned char buf[1024];
         int len = res_query("example.com", C_IN, T_A, buf, sizeof(buf));
         if (len > 0) {
             printf("Query successful.\n");
         }
         return 0;
     }
     ```
   - 编译命令:
     ```sh
     gcc -o resolv_example resolv_example.c -lresolv
     ```

7. libcrypt.so
   - 功能: 提供加密和解密函数，如 `crypt`。
   - 示例代码:
     ```c
     #include <crypt.h>
     #include <stdio.h>

     int main() {
         char *hash = crypt("password", "salt");
         printf("Hashed password: %s\n", hash);
         return 0;
     }
     ```
   - 编译命令:
     ```sh
     gcc -o crypt_example crypt_example.c -lcrypt
     ```

8. libutil.so
   - 功能: 提供系统实用程序函数，如获取用户信息等。
   - 示例代码:
     ```c
     #include <pty.h>
     #include <utmp.h>
     #include <stdio.h>

     int main() {
         int master, slave;
         char name[100];
         openpty(&master, &slave, name, NULL, NULL);
         printf("Pseudo-terminal name: %s\n", name);
         return 0;
     }
     ```
   - 编译命令:
     ```sh
     gcc -o util_example util_example.c -lutil
     ```

9. libanl.so
   - 功能: 提供异步网络编程支持，如异步 DNS 查询。
   - 示例代码:
     ```c
     #include <netdb.h>
     #include <stdio.h>

     int main() {
         struct hostent *host = gethostbyname("example.com");
         if (host) {
             printf("Host name: %s\n", host->h_name);
         }
         return 0;
     }
     ```
   - 编译命令:
     ```sh
     gcc -o anl_example anl_example.c -lanl
     ```

### 总结

glibc 提供了丰富的库，涵盖了系统编程中的方方面面。从基本的 C 标准库函数到多线程支持，再到动态加载库和实时编程接口，glibc 为开发人员提供了强大的工具。通过了解和使用这些库，开发人员可以更加高效地进行系统编程。


glibc最主要的功能就是对系统调用的封装


libc,glib,glibc,eglibc,libc++,libstdc++,gcc,g++。
从libc说起。
libc是Linux下原来的标准C库，也就是当初写hello world时包含的头文件#include < stdio.h> 定义的地方。
后来逐渐被glibc取代，也就是传说中的GNU C Library,在此之前除了有libc，还有klibc,uclibc。现在只要知道用的最多的是glibc就行了，主流的一些linux操作系统如 Debian, Ubuntu，Redhat等用的都是glibc（或者其变种，下面会说到).
那glibc都做了些什么呢？ glibc是Linux系统中最底层的API，几乎其它任何的运行库都要依赖glibc。 glibc最主要的功能就是对系统调用的封装，你想想看，你怎么能在C代码中直接用fopen函数就能打开文件？ 打开文件最终还是要触发系统中的sys_open系统调用，而这中间的处理过程都是glibc来完成的。这篇文章详细介绍了glibc是如何与上层应用程序和系统调用交互的。除了封装系统调用，glibc自身也提供了一些上层应用函数必要的功能,如string,malloc,stdlib,linuxthreads,locale,signal等等。
好了，那eglibc又是什么？ 这里的e是Embedded的意思，也就是前面说到的变种glibc。eglibc的主要特性是为了更好的支持嵌入式架构，可以支持不同的shell(包括嵌入式)，但它是二进制兼容glibc的，就是说如果你的代码之前依赖eglibc库，那么换成glibc后也不需要重新编译。ubuntu系统用的就是eglibc（而不是glibc）,不信，你执行 ldd –version 或者 /lib/i386-linux-gnu/libc.so.6
(64位系统运行/lib/x86_64-linux-gnu）看看，便会显示你系统中eglibc/glibc的版本信息。 这里提到了libc.so.6,这个文件就是eglibc/glibc编译后的生成库文件。
还有一个glib看起来也很相似，那它又是什么呢？glib也是个c程序库，不过比较轻量级，glib将C语言中的数据类型统一封装成自己的数据类型，提供了C语言常用的数据结构的定义以及处理函数，有趣的宏以及可移植的封装等(注：glib是可移植的，说明你可以在linux下，也可以在windows下使用它）。那它跟glibc有什么关系吗？其实并没有，除非你的程序代码会用到glib库中的数据结构或者函数，glib库在ubuntu系统中并不会默认安装(可以通过apt-get install libglib2.0-dev手动安装)，著名的GTK+和Gnome底层用的都是glib库。想更详细了解glib？ 可以参考这里
看到这里，你应该知道这些库有多重要了吧？ 你写的C代码在编译的过程中有可能出现明明是这些库里面定义的变,却量还会出现’Undefined’, ‘Unreference’等错误，这时候你可能会怀疑是不是这些库出问题了？ 是不是该动手换个gilbc/eglibc了？ 这里强调一点，在你准备更换/升级这些库之前，你应该好好思考一下，你真的要更换/升级吗？你要知道你自己在做什么！你要时刻知道glibc/eglibc的影响有多大，不管你之前部署的什么程序，linux系统的ls,cd,mv,ps等等全都得依赖它，很多人在更换/升级都有过惨痛的教训，甚至让整个系统奔溃无法启动。所以，强烈不建议更换/升级这些库！
当然如果你写的是C++代码，还有两个库也要非常重视了，libc++/libstdc++,这两个库有关系吗？有。两个都是C++标准库。libc++是针对clang编译器特别重写的C++标准库，那libstdc++自然就是gcc的事儿了。libstdc++与gcc的关系就像clang与libc++. 其中的区别这里不作详细介绍了。
再说说libstdc++，glibc的关系。 libstdc++与gcc是捆绑在一起的，也就是说安装gcc的时候会把libstdc++装上。 那为什么glibc和gcc没有捆绑在一起呢？
相比glibc，libstdc++虽然提供了c++程序的标准库，但它并不与内核打交道。对于系统级别的事件，libstdc++首先是会与glibc交互，才能和内核通信。相比glibc来说，libstdc++就显得没那么基础了。
说完了这些库，这些库最终都是拿来干嘛的？当然是要将它们与你的程序链接在一起！ 这时候就不得不说说gcc了(当然还有前文提到的clang以及llvm等编译器，本文就不细说它们的区别了)。
你写的C代码.c文件通过gcc首先转化为汇编.S文件，之后汇编器as将.S文件转化为机器代码.o文件，生成的.o文件再与其它.o文件，或者之前提到的libc.so.6库文件通过ld链接器链接在一块生成可执行文件。当然，在你编译代码使用gcc的时候，gcc命令已经帮你把这些细节全部做好了。
那g++是做什么的? 慢慢说来，不要以为gcc只能编译C代码，g++只能编译c++代码。 后缀为.c的，gcc把它当作是C程序，而g++当作是c++程序；后缀为.cpp的，两者都会认为是c++程序，注意，虽然c++是c的超集，但是两者对语法的要求是有区别的。在编译阶段，g++会调用gcc,对于c++代码，两者是等价的，但是因为gcc命令不能自动和C++程序使用的库联接，需要这样，gcc -lstdc++, 所以如果你的Makefile文件并没有手动加上libstdc++库，一般就会提示错误，要求你安装g++编译器了。
好了，就说到这，理清这些库与编译器之间的关系，相信会对你解决编译链接过程中遇到的错误起到一点帮助。
如果你的编译器不支持一些新的C/C++特性，想升级gcc/g++, 这里也给出一个基于ubuntu系统的参考方法。
添加ppa
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
添加ppa，是因为你所用的ubuntu版本的更新源中可能并没有你想要的gcc/g++版本。
安装新版gcc/g++
sudo apt-get install gcc-4.8
sudo apt-get install g++-4.8
可以到/usr/bin/gcc查看新安装的gcc,g++
配置系统gcc/g++
使用update-alternatives,统一更新gcc/g++
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.6 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.6
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 80 --slave /usr/bin/g++ g++ /usr/bin/g++-4.8
sudo update-alternatives --config gcc
数字优先级(如60，80)高的会被系统选择为默认的编译器,也可以执行第三条命令就是来手动配置系统的gcc,此处按照提示,选择4.8版本的即可。

原文链接：https://blog.csdn.net/p656456564545/article/details/89184141


strings /usr/lib64/libstdc++.so.6 | grep GLIBC

```
rpm -ql glibc
/etc/gai.conf
/etc/ld.so.cache
/etc/ld.so.conf
/etc/ld.so.conf.d
/etc/nsswitch.conf
/etc/rpc
/lib64/ld-2.17.so
/lib64/ld-linux-x86-64.so.2
/lib64/libBrokenLocale-2.17.so
/lib64/libBrokenLocale.so.1
/lib64/libSegFault.so
/lib64/libanl-2.17.so
/lib64/libanl.so.1
/lib64/libc-2.17.so
/lib64/libc.so.6
/lib64/libcidn-2.17.so
/lib64/libcidn.so.1
/lib64/libcrypt-2.17.so
/lib64/libcrypt.so.1
/lib64/libdl-2.17.so
/lib64/libdl.so.2
/lib64/libm-2.17.so
/lib64/libm.so.6
/lib64/libnsl-2.17.so
/lib64/libnsl.so.1
/lib64/libnss_compat-2.17.so
/lib64/libnss_compat.so.2
/lib64/libnss_db-2.17.so
/lib64/libnss_db.so.2
/lib64/libnss_dns-2.17.so
/lib64/libnss_dns.so.2
/lib64/libnss_files-2.17.so
/lib64/libnss_files.so.2
/lib64/libnss_hesiod-2.17.so
/lib64/libnss_hesiod.so.2
/lib64/libnss_nis-2.17.so
/lib64/libnss_nis.so.2
/lib64/libnss_nisplus-2.17.so
/lib64/libnss_nisplus.so.2
/lib64/libpthread-2.17.so
/lib64/libpthread.so.0
/lib64/libresolv-2.17.so
/lib64/libresolv.so.2
/lib64/librt-2.17.so
/lib64/librt.so.1
/lib64/libthread_db-1.0.so
/lib64/libthread_db.so.1
/lib64/libutil-2.17.so
/lib64/libutil.so.1
/lib64/rtkaio
/lib64/rtkaio/librt.so.1
/lib64/rtkaio/librtkaio-2.17.so
/sbin/ldconfig
/sbin/sln
/usr/lib64/audit
/usr/lib64/audit/sotruss-lib.so
/usr/lib64/gconv
/usr/lib64/gconv/ANSI_X3.110.so
/usr/lib64/gconv/ARMSCII-8.so
/usr/lib64/gconv/ASMO_449.so
/usr/lib64/gconv/BIG5.so
/usr/lib64/gconv/BIG5HKSCS.so
/usr/lib64/gconv/BRF.so
/usr/lib64/gconv/CP10007.so
/usr/lib64/gconv/CP1125.so
/usr/lib64/gconv/CP1250.so
/usr/lib64/gconv/CP1251.so
/usr/lib64/gconv/CP1252.so
/usr/lib64/gconv/CP1253.so
/usr/lib64/gconv/CP1254.so
/usr/lib64/gconv/CP1255.so
/usr/lib64/gconv/CP1256.so
/usr/lib64/gconv/CP1257.so
/usr/lib64/gconv/CP1258.so
/usr/lib64/gconv/CP737.so
/usr/lib64/gconv/CP770.so
/usr/lib64/gconv/CP771.so
/usr/lib64/gconv/CP772.so
/usr/lib64/gconv/CP773.so
/usr/lib64/gconv/CP774.so
/usr/lib64/gconv/CP775.so
/usr/lib64/gconv/CP932.so
/usr/lib64/gconv/CSN_369103.so
/usr/lib64/gconv/CWI.so
/usr/lib64/gconv/DEC-MCS.so
/usr/lib64/gconv/EBCDIC-AT-DE-A.so
/usr/lib64/gconv/EBCDIC-AT-DE.so
/usr/lib64/gconv/EBCDIC-CA-FR.so
/usr/lib64/gconv/EBCDIC-DK-NO-A.so
/usr/lib64/gconv/EBCDIC-DK-NO.so
/usr/lib64/gconv/EBCDIC-ES-A.so
/usr/lib64/gconv/EBCDIC-ES-S.so
/usr/lib64/gconv/EBCDIC-ES.so
/usr/lib64/gconv/EBCDIC-FI-SE-A.so
/usr/lib64/gconv/EBCDIC-FI-SE.so
/usr/lib64/gconv/EBCDIC-FR.so
/usr/lib64/gconv/EBCDIC-IS-FRISS.so
/usr/lib64/gconv/EBCDIC-IT.so
/usr/lib64/gconv/EBCDIC-PT.so
/usr/lib64/gconv/EBCDIC-UK.so
/usr/lib64/gconv/EBCDIC-US.so
/usr/lib64/gconv/ECMA-CYRILLIC.so
/usr/lib64/gconv/EUC-CN.so
/usr/lib64/gconv/EUC-JISX0213.so
/usr/lib64/gconv/EUC-JP-MS.so
/usr/lib64/gconv/EUC-JP.so
/usr/lib64/gconv/EUC-KR.so
/usr/lib64/gconv/EUC-TW.so
/usr/lib64/gconv/GB18030.so
/usr/lib64/gconv/GBBIG5.so
/usr/lib64/gconv/GBGBK.so
/usr/lib64/gconv/GBK.so
/usr/lib64/gconv/GEORGIAN-ACADEMY.so
/usr/lib64/gconv/GEORGIAN-PS.so
/usr/lib64/gconv/GOST_19768-74.so
/usr/lib64/gconv/GREEK-CCITT.so
/usr/lib64/gconv/GREEK7-OLD.so
/usr/lib64/gconv/GREEK7.so
/usr/lib64/gconv/HP-GREEK8.so
/usr/lib64/gconv/HP-ROMAN8.so
/usr/lib64/gconv/HP-ROMAN9.so
/usr/lib64/gconv/HP-THAI8.so
/usr/lib64/gconv/HP-TURKISH8.so
/usr/lib64/gconv/IBM037.so
/usr/lib64/gconv/IBM038.so
/usr/lib64/gconv/IBM1004.so
/usr/lib64/gconv/IBM1008.so
/usr/lib64/gconv/IBM1008_420.so
/usr/lib64/gconv/IBM1025.so
/usr/lib64/gconv/IBM1026.so
/usr/lib64/gconv/IBM1046.so
/usr/lib64/gconv/IBM1047.so
/usr/lib64/gconv/IBM1097.so
/usr/lib64/gconv/IBM1112.so
/usr/lib64/gconv/IBM1122.so
/usr/lib64/gconv/IBM1123.so
/usr/lib64/gconv/IBM1124.so
/usr/lib64/gconv/IBM1129.so
/usr/lib64/gconv/IBM1130.so
/usr/lib64/gconv/IBM1132.so
/usr/lib64/gconv/IBM1133.so
/usr/lib64/gconv/IBM1137.so
/usr/lib64/gconv/IBM1140.so
/usr/lib64/gconv/IBM1141.so
/usr/lib64/gconv/IBM1142.so
/usr/lib64/gconv/IBM1143.so
/usr/lib64/gconv/IBM1144.so
/usr/lib64/gconv/IBM1145.so
/usr/lib64/gconv/IBM1146.so
/usr/lib64/gconv/IBM1147.so
/usr/lib64/gconv/IBM1148.so
/usr/lib64/gconv/IBM1149.so
/usr/lib64/gconv/IBM1153.so
/usr/lib64/gconv/IBM1154.so
/usr/lib64/gconv/IBM1155.so
/usr/lib64/gconv/IBM1156.so
/usr/lib64/gconv/IBM1157.so
/usr/lib64/gconv/IBM1158.so
/usr/lib64/gconv/IBM1160.so
/usr/lib64/gconv/IBM1161.so
/usr/lib64/gconv/IBM1162.so
/usr/lib64/gconv/IBM1163.so
/usr/lib64/gconv/IBM1164.so
/usr/lib64/gconv/IBM1166.so
/usr/lib64/gconv/IBM1167.so
/usr/lib64/gconv/IBM12712.so
/usr/lib64/gconv/IBM1364.so
/usr/lib64/gconv/IBM1371.so
/usr/lib64/gconv/IBM1388.so
/usr/lib64/gconv/IBM1390.so
/usr/lib64/gconv/IBM1399.so
/usr/lib64/gconv/IBM16804.so
/usr/lib64/gconv/IBM256.so
/usr/lib64/gconv/IBM273.so
/usr/lib64/gconv/IBM274.so
/usr/lib64/gconv/IBM275.so
/usr/lib64/gconv/IBM277.so
/usr/lib64/gconv/IBM278.so
/usr/lib64/gconv/IBM280.so
/usr/lib64/gconv/IBM281.so
/usr/lib64/gconv/IBM284.so
/usr/lib64/gconv/IBM285.so
/usr/lib64/gconv/IBM290.so
/usr/lib64/gconv/IBM297.so
/usr/lib64/gconv/IBM420.so
/usr/lib64/gconv/IBM423.so
/usr/lib64/gconv/IBM424.so
/usr/lib64/gconv/IBM437.so
/usr/lib64/gconv/IBM4517.so
/usr/lib64/gconv/IBM4899.so
/usr/lib64/gconv/IBM4909.so
/usr/lib64/gconv/IBM4971.so
/usr/lib64/gconv/IBM500.so
/usr/lib64/gconv/IBM5347.so
/usr/lib64/gconv/IBM803.so
/usr/lib64/gconv/IBM850.so
/usr/lib64/gconv/IBM851.so
/usr/lib64/gconv/IBM852.so
/usr/lib64/gconv/IBM855.so
/usr/lib64/gconv/IBM856.so
/usr/lib64/gconv/IBM857.so
/usr/lib64/gconv/IBM858.so
/usr/lib64/gconv/IBM860.so
/usr/lib64/gconv/IBM861.so
/usr/lib64/gconv/IBM862.so
/usr/lib64/gconv/IBM863.so
/usr/lib64/gconv/IBM864.so
/usr/lib64/gconv/IBM865.so
/usr/lib64/gconv/IBM866.so
/usr/lib64/gconv/IBM866NAV.so
/usr/lib64/gconv/IBM868.so
/usr/lib64/gconv/IBM869.so
/usr/lib64/gconv/IBM870.so
/usr/lib64/gconv/IBM871.so
/usr/lib64/gconv/IBM874.so
/usr/lib64/gconv/IBM875.so
/usr/lib64/gconv/IBM880.so
/usr/lib64/gconv/IBM891.so
/usr/lib64/gconv/IBM901.so
/usr/lib64/gconv/IBM902.so
/usr/lib64/gconv/IBM903.so
/usr/lib64/gconv/IBM9030.so
/usr/lib64/gconv/IBM904.so
/usr/lib64/gconv/IBM905.so
/usr/lib64/gconv/IBM9066.so
/usr/lib64/gconv/IBM918.so
/usr/lib64/gconv/IBM921.so
/usr/lib64/gconv/IBM922.so
/usr/lib64/gconv/IBM930.so
/usr/lib64/gconv/IBM932.so
/usr/lib64/gconv/IBM933.so
/usr/lib64/gconv/IBM935.so
/usr/lib64/gconv/IBM937.so
/usr/lib64/gconv/IBM939.so
/usr/lib64/gconv/IBM943.so
/usr/lib64/gconv/IBM9448.so
/usr/lib64/gconv/IEC_P27-1.so
/usr/lib64/gconv/INIS-8.so
/usr/lib64/gconv/INIS-CYRILLIC.so
/usr/lib64/gconv/INIS.so
/usr/lib64/gconv/ISIRI-3342.so
/usr/lib64/gconv/ISO-2022-CN-EXT.so
/usr/lib64/gconv/ISO-2022-CN.so
/usr/lib64/gconv/ISO-2022-JP-3.so
/usr/lib64/gconv/ISO-2022-JP.so
/usr/lib64/gconv/ISO-2022-KR.so
/usr/lib64/gconv/ISO-IR-197.so
/usr/lib64/gconv/ISO-IR-209.so
/usr/lib64/gconv/ISO646.so
/usr/lib64/gconv/ISO8859-1.so
/usr/lib64/gconv/ISO8859-10.so
/usr/lib64/gconv/ISO8859-11.so
/usr/lib64/gconv/ISO8859-13.so
/usr/lib64/gconv/ISO8859-14.so
/usr/lib64/gconv/ISO8859-15.so
/usr/lib64/gconv/ISO8859-16.so
/usr/lib64/gconv/ISO8859-2.so
/usr/lib64/gconv/ISO8859-3.so
/usr/lib64/gconv/ISO8859-4.so
/usr/lib64/gconv/ISO8859-5.so
/usr/lib64/gconv/ISO8859-6.so
/usr/lib64/gconv/ISO8859-7.so
/usr/lib64/gconv/ISO8859-8.so
/usr/lib64/gconv/ISO8859-9.so
/usr/lib64/gconv/ISO8859-9E.so
/usr/lib64/gconv/ISO_10367-BOX.so
/usr/lib64/gconv/ISO_11548-1.so
/usr/lib64/gconv/ISO_2033.so
/usr/lib64/gconv/ISO_5427-EXT.so
/usr/lib64/gconv/ISO_5427.so
/usr/lib64/gconv/ISO_5428.so
/usr/lib64/gconv/ISO_6937-2.so
/usr/lib64/gconv/ISO_6937.so
/usr/lib64/gconv/JOHAB.so
/usr/lib64/gconv/KOI-8.so
/usr/lib64/gconv/KOI8-R.so
/usr/lib64/gconv/KOI8-RU.so
/usr/lib64/gconv/KOI8-T.so
/usr/lib64/gconv/KOI8-U.so
/usr/lib64/gconv/LATIN-GREEK-1.so
/usr/lib64/gconv/LATIN-GREEK.so
/usr/lib64/gconv/MAC-CENTRALEUROPE.so
/usr/lib64/gconv/MAC-IS.so
/usr/lib64/gconv/MAC-SAMI.so
/usr/lib64/gconv/MAC-UK.so
/usr/lib64/gconv/MACINTOSH.so
/usr/lib64/gconv/MIK.so
/usr/lib64/gconv/NATS-DANO.so
/usr/lib64/gconv/NATS-SEFI.so
/usr/lib64/gconv/PT154.so
/usr/lib64/gconv/RK1048.so
/usr/lib64/gconv/SAMI-WS2.so
/usr/lib64/gconv/SHIFT_JISX0213.so
/usr/lib64/gconv/SJIS.so
/usr/lib64/gconv/T.61.so
/usr/lib64/gconv/TCVN5712-1.so
/usr/lib64/gconv/TIS-620.so
/usr/lib64/gconv/TSCII.so
/usr/lib64/gconv/UHC.so
/usr/lib64/gconv/UNICODE.so
/usr/lib64/gconv/UTF-16.so
/usr/lib64/gconv/UTF-32.so
/usr/lib64/gconv/UTF-7.so
/usr/lib64/gconv/VISCII.so
/usr/lib64/gconv/gconv-modules
/usr/lib64/gconv/gconv-modules.cache
/usr/lib64/gconv/libCNS.so
/usr/lib64/gconv/libGB.so
/usr/lib64/gconv/libISOIR165.so
/usr/lib64/gconv/libJIS.so
/usr/lib64/gconv/libJISX0213.so
/usr/lib64/gconv/libKSC.so
/usr/lib64/libmemusage.so
/usr/lib64/libpcprofile.so
/usr/libexec/getconf
/usr/libexec/getconf/POSIX_V6_LP64_OFF64
/usr/libexec/getconf/POSIX_V7_LP64_OFF64
/usr/libexec/getconf/XBS5_LP64_OFF64
/usr/sbin/glibc_post_upgrade.x86_64
/usr/sbin/iconvconfig
/usr/sbin/iconvconfig.x86_64
/usr/share/doc/glibc-2.17
/usr/share/doc/glibc-2.17/BUGS
/usr/share/doc/glibc-2.17/CONFORMANCE
/usr/share/doc/glibc-2.17/COPYING
/usr/share/doc/glibc-2.17/COPYING.LIB
/usr/share/doc/glibc-2.17/INSTALL
/usr/share/doc/glibc-2.17/LICENSES
/usr/share/doc/glibc-2.17/NEWS
/usr/share/doc/glibc-2.17/PROJECTS
/usr/share/doc/glibc-2.17/README
/usr/share/doc/glibc-2.17/README.hesiod
/usr/share/doc/glibc-2.17/rtld-debugger-interface.txt
/var/cache/ldconfig
/var/cache/ldconfig/aux-cache
/var/db/Makefile
```

glibc.sh

代码学习意义不大


## 下载glibc源码

```shell

git clone https://github.com/bminor/glibc.git

```

## ubuntu 16.04 tls 编译glibc

[configure: error: you must configure in a separate build directory](https://blog.csdn.net/dbkmeteor/article/details/6764650)


```shell

*** These critical programs are missing or too old: make compiler
*** Check the INSTALL file for required versions.

```

INSTALL文件是安装说明文档

make 不低于4.0

linux上c的标准库 封装了系统调用
Rust go标准库有时也依赖

android bionic

musl


openwrt LEDE默认使用Musl-libc
uClibc 一个小型的C语言标准库，主要用于嵌入式。

glibc，uClibc，eglibc都是C语言函数库： 1. uClibc是嵌入式系统中用的，glibc是桌面系统用的
2. eglibc也是嵌入式系统中用的，是glibc的嵌入式版本，和glibc在源码和二进制上兼容。

