EROFS
EROFS 的源代码主要托管在 Linux 内核的官方仓库中，此外还有一个独立的用户态工具仓库。这里是在 2018 年开源时最核心的两个代码仓库地址：

### 核心源代码仓库

*   内核驱动代码 (Linux Kernel)：EROFS 作为 Linux 内核的一部分，其核心驱动代码就位于内核源码树的 `fs/erofs/` 目录下。你可以通过以下链接浏览各个版本的内核代码，其中许多早期文件带有华为的版权声明。
    *   官方主线仓库：[https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/fs/erofs](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/fs/erofs)
    *   EROFS 开发仓库：[https://git.kernel.org/pub/scm/linux/kernel/git/xiang/erofs.git](https://git.kernel.org/pub/scm/linux/kernel/git/xiang/erofs.git)

*   用户态工具仓库 (erofs-utils)：这是用于创建和操作 EROFS 镜像的用户态工具集（如 `mkfs.erofs`），与内核代码分开维护。
    *   官方仓库：[git://git.kernel.org/pub/scm/linux/kernel/git/xiang/erofs-utils.git](git://git.kernel.org/pub/scm/linux/kernel/git/xiang/erofs-utils.git)

### 重要细节

1.  开源协议：EROFS 的内核代码遵循 GPL-2.0 协议，部分头文件（如 `erofs_fs.h`）采用了 GPL-2.0 或 Apache-2.0 的双重许可。
2.  早期代码标识：在 2018 年左右提交的早期源代码文件中，可以清晰地看到 `Copyright (C) 2018 HUAWEI, Inc.` 的版权信息，以及主要作者 Gao Xiang 的名字。