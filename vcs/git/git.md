# git

## version

2.34.1.windows.1

## some

(要将Git中a分支从b到c的变动应用到d分支，可以使用`git cherry-pick`命令。以下是具体步骤和分析过程：)

### 分析过程
1. 确定变动范围：
   - 首先，需要明确a分支上从b到c的具体变动范围。可以使用`git log`命令查看a分支上的提交记录，并确定b和c对应的提交哈希值。

2. 应用变动到d分支：
   - 使用`git cherry-pick`命令将a分支上从b到c的提交应用到d分支。

### 具体步骤
1. 切换到a分支并查看提交记录：
   ```sh
   git checkout a
   git log
   ```
   - 记录下b和c对应的提交哈希值（例如，b对应的哈希值是`commit_b_hash`，c对应的哈希值是`commit_c_hash`）。

2. 切换到d分支：
   ```sh
   git checkout d
   ```

3. 使用git cherry-pick应用变动：
   - 使用`git cherry-pick`命令将b到c之间的提交应用到d分支。可以使用以下命令：
     ```sh
     git cherry-pick commit_b_hash^..commit_c_hash
     ```
   - 注意：`commit_b_hash^`表示b提交的前一个提交，这样可以确保从b提交开始应用变动。

4. 解决冲突（如果有）：
   - 如果在应用变动过程中出现冲突，Git会提示你解决冲突。解决冲突后，使用以下命令继续应用变动：
     ```sh
     git add <resolved_file>
     git cherry-pick --continue
     ```

5. 完成应用变动：
   - 如果没有冲突或冲突已解决，变动将被成功应用到d分支。

### 示例
假设a分支上b提交的哈希值是`abc123`，c提交的哈希值是`def456`，以下是具体命令：
```sh
git checkout a
git log
# 记录下abc123和def456
git checkout d
git cherry-pick abc123^..def456
```

### 注意事项
- 确保在执行`git cherry-pick`之前，d分支是最新的，以避免不必要的冲突。
- 如果在应用变动过程中出现冲突，务必仔细解决冲突并测试代码。

使用* model DeepSeek-R1来切换满血版R1模型。

## tag
git 查看当前切换到哪个tag
git describe --tags --exact-match

Git patch 文件是纯文本文件。
https://github.com/c-ares/c-ares/commit/d41db1b7916fadea987e5bb05fd4aafaf0d1d6ea.patch?full_index=1 

## sh
git blame是Git版本控制系统中的一个非常有用的命令，它用于显示指定文件中每一行代码的修改历史。具体来说，git blame可以追踪到每一行代码是由哪位开发者在何时最后修改的，包括提交的哈希值、作者、修改时间和提交注释等信息。这个命令对于开发人员来说非常有帮助，因为它可以帮助他们了解代码的修改历史，找出特定代码段的贡献者，并追溯代码的演变过程。

以下是关于git blame命令的一些详细信息和用法：

功能与用途
追踪修改历史：git blame能够显示文件中每一行代码的最后一次修改信息，包括修改者、修改时间和提交注释。
代码审查与知识共享：通过查看代码的修改历史，团队成员可以更好地理解代码的结构和逻辑，促进代码审查和知识共享。
问题追踪：当遇到代码中的问题时，git blame可以帮助开发人员快速定位到引入问题的提交，从而更快地解决问题。
使用方法
git blame命令的基本语法如下：

bash
git blame [选项] [文件路径]
其中，<文件路径>是可选的，如果不指定文件路径，则默认显示当前目录下所有文件的修改历史。

常用选项
-L <起始行号>,<结束行号>：只显示指定行号范围内的代码修改历史。
-C：对于重命名或拷贝的代码行，也进行代码行溯源。
-M：对于移动的代码行，也进行代码行溯源。
--date=short：只显示提交日期的简略形式。
--show-stats：显示包含每个作者的行数统计信息。
注意事项
使用git blame时，应避免将责任归咎于代码的修改者，而应以积极和建设性的方式与团队成员合作和讨论问题。
git blame提供的信息是基于Git的提交历史，因此它只能显示到Git仓库中的修改历史，对于仓库之外的修改则无法追踪。
总之，git blame是Git中一个非常实用的命令，它能够帮助开发人员更好地理解和维护代码，促进团队协作和代码质量的提升。

git submodule update --init --recursive
下载.gitmodules文件中指定的依赖到指定文件夹

git submodule被cmake中FetchContent_Declare替代

FetchContent_Declare(
  EABase
  GIT_REPOSITORY https://github.com/electronicarts/EABase.git
  GIT_TAG        521cb053d9320636f53226ffc616216cf532f0ef
  GIT_SUBMODULES "" # This should be temporary until we update the cyclic submodule dependencies in EABase.
)

FetchContent_MakeAvailable(EABase)

target_link_libraries(EASTL EABase)

例子：
https://github.com/electronicarts/EASTL


## git 获取tag
当你使用 `git clone` 克隆 vcpkg 仓库并尝试通过 `git pull` 更新时，发现没有下载标签（tags），这是因为默认情况下，`git pull` 只会拉取最新的提交，而不会自动拉取标签。

### 解决方法
1. 手动拉取标签
   你可以使用 `git fetch` 来手动拉取标签：
```bash
git fetch --tags
```
这将获取远程仓库中的所有标签。
2. 合并标签到本地
   如果你想将所有标签合并到本地分支，可以使用以下命令：
```bash
git pull --tags
```
3. 克隆时拉取标签
   在克隆仓库时，你可以直接拉取所有标签：
