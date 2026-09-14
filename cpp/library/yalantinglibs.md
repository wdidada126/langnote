# yalantinglibs
https://github.com/alibaba/yalantinglibs

git clone https://github.com/alibaba/yalantinglibs.git -b 0.6.1
cd yalantinglibs
mkdir build && cd build
cmake ..
cmake --build . --config debug # 可以在末尾加上-j 选项, 通过并行编译加速
ctest . # 执行测试
sudo cmake --install . # --prefix ./user_defined_install_path

https://github.com/edidada/test_cpp_yalantinglibs