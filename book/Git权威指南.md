# git权威指南

git fetch
git merge

rebase

git查看当前冲突的文件列表

git 显示大小超过50M的文件

[修改已经提交的commit用户名](https://help.github.com/en/articles/changing-author-info)


修改git commit用户名密码先失败，后成功

[git doc](https://git-scm.com/docs/git-rev-parse)

git stash
git stash pop


git grep

Windows

.gitconfig

Unix like

/etc/gitconfig

git config --global alias.st "-p status"
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cf config
git config --global alias.fc fetch
git config --global alias.ci "commit -s"

git rev-parse --git-dir

查看.git文件

git rev-parse --show-toplevel 

git config --unset --global user.name

git commit --amend --author "edidada <sandisks555@gmail.com>"
git filter-branch --commit-filter "GIT_AUTHOR_NAME='edidada'; GIT_AUTHOR_EMAIL='sandisks555@gmail.com'"
git filter-branch --commit-filter "GIT_AUTHOR_NAME='edidada'; GIT_AUTHOR_EMAIL='1664884095@qq.com'"
git filter-branch --commit-filter "GIT_AUTHOR_NAME='wucheneg'; GIT_AUTHOR_EMAIL='wucheng-it@xxxx.com.cn'"


#### Chap. 5

暂存区
git ls-files

40位的SHA1哈希值格式的ID

git diff单个文件？
git diff commit_id1 commit_id2 -- somefile
8f501d03faef1e8f114656bdde05abec46d8539c 83c40503061f8588a30ec0306eaebb9add5015f7 

工作区和暂存区比较
git diff

暂存区和HEAD比较

git diff --cached

工作区和HEAD比较

git diff HEAD

### Chap. 40

跨操作系统
需要实际操作下
目前遇到过commit信息乱码
文件名乱码


git merge
git rebase


