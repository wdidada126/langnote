# xlnt

https://github.com/edidada/xlntExample

https://github.com/tfussell/xlnt
先登录gitbook，然后在访问

https://docs.xlnt.dev/
文档不行，换libxl 收费的
autoit 免费

git clone https://github.com/tfussell/xlnt.git xlnt --recurse-submodules
cd xlnt
sudo apt-get update
sudo apt-get install zlibc -y
cmake .
make -j 2
sudo make install
git submodule init
git submodule update
