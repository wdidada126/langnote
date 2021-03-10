#!/bin/sh

while [ 0 -eq 0 ]
do
    echo ".................. job begin  ..................."
    
/root/vcpkg/vcpkg install thrift gtest boost poco pistache folly libmysql
    # ...... call your command here 在这里调用你的命令 ......

    # check and retry   

    if [ $? -eq 0 ]; then
        echo "--------------- job complete ---------------"
        break;
    else
        echo "...............error occur, retry.........."
#       sleep 2
    fi
done
