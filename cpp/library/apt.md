# apt


```shell
apt-cache showpkg libcurl4-openssl-dev
Package: libcurl4-openssl-dev
Versions:
7.68.0-1ubuntu2.22 (/var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_focal-updates_main_binary-amd64_Packages) (/var/lib/apt/lists/security.ubuntu.com_ubuntu_dists_focal-security_main_binary-amd64_Packages) (/var/lib/dpkg/status)
 Description Language:
                 File: /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_focal_main_binary-amd64_Packages
                  MD5: 133120dd689c1a9785ccd7cd427dd344
 Description Language: en
                 File: /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_focal_main_i18n_Translation-en
                  MD5: 133120dd689c1a9785ccd7cd427dd344
 Description Language:
                 File: /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_focal-updates_main_binary-amd64_Packages
                  MD5: 133120dd689c1a9785ccd7cd427dd344

7.68.0-1ubuntu2 (/var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_focal_main_binary-amd64_Packages)
 Description Language:
                 File: /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_focal_main_binary-amd64_Packages
                  MD5: 133120dd689c1a9785ccd7cd427dd344
 Description Language: en
                 File: /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_focal_main_i18n_Translation-en
                  MD5: 133120dd689c1a9785ccd7cd427dd344
 Description Language:
                 File: /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_focal-updates_main_binary-amd64_Packages
                  MD5: 133120dd689c1a9785ccd7cd427dd344


Reverse Depends:
  libzypp-dev,libcurl4-openssl-dev 7.19.4
  libcurl4-nss-dev,libcurl4-openssl-dev
  libcurl4-gnutls-dev,libcurl4-openssl-dev
  libcurl4-doc,libcurl4-openssl-dev 7.30.0-2
  libcurl4-doc,libcurl4-openssl-dev 7.30.0-2
  libcurl4-doc,libcurl4-openssl-dev 7.30.0-2
  libxmltooling-dev,libcurl4-openssl-dev
  libleatherman-dev,libcurl4-openssl-dev
  libjsonrpccpp-dev,libcurl4-openssl-dev
  libignition-fuel-tools1-dev,libcurl4-openssl-dev
  libghc-curl-dev,libcurl4-openssl-dev
  libgazebo9-dev,libcurl4-openssl-dev
  janus-dev,libcurl4-openssl-dev
  diaspora-installer,libcurl4-openssl-dev
  libcurl4-nss-dev,libcurl4-openssl-dev
  libcurl4-gnutls-dev,libcurl4-openssl-dev
  libcurl4-doc,libcurl4-openssl-dev 7.30.0-2
Dependencies:
7.68.0-1ubuntu2.22 - libcurl4 (5 7.68.0-1ubuntu2.22) libcurl4-gnutls-dev (0 (null)) libcurl4-nss-dev (0 (null)) libssl-dev (3 1.1) libssl1.0-dev (0 (null)) libcurl4-doc (0 (null)) libidn11-dev (0 (null)) libkrb5-dev (0 (null)) libldap2-dev (0 (null)) librtmp-dev (0 (null)) libssh2-1-dev (0 (null)) libssl-dev (2 1.1) pkg-config (0 (null)) zlib1g-dev (0 (null))
7.68.0-1ubuntu2 - libcurl4 (5 7.68.0-1ubuntu2) libcurl4-gnutls-dev (0 (null)) libcurl4-nss-dev (0 (null)) libssl-dev (3 1.1) libssl1.0-dev (0 (null)) libcurl4-doc (0 (null)) libidn11-dev (0 (null)) libkrb5-dev (0 (null)) libldap2-dev (0 (null)) librtmp-dev (0 (null)) libssh2-1-dev (0 (null)) libssl-dev (2 1.1) pkg-config (0 (null)) zlib1g-dev (0 (null))
Provides:
7.68.0-1ubuntu2.22 - libcurl4-dev (= ) libcurl3-openssl-dev (= ) libcurl3-dev (= ) libcurl-ssl-dev (= ) libcurl-dev (= )
7.68.0-1ubuntu2 - libcurl4-dev (= ) libcurl3-openssl-dev (= ) libcurl3-dev (= ) libcurl-ssl-dev (= ) libcurl-dev (= )
Reverse Provides:
```

