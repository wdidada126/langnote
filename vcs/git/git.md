# git
.gitmodules

```
[submodule "node_modules/loader"]
	path = node_modules/loader
	url = git://github.com/jonlb/node-jxLoader.git
[submodule "node_modules/uglifyjs"]
	path = node_modules/uglifyjs
	url = https://github.com/mishoo/UglifyJS.git
[submodule "node_modules/pkginfo"]
	path = node_modules/pkginfo
	url = git://github.com/indexzero/node-pkginfo.git
```

git submodule init
git submodule update

hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint: 
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only


```shell
git pull
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint: 
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint: 
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.
```

https://github.com/git/git/releases

## git remote add xxx之后，不能从新添加的分支检出

git fetch一下
git fetch xxx master:master

## git pull 磁盘不够了

error: The following untracked working tree files would be overwritten by merge:
.gitignore
2023/202308/202308_month.md

你遇到的这个问题是因为你本地有一些未被跟踪（untracked）的文件，这些文件在远程仓库中可能已经发生了改变。如果你试图使用 git pull 命令，Git 会试图合并远程的更改到你的本地环境，这可能会导致你的本地文件被覆盖。因此，Git 阻止了这个操作并抛出了这个错误信息。

你有以下几种解决方案：

保存你的本地更改：你可以把这些未被跟踪的文件添加到Git，然后用git stash命令保存这些更改。这样你就可以安全地拉取远程的更改，而不会丢失你的本地更改。如果你已经添加了这些文件到Git，那么你可能需要把这些文件从Git中移除（使用git rm --cached `<file>`），然后再重新添加。
丢弃你的本地更改：如果你确定这些未被跟踪的文件的更改不重要，你可以直接丢弃这些更改。使用 git clean -df 命令可以删除这些文件。
分开操作：你可以在拉取远程更改之前，先把你的本地更改推送到远程仓库。使用 git commit -a 和 git push 可以完成这个操作。这样你的本地更改就会安全地保存在远程仓库，而不会在拉取远程更改时被覆盖。
这是一个可能的流程：

添加所有文件到暂存区

git add .

# 提交所有暂存区的文件

git commit -a -m "Adding local changes"

# 将你的更改推送到远程仓库

git push

# 拉取远程的更改

# 添加所有文件到暂存区

git add .

# 提交所有暂存区的文件

git commit -a -m "Adding local changes"

# 将你的更改推送到远程仓库

git push

# 拉取远程的更改

git pull
这样，你可以安全地拉取远程的更改，而不会丢失你的本地更改。

recursive git 循环克隆子项目
git clone 重命名
git clone xxx.git anothername

TortoiseGit和Git使用教程
https://blog.csdn.net/hjwdz2015/article/details/90487554

git diff bc7e28c568f4af0bd39c26d71de6060c0baf7a5b e9b4f421e1f02d01ca6b4a0e5fee171a42fab5f9

## git跨分支合并

git支持不同分支之间合并代码

## git暂存代码

Git 的暂存操作是通过 git add 命令来完成的。git add 可以将工作区中的文件更改或添加到 Git 的暂存区，以备提交。

下面是一些示例：

暂存所有更改：

bash
git add .
这会将工作区的所有更改（包括新文件）添加到暂存区。
2. 暂存特定文件：

```bash
git add file1.txt file2.txt
```

这会将 file1.txt 和 file2.txt 添加到暂存区。
3. 暂存所有删除的文件：

```bash
git add -u
```

这会将所有已删除的文件添加到暂存区。
4. 暂存所有更改和删除的文件：

```bash
git add -A
```

这会将所有更改（包括新文件）和已删除的文件添加到暂存区。
在暂存了文件之后，你可以使用 git commit 命令将这些更改提交到你的 Git 仓库。例如：

```bash
git commit -m "描述你的更改"
```

请注意，git commit 命令默认不会将工作区中的未暂存更改包含在提交中。如果你试图只提交暂存的文件，而忽略未暂存的更改，你可以使用 git commit -a 命令，但请谨慎使用，以避免误提交非预期的文件。

`git merge origin/master`

`git merge` 命令用于将两个分支合并。当你要将远程分支合并到本地分支时，可以使用以下命令：

1. 首先，切换到本地分支：

   ```
   git checkout <local-branch>
   ```
