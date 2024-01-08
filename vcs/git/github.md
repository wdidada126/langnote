# github

## 2fa
当让 GitHub 告诉我无法获取一次性密码（TOTP）的时候可以使用 recovery code 进行恢复，然而理想很丰满现实很骨感，这种一年不用一次的 recovery code 等你真用的时候真的找得到吗？
那 GitHub 为什么不提供手机验证码呢？
查看了 GitHub 的 F2A 文档，原来是在国内不支持
github-edidada-recovery-codes.txt

https://zhuanlan.zhihu.com/p/671682341

## github cli

gh repo clone edidada/odb
gh auth login

## action
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
