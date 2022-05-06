# tree

tree.x86_64 : File system tree viewer

yum search tree | grep ^t

yum install tree -y


https://www.cnblogs.com/centos2017/p/7896807.html

```shell
[wdidada@10-23-29-39 great-project]$ tree .
.
├── build
│   ├── linux
│   │   └── x86_64
│   │       └── release
│   │           └── great-project
│   └── packages
│       └── g
│           └── great-project
│               └── xmake.lua
├── README.md
├── src
│   └── main.cpp
└── xmake.lua
```

tree跟dir对比
tree展示子文件子文件夹