```bash
git clone --branch master --single-branch --depth 1 --tags https://github.com/microsoft/vcpkg.git
```
### 检查标签
拉取标签后，可以通过以下命令查看本地标签：
```bash
git tag
```
这样你就可以看到所有从远程仓库拉取到的标签。
### 示例
假设你已经克隆了 vcpkg 仓库：
```bash
git clone https://github.com/microsoft/vcpkg.git
cd vcpkg
```
然后，使用 `git fetch` 来拉取标签：
```bash
git fetch --tags
```
或者使用 `git pull` 并包含标签：
```bash
git pull --tags
```
最后，检查标签：

```bash
git tag
```

### 总结
通过以上步骤，你可以确保从远程仓库获取到所有标签。这样，你就可以在本地使用和参考这些标签。例如，在版本管理和回退到特定版本时，标签是非常有用的。

## dd

git config --global core.editor "'D:\dev_tools\npp.8.5.8.portable.x64\notepad++.exe' -multiInst -notabbar -nosession -noPlugin"

如果你在使用 git pull 命令时，系统默认打开了 Visual Studio Code (VSC) 而不是在命令行中显示输出，这通常是因为你的 Git 配置或者系统的某些设置与 VSC 的集成有关。

要取消这种集成，并确保 git pull 命令只在命令行中显示输出，你可以尝试以下几个步骤：

检查 Git 配置：
运行 git config --global --list 来查看你的全局 Git 配置。查找与 Visual Studio Code 相关的配置，比如 core.editor 或其他可能与编辑器集成的设置。
如果找到与 VSC 相关的配置，你可以使用 git config --global --unset <配置项名> 来取消它。

检查环境变量：
有时，环境变量可能会影响 Git 的行为。检查是否有任何与 VSC 相关的环境变量，特别是 GIT_EDITOR、VISUAL 或 EDITOR。
你可以使用 echo $GIT_EDITOR、echo $VISUAL 和 echo $EDITOR（在 Unix/Linux/macOS 上）或 echo %GIT_EDITOR%、echo %VISUAL% 和 echo %EDITOR%（在 Windows 上）来查看这些变量的值。

如果找到了与 VSC 相关的值，你可以取消它们或将其设置为其他文本编辑器（如 nano、vim 或 emacs）。

检查 Git 钩子（Hooks）：
Git 钩子是在 Git 仓库的 .git/hooks 目录中定义的脚本，它们会在特定的 Git 事件（如 commit、push、pull 等）触发时运行。检查这个目录，看是否有与 VSC 相关的脚本。
如果有，你可以重命名或删除这些脚本，或者修改它们的内容以确保它们不再调用 VSC。

检查 VSC 设置：
在 VSC 中，检查是否有任何与 Git 集成相关的设置。通常，这些设置可以在 VSC 的设置菜单（通过 File > Preferences > Settings 或 Ctrl+, 快捷键访问）中找到。
查找与 Git 或编辑器集成相关的设置，并确保它们没有配置为在 git pull 时自动打开 VSC。

重启命令行或终端：
在更改了配置或环境变量后，确保重启你的命令行或终端窗口，以使更改生效。
测试：
最后，运行 git pull 命令来测试你的更改是否生效。如果一切正常，你应该只会在命令行中看到 git pull 的输出，而 VSC 不会自动打开。

比较两个分支 哪些文件
git diff --name-only prod_sync_no_modify_pom prod-20240531_0612

如果你想要查看两个分支之间的差异，但不想查看文件的具体内容（即只查看哪些文件有差异，而不查看差异的具体内容），你可以使用 git diff 命令的 --name-status 或 --name-only 选项。

--name-status 会显示每个有差异文件的名称以及状态（例如：修改、添加、删除等）。
--name-only 会仅显示有差异的文件名称。
以下是如何使用这些选项的示例：

显示文件名称和状态
bash
git diff --name-status prod_sync_no_modify_pom...prod-20240531_0612
注意，这里使用了三个点 ... 而不是两个点 ..。两个点 .. 会显示从 prod_sync_no_modify_pom 分支到 prod-20240531_0612 分支的合并路径上的所有差异，而三个点 ... 会显示两个分支之间在它们共同祖先之后的差异。

仅显示文件名称
bash
git diff --name-only prod_sync_no_modify_pom...prod-20240531_0612
这些命令将只列出在两个分支之间有差异的文件，而不会显示这些文件的具体差异内容。

1. 显示出branch1和branch2中差异的部分
git diff branch1 branch2 --stat
2. 显示指定文件的详细差异
git diff branch1 branch2 具体文件路径
3. 显示出所有有差异的文件的详细差异
git diff branch1 branch2
4. 查看branch1分支有，而branch2中没有的log
git log branch1 ^branch2
5. 查看branch2中比branch1中多提交了哪些内容
git log branch1..branch2
注意，列出来的是两个点后边（此处即dev）多提交的内容。
6. 不知道谁提交的多谁提交的少，单纯想知道有什么不一样
git log branch1...branch2
7. 在上述情况下，在显示出每个提交是在哪个分支上
git log -lefg-right branch1...branch2
注意commit后面的箭头，根据我们在 –left-right branch1…branch2 的顺序，左箭头 < 表示是 branch1 的，右箭头 > 表示是branch2的。

本地main分支，远程master分支，强行推送
error: src refspec master does not match any


```shell
PS D:\git\github\testjdk8> git rm -r --cached testjdk8.und/
error: the following file has staged content different from both the
file and the HEAD:
    testjdk8.und/settings.xml
(use -f to force removal)
PS D:\git\github\testjdk8> git rm -r --cached testjdk8.und/ -f
rm 'testjdk8.und/id.txt'
rm 'testjdk8.und/settings.xml'
```

Netty

And need to pay attention to the configuration of git. If using Windows, when you checkout code, LF will be automatically converted to CRLF:

git config --global core.autocrlf true

