# tar

## 使用 gzip 压缩
tar -zcvf my_folder.tar.gz my_folder

## 使用 bzip2 压缩
tar -jcvf my_folder.tar.bz2 my_folder

## 使用 xz 压缩
tar -Jcvf my_folder.tar.xz my_folder

## 只打包不压缩

`tar` 是一个在 Unix 和类 Unix 系统中常用的归档工具，它可以打包文件和文件夹，并且可以配合压缩工具（如 gzip、bzip2、xz 等）使用来压缩打包后的文件。

要使用 `tar` 命令打包整个文件夹，你可以使用以下命令格式：

```bash
tar -cvf archive_name.tar directory_name
```

这里的各个参数代表：
- `c` 代表创建一个新的归档文件。
- `v` 代表在创建归档文件时显示详细信息。
- `f` 代表指定归档文件的名称。

`archive_name.tar` 是你想要创建的归档文件的名称，`directory_name` 是你想要打包的文件夹的名称。

例如，如果你有一个名为 `my_folder` 的文件夹，并且想要将其打包为名为 `my_folder.tar` 的归档文件，你可以使用以下命令：

```bash
tar -cvf my_folder.tar my_folder
```

如果你想要压缩归档文件，可以使用 `gzip`（创建 `.tar.gz` 或 `.tgz` 文件）：

```bash
tar -czvf my_folder.tar.gz my_folder
```

或者使用 `bzip2`（创建 `.tar.bz2` 文件）：

```bash
tar -cjvf my_folder.tar.bz2 my_folder
```

或者使用 `xz`（创建 `.tar.xz` 文件）：

```bash
tar -cJvf my_folder.tar.xz my_folder
```

记得替换 `my_folder` 和 `my_folder.tar` 为你实际的文件夹名称和归档文件名称。

好的,让我来解释一下如何使用 tar 命令将 `zookeeper/` 文件夹打包成 `zookeeper.tgz` 文件。

1. 使用 tar 命令将 `zookeeper/` 文件夹打包成 `.tar` 文件:

   ```
   tar -cvf zookeeper.tar zookeeper/
   ```

   - `c`: 创建新的归档文件
   - `v`: 显示详细信息
   - `f`: 指定输出文件名为 `zookeeper.tar`

2. 使用 gzip 命令压缩 `zookeeper.tar` 文件:

   ```
   gzip zookeeper.tar
   ```

   这个操作会将 `zookeeper.tar` 文件压缩成 `zookeeper.tar.gz` 文件。

3. 如果您想将 `.tar.gz` 文件重命名为 `.tgz`,可以使用以下命令:

   ```
   mv zookeeper.tar.gz zookeeper.tgz
   ```

综合起来,完整的命令如下:

```
tar -cvf zookeeper.tar zookeeper/
gzip zookeeper.tar
mv zookeeper.tar.gz zookeeper.tgz
```

这样就可以将 `zookeeper/` 文件夹打包成 `zookeeper.tgz` 文件了。

如果您想直接使用 `tar -zxvf` 命令解压缩 `zookeeper.tgz` 文件,可以省略第 2 和第 3 步,直接使用以下命令:

```
tar -zxvf zookeeper.tgz
```

这样就可以直接解压缩 `zookeeper.tgz` 文件了。



打包 压缩 命令tar zip 
tar语法

#压缩
tar -czvf ***.tar.gz
tar -cjvf ***.tar.bz2
#解压缩
tar -xzvf ***.tar.gz
tar -xjvf ***.tar.bz2

https://www.cnblogs.com/centos2017/p/7896807.html

在 `cd /home/wdidada` 后，要打包 `/home/wdidada/llvm-project_bak` 整个文件夹，您可以使用 `tar` 命令，并指定正确的源路径和目标文件名。下面是正确的命令格式：

```bash
tar -czvf llvm-project_bak.tar.gz llvm-project_bak/
```

这里是命令的解释：

- `c`：创建一个新的归档文件。
- `z`：通过 gzip 进行压缩。
- `v`：详细模式，显示正在归档或解归档的文件名。
- `f`：指定归档文件的名称。

`llvm-project_bak.tar.gz` 是您将要创建的 tar.gz 文件的名称。您可以根据需要更改此名称。

`llvm-project_bak/` 是您要打包的文件夹路径。请确保路径的末尾有一个斜杠 `/`，这表示您正在打包该文件夹及其内容，而不是仅仅打包一个名为 `llvm-project_bak` 的文件（如果存在的话）。

确保您在 `/home/wdidada` 目录下执行此命令，否则您需要提供 `llvm-project_bak` 文件夹的完整路径。

如果您已经处于 `/home/wdidada` 目录下，上述命令应该可以正确执行并打包 `llvm-project_bak` 文件夹。如果打包成功，您将在 `/home/wdidada` 目录下看到一个名为 `llvm-project_bak.tar.gz` 的文件。

# windows下如何生成tar或gz压缩包



7z 两次压缩


tar
-tvf
-vf

tar -zcvf xxx.tgz .

当前文件夹，创建压缩包 