# github


https://www.githubstatus.com/history

rust.yml

默认分支无法通过
git push -d origin main来删除

git branch -m cpp11 <BRANCH>
git fetch origin
git branch -u origin/<BRANCH> <BRANCH>
git remote set-head origin -a


在 GitHub 上设置默认分支（default branch）是一个简单的过程。以下是详细的步骤：
1. 登录到你的 GitHub 账户。
2. 导航到你想要更改默认分支的仓库。
3. 在仓库主页，点击顶部的 "Settings" 标签。
4. 在左侧菜单中，点击 "Branches"。
5. 在 "Default branch" 部分，你会看到一个下拉菜单，显示当前的默认分支。
6. 点击这个下拉菜单，选择你想要设置为新的默认分支的分支名称。
7. 点击 "Update" 按钮。
8. GitHub 会要求你确认这个更改。仔细阅读警告信息，因为更改默认分支可能会影响依赖于旧默认分支的工作流程。
9. 如果你确定要进行更改，点击 "I understand, update the default branch."

完成这些步骤后，你选择的分支就会成为新的默认分支。

注意事项：

- 更改默认分支会影响新的 pull requests 和代码比较。
- 它不会改变你的本地仓库设置。你可能需要在本地进行一些额外的操作，比如更新远程跟踪分支。
- 如果你的仓库被其他项目 fork，这个更改可能会影响那些 fork。

如果你在本地也想更新默认分支，可以使用以下 Git 命令：

```
git branch -m old_branch new_branch
git fetch origin
git branch -u origin/new_branch new_branch
git remote set-head origin -a
```

这里的 `old_branch` 是原来的默认分支名，`new_branch` 是新的默认分支名。

如果你需要更多帮助或有其他问题，请随时问我。


ucloud服务器，同时配置两个github账户ssh免密码通信复制数据，只能注释掉一个，使用另一个

在同一台主机上配置两个 GitHub 密钥对可以实现通过不同的密钥对进行 `git clone`。要做到这一点，您可以使用 SSH 配置文件（`~/.ssh/config`）来指定不同的密钥对与不同的主机关联。

以下是一个示例 `~/.ssh/config` 文件的配置：

```plaintext
# 默认的 SSH 配置
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa

# 第二个密钥对的 SSH 配置
Host github-edidada
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa_second
```

在上面的配置中，我们使用了两个不同的 Host 条目。第一个 Host 条目是默认的配置，使用默认的密钥对文件 `~/.ssh/id_rsa`。第二个 Host 条目是针对第二个密钥对的配置，使用密钥对文件 `~/.ssh/id_rsa_second`。

现在，您可以使用 `git clone` 命令时，通过指定不同的远程主机别名来选择使用不同的密钥对。
例如，使用第一个密钥对进行克隆：
```shell
git clone git@github.com:username/repo.git
```
使用第二个密钥对进行克隆：
```shell
git clone git@github-second:username/repo.git
```
通过在 `git clone` 命令中指定不同的远程主机别名，可以选择使用不同的密钥对进行身份验证。
请确保将 `username/repo.git` 替换为实际的 GitHub 用户名和存储库名称。
这样，您就可以在同一台主机上使用不同的 GitHub 密钥对进行 `git clone` 操作了。


ucloud服务器
git remote remove githubsandisks
git remote add githubsandisks git@github-sandisks:sandisks/myqt6app.git
git fetch githubsandisks

时序图
githubsandisks -> git@github-sandisks:sandisks/myqt6app.git -> 读取~/.ssh/config或者/etc/ssh/config文件，替换Host，github-sandisks替换成github.com

git权威指南 第29章

edidada555@gmail.com https方式使用的应用密码
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

## 2fa
当让 GitHub 告诉我无法获取一次性密码（TOTP）的时候可以使用 recovery code 进行恢复，然而理想很丰满现实很骨感，这种一年不用一次的 recovery code 等你真用的时候真的找得到吗？
那 GitHub 为什么不提供手机验证码呢？
查看了 GitHub 的 F2A 文档，原来是在国内不支持
github-edidada-recovery-codes.txt
github-recovery-codes_sandisks.txt

https://zhuanlan.zhihu.com/p/671682341

## github cli

gh repo clone edidada/odb
gh auth login

## action
不支持java文件是gbk，必须是UTF8
Error:  COMPILATION ERROR : 
[INFO] -------------------------------------------------------------
Error:  /home/runner/work/BusTub/BusTub/src/main/java/run/yuyang/db/storage/page/HashTableHeaderPage.java:[59,41] unmappable character for encoding UTF8
Error:  /home/runner/work/BusTub/BusTub/src/main/java/run/yuyang/db/storage/page/HashTableHeaderPage.java:[59,42] unmappable character for encoding UTF8
Error:  /home/runner/work/BusTub/BusTub/src/main/java/run/yuyang/db/storage/page/HashTableHeaderPage.java:[59,43] unmappable character for encoding UTF8
Error:  /home/runner/work/BusTub/BusTub/src/main/java/run/yuyang/db/storage/page/HashTableHeaderPage.java:[59,45] unmappable character for encoding UTF8

### macos
#### c c++
macos.md

### ubuntu 24