Or if using MacOS, when you commit code, CRLF will be automatically converted to LF:
git config --global core.autocrlf input

git config core.autocrlf input

git config core.autocrlf 的配置选项有三个可能的值：true、input 和 false。这些值决定了 Git 在检出（checkout）和提交（commit）代码时如何处理行尾字符（换行符）。

true：
检出时：将行尾从 LF 转换为 CRLF。
提交时：将行尾从 CRLF 转换回 LF。
这个设置通常用于 Windows 系统，因为 Windows 系统通常使用 CRLF（即 \r\n）作为行尾字符，而 Git 仓库和其他 UNIX-like 系统（如 Linux 和 macOS）则通常使用 LF（即 \n）。

input：
检出时：不转换行尾字符。
提交时：将行尾从 CRLF 转换回 LF。
这个设置对于跨平台协作开发很有用。例如，在 Windows 上检出代码时保留原有的行尾字符（可能是 LF 或 CRLF），但在提交代码到仓库时总是转换为 LF。这有助于避免因为行尾字符不同而导致的代码变化和冲突。

false：
检出时：不转换行尾字符。
提交时：也不转换行尾字符。
这个设置意味着 Git 不会自动处理行尾字符的转换。所有文件的行尾字符将保持原样。

在选择合适的 core.autocrlf 设置时，你需要考虑你的工作环境和你的团队成员使用的操作系统。通常，在 Windows 系统上设置为 true，在 Linux 和 macOS 上设置为 input 是比较保险的选择。如果所有使用者都在同一系统下工作，并且希望保持行尾字符的一致性，可以设置为 false。



git clone https://github.com/tfussell/xlnt.git xlnt --recurse-submodules

.git/config纯文本文件下，有config remote等信息

## 官网
https://git-scm.com/

## minigit

github.com/DQNEO/minigit

git 一次性merge多个分支?

```shell
git merge localbranchA localbranchB
git merge localbranchA remoteName/branchB

git fetch origin new_branch
git merge origin/new_branch
```
## 版本

git version
git version 2.45.1.windows.1

git version 2.42.0.windows.2

git --version
git version 2.37.1 (Apple Git-137.1)

要在 Git 中合并 patch 文件，您可以使用 `git apply` 命令。以下是在命令行中合并 patch 文件的示例：
1. 使用 `git apply` 命令合并 patch 文件：
```
git apply patchfile.patch
```
其中，`patchfile.patch` 是您要合并的 patch 文件的文件名。请确保在运行该命令之前，您已经位于正确的 Git 仓库目录下。
2. 如果您希望将合并后的更改直接提交到 Git 仓库，可以使用 `git apply` 命令的 `--index` 或 `-i` 选项：
```
git apply --index patchfile.patch
```
或
```
git apply -i patchfile.patch
```
这将在合并 patch 文件后将更改添加到暂存区，以便您可以在之后执行提交操作。
请注意，`git apply` 命令仅将 patch 文件中的更改应用到您的工作目录中，并不会在 Git 中创建新的提交。如果您想要将合并后的更改提交到 Git 仓库，您需要手动执行 `git commit` 命令。
如果您想要在应用 patch 文件之前预览更改，可以使用 `git apply` 命令的 `--check` 选项。这会检查 patch 文件是否能够成功应用，但不会实际应用更改。
```
git apply --check patchfile.patch
```
在 Git 中，`git apply` 和 `git am` 是两个用于应用补丁的命令，它们之间有一些区别。
1. `git apply`：
   - `git apply` 命令用于将补丁文件应用到当前工作目录，但不会创建新的提交。
   - 它可以应用普通的 diff 格式补丁文件（如 `.patch` 或 `.diff` 文件）。
   - `git apply` 可以通过使用 `--check` 选项进行预览，以验证补丁文件能否成功应用。
   - 使用 `git apply` 时，您需要手动执行 `git add` 命令将更改添加到暂存区，并使用 `git commit` 命令创建新的提交。
2. `git am`：
   - `git am` 命令用于将补丁文件应用到当前工作目录，并自动创建新的提交。
   - 它可以应用邮件格式的补丁文件（如 `.patch` 或 `.mbox` 文件），这些文件通常由 `git format-patch` 命令生成。
   - `git am` 会解析补丁文件中的作者、提交日期等信息，并自动创建提交记录。
   - `git am` 还支持在多个补丁文件中进行批量应用。
   - 使用 `git am` 时，您可以使用 `--signoff` 选项将补丁作者的签名信息添加到提交中。
总结一下：
- `git apply` 用于将补丁文件应用到工作目录，不创建新的提交，需要手动执行 `git add` 和 `git commit`。
- `git am` 用于将补丁文件应用到工作目录，自动创建新的提交，支持邮件格式补丁文件。

根据您的需求和补丁文件的格式，选择适当的命令进行补丁应用。

Git的commit id是通过哈希算法（如SHA-1、SHA-256等）对提交信息进行摘要生成的。具体步骤如下：

1. 将提交信息进行编码，通常是UTF-8编码。
2. 使用哈希算法（如SHA-1、SHA-256等）对编码后的提交信息进行摘要计算。
3. 将摘要结果转换为16进制字符串，作为commit id。

在Git中，可以使用`git rev-parse HEAD`命令查看当前分支的最新commit id。


git format-patch <commit_id>

