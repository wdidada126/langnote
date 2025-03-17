# Poco

## c++关键字virtual

class Foundation_API Base32DecoderIOS: public virtual std::ios中virtual是干嘛的？

在C++中，`virtual` 关键字用于实现虚函数，允许在继承关系中实现多态性。也就是说，当你在基类中声明一个函数为 `virtual` 时，这个函数可以在派生类中被重写（覆盖），并且在运行时，可以根据对象的实际类型调用相应的函数版本，而不是编译时所确定的函数版本。

在你提到的 `Base32DecoderIOS` 类中，`std::ios` 是一个标准的I/O流类，而 `virtual` 的使用意味着 `Base32DecoderIOS` 类可能被进一步派生，并且派生类中可以重写 `std::ios` 类中的一些虚函数，从而实现特定的行为。

具体来说：
1. 虚继承：在这里，`Base32DecoderIOS` 通过虚继承 `std::ios`，这通常用于避免“钻石继承”问题，也就是在多重继承的情况下，避免多个基类之间重复继承的成员造成的二义性问题。虚继承确保基类 `std::ios` 在最终派生类中只有一个实例。
2. 多态性：虚函数允许在派生类中重写 `std::ios` 的功能，使得你可以在派生类中定制输入输出的行为，同时保留通过基类指针或引用调用这些重写方法的能力。

总结来说，`virtual` 关键字在这个上下文中用于解决复杂的继承关系问题，并为派生类提供重写和定制基类行为的灵活性。

这些错误表明您的CMake项目未能找到APR（Apache Portable Runtime）、APRUTIL（APR Utility Library）以及Apache2的头文件和库。可能是因为这些库没有安装，或者没有正确配置CMake以找到它们。

### 解决方案

#### 1. 安装APR和APRUTIL库
如果您还没有安装这些库，请在系统上安装它们。

在Ubuntu或Debian上，您可以使用以下命令安装这些库：

```bash
sudo apt-get update
sudo apt-get install libapr1-dev libaprutil1-dev apache2-dev
```

在Red Hat或CentOS上，您可以使用：

```bash
sudo yum install apr-devel apr-util-devel httpd-devel
```

在MacOS上，如果您使用的是Homebrew，可以使用以下命令安装：

```bash
brew install apr apr-util
```

#### 2. 手动指定路径
如果您已经安装了这些库，但CMake仍然无法找到它们，您可以在CMakeLists.txt中手动指定这些库的路径。例如：

```cmake
set(APR_INCLUDE_DIR "/path/to/apr/include")
set(APR_LIBRARY "/path/to/apr/lib/libapr-1.so")
set(APRUTIL_INCLUDE_DIR "/path/to/apr-util/include")
set(APRUTIL_LIBRARY "/path/to/apr-util/lib/libaprutil-1.so")
set(APACHE2_INCLUDE_DIR "/path/to/apache2/include")
```

然后在`find_package`命令后添加这些变量。例如：

```cmake
find_package(APR REQUIRED)
find_package(APRUTIL REQUIRED)
find_package(Apache2 REQUIRED)
```

#### 3. 使用CMake GUI或ccmake指定路径
如果您更习惯图形界面，可以使用`cmake-gui`或`ccmake`来手动指定这些库的路径。

1. 运行`cmake-gui`或`ccmake`并加载您的CMakeLists.txt文件。
2. 搜索`APR_INCLUDE_DIR`、`APRUTIL_INCLUDE_DIR`和`APACHE2_INCLUDE_DIR`等变量。
3. 手动设置它们指向正确的路径。
4. 点击“Configure”并重新生成项目文件。

#### 4. 环境变量
另一种方法是通过设置环境变量来让CMake找到这些库：

```bash
export CMAKE_INCLUDE_PATH=/path/to/apr/include:/path/to/apr-util/include:/path/to/apache2/include
export CMAKE_LIBRARY_PATH=/path/to/apr/lib:/path/to/apr-util/lib:/path/to/apache2/lib
```

然后重新运行`cmake`。

### 总结
这些步骤应该可以帮助您解决CMake找不到APR、APRUTIL和Apache2库的问题。如果问题仍然存在，您可能需要检查这些库的安装路径是否正确，或者检查CMake的版本和配置。

