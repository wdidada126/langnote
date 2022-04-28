# ripgrep
后端llvm

rg能检索word中的内容吗？

https://github.com/BurntSushi/ripgrep
rust_README.md
可以学习不同linux Unix系统的包管理工具

[ripgrep](https://github.com/BurntSushi/ripgrep)

1.ripgrep Windows版命令行版搜索 挺好用的
2.vscode最新版有一个搜索图标 该功能底层调用ripgrep 当打开所需要搜索的文件夹再搜索就可以查询



推荐个windows平台的类似grep工具 ripgrep



工具	命令	时间（秒）
grep	grep -FR ext4 .	37.972
ucg	ucg -Q --nosmart-case ext4	1.196
pt	pt ext4	0.994
ack	ack -Q ext4	8.523
sift	sift -SQ ext4	1.886
git grep	git grep -F ext4	1.911
ag	ag -sQ ext4	1.011
rg	rg -sF ext4	0.955


rg 搜索的字符串中间有空格



