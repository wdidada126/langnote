# Poco

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

## doc
