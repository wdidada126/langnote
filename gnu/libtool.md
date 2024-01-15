# libtool

https://www.gnu.org/software/libtool/manual/

git clone git://git.savannah.gnu.org/libtool.git
cd libtool
git checkout v2.4.7
sudo yum update
sudo yum install help2man texinfo -y
chmod +x bootstrap
./bootstrap
./configure
make -j4
sudo make install
