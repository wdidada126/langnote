#  brew

brew --version
Homebrew >=2.5.0 (shallow or no git repository)
Homebrew/homebrew-core (git revision ddf4b01b780; last commit 2025-03-14)
Homebrew/homebrew-cask (git revision fcd1cb79c80; last commit 2025-03-14)

`Homebrew/homebrew-cask` 和 `Homebrew/homebrew-core` 都是 Homebrew（一款 macOS 和 Linux 系统上的软件包管理器）的重要组成部分，它们分别承担着不同的作用：

### Homebrew/homebrew-core
- 主要作用：它是 Homebrew 的核心软件仓库，提供了大量的开源命令行工具和开发库。这些软件包大多是基于源码编译安装的，涵盖了各种编程语言的解释器和编译器（如 Python、Ruby、GCC 等）、数据库管理系统（如 MySQL、PostgreSQL 等）、网络工具（如 wget、curl 等）以及其他许多在开发和系统管理中常用的工具。
- 示例：当你在终端中使用 `brew install` 命令安装一些基础的开发工具时，默认就是从 `Homebrew/homebrew-core` 这个仓库中下载并安装的。例如，要安装 `git` 这个版本控制工具，只需运行 `brew install git`，Homebrew 就会从 `Homebrew/homebrew-core` 中获取 `git` 的安装脚本和相关依赖，然后进行编译和安装。

### Homebrew/homebrew-cask
- 主要作用：它主要用于管理 macOS 上的图形化应用程序（GUI 应用）。与 `Homebrew/homebrew-core` 不同，`Homebrew/homebrew-cask` 安装的应用通常是已经编译好的二进制文件，安装过程更加便捷，无需用户手动从应用官网下载 `.dmg` 或 `.pkg` 文件，然后再进行安装操作。此外，`Homebrew/homebrew-cask` 还支持安装一些系统级别的字体、驱动程序等。
- 示例：如果你想安装 Google Chrome 浏览器，只需在终端中运行 `brew install --cask google-chrome`，Homebrew 就会从 `Homebrew/homebrew-cask` 仓库中下载 Chrome 的安装包，并自动完成安装过程。

### 总结
`Homebrew/homebrew-core` 侧重于提供命令行工具和开发库，适合开发者和系统管理员在命令行环境下进行软件开发和系统配置；而 `Homebrew/homebrew-cask` 则专注于图形化应用程序的管理，让用户能够更方便地安装和更新各种 macOS 应用。两者结合使用，使得 Homebrew 成为了一个功能强大且全面的软件包管理解决方案。 

## macos 12.7
https://github.com/Homebrew/brew/releases?page=14
3.6.19

export HOMEBREW_GITHUB_API_TOKEN=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

## some
brew -h
Example usage:
  brew search TEXT|/REGEX/
  brew info [FORMULA|CASK...]
  brew install FORMULA|CASK...
  brew update
  brew upgrade [FORMULA|CASK...]
  brew uninstall FORMULA|CASK...
  brew list [FORMULA|CASK...]

Troubleshooting:
  brew config
  brew doctor
  brew install --verbose --debug FORMULA|CASK

Contributing:
  brew create URL [--no-fetch]
  brew edit [FORMULA|CASK...]

Further help:
  brew commands
  brew help [COMMAND]
  man brew
  https://docs.brew.sh


brew update
brew --prefix openssl

conan install libmysql报错，需要
brew unlink boost

brew install boost
Warning: boost 1.80.0 is already installed, it's just not linked.
To link this version, run:
  brew link boost
ibqodeMacBook-Pro:cpp-5th_ZhengLi ibqo$ brew link boost
Linking /usr/local/Cellar/boost/1.80.0... 186 symlinks created.


## 官网

https://brew.sh/

## install

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## brew设置国内镜像

在Mac上使用brew（Homebrew）时，由于网络问题，可能会遇到下载速度慢或下载失败的情况。为了改善这种情况，可以将brew的源切换为国内镜像源。以下是将brew设置为国内镜像的步骤，以阿里云镜像为例：

