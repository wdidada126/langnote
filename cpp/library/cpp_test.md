# cpp test

boost.test
ctest
qt test

google test
doctest
catch


export PATH=/root/grpc_1.15.1_withoutgit/cmake/build:$PATH

头文件
/root/grpc_1.15.1_withoutgit/include



#增加.so搜索路径  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/liheyuan/soft/lib  
  
#增加.a搜索路径  
export LIBRARY_PATH=$LIBRARY_PATH:/home/liheyuan/soft/lib  
  
#增加bin搜索路径  
export PATH=$PATH:/home/liheyuan/soft/bin  
  
#增加GCC的include文件搜索路径  
export C_INCLUDE_PATH=$C_INCLUDE_PATH:/home/liheyuan/soft/include  
  
#增加G++的include文件搜索路径  


export C_INCLUDE_PATH=$C_INCLUDE_PATH:/root/grpc_1.15.1_withoutgit/include
export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:/root/grpc_1.15.1_withoutgit/include


ld: cannot find -lgrpc++_reflection


export LIBRARY_PATH=$LIBRARY_PATH:/root/grpc_1.15.1_withoutgit/cmake/build
/root/grpc_1.15.1_withoutgit/cmake/build/libgrpc++_reflection.a




helloworld.pb.cc:(.text+0x74): undefined reference to `google::protobuf::internal::VerifyVersion(int, int, char const*)'


/root/.local/lib64
export LIBRARY_PATH=$LIBRARY_PATH:/root/.local/lib64