```shell
/usr/bin/java
openjdk version "17.0.16" 2025-07-15
OpenJDK Runtime Environment Temurin-17.0.16+8 (build 17.0.16+8)
OpenJDK 64-Bit Server VM Temurin-17.0.16+8 (build 17.0.16+8, mixed mode, sharing)
/usr/bin/mvn
Apache Maven 3.9.11 (3e54c93a704957b63ee3494413a2b544fd3d825b)
Maven home: /usr/share/apache-maven-3.9.11
Java version: 17.0.16, vendor: Eclipse Adoptium, runtime: /usr/lib/jvm/temurin-17-jdk-amd64
Default locale: en, platform encoding: UTF-8
OS name: "linux", version: "6.11.0-1018-azure", arch: "amd64", family: "unix"
```

### doc

```shell
conanvcvars.bat: Activating environment Visual Studio 17 - amd64 - winsdk_version=None - vcvars_ver=14.3
[ERROR:vcvars.bat] Toolset directory for version '14.3' was not found.
[ERROR:VsDevCmd.bat] *** VsDevCmd.bat encountered errors. Environment may be incomplete and/or incorrect. ***
[ERROR:VsDevCmd.bat] In an uninitialized command prompt, please 'set VSCMD_DEBUG=[value]' and then re-run
[ERROR:VsDevCmd.bat] vsdevcmd.bat [args] for additional details.
[ERROR:VsDevCmd.bat] Where [value] is:
[ERROR:VsDevCmd.bat]    1 : basic debug logging
[ERROR:VsDevCmd.bat]    2 : detailed debug logging
[ERROR:VsDevCmd.bat]    3 : trace level logging. Redirection of output to a file when using this level is recommended.
[ERROR:VsDevCmd.bat] Example: set VSCMD_DEBUG=3
[ERROR:VsDevCmd.bat]          vsdevcmd.bat > vsdevcmd.trace.txt 2>&1
```
解决方案

```shell
      - name: Setup MSVC with vswhere
        shell: cmd
        run: |
          SET VSWhere="C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe"
          FOR /F "tokens=*" %%i IN ('%VSWhere% -latest -property installationPath') DO SET VSInstallDir=%%i
          call "%VSInstallDir%\VC\Auxiliary\Build\vcvars64.bat"
          echo Visual Studio environment activated for x64
```

### 可选的操作系统
Available GitHub-hosted runner types are:

ubuntu-latest, ubuntu-22.04, ubuntu-20.04
windows-latest, windows-2022, windows-2019
macos-latest, macos-12, macos-11

https://docs.github.com/zh/actions

cmake默认版本，最新版
3.28

https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#choosing-github-hosted-runners
ubuntu-latest, ubuntu-22.04, ubuntu-20.04
windows-latest, windows-2022, windows-2019
macos-latest, macos-12, macos-11
https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idruns-on


Tests run: 12, Failures: 0, Errors: 0, Skipped: 0
```
[INFO] 
[INFO] --- maven-jar-plugin:2.4:jar (default-jar) @ SkipList ---
[INFO] 
[INFO] --- maven-install-plugin:2.4:install (default-install) @ SkipList ---
[INFO] Installing D:\git\github\SkipList2\target\SkipList-1.0-SNAPSHOT.jar to D:\mavenrepository\201904\com\github\mottox\SkipList\1.0-SNAPSHOT\SkipList-1.0-SNAPSHOT.jar
[INFO] Installing D:\git\github\SkipList2\pom.xml to D:\mavenrepository\201904\com\github\mottox\SkipList\1.0-SNAPSHOT\SkipList-1.0-SNAPSHOT.pom
[INFO] 
[INFO] --- maven-deploy-plugin:2.7:deploy (default-deploy) @ SkipList ---
Downloading from github: https://maven.pkg.github.com/edidada/SkipList/com/github/mottox/SkipList/1.0-SNAPSHOT/maven-metadata.xml
Uploading to github: https://maven.pkg.github.com/edidada/SkipList/com/github/mottox/SkipList/1.0-SNAPSHOT/SkipList-1.0-20231222.115208-1.jar
Uploading to github: https://maven.pkg.github.com/edidada/SkipList/com/github/mottox/SkipList/1.0-SNAPSHOT/SkipList-1.0-20231222.115208-1.pom
[IJ]-1-MojoFailed-[IJ]-source=LIFECYCLE-[IJ]-goal=deploy-[IJ]-id=com.github.mottox:SkipList:jar:1.0-SNAPSHOT-[IJ]-error=Failed to transfer file https://maven.pkg.github.com/edidada/SkipList/com/github/mottox/SkipList/1.0-SNAPSHOT/SkipList-1.0-20231222.115208-1.jar with status code 422
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  16.265 s
[INFO] Finished at: 2023-12-22T19:52:10+08:00
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-deploy-plugin:2.7:deploy (default-deploy) on project SkipList: Failed to deploy artifacts: Could not transfer artifact com.github.mottox:SkipList:jar:1.0-20231222.115208-1 from/to github (https://maven.pkg.github.com/edidada/SkipList): Failed to transfer file https://maven.pkg.github.com/edidada/SkipList/com/github/mottox/SkipList/1.0-SNAPSHOT/SkipList-1.0-20231222.115208-1.jar with status code 422 -> [Help 1]
```
别人的项目

github topic

![github_topic](./imgs/github_topic.jpg)

一、打开IPAddress.com网站，查询下面3个网址对应的IP地址
1. github.com
2. assets-cdn.github.com
3. github.global.ssl.fastly.net

改本地hosts

ipconfig /flushdns

[GitHub 私人private仓库添加成员（协作者Collaborators）](https://blog.csdn.net/chenbetter1996/article/details/82871518)

## github国内下载镜像代理地址
https://kgithub.com/apache/rocketmq.git