git format-patch -h
usage: git format-patch [<options>] [<since> | <revision-range>]          
                                                                          
    -n, --numbered        use [PATCH n/m] even with a single patch        
    -N, --no-numbered     use [PATCH] even with multiple patches          
    -s, --signoff         add a Signed-off-by trailer                     
    --stdout              print patches to standard out                   
    --cover-letter        generate a cover letter                         
    --numbered-files      use simple number sequence for output file names
    --suffix <sfx>        use <sfx> instead of '.patch'                   
    --start-number <n>    start numbering patches at <n> instead of 1     
    -v, --reroll-count <reroll-count>                                     
                          mark the series as Nth re-roll
    --filename-max-length <n>
                          max length of output filename
    --rfc                 use [RFC PATCH] instead of [PATCH]
    --cover-from-description <cover-from-description-mode>
                          generate parts of a cover letter based on a branch's description
    --subject-prefix <prefix>
                          use [<prefix>] instead of [PATCH]
    -o, --output-directory <dir>
                          store resulting files in <dir>
    -k, --keep-subject    don't strip/add [PATCH]
    --no-binary           don't output binary diffs
    --zero-commit         output all-zero hash in From header
    --ignore-if-in-upstream
                          don't include a patch matching a commit upstream
    -p, --no-stat         show patch format instead of default (patch + stat)

Messaging
    --add-header <header> add email header
    --to <email>          add To: header
    --cc <email>          add Cc: header
    --from[=<ident>]      set From address to <ident> (or committer ident if absent)
    --in-reply-to <message-id>
                          make first mail a reply to <message-id>
    --attach[=<boundary>] attach the patch
    --inline[=<boundary>] inline the patch
    --thread[=<style>]    enable message threading, styles: shallow, deep
    --signature <signature>
                          add a signature
    --base <base-commit>  add prerequisite tree info to the patch series
    --signature-file <file>
                          add a signature from a file
    -q, --quiet           don't print the patch filenames
    --progress            show progress while generating patches
    --interdiff <rev>     show changes against <rev> in cover letter or single patch
    --range-diff <refspec>
                          show changes against <refspec> in cover letter or single patch
    --creation-factor <n> percentage by which creation is weighted
    --force-in-body-from  show in-body From: even if identical to the e-mail header

## 二级命令行
log
config
rebase
branch
merge
push
pull
fetch
diff
revert
restore

git merge -h
usage: git merge [<options>] [<commit>...]
   or: git merge --abort
   or: git merge --continue

    -n                    do not show a diffstat at the end of the merge
    --stat                show a diffstat at the end of the merge
    --summary             (synonym to --stat)
    --log[=<n>]           add (at most <n>) entries from shortlog to merge commit message
    --squash              create a single commit instead of doing a merge
    --commit              perform a commit if the merge succeeds (default)
    -e, --edit            edit message before committing
    --cleanup <mode>      how to strip spaces and #comments from message
    --ff                  allow fast-forward (default)
    --ff-only             abort if fast-forward is not possible
    --rerere-autoupdate   update the index with reused conflict resolution if possible
    --verify-signatures   verify that the named commit has a valid GPG signature
    -s, --strategy <strategy>
                          merge strategy to use
    -X, --strategy-option <option=value>
                          option for selected merge strategy
    -m, --message <message>
                          merge commit message (for a non-fast-forward merge)
    -F, --file <path>     read message from file
    --into-name <name>    use <name> instead of the real target
    -v, --verbose         be more verbose
    -q, --quiet           be more quiet
    --abort               abort the current in-progress merge
    --quit                --abort but leave index and working tree alone
    --continue            continue the current in-progress merge
    --allow-unrelated-histories
                          allow merging unrelated histories
    --progress            force progress reporting
    -S, --gpg-sign[=<key-id>]
                          GPG sign commit
    --autostash           automatically stash/stash pop before and after
    --overwrite-ignore    update ignored files (default)
    --signoff             add a Signed-off-by trailer
    --no-verify           bypass pre-merge-commit and commit-msg hooks

## ubuntu 安装不同版本git
Git 的官方 PPA（Personal Package Archive）
sudo add-apt-repository ppa:git-core/ppa


.gitmodules

```
[submodule "node_modules/loader"]
	path = node_modules/loader
	url = git://github.com/jonlb/node-jxLoader.git
[submodule "node_modules/uglifyjs"]
	path = node_modules/uglifyjs
	url = https://github.com/mishoo/UglifyJS.git
[submodule "node_modules/pkginfo"]
	path = node_modules/pkginfo
	url = git://github.com/indexzero/node-pkginfo.git
```

git submodule init
git submodule update
git submodule update --init --recursive <commit_id>
git submodule指定commit id

hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint: 
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only


```shell
git pull
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint: 
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint: 
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.
```

https://github.com/git/git/releases

## git remote add xxx之后，不能从新添加的分支检出

git fetch一下
git fetch xxx master:master

## git pull 磁盘不够了

error: The following untracked working tree files would be overwritten by merge:
.gitignore
2023/202308/202308_month.md

你遇到的这个问题是因为你本地有一些未被跟踪（untracked）的文件，这些文件在远程仓库中可能已经发生了改变。如果你试图使用 git pull 命令，Git 会试图合并远程的更改到你的本地环境，这可能会导致你的本地文件被覆盖。因此，Git 阻止了这个操作并抛出了这个错误信息。

你有以下几种解决方案：

保存你的本地更改：你可以把这些未被跟踪的文件添加到Git，然后用git stash命令保存这些更改。这样你就可以安全地拉取远程的更改，而不会丢失你的本地更改。如果你已经添加了这些文件到Git，那么你可能需要把这些文件从Git中移除（使用git rm --cached `<file>`），然后再重新添加。
丢弃你的本地更改：如果你确定这些未被跟踪的文件的更改不重要，你可以直接丢弃这些更改。使用 git clean -df 命令可以删除这些文件。
分开操作：你可以在拉取远程更改之前，先把你的本地更改推送到远程仓库。使用 git commit -a 和 git push 可以完成这个操作。这样你的本地更改就会安全地保存在远程仓库，而不会在拉取远程更改时被覆盖。
这是一个可能的流程：

