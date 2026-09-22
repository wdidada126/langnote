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
git format-patch -s HEAD~3..HEAD

0001-add-11.1_1.patch

git format-patch <commit_id>

git format-patch -h
usage: git format-patch [<options>] [<since> | <revision-range>]          
                                                                          
    -n, --numbered        use [PATCH n/m] even with a single patch        
    -N, --no-numbered     use [PATCH] even with multiple patches          
    -s, --signoff         add a Signed-off-by trailer                     
    --stdout              print patches to standard out                   
    --cover-letter        generate a cover letter                         
    --numbered-files      use simple number sequence for output file names
    --suffix <sfx>        use <sfx> instead of '.patch'                   
    --start-number <n>    start numbering patches at <n> instead of 1     
    -v, --reroll-count <reroll-count>                                     
                          mark the series as Nth re-roll
    --filename-max-length <n>
                          max length of output filename
    --rfc                 use [RFC PATCH] instead of [PATCH]
    --cover-from-description <cover-from-description-mode>
                          generate parts of a cover letter based on a branch's description
    --subject-prefix <prefix>
                          use [<prefix>] instead of [PATCH]
    -o, --output-directory <dir>
                          store resulting files in <dir>
    -k, --keep-subject    don't strip/add [PATCH]
    --no-binary           don't output binary diffs
    --zero-commit         output all-zero hash in From header
    --ignore-if-in-upstream
                          don't include a patch matching a commit upstream
    -p, --no-stat         show patch format instead of default (patch + stat)

Messaging
    --add-header <header> add email header
    --to <email>          add To: header
    --cc <email>          add Cc: header
    --from[=<ident>]      set From address to <ident> (or committer ident if absent)
    --in-reply-to <message-id>
                          make first mail a reply to <message-id>
    --attach[=<boundary>] attach the patch
    --inline[=<boundary>] inline the patch
    --thread[=<style>]    enable message threading, styles: shallow, deep
    --signature <signature>
                          add a signature
    --base <base-commit>  add prerequisite tree info to the patch series
    --signature-file <file>
                          add a signature from a file
    -q, --quiet           don't print the patch filenames
    --progress            show progress while generating patches
    --interdiff <rev>     show changes against <rev> in cover letter or single patch
    --range-diff <refspec>
                          show changes against <refspec> in cover letter or single patch
    --creation-factor <n> percentage by which creation is weighted
    --force-in-body-from  show in-body From: even if identical to the e-mail header
要在 Git 中合并 patch 文件，您可以使用 `git apply` 命令。以下是在命令行中合并 patch 文件的示例：
1. 使用 `git apply` 命令合并 patch 文件：
```
git apply patchfile.patch
```
其中，`patchfile.patch` 是您要合并的 patch 文件的文件名。请确保在运行该命令之前，您已经位于正确的 Git 仓库目录下。
2. 如果您希望将合并后的更改直接提交到 Git 仓库，可以使用 `git apply` 命令的 `--index` 或 `-i` 选项：
```
git apply --index patchfile.patch
```
或
```
git apply -i patchfile.patch
```
这将在合并 patch 文件后将更改添加到暂存区，以便您可以在之后执行提交操作。
请注意，`git apply` 命令仅将 patch 文件中的更改应用到您的工作目录中，并不会在 Git 中创建新的提交。如果您想要将合并后的更改提交到 Git 仓库，您需要手动执行 `git commit` 命令。
如果您想要在应用 patch 文件之前预览更改，可以使用 `git apply` 命令的 `--check` 选项。这会检查 patch 文件是否能够成功应用，但不会实际应用更改。
```
git apply --check patchfile.patch
```
在 Git 中，`git apply` 和 `git am` 是两个用于应用补丁的命令，它们之间有一些区别。
1. `git apply`：
   - `git apply` 命令用于将补丁文件应用到当前工作目录，但不会创建新的提交。
   - 它可以应用普通的 diff 格式补丁文件（如 `.patch` 或 `.diff` 文件）。
   - `git apply` 可以通过使用 `--check` 选项进行预览，以验证补丁文件能否成功应用。
   - 使用 `git apply` 时，您需要手动执行 `git add` 命令将更改添加到暂存区，并使用 `git commit` 命令创建新的提交。
2. `git am`：
   - `git am` 命令用于将补丁文件应用到当前工作目录，并自动创建新的提交。
   - 它可以应用邮件格式的补丁文件（如 `.patch` 或 `.mbox` 文件），这些文件通常由 `git format-patch` 命令生成。
   - `git am` 会解析补丁文件中的作者、提交日期等信息，并自动创建提交记录。
   - `git am` 还支持在多个补丁文件中进行批量应用。
   - 使用 `git am` 时，您可以使用 `--signoff` 选项将补丁作者的签名信息添加到提交中。
总结一下：
- `git apply` 用于将补丁文件应用到工作目录，不创建新的提交，需要手动执行 `git add` 和 `git commit`。
- `git am` 用于将补丁文件应用到工作目录，自动创建新的提交，支持邮件格式补丁文件。

根据您的需求和补丁文件的格式，选择适当的命令进行补丁应用。

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
~/.ssh/config
```
host bj
  user git
  hostname bj.ossxp.com
  port 22
  identityfile ~/.ssh/jiangxin
```

ssh bj
git clone bj:/path/to/repos/myrepos.git

实际操作例子

ucloud服务器
git remote remove githubsandisks
git remote add githubsandisks git@github-sandisks:sandisks/myqt6app.git
git fetch githubsandisks

时序图
githubsandisks -> git@github-sandisks:sandisks/myqt6app.git -> 读取~/.ssh/config或者/etc/ssh/config文件，替换Host，github-sandisks替换成github.com

git权威指南 第29章

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



## 跨年摘录（2020–2026 日常笔记聚合，2026-09-23 整理）

### 2024-06
> 2. 《Linux性能优化权威指南》

### 2024-07
> 2. 《Linux性能优化权威指南》

