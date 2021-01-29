# pull

[git pull pr](https://www.centos.bz/2018/03/git-%E5%87%BA%E7%8E%B0-fatal-refusing-to-merge-unrelated-histories-%E9%94%99%E8%AF%AF/)

https://help.github.com/en/articles/removing-files-from-a-repositorys-history

## 20190223 合并同名Repo遇到的问题

报错信息：
```shell

From github.com:edidada/LangNote
 * [new branch]      master     -> origin/master
There is no tracking information for the current branch.
Please specify which branch you want to merge with.
See git-pull(1) for details.

    git pull <remote> <branch>

If you wish to set tracking information for this branch you can do so with:

    git branch --set-upstream-to=origin/<branch> master

```


[Git新建本地分支与远程分支关联问题](https://blog.csdn.net/hshl1214/article/details/51074206)

解决：
```shell

git branch --set-upstream-to=origin/master master

```

远程仓库新增文件，本地仓库直接提交报错：
```shell

git push origin master --tags
To github.com:edidada/LangNote.git
 ! [rejected]        master -> master (fetch first)
error: failed to push some refs to 'git@github.com:edidada/LangNote.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes
hint: (e.g., 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.

```



解决：
```shell

git pull

```

```shell

fatal: refusing to merge unrelated histories

```

