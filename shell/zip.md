# zip

在 Linux 系统中，你可以使用 `zip` 命令将整个文件夹打包为 `.zip` 格式的压缩包。以下是完整的命令示例：

---

### ✅ 命令格式：

```bash
zip -r 压缩包名称.zip 要压缩的文件夹路径/
```

---

### ✅ 示例：

假设你要将名为 `my_folder` 的文件夹打包成 `backup.zip`：

```bash
zip -r backup.zip my_folder/
```

---

### 🛠️ 常用选项说明：

- `-r`：递归处理，用于压缩整个目录及其子目录中的所有文件。
- 如果没有安装 `zip` 工具，可以通过以下方式安装（根据你的发行版）：

  - Debian/Ubuntu：
    ```bash
    sudo apt update && sudo apt install zip
    ```

  - CentOS/RHEL：
    ```bash
    sudo yum install zip
    # 或者对于较新的版本：
    sudo dnf install zip
    ```

  - Fedora：
    ```bash
    sudo dnf install zip
    ```

---

### 📁 额外技巧：

如果你希望压缩时排除某些文件或文件夹，可以这样做：

#### 示例：排除 `.git` 和 `logs` 文件夹

```bash
zip -r backup.zip my_folder/ -x "my_folder/.git/*" -x "my_folder/logs/*"
```

或者更通用的方式：

```bash
cd /path/to/parent
zip -r backup.zip folder_name -x "*.git*"
```

---

如需进一步压缩，还可以加上 `-q`（静默模式）或 `-O` 指定输出文件编码等参数。

需要我帮你写一个 shell 脚本来自动打包并命名时间戳吗？
