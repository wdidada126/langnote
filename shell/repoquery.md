# repoquery

https://www.cnblogs.com/JMLiu/p/7692784.html

repoquery是yum扩展工具包yum-utils中的一个工具，所有如果你没有repoquery命令的话，可以先 sudo yum install yum-utils 安装yum-utils包。是为了加强和补充yum功能的工具，重点是查询包的关系。repoquery的官方说明是：query information from Yum repositories，故名意思，它只能查看信息，并不能执行安装卸载更新等实质性的操作。而且要和Yum库配合使用。

    repoquery的命令格式和yum很像，但是又有不同，yum 的命令格式是yun [options] [command] [package ...]， repoquery的命令格式是repoquery [options] [item ...]，当然，也可以是repoquery -a [options]，没有item，表示所有。从命令格式的不同，也可以反映出repoquery只能做查询而不支持实质性的操作。

    repoquery的操作分为5类，分别是常规操作、包查询、包选择、组查询和组选择