.cpp文件里面有class定义

class Foundation_API Base32DecoderIOS: public virtual std::ios 这个c++代码中，virtual含义。

在这个代码片段中，Foundation_API Base32DecoderIOS: public virtual std::ios表示Base32DecoderIOS类继承了std::ios类，并且std::ios类中的虚函数可以被Base32DecoderIOS类重写。这意味着Base32DecoderIOS类可以继承并扩展std::ios类的功能，同时保持其作为流对象的接口。

https://pocoproject.org/download.html#conan

conan安装poco

## Poco::json

AbstractConfiguration
子类
PropertyFileConfiguration
ConfigurationMapper
FilesystemConfiguration
SystemConfiguration
XMLConfiguration
JSONConfiguration
MapConfiguration

ConfigurationView, WinRegistryConfiguration, IniFileConfiguration, LocalConfigurationView,LayeredConfiguration


Object
Array

ParserImpl
Parser


Handler
ParseHandler
PrintHandler

JSONException
POCO_DECLARE_EXCEPTION(JSON_API, JSONException, Poco::Exception)
POCO_IMPLEMENT_EXCEPTION(JSONTemplateException, Exception, "Template Exception")

Query

Stringifier

Part
StringPart
MultiPart
LogicPart
LoopPart


EchoPart

LogicQuery
LogicExistQuery
LogicElseQuery


Choose lmplementation of Part (7 found)

@EchoPart (Poco::JSON) Poco::JSON@
IncludePart(Poco::JSON) Poco::JSON@
LogicPart(Poco::JSON)@
LoopPart(Poco::JSON)@
MultiPart(Poco::JSON)@
Part(Poco::JSON)
@StringPart (Poco::JSON)

TemplateCache


## Poco::Util
AbstractConfiguration
	ConfigurationMapper
	ConfigurationView
	FilesystemConfiguration
	IniFileConfiguration
	JSONConfiguration
	LayeredConfiguration
	LocalConfigurationView
	MapConfiguration
		PropertyFileConfiguration


AtomicCounter

RefCountedObject
	Subsystem
		Application
		LoggingSubsystem


HelpFormatter

Validator
	IntValidator  是Validator子类


LoggingConfigurator

Option


AbstractOptionCallback
	OptionCallback

POCO_IMPLEMENT_EXCEPTION(OptionException, Poco::DataException, "Option exception")
POCO_IMPLEMENT_EXCEPTION(UnknownOptionException, OptionException, "Unknown option specified")
POCO_IMPLEMENT_EXCEPTION(AmbiguousOptionException, OptionException, "Ambiguous option specified")
POCO_IMPLEMENT_EXCEPTION(MissingOptionException, OptionException, "Required option not specified")
POCO_IMPLEMENT_EXCEPTION(MissingArgumentException, OptionException, "Missing option argument")
POCO_IMPLEMENT_EXCEPTION(InvalidArgumentException, OptionException, "Invalid option argument")
POCO_IMPLEMENT_EXCEPTION(UnexpectedArgumentException, OptionException, "Unexpected option argument")
POCO_IMPLEMENT_EXCEPTION(IncompatibleOptionsException, OptionException, "Incompatible options")
POCO_IMPLEMENT_EXCEPTION(DuplicateOptionException, OptionException, "Option must not be given more than once")
POCO_IMPLEMENT_EXCEPTION(EmptyOptionException, OptionException, "Empty option specified")

OptionSet

OptionProcessor


ServerApplication 是Application子类

TimerNotification 是Notification子类

WinRegistryConfiguration

WinRegistryKey

Thread 是ThreadImpl子类

## Poco::Foundation

https://docs.pocoproject.org/1.12.1/Poco.Logger.html

AbstractObserver

ActiveDispatcher 
		ArchiveCompressor	

ActiveStarter<ActiveDispatcher>

NewActionNotification

AutoPtr

ActiveThread

ActiveThreadPool

Condition
ScopedLock

Base32DecoderBuf  是UnbufferedStreamBuf子类
Base32DecoderIOS

Base32Decoder 是Base32DecoderIOS子类


Base32EncoderBuf UnbufferedStreamBuf
Base32EncoderIOS
Base32Encoder