在Debian或基于Debian的系统（如Ubuntu）中，你可以使用apt或aptitude工具来查看包的依赖关系。当你想要安装一个包，比如libcurl4-openssl-dev，并想了解它的依赖关系时，有几种方法可以做到这一点。

使用apt-cache showpkg
apt-cache showpkg命令可以显示有关特定包的详细信息，包括其依赖关系。使用此命令时，你可以查找Depends、Pre-Depends、Recommends和Suggests等字段，这些字段列出了包的各种依赖。

bash
apt-cache showpkg libcurl4-openssl-dev
在输出中，查找Depends行以查看直接依赖。但请注意，输出可能包含很多信息，所以使用grep来过滤可能更方便：

bash
apt-cache showpkg libcurl4-openssl-dev | grep -E '^(Depends|Pre-Depends|Recommends|Suggests)'
使用apt-rdepends
如果你想要查看更详细的依赖树（即包不仅直接依赖哪些包，还间接依赖哪些包），你可以使用apt-rdepends工具。这个工具不是所有系统都预装的，但你可以通过apt安装它。

首先，安装apt-rdepends（如果尚未安装）：

bash
sudo apt-get install apt-rdepends
然后，使用它来查看libcurl4-openssl-dev的依赖树：

bash
apt-rdepends libcurl4-openssl-dev
或者，如果你想要更简洁的输出，可以尝试使用apt-rdepends的-s（或--simple）选项，但这可能不会显示所有级别的依赖。

使用aptitude
aptitude是另一个包管理工具，它提供了比apt更丰富的界面和选项。你可以使用aptitude来查看包的依赖关系，但请注意，aptitude的命令行界面可能与apt略有不同。

bash
aptitude show libcurl4-openssl-dev
然后，在输出中查找Depends、Recommends等字段。然而，aptitude的主要优势在于其图形界面和更强大的包管理能力，而不是简单的依赖关系查看。

结论
对于大多数基本的依赖关系查看需求，apt-cache showpkg或apt-cache depends（仅查看直接依赖）应该就足够了。如果你需要更详细的依赖树，那么apt-rdepends是一个很好的选择。不过，请记住，依赖关系可能会随着包版本和发行版的不同而有所变化。


sudo apt update
apt-cache showpkg libboost-all-dev

`sudo apt-get --only-upgrade install google-chrome-stable`

自己开发的包，如何上传到apt仓库

Debian/Ubuntu自有软件包构建私有源

https://www.cnblogs.com/lidp/archive/2009/02/26/1696283.html

[ubnutu/apt与apt-get/更新某一软件](https://blog.csdn.net/superjunenaruto/article/details/95173065)

apt可以安装共享库

apt install之后，二进制文件安装路径？

[Ubuntu中apt-get安装的文件位置](https://blog.csdn.net/younothings/article/details/103208387)

形如 apt-get install apps 这样的命令，一般会将下载文件放在 /var/cache/apt/archives目录下，然后安装。

如果不及时清理，这个目录所占空间会越来越大，幸运的是apt提供了相应的管理工具apt-get clean删除/var/cache/apt/archives/ 和 /var/cache/apt/archives/partial/目录下所有包(锁定的除外)。
apt-get autoclean仅删除不再能被下载的包。 

另外，aptitude clean也可删除/var/cache/apt/archives/ 和 /var/cache/apt/archives/partial/目录下所有包(锁定的除外)。

https://www.cnblogs.com/mch0dm1n/p/5422179.html

sudo apt install libpoco-dev -y
dpkg -l | grep libpoco
dpkg -L libpoco-dev
http://blog.chinaunix.net/uid-23254875-id-341021.html
https://blog.csdn.net/Kenny_GuanHua/article/details/123842699

apt-cache pkgnames | grep -i crypto++

apt-cache pkgnames | grep -i mysqlclient
apt-cache pkgnames | grep -i rapidjson

## apt安装时候，如何查看安装的依赖库

apt-cache showpkg libboost-all-dev

