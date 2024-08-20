# just
如果在 Windows 上使用 `just build test` 命令时找不到 `just`，可能是因为你没有安装 `just` 或者它没有正确配置在你的系统路径中。

### 什么是 `just`？
`just` 是一个命令行工具，可以用于构建脚本、任务自动化等。如果你在执行该命令时收到“找不到 just”的错误，说明系统无法找到该工具。

### 解决方法：
1. **检查是否已安装 `just`：**
   - 如果未安装 `just`，你需要先安装它。

2. **在 Windows 上安装 `just`：**
   - **通过 Scoop 安装：**
     如果你使用 [Scoop](https://scoop.sh/) 包管理器，可以通过以下命令安装 `just`：
     ```powershell
     scoop install just
     ```

   - **通过 Chocolatey 安装：**
     如果你使用 [Chocolatey](https://chocolatey.org/) 包管理器，可以通过以下命令安装 `just`：
     ```powershell
     choco install just
     ```

   - **手动安装：**
     你也可以从 `just` 的 [GitHub Releases](https://github.com/casey/just/releases) 页面下载 Windows 可执行文件，并将其添加到系统路径中。

3. **将 `just` 添加到系统路径：**
   - 如果你手动下载了 `just`，需要将其路径添加到 `PATH` 环境变量中。可以通过以下步骤完成：
     1. 打开“开始”菜单，搜索“环境变量”并选择“编辑系统环境变量”。
     2. 点击“环境变量”按钮。
     3. 在“系统变量”部分找到并选择 `Path`，然后点击“编辑”。
     4. 点击“新建”，然后输入 `just` 所在的目录路径。
     5. 点击“确定”保存。

4. **重启终端：**
   - 如果你已经安装并配置了 `just`，但仍然无法找到，请尝试重启你的命令行终端，以确保新的 `PATH` 环境变量生效。

### 验证安装：
安装完成后，可以通过以下命令验证是否安装成功：
```bash
just --version
```
如果返回版本号，说明 `just` 已经成功安装并可以使用。

### 总结
确保安装并正确配置了 `just`，然后重新运行 `just build test` 命令。