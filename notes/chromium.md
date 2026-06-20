# chromium

https://www.chromium.org/developers/how-tos/get-the-code/

https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md


## 编译源码 source code
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
curPwd=$(pwd)
export PATH="$curPwd/depot_tools:$PATH"
mkdir chromium && cd chromium
fetch --nohooks chromium
cd src
./build/install-build-deps.sh
gclient runhooks
gn gen out/Default
autoninja -C out/Default chrome
out/Default/chrome

备注：这个./build/install-build-deps.sh，需要手动输入Y

下载别人编译好的chromium
docker版本的

微软是真有钱，github action下载速度34M/s
Receiving objects: 100% (21983990/21983990), 43.76 GiB | 34.66 MiB/s, done.