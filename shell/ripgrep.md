# [ripgrep](https://github.com/BurntSushi/ripgrep)

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
————————————————
版权声明：本文为CSDN博主「nieops」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_38625669/article/details/91521757