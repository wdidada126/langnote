# ubuntu

https://mirrors.aliyun.com/ubuntu-releases/24.04/

wget -O ubuntu-24.04-desktop-amd64.iso https://mirrors.aliyun.com/ubuntu-releases/24.04/ubuntu-24.04-desktop-amd64.iso


wget -O ubuntu-24.04-desktop-amd64.iso https://releases.ubuntu.com/24.04/ubuntu-24.04-desktop-amd64.iso

dpkg -L libmysqlclient-dev | grep ".so"

在Ubuntu中，你可以通过以下方法来查询服务端有哪些库：

首先，你可以使用`apt-get update`命令扫描每一个软件源服务器，并为该服务器所具有的软件包资源建立索引文件。这些索引文件会被存放在本地的`/var/lib/apt/lists/`目录中。此外，你也可以通过查看`/etc/apt/sources.list`文件来查看当前系统中所有的镜像源列表，其中以"deb"开头的行指定了软件包的下载地址。

另外，可以使用`apt search`和`apt show`命令获取Ubuntu中可用版本、依赖项、存储库以及有关软件包的其他重要信息。例如，如果你想要知道某个软件包是否可以通过apt软件包管理器安装，或者想确认Ubuntu存储库提供的软件包是否是最新的，可以使用这两个命令进行查找。

最后，如果你需要查询某个具体软件的所有版本或者所有来源，可以使用`apt-cache madison`和`apt-cache policy`命令。前者可以列出软件的所有来源，后者则可以列出软件的所有版本。

sudo apt update 是一个用于管理 Debian 和 Ubuntu 系统软件包的命令。当你运行这个命令时，它会执行以下操作：

连接软件源：sudo apt update 命令会连接到配置的软件源，从中获取软件包信息和更新。
更新软件包列表：在连接到软件源后，该命令会更新本地软件包列表。它会检查每个软件包的版本信息和依赖关系，并将这些信息存储在本地。
检查可用更新：一旦软件包列表更新完成，该命令会检查是否有可用的软件包更新。它会比较本地软件包版本和软件源中的最新版本，确定哪些软件包需要更新。
通过运行 sudo apt update 命令，可以确保系统中的软件包列表是最新的，以便后续的软件包管理。这个命令是管理软件包和保持系统更新的重要步骤。
在 Linux 系统中，sudo apt update 命令用于更新本地软件包列表，它会检查每个软件包的版本信息和依赖关系，并将这些信息存储在本地。这些本地软件包列表通常存储在 /var/lib/apt/lists/ 文件夹下。具体来说，当你运行 sudo apt update 命令时，它会从配置的软件源中获取最新的软件包信息，并将其保存在 /var/lib/apt/lists/ 文件夹下的各个文件中。这些文件包含了软件包的名称、版本号、依赖关系等信息，用于后续的软件包安装、升级和删除操作。因此，当你需要管理软件包时，系统会从这些本地软件包列表中检索信息，以便进行相应的操作。

sudo apt upgrade 是一个用于更新已安装软件包的命令。当你运行这个命令时，它会执行以下操作：
检查可用更新：sudo apt upgrade 命令会检查已安装软件包的版本，并将其与软件源中的最新版本进行比较。它确定哪些软件包有可用的更新。
安装软件包更新：一旦确定了可用的软件包更新，该命令会下载并安装这些更新。它会自动解决软件包之间的依赖关系，并确保更新的软件包成功安装。
通过运行 sudo apt upgrade 命令，可以更新系统中已安装的软件包，以获取最新的功能和修复的漏洞。这有助于提高系统的安全性、稳定性和性能。因此，保持系统更新是非常重要的，以防止安全漏洞和系统不稳定。

Ubuntu官方仓库可能不提供旧版本


https://www.vpsdp.net/dev-sda1-clean-files-blocks/

[Wlp6s0: failed to remove key (1, ff:ff:ff:ff:ff:ff) from hardware (-22)](https://askubuntu.com/questions/967441/17-1-wlp6s0-failed-to-remove-key-1-ffffffffffff-from-hardware-22)

https://unix.stackexchange.com/questions/422254/kernel-wlp2s0-failed-to-remove-key-1-ffffffffffff-from-hardware-22

https://askubuntu.com/questions/967441/17-1-wlp6s0-failed-to-remove-key-1-ffffffffffff-from-hardware-22

如果您正在运行Ubuntu，请尽量使用像 aptitude 或者 synaptic 一样的软件包管理器，代替人工手动操作的方式从这个网页下载并安装软件包。

## ubuntu22

```shell
sudo systemctl enable ssh
Synchronizing state of ssh.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable ssh
```
Ubuntu 22.04 的 SSH 服务名称为 ssh.service，而非 sshd.service。