添加所有文件到暂存区

git add .

# 提交所有暂存区的文件

git commit -a -m "Adding local changes"

# 将你的更改推送到远程仓库

git push

# 拉取远程的更改

# 添加所有文件到暂存区

git add .

# 提交所有暂存区的文件

git commit -a -m "Adding local changes"

# 将你的更改推送到远程仓库

git push

# 拉取远程的更改

git pull
这样，你可以安全地拉取远程的更改，而不会丢失你的本地更改。

recursive git 循环克隆子项目
git clone 重命名
git clone xxx.git anothername

TortoiseGit和Git使用教程
https://blog.csdn.net/hjwdz2015/article/details/90487554

git diff bc7e28c568f4af0bd39c26d71de6060c0baf7a5b e9b4f421e1f02d01ca6b4a0e5fee171a42fab5f9

## git跨分支合并

git支持不同分支之间合并代码

## git暂存代码

Git 的暂存操作是通过 git add 命令来完成的。git add 可以将工作区中的文件更改或添加到 Git 的暂存区，以备提交。

下面是一些示例：

暂存所有更改：

bash
git add .
这会将工作区的所有更改（包括新文件）添加到暂存区。
2. 暂存特定文件：

```bash
git add file1.txt file2.txt
```

这会将 file1.txt 和 file2.txt 添加到暂存区。
3. 暂存所有删除的文件：

```bash
git add -u
```

这会将所有已删除的文件添加到暂存区。
4. 暂存所有更改和删除的文件：

```bash
git add -A
```

这会将所有更改（包括新文件）和已删除的文件添加到暂存区。
在暂存了文件之后，你可以使用 git commit 命令将这些更改提交到你的 Git 仓库。例如：

```bash
git commit -m "描述你的更改"
```

请注意，git commit 命令默认不会将工作区中的未暂存更改包含在提交中。如果你试图只提交暂存的文件，而忽略未暂存的更改，你可以使用 git commit -a 命令，但请谨慎使用，以避免误提交非预期的文件。

`git merge origin/master`

`git merge` 命令用于将两个分支合并。当你要将远程分支合并到本地分支时，可以使用以下命令：

1. 首先，切换到本地分支：

   ```
   git checkout <local-branch>
   ```
2. 然后，从远程仓库获取最新的代码：

   ```
   git fetch
   ```

   这个命令会更新本地仓库中对应的远程分支引用，但是不会改变当前分支的状态。
3. 最后，将远程分支合并到本地分支：

   ```
   git merge origin/<remote-branch>
   ```

   这个命令会将本地分支与远程分支合并。注意，`origin/<remote-branch>` 是远程分支的完整名称，其中 `origin` 是远程仓库的名称，`<remote-branch>` 是远程分支的名称。

在执行 `git merge` 命令之前，建议先运行 `git diff` 命令查看本地分支和远程分支之间的差异，以便更好地理解合并的影响。如果合并过程中出现了代码冲突，需要手动解决冲突并提交变更。

需要注意的是，如果你在本地分支中已经有了对应的修改，执行 `git merge` 命令可能会导致代码冲突。在这种情况下，你需要先将本地分支提交变更，然后再执行 `git fetch` 命令获取最新的代码，最后再执行 `git merge` 命令将远程分支合并到本地分支。

`git merge` 命令用于将不同的分支合并到当前分支。在执行 `git merge` 命令时，Git 会将指定的分支的修改合并到当前分支中。

以下是一个简单的 `git merge` 示例，假设你当前在 `main` 分支上，想要将 `feature` 分支的修改合并到 `main` 分支上：

```
git merge feature
```

执行此命令后，Git 将会自动尝试将 `feature` 分支上的修改合并到 `main` 分支上，如果有冲突，则需要手动解决冲突。

如果你想要保留原始分支中的修改，可以使用 `--no-ff` 参数执行非快进合并，例如：

```
git merge --no-ff feature
```

这将会在 `main` 分支上创建一个新的合并提交，保留原始分支和合并分支的修改历史。

如果你想要撤销合并操作，可以使用 `git merge --abort` 命令。

git remote set-url gitremote https://github.com/wimoor-erp/wimoor.git

1. 如果你的GIT设置了多个remote地址，在不同的remote间pull方法为：
   $ git pull <remote_name> <branch_name>
2. 每次都需要输入 remote name 和 branch name 比较麻烦，我们可以将某个remote 设置为默认
   设置方法：
   $ git config branch.master.remote `<remote origin>`
   $ git config branch.master.merge refs/heads/master
3. 也可以直接通过修改git的配置文件进行设置。(工程所在.git目录)
   $ vi .git/config
4. 如果需要对所有的项目都进行设置可以使用 --global 参数，进行设置
   https://blog.csdn.net/Andy_Dou/article/details/84602414

本地main，远程master分支
git push --set-upstream origin main

--set-upstream 远程不存在，在远程创建分支

提示：使用 'master' 作为初始分支的名称。这个默认分支名称可能会更改。要在新仓库中
提示：配置使用初始分支名，并消除这条警告，请执行：
提示：
提示： git config --global init.defaultBranch <名称>
提示：
提示：除了 'master' 之外，通常选定的名字有 'main'、'trunk' 和 'development'。
提示：可以通过以下命令重命名刚创建的分支：
提示：
提示： git branch -m `<name>`

```
git config --global user.email "xxx@qq.com"
git config --global user.name "wdidada"
```

git config user.email "1664884095@qq.com"
git config user.name "wdidada"
```
git config user.email "xxx@qq.com"
git config user.name "WuCheng"
```

```
git config  --global user.email "wdidada@qq.com"
git config  --global user.name "wdidada"
```

