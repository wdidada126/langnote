# git submodule说明


maven submodule
cmake submodule

开发过程中，经常会有一些通用的部分希望抽取出来做成一个公共库来提供给别的工程来使用，而公共代码库的版本管理是个麻烦的事情。今天无意中发现了git的git submodule命令，之前的问题迎刃而解了。

    开发过程中，经常会有一些通用的部分希望抽取出来做成一个公共库来提供给别的工程来使用，而公共代码库的版本管理是个麻烦的事情。今天无意中发现了git的git submodule命令，之前的问题迎刃而解了。


添加
为当前工程添加submodule，命令如下：

```shell
git submodule add 仓库地址 路径
```

其中，仓库地址是指子模块仓库地址，路径指将子模块放置在当前工程下的路径。 
注意：路径不能以 / 结尾（会造成修改不生效）、不能是现有工程已有的目录（不能順利 Clone）

命令执行完成，会在当前工程根路径下生成一个名为“.gitmodules”的文件，其中记录了子模块的信息。添加完成以后，再将子模块所在的文件夹添加到工程中即可。

删除
submodule的删除稍微麻烦点：首先，要在“.gitmodules”文件中删除相应配置信息。然后，执行“git rm –cached ”命令将子模块所在的文件从git中删除。

下载的工程带有submodule
当使用git clone下来的工程中带有submodule时，初始的时候，submodule的内容并不会自动下载下来的，此时，只需执行如下命令：

```shell
git submodule update --init --recursive
```

即可将子模块内容下载下来后工程才不会缺少相应的文件。

#  git remote

```shell

git remote show origin

```

# git版本控制系统学习笔记



 - git add
向本地仓库添加文件
 - git commit
 向本地仓库提交
 - git push
 提交到本地仓库
 - git status
 查看仓库状态
 - git reset
 回退到某个版本
 - git reflog
 查看日志
 - commit id
 提交的id
 - git diff
查看区别
 - HEAD
 指向当前版本
第一步是用git add把文件添加进去，实际上就是把文件修改添加到暂存区；
第二步是用git commit提交更改，实际上就是把暂存区的所有内容提交到当前分支。
需要提交的文件修改通通放到暂存区，然后，一次性提交暂存区的所有修改。

当你改乱了工作区某个文件的内容，想直接丢弃工作区的修改时，用命令git checkout -- file。

当你不但改乱了工作区某个文件的内容，还添加到了暂存区时，想丢弃修改，分两步，第一步用命令git reset HEAD file，就回到了场景1，第二步按场景1操作。
已经提交了不合适的修改到版本库时，想要撤销本次提交，参考版本回退一节，不过前提是没有推送到远程库。

## Git分支

- git branch
查看分支
当前分支名称前面有 '*' 号
- git branch <name>
创建分支
-git checkout <name>
切换分支
- git checkout -b <name>
创建+切换分支
- git merge <name>
合并某分支到当前分支
- git branch -d <name>
删除分支

- git log --graph
命令可以看到分支合并图。

git fetch
//TODO:


[git reflog 和 git log 的区别](http://wjp2013.github.io/tool/git-reflog-git-log-git-cherry-pick/)

git reflog
可以查看所有分支的所有操作记录（包括已经被删除的 commit 记录和 reset 的操作），
git log
则不能察看已经删除了的commit记录

