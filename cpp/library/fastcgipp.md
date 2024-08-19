# fastcgipp

mac编译失败

git clone https://github.com/eddic/fastcgipp.git fastcgi++
mkdir fastcgi++.build
cd fastcgi++.build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=RELEASE ../fastcgi++
make