2. 然后，从远程仓库获取最新的代码：

   ```
   git fetch
   ```

   这个命令会更新本地仓库中对应的远程分支引用，但是不会改变当前分支的状态。
3. 最后，将远程分支合并到本地分支：

   ```
   git merge origin/<remote-branch>
   ```

   这个命令会将本地分支与远程分支合并。注意，`origin/<remote-branch>` 是远程分支的完整名称，其中 `origin` 是远程仓库的名称，`<remote-branch>` 是远程分支的名称。

在执行 `git merge` 命令之前，建议先运行 `git diff` 命令查看本地分支和远程分支之间的差异，以便更好地理解合并的影响。如果合并过程中出现了代码冲突，需要手动解决冲突并提交变更。

需要注意的是，如果你在本地分支中已经有了对应的修改，执行 `git merge` 命令可能会导致代码冲突。在这种情况下，你需要先将本地分支提交变更，然后再执行 `git fetch` 命令获取最新的代码，最后再执行 `git merge` 命令将远程分支合并到本地分支。

`git merge` 命令用于将不同的分支合并到当前分支。在执行 `git merge` 命令时，Git 会将指定的分支的修改合并到当前分支中。

以下是一个简单的 `git merge` 示例，假设你当前在 `main` 分支上，想要将 `feature` 分支的修改合并到 `main` 分支上：

```
git merge feature
```

执行此命令后，Git 将会自动尝试将 `feature` 分支上的修改合并到 `main` 分支上，如果有冲突，则需要手动解决冲突。

如果你想要保留原始分支中的修改，可以使用 `--no-ff` 参数执行非快进合并，例如：

```
git merge --no-ff feature
```

这将会在 `main` 分支上创建一个新的合并提交，保留原始分支和合并分支的修改历史。

如果你想要撤销合并操作，可以使用 `git merge --abort` 命令。

git remote set-url gitremote https://github.com/wimoor-erp/wimoor.git

1. 如果你的GIT设置了多个remote地址，在不同的remote间pull方法为：
   $ git pull <remote_name> <branch_name>
2. 每次都需要输入 remote name 和 branch name 比较麻烦，我们可以将某个remote 设置为默认
   设置方法：
   $ git config branch.master.remote `<remote origin>`
   $ git config branch.master.merge refs/heads/master
3. 也可以直接通过修改git的配置文件进行设置。(工程所在.git目录)
   $ vi .git/config
4. 如果需要对所有的项目都进行设置可以使用 --global 参数，进行设置
   https://blog.csdn.net/Andy_Dou/article/details/84602414

本地main，远程master分支
git push --set-upstream origin main

--set-upstream 远程不存在，在远程创建分支

提示：使用 'master' 作为初始分支的名称。这个默认分支名称可能会更改。要在新仓库中
提示：配置使用初始分支名，并消除这条警告，请执行：
提示：
提示： git config --global init.defaultBranch <名称>
提示：
提示：除了 'master' 之外，通常选定的名字有 'main'、'trunk' 和 'development'。
提示：可以通过以下命令重命名刚创建的分支：
提示：
提示： git branch -m `<name>`

```
git config --global user.email "xxx@qq.com"
git config --global user.name "wdidada"
```

git config user.email "1664884095@qq.com"

```
git config user.email "xxx@qq.com"
git config user.name "WuCheng"
```

```
git config  --global user.email "wdidada@qq.com"
git config  --global user.name "wdidada"
```

```
git config --global user.email "xxx@qq.com"
git config --global user.name "WuCheng"
```

```
git config user.email "xxx@qq.com"
git config user.name "wdidada"
```

git log --author="xxx"

git add -A
git add .
相同点 不同点

### 查看

查看某个人的git提交记录
git log --author="author"

git查看本地有多少个commit没有提交到远程仓库

git status 只能查看到本地当前有多少个提交还未推送，但看不到具体是哪些提交

git log  branch_name  ^origin/branch_name

### git多分支合并

场景a b分支

a分支改变
b分支 改变 提交

a分支 merge b
a分支之前的改动直接提交

testgit 仓库

git revert和reset

git revert 用法
一、初级用法
git revert撤销某次操作，此次操作之前和之后的commit和history都会保留，并且把这次撤销，作为一次最新的提交。
git revert HEAD                  撤销前一次 commit
git revert HEAD^               撤销前前一次 commit
git revert commit_id （比如:fa042ce57ebbe5bb9c8db709f719cec2c58ee7ff）

 git revert是提交一个新的版本，将需要revert的版本的内容再反向修改回去，版本会递增，不影响之前提交的内容.