```
git config --global user.email "xxx@qq.com"
git config --global user.name "WuCheng"
```

```
git config user.email "wc@eteng.cn"
git config user.name "WuCheng"
```

```
git config user.email "xxx@qq.com"
git config user.name "wdidada"
```

git log --author="xxx"

git add -A
git add .
相同点 不同点

git config --global pull.rebase false  # merge


### 查看

查看某个人的git提交记录
git log --author="author"

git查看本地有多少个commit没有提交到远程仓库

git status 只能查看到本地当前有多少个提交还未推送，但看不到具体是哪些提交

git log  branch_name  ^origin/branch_name

### git多分支合并

场景a b分支

a分支改变
b分支 改变 提交

a分支 merge b
a分支之前的改动直接提交

https://github.com/edidada/testgit
testgit 仓库
要查看已添加到暂存区的文件列表，可以使用以下命令：
git diff --cached --name-only


git diff -h       
usage: git diff [<options>] [<commit>] [--] [<path>...]
   or: git diff [<options>] --cached [--merge-base] [<commit>] [--] [<path>...]
   or: git diff [<options>] [--merge-base] <commit> [<commit>...] <commit> [--] [<path>...]
   or: git diff [<options>] <commit>...<commit> [--] [<path>...]
   or: git diff [<options>] <blob> <blob>
   or: git diff [<options>] --no-index [--] <path> <path>

common diff options:
  -z            output diff-raw with lines terminated with NUL.
  -p            output patch format.
  -u            synonym for -p.
  --patch-with-raw
                output both a patch and the diff-raw format.
  --stat        show diffstat instead of patch.
  --numstat     show numeric diffstat instead of patch.
  --patch-with-stat
                output a patch and prepend its diffstat.
  --name-only   show only names of changed files.
  --name-status show names and status of changed files.
                try unchanged files as candidate for copy detection.
  -l<n>         limit rename attempts up to <n> paths.
  -O<file>      reorder diffs according to the <file>.
  -S<string>    find filepair whose only one side contains the string.
  --pickaxe-all
                show all files diff when -S is used and hit is found.
  -a  --text    treat all files as text.

`git diff` 命令用于比较工作区和暂存区之间的差异。以下是一些典型的用法：

1. 查看工作区与暂存区的差异：
```
git diff
```

2. 查看工作区与最近一次提交的差异：
```
git diff HEAD
```

3. 查看工作区与指定提交之间的差异：
```
git diff <commit_id>
```

4. 查看工作区与暂存区的差异，并显示详细的文件差异信息：
```
git diff --stat
```

5. 查看工作区与暂存区的差异，并显示详细的文件差异信息，包括行数变化：
```
git diff --stat -M
```

6. 查看工作区与暂存区的差异，并显示详细的文件差异信息，包括新增、修改和删除的文件：
```
git diff --name-status
```

7. 查看工作区与暂存区的差异，并显示详细的文件差异信息，包括新增、修改和删除的文件，以及具体的文件内容差异：
```
git diff --name-status -C
```

git restore --staged .
`git restore --staged .`命令的作用是撤销已经暂存（add）的文件。

git restore -h
usage: git restore [<options>] [--source=<branch>] <file>...

    -s, --source <tree-ish>
                          which tree-ish to checkout from
    -S, --staged          restore the index
    -W, --worktree        restore the working tree (default)
    --ignore-skip-worktree-bits
                          do not limit pathspecs to sparse entries only
    --pathspec-from-file <file>
                          read pathspec from file
    --pathspec-file-nul   with --pathspec-from-file, pathspec elements are separated with NUL character

具体来说，这个命令会将当前目录下所有已经通过`git add`命令添加到暂存区的文件还原到工作区，同时保留这些文件的修改状态。也就是说，这些文件并没有被删除，只是不再作为下一次提交的内容。如果需要再次提交这些文件，可以使用`git add`命令重新将它们添加到暂存区。

如果你想要取消已经使用`git add`命令添加（即暂存）的文件，你可以采取以下步骤：
1. 如果你想撤销已经添加（git add）到暂存区的单个文件，可以使用 `git reset` 命令。具体的命令格式是：`git reset <file>`。在这里，`<2009-11-28 20:55:48Z d36078e8c3d9$ git add *.txt`
To unstage all the "*.txt" files that were added, you can use the command `git reset *.txt`. This will remove these files from the staging area and leave them in your working directory.
2. 另一种方法是使用`git restore`命令来取消Git add操作并删除已添加到暂存区的文件。你可以使用`git restore --staged <file>`命令，其中`<file>`是你想要从暂存区中移除的文件名。
3. 如果你误添加了整个目录，你可以使用`git restore --staged .`来取消暂存所有文件。
4. 如果你不想保留对已暂存文件的修改，可以使用`git reset --hard HEAD~1`命令来取消暂存并还原文件到上一次提交的状态。

git revert和reset

git revert 用法
一、初级用法
git revert撤销某次操作，此次操作之前和之后的commit和history都会保留，并且把这次撤销，作为一次最新的提交。
git revert HEAD                  撤销前一次 commit
git revert HEAD^               撤销前前一次 commit
git revert commit_id （比如:fa042ce57ebbe5bb9c8db709f719cec2c58ee7ff）

 git revert是提交一个新的版本，将需要revert的版本的内容再反向修改回去，版本会递增，不影响之前提交的内容.

Tip : 通常情况下，上面这条revert命令会让程序员修改注释，这时候程序员应该标注revert的原因，假设程序员就想使用默认的注释，可以在命令中加上-n或者--no-commit，应用这个参数会让revert 改动只限于程序员的本地仓库，而不自动进行commit，如果程序员想在revert之前进行更多的改动，或者想要revert多个commit。

