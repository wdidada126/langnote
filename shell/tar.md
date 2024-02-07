# tar

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