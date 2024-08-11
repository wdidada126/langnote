# openh264

https://www.openh264.org/

有各个平台编译好的库
https://sourceforge.net/projects/openh264.mirror/files/v2.4.1/


git clone https://github.com/cisco/openh264.git
cd openh264
git checkout v2.4.1
meson builddir
ninja -C builddir
meson test -C builddir -v

## mac
brew install nasm