二、进阶用法
当有多个commit需要撤销，有可能是连续的，或是不连续的，那该怎么操作？

1.连续
git revert -n commit_id_start..commit_id_end
使用该命令可以将提交撤回到commit_id_start的位置

2.不连续
git revert -n commit_id_1
git revert -n commit_id_3
使用该命令可以撤回到commit_id_1和commit_id_3的提交

1.git删除远程分支 git push origin --delete [branch_name]
2.删除本地分支区别 git branch -d 会在删除前检查merge状态(其与上游分支或者与head)。 
3.git查看分支: 查看本地分支 git branch 查看远程分支 git branch -r 查看本地和远程分支 git branch -a
4.git删除分支: 删除本地分支 git branch -d 本地分支名 删除远程分支 git push origin --delete [branch_name]

git push origin --delete master
remote: Powered by GITEE.COM [GNK-6.3]
remote: error: By default, deleting the current branch is denied, because the next
remote: 'git clone' won't result in any file checked out, causing confusion.
remote:
remote: You can set 'receive.denyDeleteCurrent' configuration variable to
remote: 'warn' or 'ignore' in the remote repository to allow deleting the
remote: current branch, with or without a warning message.
remote:
remote: To squelch this message, you can set it to 'refuse'.
remote: error: refusing to delete the current branch: refs/heads/master
To gitee.com:edidada/mypagehelper.git
 ! [remote rejected] master (deletion of the current branch prohibited)
error: failed to push some refs to 'gitee.com:edidada/mypagehelper.git'

原因 master是默认分支，不能删除

git branch -d main
error: The branch 'main' is not fully merged.
If you are sure you want to delete it, run 'git branch -D main'.

git reset vs恢复
那我们学到了什么？ 好吧，当我们git reset到先前的提交并推送到远程存储库时，不会发布任何撤消提交的痕迹。 这与git revert形成了鲜明的对比，在git revert中，revert命令本身会创建一个新的提交，并且不会丢失过去的提交历史。 因此，如果您想使用Git 撤消先前的提交 ，则reset是使用而不是还原的正确Git命令。

https://juejin.cn/post/6844904005773213704

远程仓库新建有分支
本地仓库分支已经存在

报错信息

实验计划:

本地仓库A，新建master，提交到远程仓库

从远程仓库复制一份，新建分支dev，提交到远程仓库，本地仓库称为B

仓库A新建dev分支，git pull一下

