# git权威指南

[git权威指南 豆瓣](https://book.douban.com/subject/6526452/)
Windows电脑上有pdf

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

## 第2篇　Git独奏
#### 第4章　Git 初始化
#### 第5章　Git 暂存区

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
#### 第7章　Git 重置
#### 第8章　Git 检出  
#### 第9章　恢复进度
### 第10章　Git 基本操作
### 第11章　历史穿梭
### 第12章　改变历史
### 第13章　Git 克隆
### 第14章　Git库管理/ 187

## 第3篇　Git和声
### 第15章　Git协议与工作协同/ 200
### 第16章　冲突解决/ 210
### 第17章　Git 里程碑/ 233
### 第18章　Git 分支/ 253
### 第19章　 远程版本库/ 284

### 第20章　补丁文件交互/ 296
## 第4篇　Git协同模型
### 第21章　经典Git协同模型/ 308
### 第22章　Topgit 协同模型/ 314

### 第23章　子模组协同模型/ 336
### 第24章　子树合并/ 347
### 第25章　Android 式多版本库协同/ 356
### 第26章　Git 和 SVN 协同模型/ 378
## 第5篇　搭建Git服务器
### 第27章　使用 HTTP 协议
### 第28章　使用 Git 协议/ 406


### 第29章　使用 SSH 协议/ 409
### 第30章　Gitolite 服务架设/ 413
### 第31章　Gitosis 服务架设/ 441
### 第32章　Gerrit 代码审核服务器/ 452
### 第33章　Git 版本库托管/ 487
## 第6篇　迁移到Git
### 第34章　CVS版本库到Git的迁移/ 492
### 第35章　更多版本控制系统的迁移/ 502


## 第7篇　Git的其他应用
### 第36章　etckeeper
## 第8篇　Git杂谈
### Chap. 40 跨平台操作 Git

跨操作系统
需要实际操作下
目前遇到过commit信息乱码
文件名乱码


git merge
git rebase