Base64DecoderBuf
Base64DecoderIOS
Base64Decoder

enum Base64EncodingOptions
{
	BASE64_URL_ENCODING = 0x01,

	BASE64_NO_PADDING   = 0x02
};

Base64EncoderBuf
Base64EncoderIOS
Base64Encoder


enum BignumDtoaMode {

  BIGNUM_DTOA_SHORTEST,

  BIGNUM_DTOA_SHORTEST_SINGLE,

  BIGNUM_DTOA_FIXED,

  BIGNUM_DTOA_PRECISION
};


BinaryReader
BasicMemoryBinaryReader

BinaryWriter
	BasicMemoryBinaryWriter

typedef BasicMemoryBinaryWriter<char> MemoryBinaryWriter;


Bugcheck

Channel  是Configurable RefCountedObject子类

Checksum

Clock

typedef struct z_stream_s 


Condition

Configurable

ConsoleChannel: public Channel

ColorConsoleChannel: public Channel

CountingStreamBuf
CountingIOS
CountingInputStream
CountingOutputStream


DataURIStreamIOS: public virtual std::ios

DataURIStream: public DataURIStreamIOS, public std::istream

DateTime

DateTimeFormatter

DeflatingStreamBuf: public BufferedStreamBuf

DeflatingIOS: public virtual std::ios

DeflatingOutputStream: public std::ostream, public DeflatingIOS

DeflatingInputStream: public std::istream, public DeflatingIOS

Environment

EnvironmentImpl

Error

ErrorHandler

public:
    enum EventType
    {
        EVENT_MANUALRESET, /// Manual reset event
        EVENT_AUTORESET    /// Auto-reset event
    };

class Foundation_API Event: private EventImpl

EventArgs

class Foundation_API EventChannel: public Channel
class Foundation_API EventLogChannel: public Channel

class Foundation_API FIFOBufferStreamBuf: public BufferedBidirectionalStreamBuf

class Foundation_API File: private FileImpl

class Foundation_API FileChannel: public Channel

class Foundation_API FileIOS: public virtual std::ios

class Foundation_API FileStreamFactory: public URIStreamFactory
class Foundation_API Formatter: public Configurable, public RefCountedObject

FormattingChannel


public:
    enum RoundingMode
    {
        FP_ROUND_DOWNWARD   = FP_ROUND_DOWNWARD_IMPL,
        FP_ROUND_UPWARD     = FP_ROUND_UPWARD_IMPL,
        FP_ROUND_TONEAREST  = FP_ROUND_TONEAREST_IMPL,
        FP_ROUND_TOWARDZERO = FP_ROUND_TOWARDZERO_IMPL
    };

    enum Flag
    {
        FP_DIVIDE_BY_ZERO = FP_DIVIDE_BY_ZERO_IMPL,
        FP_INEXACT        = FP_INEXACT_IMPL,
        FP_OVERFLOW       = FP_OVERFLOW_IMPL,
        FP_UNDERFLOW      = FP_UNDERFLOW_IMPL,
        FP_INVALID        = FP_INVALID_IMPL
    };

class Foundation_API FPEnvironment: private FPEnvironmentImpl

Glob

template <class T> struct Hash

HashStatistic
class Foundation_API HexBinaryDecoderBuf: public UnbufferedStreamBuf
class Foundation_API HexBinaryDecoderIOS: public virtual std::ios

class Foundation_API HexBinaryDecoder: public HexBinaryDecoderIOS, public std::istream


class Foundation_API HexBinaryEncoderBuf: public UnbufferedStreamBuf


class Foundation_API HexBinaryEncoderIOS: public virtual std::ios

class Foundation_API HexBinaryEncoder: public HexBinaryEncoderIOS, public std::ostream

class Foundation_API InflatingStreamBuf: public BufferedStreamBuf

class Foundation_API InflatingIOS: public virtual std::ios

class Foundation_API InflatingOutputStream: public std::ostream, public InflatingIOS

class Foundation_API InflatingInputStream: public std::istream, public InflatingIOS


enum JSONOptions
{
    JSON_PRESERVE_KEY_ORDER = 1,

    JSON_ESCAPE_UNICODE = 2,

