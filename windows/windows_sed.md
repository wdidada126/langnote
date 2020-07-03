# windows



cmd下运行

powershell下不行



`set sed="C:\Program Files\Git\usr\bin\sed.exe"`



`%sed% -i s/XXXXXX/xxx/g *.md`
/usr/bin/sed: can't read *.md: No such file or directory





`%sed% -i s/XXXXXX/xxx/g *.md`



```shell
%sed% : 无法将“%sed%”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正
确，然后再试一次。
所在位置 行:1 字符: 1
+ %sed% -i s/XXXXXX/xxx/g *.md
+ ~~~~~
    + CategoryInfo          : ObjectNotFound: (%sed%:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
```



sed

windows下使用sed和tee命令

[windows下使用sed和tee命令](https://www.cnblogs.com/zndxall/p/9319077.html)

```shell
set sed="C:\Program Files\Git\usr\bin\sed.exe"
sed -i s/1234/5678/g test.txt

```

sed：流编辑器，用来把文档里面的文字经过一系列编辑命令转换为另一种格式输出；通常用来匹配一个或多个正则表达式的文本进行处理。



