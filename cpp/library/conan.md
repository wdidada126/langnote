# conan

Conan_examples
https://github.com/edidada/Conan_examples

pip install conan
pip3 install conan

https://docs.conan.io/en/latest/installation.html

要求python3吗？

conan search grpc -r conancenter


默认远程地址 conancenter

默认配置文件
~/.conan/conan.conf
编译

conan install .

安装

conan inspect poco/1.9.4

`conan install cjson/1.7.13@`
`conan install packagename/1.0@`
@很重要，有这个后缀才conan install才会把输入参数当做一个包名，如果没有@,conan install 会把 cjson/1.7.13当做一个路径


************************* WARNING: GCC OLD ABI COMPATIBILITY ***********************
 
Conan detected a GCC version > 5 but has adjusted the 'compiler.libcxx' setting to
'libstdc++' for backwards compatibility.
Your compiler is likely using the new CXX11 ABI by default (libstdc++11).
If you want Conan to use the new ABI for the default profile, run:
    $ conan profile update settings.compiler.libcxx=libstdc++11 default
Or edit '/home/wdidada/.conan/profiles/default' and set compiler.libcxx=libstdc++11
************************************************************************************

conan 添加自定义的库

https://blog.csdn.net/hezhanran/article/details/112170151