    JSON_WRAP_STRINGS = 4
};


Latin1Encoding
Latin2Encoding
Latin9Encoding

LineEnding

class Foundation_API LineEndingConverterStreamBuf: public UnbufferedStreamBuf


class Foundation_API LineEndingConverterIOS: public virtual std::ios
class Foundation_API InputLineEndingConverter: public LineEndingConverterIOS, public std::istream
class Foundation_API OutputLineEndingConverter: public LineEndingConverterIOS, public std::ostream

LocalDateTime

class Foundation_API LogFile: public LogFileImpl

class Foundation_API Logger: public Channel

LoggingFactory

LoggingRegistry

class Foundation_API LogStreamBuf: public UnbufferedStreamBuf

ManifestBase

MemoryPool

class BasicMemoryStreamBuf: public std::basic_streambuf<ch, tr>

class Foundation_API MemoryIOS: public virtual std::ios

class Foundation_API MemoryInputStream: public MemoryIOS, public std::istream
class Foundation_API MemoryOutputStream: public MemoryIOS, public std::ostream

class Foundation_API MemoryOutputStream: public MemoryIOS, public std::ostream


Message

class Foundation_API Mutex: private MutexImpl

NamedEvent
NamedEvent_Android
NamedEvent_UNIX
NamedEvent_WIN32U

NamedMutex
NamedMutex_Android
NamedMutex_WIN32U

NestedDiagnosticContext
Notification
NotificationCenter
NotificationQueue
NullChannel
NullStream
NumberFormatter
NumberParser
NumericString

Path
Path_UNIX
Path_WIN32U
Path_WINCE

Pipe
PipeImpl
PipeImpl_DUMMY
PipeImpl_POSIX
PipeImpl_WIN32

PipeStream
PriorityNotificationQueue
Process
Process_UNIX
Process_VX
Process_WIN32U
Process_WINCE

PurgeStrategy

Random
RandomStream
RegularExpression
RotateStrategy

RWLock
RWLock_Android
RWLock_POSIX
RWLock_VX
RWLock_WIN32
RWLock_WINCE

Semaphore
Semaphore_POSIX

SHA1Engine

SharedLibrary
SharedLibrary_HPUX
SharedLibrary_UNIX
SharedLibrary_VX
SharedLibrary_WIN32U

SharedMemory
SharedMemory_DUMMY
SharedMemory_POSIX
SharedMemory_WIN32

SignalHandler
SimpleFileChannel
SortedDirectoryIterator

SplitterChannel
Stopwatch

String
StringTokenizer
SynchronizedObject
SyslogChannel

Task
TaskManager
TaskNotification

TeeStream
TemporaryFile
TextBufferIterator
TextConverter
TextEncoding
TextIterator
Thread
Thread_POSIX
Thread_VX


## Poco::JWT

POCO_IMPLEMENT_EXCEPTION(JWTException, Exception, "JWT Exception")
POCO_IMPLEMENT_EXCEPTION(ParseException, JWTException, "JWT parsing failed")
POCO_IMPLEMENT_EXCEPTION(UnsupportedAlgorithmException, JWTException, "Unsupported signing algorithm")
POCO_IMPLEMENT_EXCEPTION(UnallowedAlgorithmException, JWTException, "Unallowed signing algorithm")
POCO_IMPLEMENT_EXCEPTION(SignatureException, JWTException, "JWT Signature Exception")
POCO_IMPLEMENT_EXCEPTION(SignatureVerificationException, SignatureException, "JWT signature verification failed")
POCO_IMPLEMENT_EXCEPTION(SignatureGenerationException, SignatureException, "JWT signature generation failed")


Serializer
Signer
Token

POCO::NET


HTTPRequestHandler
AbstractHTTPRequestHandler


最朴实无华的c艹基础库，非常易懂，大多数实现初学者看起来毫无压力；功能也非常全面，功能集相当于一个小Qt；目前很火的ClickHouse里面也用到了。学完这个里面的东西，对于一般c艹应用开发绝对够了。缺点可能就是由于实现朴实有些地方可能性能不够好（不过这是个取舍的问题，CH性能很好不也用了poco，如果发现性能问题的地方可以换做其他的），还有就是实现可能不够modern。

