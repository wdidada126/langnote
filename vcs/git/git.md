# Git



https://centos.pkgs.org/7/endpoint-x86_64/git-2.23.0-1.ep7.x86_64.rpm.html

https://packages.endpoint.com/rhel/7/os/x86_64/git-2.23.0-1.ep7.x86_64.rpm


git centos 7新版本安装
https://blog.csdn.net/caimengyuan/article/details/80634752

yum search git
yum remove -y git | yum -y install git2u


rpm包名称可能是git224

```shell
git branch 0a
192:LangNote ibqo$ git branch -a
  0a
* master
  remotes/b/master
  remotes/origin/master
```





```shell
git branch -d 0a
Deleted branch 0a (was 99c7b17).
192:LangNote ibqo$ git branch -a
* master
  remotes/b/master
  remotes/origin/master
```





git 回退到某个commit
回退命令:
$ git reset --hard HEAD^ 回退到上个版本
$ git reset --hard HEAD~3 回退到前3次提交之前,以此类推,回退到n次提交之前
$ git reset --hard commit_id 退到/进到 指定commit的..


git config  user.name "Edidada Tom"
git config  user.email "sandisks555@gmail.com"

[How to “git clone” including submodules](https://stackoverflow.com/questions/3796927/how-to-git-clone-including-submodules)





```
git remote rename origin old-origin
git remote add origin git@gitlab.com:edidada/buildgrpc.git
git push -u origin --all
git push -u origin --tags
```





下次关注下配置库 自己的配置有没有被别人回滚了



git 查看某个文件的更新历史 更新时间



ssh



[git error stackoverflow](https://stackoverflow.com/questions/9393409/ssh-could-not-resolve-hostname-github-com-name-or-service-not-known-fatal-th)



[git 报错](https://www.cnblogs.com/niuniui/p/8783273.html)



插槽不会git回退

https://www.liaoxuefeng.com/wiki/896043488029600/897013573512192



fatal: refusing to merge unrelated histories



`git merge origin/master  --allow-unrelated-histories`



[git fork后同步更新](https://blog.csdn.net/csm201314/article/details/83045605)



#### git 统计代码行数

```shell script
git log --author="edidada" --pretty=tformat: --numstat | awk '{ add += $1; subs += $2; loc += $1 - $2 } END { printf "added lines: %s, removed lines: %s, total lines: %s\n", add, subs, loc }' -
```


`git clone -b branchname`

[git fork之后，再次同步](https://blog.csdn.net/qq1332479771/article/details/56087333)

```

warning: the following paths have collided (e.g. case-sensitive paths
on a case-insensitive filesystem) and only one from the same
colliding group is in the working tree:

  'googletest/docs/FAQ.md'
  'googletest/docs/faq.md'
  'googletest/docs/Primer.md'
  'googletest/docs/primer.md'
  'googletest/docs/Samples.md'
  'googletest/docs/samples.md'

```

git@github.com:apache/incubator-shardingsphere.git

[git reset 回退到某一版本](https://blog.csdn.net/pzhtpf/article/details/52212671)


git merge完全解析
https://www.jianshu.com/p/58a166f24c81

https://blog.csdn.net/u012150179/article/details/14047183

现在，我们把dev分支的工作成果合并到master分支上：

```
$ git merge dev
Updating d46f35e..b17d20e
Fast-forward
 readme.txt | 1 +
 1 file changed, 1 insertion(+)
```

git merge命令用于合并指定分支到当前分支。合并后，再查看readme.txt的内容，就可以看到，和dev分支的最新提交是完全一样的。
注意到上面的Fast-forward信息，Git告诉我们，这次合并是“快进模式”，也就是直接把master指向dev的当前提交，所以合并速度非常快。
当然，也不是每次合并都能Fast-forward，我们后面会讲其他方式的合并。


廖雪峰 git js

`git fetch`
`git merge`

远程仓库的备份

https://blog.csdn.net/csm201314/article/details/83045605

git reset ff391a57c55ffaf3a625de19bd7af218e4037e1a


https://stackoverflow.com/questions/14040754/deleting-remote-master-branch-refused-due-to-being-current-branch

#### git 

https://blog.csdn.net/qq_32452623/article/details/54340749




[git 获取指定的tag处代码](https://blog.csdn.net/jeffasd/article/details/72520668)

[git命令－切换分支](http://www.cnblogs.com/smiler/p/6924583.html)


`git ls-files -u  | cut -f 2 | sort -u`

#### git忽略指定文件夹

.gitignore

target/



[git丢弃本地修改的所有文件](https://blog.csdn.net/leedaning/article/details/51304690)

`git checkout .`

```

git log --author="edidada" --pretty=tformat: --numstat | awk '{ add += $1; subs += $2; loc += $1 - $2 } END { printf "added lines: %s, removed lines: %s, total lines: %s\n", add, subs, loc }' -

```



[Mac、Windows下git log中文乱码](https://www.jianshu.com/p/df01196bd4db)

windows下是gbk编码





git fetch origin


[ls-files](https://git-scm.com/docs/git-ls-files)


git config --list --gloable


### 


```shell
git add .
git status
On branch master
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

        modified:   README.txt
        modified:   benchmarks.rb		
```




[Git 修改已提交的commit注释](https://www.jianshu.com/p/098d85a58bf1)

`git commit --amend`





[GIT Submodule的使用](https://www.jianshu.com/p/0107698498af)






git submodule add git@github.com:google/googletest.git


https://git-scm.com/book/en/v2/Git-Tools-Submodules

git submodules add 当前文件夹不能有同名子文件夹，不然报错

https://blog.csdn.net/guotianqing/article/details/82391665
git module 删除





 https://stackoverflow.com/questions/1777854/how-can-i-specify-a-branch-tag-when-adding-a-git-submodule 



切换子模块分支


[Git之同一台电脑连接多个远程仓库](https://www.cnblogs.com/zhengyan/p/10728527.html)

 https://www.cnblogs.com/zhengyan/p/10728527.html 



#### 测试git能否连接github

https://blog.csdn.net/littlehaes/article/details/102082142



Permission denied (publickey).报错解决

ssh-keygen之后，

#### 把ssh 添加到keychain中

ssh-add -K /Users/youre_user_name/.ssh/id_rsa







Could not open a connection to your authentication agent.

报错解决



https://www.cnblogs.com/sheldonxu/archive/2012/09/17/2688281.html



ssh-agent bash



电脑断网

`Please make sure you have the correct access rights`





git windows

bash

不能输入e等字符





git 主机连接多个git仓库 指定私钥文件 ssh可以指定

https://www.jianshu.com/p/ea50640ff704





##### Git fork后如何同步源仓库更新



[fork后如何同步源仓库更新](https://www.cnblogs.com/leisurelylicht/p/Git-fork-hou-ru-he-tong-bu-yuan-cang-ku-geng-xin.html)



```shell
1. 设置源仓库的远程地址
>> git remote add [新地址名称] [源仓库远程地址]
>> git remote add upstream https://github.com/leisurelicht/wtfpython-cn

2. 同步fork
>> git fetch [新地址名称]
>> git fetch upstream

3. 本地切换到想要更新的分支上
>> git checkout [branch]
>> git checkout master

4. 把源仓库的远程分支合并到本地
>> git merge [新地址名称/分支]
>> git merge upstream/master

5. 更新到自己的远程库上
>> git push origin master
```



ls



issue-5234-dev



[how to delete all commit history in github](https://stackoverflow.com/questions/13716658/how-to-delete-all-commit-history-in-github)