# du

centos 查看/app路径下各个子文件夹整个文件夹大小

在 CentOS 系统中，如果你想要查看 /app 路径下各个子文件夹的大小，你可以使用 du（disk usage）命令配合 sort 和 head 命令来得到按大小排序的文件夹列表。

以下是一个基本的命令来查看 /app 路径下各个子文件夹的大小，并按大小降序排序：

```bash
du -sh /app/* | sort -rh
```
这里的选项和命令的含义是：

du -sh /app/*：du 是 "disk usage" 的缩写，-s 选项表示汇总目录的大小（不包括子目录中的文件），-h 选项表示以人类可读的格式（如 K, M, G）显示大小。/app/* 表示 /app 下的所有文件和文件夹，但因为这里我们使用 -s 选项，它实际上只会显示文件夹的大小。
sort -rh：sort 命令用于排序，-r 选项表示降序排序，-h 选项表示按照人类可读的数字大小进行排序（即考虑 K, M, G 等单位）。
注意：如果你想要包括子目录中的文件大小，你应该去掉 -s 选项：

```bash
du -h /app/* | sort -rh
```
但是，这样会显示 /app 下的所有文件和文件夹的大小，而不仅仅是文件夹。如果你只对文件夹感兴趣，并且想要包括子目录中的文件大小，你可能需要使用 find 命令结合 du 和 sort：

```bash
find /app/ -maxdepth 1 -type d -exec du -sh {} + | sort -rh
```
这里，-maxdepth 1 表示只搜索 /app/ 下的第一层目录（不包括子目录中的子目录），-type d 表示只查找目录，-exec du -sh {} + 表示对每个找到的目录执行 du -sh 命令来获取其大小。

du -st /
du -sh

du -h -d 1


```shell
du -h -d 1
28K	./bin
3.9M	./conf
96M	./lib
15M	./logs
114M	.
`

du的英文为:disk usage,含义是磁盘空间使用情况，功能是逐级进入指定目录的每一个子目录并显示该目录占用文件系统数据块的情况，如果没有指定目录，则对当前的目录进行统计。

https://blog.csdn.net/hbiao68/article/details/52682752

du的参数

man du

GNU coreutils 8.22

SYNOPSIS
       du [OPTION]... [FILE]...
       du [OPTION]... --files0-from=F

DESCRIPTION
       Summarize disk usage of each FILE, recursively for directories.

       Mandatory arguments to long options are mandatory for short options too.

       -0, --null
              end each output line with 0 byte rather than newline

       -a, --all
              write counts for all files, not just directories

       --apparent-size
              print  apparent  sizes,  rather  than  disk  usage; although the apparent size is usually smaller, it may be larger due to holes in ('sparse')
              files, internal fragmentation, indirect blocks, and the like

       -B, --block-size=SIZE
              scale sizes by SIZE before printing them; e.g., '-BM' prints sizes in units of 1,048,576 bytes; see SIZE format below

       -b, --bytes
              equivalent to '--apparent-size --block-size=1'

       -c, --total
              produce a grand total

       -D, --dereference-args
              dereference only symlinks that are listed on the command line

       -d, --max-depth=N
              print the total for a directory (or file, with --all) only if it is N or fewer levels below the command line argument;  --max-depth=0  is  the
              same as --summarize

       --files0-from=F
              summarize disk usage of the NUL-terminated file names specified in file F; if F is -, then read names from standard input

       -H     equivalent to --dereference-args (-D)

       -h, --human-readable
              print sizes in human readable format (e.g., 1K 234M 2G)

       --inodes
              list inode usage information instead of block usage

       -k     like --block-size=1K

       -L, --dereference
              dereference all symbolic links

       -l, --count-links
              count sizes many times if hard linked

       -m     like --block-size=1M

       -P, --no-dereference
              don't follow any symbolic links (this is the default)

       -S, --separate-dirs
              for directories do not include size of subdirectories

       --si   like -h, but use powers of 1000 not 1024

       -s, --summarize
              display only a total for each argument

       -t, --threshold=SIZE
              exclude entries smaller than SIZE if positive, or entries greater than SIZE if negative

       --time show time of the last modification of any file in the directory, or any of its subdirectories

       --time=WORD
              show time as WORD instead of modification time: atime, access, use, ctime or status

       --time-style=STYLE
              show times using STYLE, which can be: full-iso, long-iso, iso, or +FORMAT; FORMAT is interpreted like in 'date'

       -X, --exclude-from=FILE
              exclude files that match any pattern in FILE

       --exclude=PATTERN
              exclude files that match PATTERN

       -x, --one-file-system
