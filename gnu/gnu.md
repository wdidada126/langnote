# gnu

https://www.gnu.org/software/#allgnupkgs

## gnu软件列表
https://www.gnu.org/software/software.html

https://www.gnu.org/software/libtool/

文档是manual
缩写man

CP命令的源代码是包含在coreutils里的，上gnu网站看看： http://www.gnu.org/software/coreutils/coreutils.html

sudo yum update
sudo yum install epel-release -y
sudo yum install help2man texinfo gnulib -y
sudo yum install autopoint gperf makeinfo texinfo-tex -y

```shell
sudo apt-get update
sudo apt-get install help2man texinfo gnulib -y
sudo apt-get install gettext gperftools-dev -y
sudo apt-get install autopoint gperf makeinfo texi2pdf -y
git clone git://git.sv.gnu.org/coreutils
cd coreutils
git checkout v9.4
./bootstrap
```
coreutils
/usr/bin/mkdir -p '/usr/local/bin'
  src/ginstall -c src/ginstall '/usr/local/bin/./install'
  src/ginstall -c src/chroot src/hostid src/timeout src/nice src/who src/users src/pinky src/stty src/df src/stdbuf src/[ src/b2sum src/base64 src/base32 src/basenc src/basename src/cat src/chcon src/chgrp src/chmod src/chown src/cksum src/comm src/cp src/csplit src/cut src/date src/dd src/dir src/dircolors src/dirname src/du src/echo src/env src/expand src/expr src/factor src/false src/fmt src/fold src/groups src/head src/id src/join src/kill src/link src/ln src/logname src/ls src/md5sum src/mkdir src/mkfifo src/mknod src/mktemp src/mv src/nl src/nproc src/nohup src/numfmt src/od src/paste src/pathchk src/pr src/printenv src/printf src/ptx src/pwd src/readlink src/realpath src/rm src/rmdir src/runcon src/seq src/sha1sum src/sha224sum src/sha256sum src/sha384sum src/sha512sum src/shred src/shuf src/sleep src/sort src/split src/stat src/sum src/sync src/tac src/tail src/tee src/test src/touch src/tr src/true src/truncate src/tsort src/tty src/uname src/unexpand src/uniq src/unlink src/uptime src/vdir src/wc src/whoami src/yes '/usr/local/bin'
