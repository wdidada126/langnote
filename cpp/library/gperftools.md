# gperftools

https://blog.csdn.net/qq_44407144/article/details/131313020

源代码安装gperftools

```
wget http://mirror.rabisu.com/savannah-nongnu/libunwind/libunwind-1.6.2.tar.gz
tar -zxv -f libunwind-1.6.2.tar.gz
cd libunwind-1.6.2
./configure 
make
sudo make install
cd ..
wget https://github.com/gperftools/gperftools/releases/download/gperftools-2.9.1/gperftools-2.9.1.tar.gz -O gperftools-2.9.1.tar.gz
tar -zxv -f gperftools-2.9.1.tar.gz
cd gperftools-2.9.1
./configure
make
sudo make install
sudo ldconfig
```
