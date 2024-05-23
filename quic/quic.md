# quic
QUIC 并没有解决 HoL blocking，只是缓解。里外高低都得先从多路复用开始说。

Quick UDP Internet Connections

msquic

https://github.com/microsoft/msquic
lsquic
https://github.com/litespeedtech/lsquic-client
vcpkg install lsquic


quic 基于udp，是传输层？协议

网络协议，先抓包

至少两个节点



**Important** Several QUIC protocol features are not yet fully implemented:

- 0-RTT
- Client-side Migration
- Server Preferred Address
- Path MTU Discovery





```
sudo apt-add-repository ppa:lttng/stable-2.10
sudo apt-get update
sudo apt-get install cmake
sudo apt-get install build-essentials
sudo apt-get install liblttng-ust-dev
sudo apt-get install lttng-tools
mkdir build && cd build
cmake -g 'Linux Makefiles' ..
cmake --build .
```