Tip : 通常情况下，上面这条revert命令会让程序员修改注释，这时候程序员应该标注revert的原因，假设程序员就想使用默认的注释，可以在命令中加上-n或者--no-commit，应用这个参数会让revert 改动只限于程序员的本地仓库，而不自动进行commit，如果程序员想在revert之前进行更多的改动，或者想要revert多个commit。

二、进阶用法
当有多个commit需要撤销，有可能是连续的，或是不连续的，那该怎么操作？

1.连续
git revert -n commit_id_start..commit_id_end
使用该命令可以将提交撤回到commit_id_start的位置

2.不连续
git revert -n commit_id_1
git revert -n commit_id_3
使用该命令可以撤回到commit_id_1和commit_id_3的提交

1.git删除远程分支 git push origin --delete [branch_name]
2.删除本地分支区别 git branch -d 会在删除前检查merge状态(其与上游分支或者与head)。 git b
3.git查看分支: 查看本地分支 git branch 查看远程分支 git branch -r 查看本地和远程分支 git branch -a
4.git删除分支: 删除本地分支 git branch -d 本地分支名 删除远程分支 git push origin --delete [branch_name]

git push origin --delete master
remote: Powered by GITEE.COM [GNK-6.3]
remote: error: By default, deleting the current branch is denied, because the next
remote: 'git clone' won't result in any file checked out, causing confusion.
remote:
remote: You can set 'receive.denyDeleteCurrent' configuration variable to
remote: 'warn' or 'ignore' in the remote repository to allow deleting the
remote: current branch, with or without a warning message.
remote:
remote: To squelch this message, you can set it to 'refuse'.
remote: error: refusing to delete the current branch: refs/heads/master
To gitee.com:edidada/mypagehelper.git
 ! [remote rejected] master (deletion of the current branch prohibited)
error: failed to push some refs to 'gitee.com:edidada/mypagehelper.git'

原因 master是默认分支，不能删除

git branch -d main
error: The branch 'main' is not fully merged.
If you are sure you want to delete it, run 'git branch -D main'.

git reset vs恢复
那我们学到了什么？ 好吧，当我们git reset到先前的提交并推送到远程存储库时，不会发布任何撤消提交的痕迹。 这与git revert形成了鲜明的对比，在git revert中，revert命令本身会创建一个新的提交，并且不会丢失过去的提交历史。 因此，如果您想使用Git 撤消先前的提交 ，则reset是使用而不是还原的正确Git命令。

https://juejin.cn/post/6844904005773213704

远程仓库新建有分支
本地仓库分支已经存在

报错信息

实验计划:

本地仓库A，新建master，提交到远程仓库

从远程仓库复制一份，新建分支dev，提交到远程仓库，本地仓库称为B

仓库A新建dev分支，git pull一下

[如何使用.gitignore忽略Git中的文件和目录](https://blog.csdn.net/Q1761991696/article/details/123572766)

问：IDEA解决git冲突
答：先执行'git add'命令

git 锁分支，不能新提交
多分支合并

本地a分支 直接合并b分支
pull = fetch + merge

git fetch 和git pull 的差别

git fetch 相当于是从远程获取最新到本地，不会自动merge
git fetch orgin master //将远程仓库的master分支下载到本地当前branch中
git log -p master ..origin/master //比较本地的master分支和origin/master分支的差别
git merge origin/master //进行合并
git pull：相当于是从远程获取最新版本并merge到本地
git pull origin master
git pull <远程主机名> <远程分支名>:<本地分支名>

https://www.jianshu.com/p/b00fea3ba207

免密登录 ssh key
gpg

freebsd 免密登录

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

git config  user.name "Wdidada Tom In Dell R630"
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

```shell
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

要删除远程分支，可以使用以下命令：

```bash
git push origin --delete <branch_name>
```

其中，`<branch_name>`是要删除的远程分支的名称。
例如，要删除名为 `feature/branch1`的远程分支，可以运行以下命令：

```bash
git push origin --delete feature/branch1
```

请注意，此命令将从远程仓库中永久删除指定的分支。确保在执行此操作之前，你已经确认了要删除的分支，并且在删除之前进行了必要的备份或合并操作。
