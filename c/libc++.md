# libc++

https://libcxx.llvm.org/

https://libcxx.llvm.org/BuildingLibcxx.html

## 源代码

git clone -b llvmorg-17.0.6 https://gitcode.com/pollyduan/llvm-project.git
cd llvm-project
mkdir build && cd build
cmake -DLLVM_ENABLE_PROJECTS=clang -DCMAKE_BUILD_TYPE=Release -G "Unix Makefiles" ../llvm
make -j5


cmake -G Ninja -S runtimes -B build -DLLVM_ENABLE_RUNTIMES="libcxx;libcxxabi;libunwind"
ninja -C build cxx cxxabi unwind
ninja -C build check-cxx check-cxxabi check-unwind
ninja -C build install-cxx install-cxxabi install-unwind

"Visual Studio 16 2019"
"Visual Studio 17 2022"

cmake -G "Visual Studio 17 2022" -DCMAKE_C_COMPILER="C:/Program Files/LLVM/bin/clang-cl.exe" -DCMAKE_CXX_COMPILER="C:/Program Files/LLVM/bin/clang-cl.exe" -S runtimes -B build -T "ClangCL" -DLLVM_ENABLE_RUNTIMES=libcxx -DLIBCXX_ENABLE_SHARED=YES -DLIBCXX_ENABLE_STATIC=NO
cmake --build build
