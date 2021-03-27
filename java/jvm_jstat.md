# jstat

jvm 性能调优工具之 jstat
https://www.jianshu.com/p/213710fb9e40

```shell
jstat -gcutil 17124
  S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT     GCT   
  0.00   5.70  63.20   1.94  96.83  94.56     25    0.602     2    0.131    0.732
```


```shell
jstat -options
-class
-compiler
-gc
-gccapacity
-gccause
-gcmetacapacity
-gcnew
-gcnewcapacity
-gcold
-gcoldcapacity
-gcutil
-printcompilation
```

