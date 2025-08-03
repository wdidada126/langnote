# nrm

nrm ls
  npm ---------- https://registry.npmjs.org/
  yarn --------- https://registry.yarnpkg.com/
  tencent ------ https://mirrors.tencent.com/npm/
  cnpm --------- https://r.cnpmjs.org/
  taobao ------- https://registry.npmmirror.com/
  npmMirror ---- https://skimdb.npmjs.com/registry/
  huawei ------- https://repo.huaweicloud.com/repository/npm/
* jf ----------- http://172.16.10.70:4873/


nrm add jf http://172.16.10.70:4873/ && nrm ls 
$ nrm use jf //切换源

nrm 只是辅助 npm 工作的一个小工具（专门管镜像源的）
nrm (npm Registry Manager)
领域：Node.js / JavaScript 生态系统。
用途：nrm 是一个命令行工具，用于管理和切换 npm 的包注册表（registry）。
功能：
查看当前可用的 npm 镜像源（如官方源、淘宝源、腾讯源等）。
快速切换到不同的镜像源（例如，切换到 https://registry.npmmirror.com 以加速国内的包下载）。
测试不同镜像源的响应速度。
类比：你可以把它想象成“npm 的镜像源切换器”或“包管理器的网络加速器”。它本身不安装包，而是改变 npm 或 yarn 等包管理器从哪里下载包。
核心作用：解决网络问题，加速包的下载。


在命令 `npm i JF-UI@0.2.7 --D` 中，`--D` 是 `--save-dev` 的简写。

### 详细解释：

*   `npm i`：是 `npm install` 的缩写，用于安装包。
*   `JF-UI@0.2.7`：指定要安装的包名（`JF-UI`）和具体的版本号（`0.2.7`）。
*   `--D` 或 `--save-dev`：这个标志表示将该包作为开发依赖（`devDependencies`）安装。

### `devDependencies`（开发依赖）是什么？

开发依赖是指那些在开发和构建项目时需要，但在最终生产环境运行时不需要的包。常见的例子包括：
*   代码打包工具（如 Webpack, Vite）
*   代码编译器（如 Babel, TypeScript）
*   代码格式化工具（如 Prettier）
*   代码质量检查工具（如 ESLint）
*   单元测试框架（如 Jest, Mocha）

### 与 `--save` 的区别

*   `--save` (或 `-S`)：将包安装为生产依赖（`dependencies`），这些包是项目在生产环境中运行所必需的。它们会被记录在 `package.json` 文件的 `"dependencies"` 字段下。
*   `--save-dev` (或 `-D`)：将包安装为开发依赖（`devDependencies`），这些包仅用于开发和构建过程。它们会被记录在 `package.json` 文件的 `"devDependencies"` 字段下。

### 总结

所以，`npm i JF-UI@0.2.7 --D` 这条命令的意思是：
安装 `JF-UI` 包的 `0.2.7` 版本，并将其作为开发依赖添加到 `package.json` 文件中。

> 注意：在较新版本的 npm（v5.0.0+）中，`npm install <package-name>` 默认会将包作为生产依赖安装（相当于 `--save`）。如果要明确安装为开发依赖，必须加上 `--save-dev` 或 `-D` 参数。