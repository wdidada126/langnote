# privoxy

https://www.privoxy.org/

https://www.privoxy.org/user-manual/index.html

https://github.com/shadowsocks/ShadowsocksX-NG
用了


源代码和安装文件
https://sourceforge.net/projects/ijbswa/files/Win32/3.0.34%20%28stable%29/


## source code 源代码
git clone https://www.privoxy.org/git/privoxy.git
cd privoxy
autoheader
autoconf
./configure      # (--help to see options)
make             # (the make from GNU, sometimes called gmake)
su               # Possibly required
make -n install  # (to see where all the files will go)
make -s install  # (to really install, -s to silence output)



git clone https://www.privoxy.org/git/privoxy.git
cd privoxy
autoheader
autoconf
./configure
make -j4
sudo make -n install