poco 1.13.0需要cpp17

~/poco/build/lib$ ldd libPocoDataMySQL.so
    linux-vdso.so.1 (0x00007ffed2dd1000)
    libPocoData.so.93 => /home/wdidada/poco/build/lib/libPocoData.so.93 (0x00007f22380bd000)
    libmysqlclient.so.21 => /lib/x86_64-linux-gnu/libmysqlclient.so.21 (0x00007f2237982000)
    libPocoFoundation.so.93 => /home/wdidada/poco/build/lib/libPocoFoundation.so.93 (0x00007f223773e000)
    libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f223771b000)
    libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007f2237539000)
    libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f2237514000)
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f2237320000)
    libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f223731a000)
    libssl.so.1.1 => /lib/x86_64-linux-gnu/libssl.so.1.1 (0x00007f2237287000)
    libcrypto.so.1.1 => /lib/x86_64-linux-gnu/libcrypto.so.1.1 (0x00007f2236fb0000)
    libresolv.so.2 => /lib/x86_64-linux-gnu/libresolv.so.2 (0x00007f2236f94000)
    /lib64/ld-linux-x86-64.so.2 (0x00007f223833f000)
    librt.so.1 => /lib/x86_64-linux-gnu/librt.so.1 (0x00007f2236f8a000)
    libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f2236e39000)

这个库不是为了高性能而诞生的，就是为了快速开发一些常用的日常功能而设计的，学习和使用都非常简单，正好符合题主的需求。

```
extern "C" const struct Net_API NetworkInitializer pocoNetworkInitializer;
```
在Poco（一个C++的跨平台C++库）的源代码中，这行代码包含了几个关键的概念，主要涉及到C++和C语言之间的互操作性，以及如何在C++中声明和使用全局变量。让我们逐一解析这行代码：
```cpp
extern "C":
```
这是C++中的一个特殊语法，用于告诉C++编译器在链接时，将这部分代码当作C语言代码来处理。这是因为C++支持函数重载（即可以有多个同名但参数不同的函数），而C语言不支持。因此，C++编译器会为每个函数（包括全局变量，因为全局变量在C++中也被视为一种特殊的函数，即“返回类型为类型本身，没有参数”的函数）生成一个唯一的名称（这个过程称为名称修饰或名称改编），以便区分不同的重载版本。然而，C语言编译器则不会进行这样的名称修饰。因此，如果C++代码想要调用C语言编写的库函数，或者C++代码中的函数/变量需要被C语言代码调用/访问，就需要使用extern "C"来告诉C++编译器这部分代码应该按照C语言的方式来处理，即不进行名称修饰。
const struct Net_API NetworkInitializer pocoNetworkInitializer;:
这部分声明了一个全局常量变量pocoNetworkInitializer，其类型为const struct Net_API。struct Net_API很可能是一个在Poco库中定义的结构体，用于封装与网络初始化相关的API或配置信息。const关键字表明这个变量一旦被初始化后，其值就不能被修改。
注意，这里的NetworkInitializer看起来像是想要用作类型名的部分，但实际上它可能是被误放在这里了，或者是某种特定于Poco库内部的命名约定。在标准的C++语法中，这里的NetworkInitializer并不作为类型名使用，而是紧随const struct Net_API之后的部分可能是个笔误或误导。正确的声明应该直接以const struct Net_API开头，后面跟变量名。
综上所述，这行代码的意图是声明一个全局常量pocoNetworkInitializer，其类型为const struct Net_API，并且这个变量在使用时需要按照C语言的方式进行链接（即不进行C++的名称修饰），以便可能与其他C或C++代码（特别是那些没有使用C++名称修饰的代码）进行互操作。

正确的声明（如果NetworkInitializer确实是笔误或误导）可能是这样的：

```cpp
extern "C" const struct Net_API pocoNetworkInitializer;
```
或者，如果Net_API已经是一个typedef的别名，那么可能连struct关键字都不需要（这取决于Net_API的具体定义）：

```cpp
extern "C" const Net_API pocoNetworkInitializer;
```

## book
https://book.douban.com/subject/17995926/

9783639973624

## windows linux都支持

