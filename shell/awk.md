# awk

https://www.cnblogs.com/ginsonwang/p/5102668.html

## example1

[linux 一行数值累加求和](https://blog.csdn.net/chenxieyy/article/details/53786313)

```

cat 1.txt | sed -n '1p' | awk '{for(i=1;i<=NF;i++){sum+=$i;} print sum;}'

```


## example2
cat count.txt
1.1
2.3
3
4
5.5

cat count.txt | awk '{sum+=$1} END {print "Sum = ", sum}'
cat count.txt | awk '{sum+=$1} END {print "Average = ", sum/NR}'


[awk内置变量](https://www.thegeekstuff.com/2010/01/8-powerful-awk-built-in-variables-fs-ofs-rs-ors-nr-nf-filename-fnr)

grep的查找，sed的编辑，awk在其对数据分析并生成报告时，显得尤为强大。

[linux awk命令详解](https://www.cnblogs.com/ggjucheng/archive/2013/01/13/2858470.html)

将grep的结果导入到一个文件中
#grep XXXXXXXX > /tmp/abc.txt
以上是将grep（XXX是你grep的参数）放入/tmp/abc.txt中，如果文件存在就清空文件，如果文件不存在就建立
#grep XXXXXXXX >> /tmp/abc.txt
以上是将grep（XXX是你grep的参数）放入/tmp/abc.txt中，如果文件存在就续写在文件的尾部，如果文件不存在就建立

[shell中用awk分割字符串](https://blog.csdn.net/huanongjingchao/article/details/18359225)

字符串为：hua nong jing chao,我想以空格为分隔符把次字符串分开
var1=`echo "hua nong jing chao"|awk -F ' ' '{print $1}'`
如果想用其他字符作为分隔符，则-F后面可以换成相应的分割付，然后进行分割

```

[root@iZ2ze9f7g12pq4tby7ewz2Z ~]# cat test_awk.txt
authcenter-medium-center.2019-07-06.0.log:30234
authcenter-medium-center.2019-07-06.1.log:4027
authcenter-medium-center.2019-07-07.0.log:30338
authcenter-medium-center.2019-07-08.0.log:33410
authcenter-medium-center.2019-07-08.1.log:2173
[root@iZ2ze9f7g12pq4tby7ewz2Z ~]# cat test_awk.txt | awk -F ':' '{print $1}'
authcenter-medium-center.2019-07-06.0.log
authcenter-medium-center.2019-07-06.1.log
authcenter-medium-center.2019-07-07.0.log
authcenter-medium-center.2019-07-08.0.log
authcenter-medium-center.2019-07-08.1.log
[root@iZ2ze9f7g12pq4tby7ewz2Z ~]# cat test_awk.txt | awk -F ':' '{print $2}'
30234
4027
30338
33410
2173

```

[root@iZ2ze9f7g12pq4tby7ewz2Z ~]# cat test_awk.txt | awk -F ':' '{print $2}' | awk '{sum+=$1} END {print "Sum = ", sum}'
Sum =  100182