[如何使用.gitignore忽略Git中的文件和目录](https://blog.csdn.net/Q1761991696/article/details/123572766)

问：IDEA解决git冲突
答：先执行'git add'命令

git 锁分支，不能新提交
多分支合并

本地a分支 直接合并b分支
pull = fetch + merge

git fetch 和git pull 的差别

git fetch 相当于是从远程获取最新到本地，不会自动merge
git fetch orgin master //将远程仓库的master分支下载到本地当前branch中
git log -p master ..origin/master //比较本地的master分支和origin/master分支的差别
git merge origin/master //进行合并
git pull：相当于是从远程获取最新版本并merge到本地
git pull origin master
git pull <远程主机名> <远程分支名>:<本地分支名>

https://www.jianshu.com/p/b00fea3ba207

免密登录 ssh key
gpg

freebsd 免密登录

https://centos.pkgs.org/7/endpoint-x86_64/git-2.23.0-1.ep7.x86_64.rpm.html

https://packages.endpoint.com/rhel/7/os/x86_64/git-2.23.0-1.ep7.x86_64.rpm

git centos 7新版本安装
https://blog.csdn.net/caimengyuan/article/details/80634752

yum search git
yum remove -y git | yum -y install git2u

rpm包名称可能是git224

```shell
git branch 0a
192:LangNote ibqo$ git branch -a
  0a
* master
  remotes/b/master
  remotes/origin/master
```

```shell
git branch -d 0a
Deleted branch 0a (was 99c7b17).
192:LangNote ibqo$ git branch -a
* master
  remotes/b/master
  remotes/origin/master
```

git 回退到某个commit
回退命令:
$ git reset --hard HEAD^ 回退到上个版本
$ git reset --hard HEAD~3 回退到前3次提交之前,以此类推,回退到n次提交之前
$ git reset --hard commit_id 退到/进到 指定commit的..

git config  user.name "Wdidada Tom In Dell R630"
git config  user.email "sandisks555@gmail.com"

[How to “git clone” including submodules](https://stackoverflow.com/questions/3796927/how-to-git-clone-including-submodules)

```
git remote rename origin old-origin
git remote add origin git@gitlab.com:edidada/buildgrpc.git
git push -u origin --all
git push -u origin --tags
```

下次关注下配置库 自己的配置有没有被别人回滚了

git 查看某个文件的更新历史 更新时间

ssh

[git error stackoverflow](https://stackoverflow.com/questions/9393409/ssh-could-not-resolve-hostname-github-com-name-or-service-not-known-fatal-th)

[git 报错](https://www.cnblogs.com/niuniui/p/8783273.html)

插槽不会git回退

https://www.liaoxuefeng.com/wiki/896043488029600/897013573512192

fatal: refusing to merge unrelated histories

`git merge origin/master  --allow-unrelated-histories`

[git fork后同步更新](https://blog.csdn.net/csm201314/article/details/83045605)

#### git 统计代码行数

```shell
git log --author="edidada" --pretty=tformat: --numstat | awk '{ add += $1; subs += $2; loc += $1 - $2 } END { printf "added lines: %s, removed lines: %s, total lines: %s\n", add, subs, loc }' -
```

`git clone -b branchname`

[git fork之后，再次同步](https://blog.csdn.net/qq1332479771/article/details/56087333)

```

warning: the following paths have collided (e.g. case-sensitive paths
on a case-insensitive filesystem) and only one from the same
colliding group is in the working tree:

  'googletest/docs/FAQ.md'
  'googletest/docs/faq.md'
  'googletest/docs/Primer.md'
  'googletest/docs/primer.md'
  'googletest/docs/Samples.md'
  'googletest/docs/samples.md'

```

git@github.com:apache/incubator-shardingsphere.git

[git reset 回退到某一版本](https://blog.csdn.net/pzhtpf/article/details/52212671)

git merge完全解析
https://www.jianshu.com/p/58a166f24c81

https://blog.csdn.net/u012150179/article/details/14047183

现在，我们把dev分支的工作成果合并到master分支上：

```
$ git merge dev
Updating d46f35e..b17d20e
Fast-forward
 readme.txt | 1 +
 1 file changed, 1 insertion(+)
```

git merge命令用于合并指定分支到当前分支。合并后，再查看readme.txt的内容，就可以看到，和dev分支的最新提交是完全一样的。
注意到上面的Fast-forward信息，Git告诉我们，这次合并是“快进模式”，也就是直接把master指向dev的当前提交，所以合并速度非常快。
当然，也不是每次合并都能Fast-forward，我们后面会讲其他方式的合并。

廖雪峰 git js

`git fetch`
`git merge`

远程仓库的备份

https://blog.csdn.net/csm201314/article/details/83045605

git reset ff391a57c55ffaf3a625de19bd7af218e4037e1a

https://stackoverflow.com/questions/14040754/deleting-remote-master-branch-refused-due-to-being-current-branch

#### git

https://blog.csdn.net/qq_32452623/article/details/54340749

[git 获取指定的tag处代码](https://blog.csdn.net/jeffasd/article/details/72520668)

[git命令－切换分支](http://www.cnblogs.com/smiler/p/6924583.html)

`git ls-files -u  | cut -f 2 | sort -u`

#### git忽略指定文件夹

.gitignore

target/

[git丢弃本地修改的所有文件](https://blog.csdn.net/leedaning/article/details/51304690)

`git checkout .`

```

git log --author="edidada" --pretty=tformat: --numstat | awk '{ add += $1; subs += $2; loc += $1 - $2 } END { printf "added lines: %s, removed lines: %s, total lines: %s\n", add, subs, loc }' -

```

[Mac、Windows下git log中文乱码](https://www.jianshu.com/p/df01196bd4db)

windows下是gbk编码

git fetch origin

[ls-files](https://git-scm.com/docs/git-ls-files)

git config --list --gloable

```shell
git add .
git status
On branch master
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

        modified:   README.txt
        modified:   benchmarks.rb
```

[Git 修改已提交的commit注释](https://www.jianshu.com/p/098d85a58bf1)

`git commit --amend`

[GIT Submodule的使用](https://www.jianshu.com/p/0107698498af)

git submodule add git@github.com:google/googletest.git

https://git-scm.com/book/en/v2/Git-Tools-Submodules

git submodules add 当前文件夹不能有同名子文件夹，不然报错

https://blog.csdn.net/guotianqing/article/details/82391665
git module 删除

 https://stackoverflow.com/questions/1777854/how-can-i-specify-a-branch-tag-when-adding-a-git-submodule

切换子模块分支

[Git之同一台电脑连接多个远程仓库](https://www.cnblogs.com/zhengyan/p/10728527.html)

 https://www.cnblogs.com/zhengyan/p/10728527.html

#### 测试git能否连接github

https://blog.csdn.net/littlehaes/article/details/102082142

Permission denied (publickey).报错解决

ssh-keygen之后，

#### 把ssh 添加到keychain中

ssh-add -K /Users/youre_user_name/.ssh/id_rsa

Could not open a connection to your authentication agent.

报错解决

https://www.cnblogs.com/sheldonxu/archive/2012/09/17/2688281.html

ssh-agent bash

电脑断网

`Please make sure you have the correct access rights`

git windows

bash

不能输入e等字符

git 主机连接多个git仓库 指定私钥文件 ssh可以指定

https://www.jianshu.com/p/ea50640ff704

##### Git fork后如何同步源仓库更新

[fork后如何同步源仓库更新](https://www.cnblogs.com/leisurelylicht/p/Git-fork-hou-ru-he-tong-bu-yuan-cang-ku-geng-xin.html)

```shell
1. 设置源仓库的远程地址
>> git remote add [新地址名称] [源仓库远程地址]
>> git remote add upstream https://github.com/leisurelicht/wtfpython-cn

2. 同步fork
>> git fetch [新地址名称]
>> git fetch upstream

3. 本地切换到想要更新的分支上
>> git checkout [branch]
>> git checkout master

4. 把源仓库的远程分支合并到本地
>> git merge [新地址名称/分支]
>> git merge upstream/master

5. 更新到自己的远程库上
>> git push origin master
```

ls

issue-5234-dev

[how to delete all commit history in github](https://stackoverflow.com/questions/13716658/how-to-delete-all-commit-history-in-github)

要删除远程分支，可以使用以下命令：

```bash
git push origin --delete <branch_name>
```

其中，`<branch_name>`是要删除的远程分支的名称。
例如，要删除名为 `feature/branch1`的远程分支，可以运行以下命令：

```bash
git push origin --delete feature/branch1
```

请注意，此命令将从远程仓库中永久删除指定的分支。确保在执行此操作之前，你已经确认了要删除的分支，并且在删除之前进行了必要的备份或合并操作。

## 源代码
git clone https://github.com/git/git
git clone https://github.com/git/git.git
cd git
git checkout v2.43.0
git submodule init
git submodule update
make prefix=/usr/local install install-doc install-html install-info

## git-lfs

