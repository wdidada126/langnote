# Poco

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
https://docs.pocoproject.org/current/

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