1. 替换brew.git的源
打开终端（Terminal），执行以下命令来替换brew的源：

bash
cd "$(brew --repo)"  
git remote set-url origin https://mirrors.aliyun.com/homebrew/brew.git
这会将brew的远程仓库地址更改为阿里云的镜像地址。

2. 替换homebrew-core.git的源
brew的公式（formula）库主要存储在homebrew-core仓库中，因此也需要将其源替换为国内镜像。执行以下命令：

bash
cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"  
git remote set-url origin https://mirrors.aliyun.com/homebrew-core.git
这会将homebrew-core的远程仓库地址更改为阿里云的镜像地址。

3. 替换其他可选的仓库（如有需要）
除了brew.git和homebrew-core.git之外，brew还可能包含其他可选的仓库，如homebrew-cask（用于安装和管理macOS应用程序的二进制分发版）、homebrew-bottles（包含预编译的二进制包）等。如果你需要使用这些仓库，并且它们也提供了国内镜像，可以类似地替换它们的源。

4. 刷新brew配置
完成上述步骤后，执行以下命令来刷新brew的配置并更新包索引：

```bash
brew update
```
这将从新的镜像源下载最新的包索引，并准备后续的安装操作。

5. 验证配置
为了确认配置已成功更改为国内镜像源，你可以执行以下命令来查看brew的配置信息：

bash
brew config
在输出信息中，你会看到HOMEBREW_REPOSITORY、HOMEBREW_CORE_GIT_REMOTE等字段的值已经更改为对应的国内镜像地址。

注意事项
不同的国内镜像源可能有不同的稳定性和更新速度，你可以根据自己的需要选择合适的镜像源。
如果你在后续使用过程中遇到问题，可以尝试切换回官方的源或尝试其他可用的国内镜像源。
替换源的操作可能需要一定的网络权限，确保你的终端会话具有足够的权限来执行这些命令。
以上步骤适用于大多数Mac用户，但在具体操作时可能会因个人环境的不同而有所差异。如果遇到问题，可以参考Homebrew的官方文档或在相关社区中寻求帮助。


https://blog.csdn.net/weixin_34399060/article/details/91923873

brew 安装devel相关的库

opencv

brew install opencv

## leveldb

```
Already downloaded: /Users/runner/Library/Caches/Homebrew/downloads/6368c90aab2f09b471f779889422bdd5bda353789dcfae8ac5f624a0333c463a--gperftools-2.15.bottle_manifest.json
==> Pouring gperftools--2.15.arm64_sonoma.bottle.tar.gz
  /opt/homebrew/Cellar/gperftools/2.15: 102 files, 4.5MB
==> Installing leveldb dependency: snappy
==> Downloading https://ghcr.io/v2/homebrew/core/snappy/manifests/1.2.1
Already downloaded: /Users/runner/Library/Caches/Homebrew/downloads/b2e6bfcdbddf1d451a8dbbb6fc3c44a267b753ac1a889dbb0b9159bf31dacdd5--snappy-1.2.1.bottle_manifest.json
==> Pouring snappy--1.2.1.arm64_sonoma.bottle.tar.gz
  /opt/homebrew/Cellar/snappy/1.2.1: 19 files, 172.2KB
==> Installing leveldb
==> Pouring leveldb--1.23_1.arm64_sonoma.bottle.tar.gz
  /opt/homebrew/Cellar/leveldb/1.23_1: 32 files, 837.4KB
```


==> Installing dependencies for leveldb: gperftools
==> Installing leveldb dependency: gperftools
==> Pouring gperftools--2.10.monterey.bottle.tar.gz
  /usr/local/Cellar/gperftools/2.10: 104 files, 4.9MB
==> Installing leveldb
==> Pouring leveldb--1.23.monterey.bottle.tar.gz
  /usr/local/Cellar/leveldb/1.23: 31 files, 876.4KB
==> Running `brew cleanup leveldb`...