## 读取配置文件
Poco 是一个开源的 C++ 类库集合，提供了许多功能，包括读写配置文件。Poco 支持 INI 文件格式。

安装 Poco：

Linux：可以通过包管理器安装（例如，sudo apt-get install libpoco-dev）。
Windows：可以从Poco官方网站下载和安装。
示例代码：

```cpp
#include <Poco/Util/IniFileConfiguration.h>
#include <Poco/AutoPtr.h>
#include <iostream>

int main() {
    Poco::AutoPtr<Poco::Util::IniFileConfiguration> pConf(new Poco::Util::IniFileConfiguration("config.ini"));

    // 获取配置值
    std::string value = pConf->getString("section.key");

    std::cout << "Value: " << value << std::endl;

    // 修改配置值
    pConf->setString("section.key", "new_value");

    // 保存配置文件
    pConf->save("config.ini");

    return 0;
}
```
编译命令：
```
g++ -o config_example config_example.cpp -lPocoUtil -lPocoFoundation
```
## SMTP

适合嵌入式设备
https://pocoproject.org/
支持cmake autotools编译
可以用conan vcpkg安装

https://github.com/pocoproject/poco/


## example
https://github.com/pocoproject/cmake-sample

vcpkg install Poco
The Poco package requires at least one component

Installed:
  poco-devel.x86_64 0:1.6.1-3.el7
  yum install poco-devel -y
Dependency Installed:
  libiodbc.x86_64 0:3.52.7-7.el7        poco-crypto.x86_64 0:1.6.1-3.el7              poco-data.x86_64 0:1.6.1-3.el7          poco-debug.x86_64 0:1.6.1-3.el7        poco-foundation.x86_64 0:1.6.1-3.el7       
  poco-json.x86_64 0:1.6.1-3.el7        poco-mongodb.x86_64 0:1.6.1-3.el7             poco-mysql.x86_64 0:1.6.1-3.el7         poco-net.x86_64 0:1.6.1-3.el7          poco-netssl.x86_64 0:1.6.1-3.el7           
  poco-odbc.x86_64 0:1.6.1-3.el7        poco-pagecompiler.x86_64 0:1.6.1-3.el7        poco-sqlite.x86_64 0:1.6.1-3.el7        poco-util.x86_64 0:1.6.1-3.el7         poco-xml.x86_64 0:1.6.1-3.el7              
  poco-zip.x86_64 0:1.6.1-3.el7 

sudo apt install libpoco-dev -y

查看安装的poco库版本
```shell
sudo apt show libpoco-dev
Package: libpoco-dev
Version: 1.11.0-3
Priority: optional
Section: universe/libdevel
Source: poco
Origin: Ubuntu
```

sudo apt-get -y update && sudo apt-get -y install git g++ make cmake libssl-dev
git clone https://github.com/pocoproject/poco.git
cd poco
git checkout poco-1.11.0-release
mkdir cmake-build
cd cmake-build
cmake ..
cmake --build . --config Release


git clone https://github.com/edidada/poco-cmake-sample.git
cd poco-cmake-sample
cmake -S . -B build-output
cmake --build build-output --target all
build-output/pocoex

## 自己的代码

https://github.com/edidada/pocoservertest

https://github.com/edidada/rest_poco

## doc
https://docs.pocoproject.org/1.12.1/
https://docs.pocoproject.org/1.13.3/99100-ReleaseNotes.html
https://docs.pocoproject.org/current/

https://docs.pocoproject.org/1.12.2/00200-DataUserManual.html

Packages
ActiveRecord
Crypto
Data
Data/MySQL
Data/ODBC
Data/PostgreSQL
Data/SQLite
Encodings
Foundation
JSON
JWT
MongoDB
Net
NetSSL_OpenSSL
Prometheus
Redis
Util
XML
Zip


Namespaces
Poco
Poco::ActiveRecord
Poco::Crypto
Poco::Data
Poco::Data::Keywords
Poco::Data::MySQL
Poco::Data::ODBC
Poco::Data::PostgreSQL
Poco::Data::SQLite
Poco::Data::Test
Poco::Details
Poco::Dynamic
Poco::Dynamic::Impl
Poco::Impl
Poco::JSON
Poco::JWT
Poco::MongoDB
Poco::Net
Poco::Net::Impl
Poco::Prometheus
Poco::Redis
Poco::Util
Poco::Util::Units
Poco::Util::Units::Constants
Poco::Util::Units::Internal
Poco::Util::Units::Units
Poco::Util::Units::Values
Poco::XML
Poco::Zip
hsql
std

