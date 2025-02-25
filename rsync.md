# rsync
## 安装
choco安装

## idea windows同步jar包问题
rsync_rename.sh

存在的问题，同步maven仓库的jar包到目标主机，文件名，文件路径全错了

https://youtrack.jetbrains.com/issue/IDEA-299338/Remote-deployment-with-rsync-doesnt-preserve-folder-structure-uses-backslashes-in-file-names-from-Windows


du -sh / 

rsync -av --files-from=filelists.txt source_folder destination_folder

D:\dev_tools\cwrsync_6.2.0_x64_free\bin\rsync.exe -zar -v -e "D:\dev_tools\cwrsync_6.2.0_x64_free\bin\ssh.exe -p 22 " --files-from=fileList.txt --exclude=*.pyc --exclude=*.pyo --exclude=*.rbc --exclude=*.yarb --exclude=*~ --exclude=.DS_Store --exclude=.git --exclude=.hg --exclude=.mypy_cache --exclude=.pytest_cache --exclude=.ruff_cache --exclude=.svn --exclude=CVS --exclude=__pycache__ --exclude=_svn --exclude=vssver.scc --exclude=vssver2.scc --exclude=.idea --delete 201904 wdidada@106.75.209.6:/home/wdidada/springbootmybatis/bmmWU2Y1fP


网上的方案
把本地的临时文件，rsync
fileList.txt
中的\ 改成 /

## doc manul

https://rsync.samba.org/documentation.html

https://rsync.samba.org/examples.html

## 官网
https://rsync.samba.org/

## 源代码编译
c代码

https://github.com/WayneD/rsync/issues?q=is%3Aissue
https://download.samba.org/pub/rsync/src/rsync-3.2.7.tar.gz

wget --no-check-certificate https://download.samba.org/pub/rsync/src/rsync-3.2.7.tar.gz -O rsync-3.2.7.tar.gz
tar -zxvf rsync-3.2.7.tar.gz
cd rsync-3.2.7
sudo update
sudo apt install -y gcc g++ gawk autoconf automake python3-cmarkgfm acl libacl1-dev attr libattr1-dev libxxhash-dev libzstd-dev liblz4-dev libssl-dev
./configure
make
sudo make install

## 版本
Rsync version 3.2.7 released October 20th, 2022

## clion rsync

D:\dev_tools\cwrsync_6.2.0_x64_free\bin\rsync.exe
D:\dev_tools\cwrsync_6.2.0_x64_free\bin\ssh.exe