## 自己总结的api

查来所有子类
Ctrl Alt B

CLion查看类代码的父类，子类
Ctrl + H

AbstractConfiguration (Poco::Util)
    IniFileConfiguration (Poco::Util)
    LayeredConfiguration (Poco::Util)
ActiveResultHolder (Poco)
ActiveRunnableBase (Poco)
    ActiveRunnable (Poco)
Channel (Poco)
    Logger (Poco)
IPAddressImpl (Poco::Net::Impl)
    IPv4AddressImpl (Poco::Net::Impl)
    IPv6AddressImpl (Poco::Net::Impl)
SessionImpl (Poco::Data)
SocketAddressImpl (Poco::Net::Impl)
    IPv4SocketAddressImpl (Poco::Net::Impl)
    IPv6SocketAddressImpl (Poco::Net::Impl)
SocketImpl (Poco::Net)
Subsystem (Poco::Util)
    Application (Poco::Util)
        ServerApplication (Poco::Util)
            MyServerApp (http_server.cpp)
            MyServerApp (mymain.cpp)
    LoggingSubsystem (Poco::Util)
TCPServerConnectionFilter (Poco::Net)
TCPServerParams (Poco::Net)
    HTTPServerParams (Poco::Net)


### 

### Poco

Exception.h
Exception
class Foundation_API Exception: public std::exception


   catch (Poco::Exception& ex) {
        // 处理 JSON 解析异常
        result["error"] = ex.displayText();
    } catch (std::exception& ex) {
        // 处理其它异常
        result["error"] = ex.what();
    }


#### Poco::ActiveRecord
#### Poco::Crypto
#### Poco::Data
#### Poco::Data::Keywords
#### Poco::Data::MySQL
#### Poco::Data::ODBC
#### Poco::Data::PostgreSQL
#### Poco::Data::SQLite
#### Poco::Data::Test
#### Poco::Details
#### Poco::Dynamic
#### Poco::Dynamic::Impl
#### Poco::Impl
#### Poco::JSON

JSONException.h


#### Poco::JWT
#### Poco::MongoDB
#### Poco::Net

void Net_API initializeNetwork();
void Net_API uninitializeNetwork();
std::string htmlize(const std::string& str);

ICMPClient

// ICMPClient.h
//
// Library: Net
// Package: ICMP
// Module:  ICMPClient

ICMPEventArgs
// ICMPEventArgs.h
//
// Library: Net
// Package: ICMP
// Module:  ICMPEventArgs

ICMPPacket
// ICMPPacket.h
//
// Library: Net
// Package: ICMP
// Module:  ICMPPacket

ICMPPacketImpl
// ICMPPacketImpl.h
//
// Library: Net
// Package: ICMP
// Module:  ICMPPacketImpl

ICMPSocket


HTTPRequest


// HTTPRequest.h
//
// Library: Net
// Package: HTTP
// Module:  HTTPRequest

HTTPServerRequest
// HTTPServerRequest.h
//
// Library: Net
// Package: HTTPServer
// Module:  HTTPServerRequest

#### Poco::Net::Impl
#### Poco::Prometheus
#### Poco::Redis
#### Poco::Util
##### Poco::Util::Units
###### Poco::Util::Units::Constants
###### Poco::Util::Units::Internal
###### Poco::Util::Units::Units
###### Poco::Util::Units::Values
#### Poco::XML
#### Poco::Zip
### hsql
### std 

HTTPRequestHandlerFactory
HTTPRequestHandler

## 官方examole
https://github.com/pocoproject/cmake-sample

github仓库代码的sample在
https://github.com/pocoproject/poco/tree/main/JSON/samples
https://github.com/pocoproject/poco/tree/main/Crypto/samples
https://github.com/pocoproject/poco/tree/main/Data/samples
https://github.com/pocoproject/poco/tree/main/Net/samples