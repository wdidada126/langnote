# 项目 9：MiniGit — 哈希寻址对象库与 commit DAG

> 对应讲次：L20–L22（哈希寻址）、L29–L31（DAG 遍历/连通）、L36（路径的"前缀树式"逐级解析，仓库侧）、L37（对象序列化）；即 **Project 3 GITLET** 的核心骨架，也是 6.824 content-addressed storage 的最小样本。
> 真实 Git 对照：`git hash-object / cat-file / log --graph`。

## 结构与知识点

```
<repoDir>/
├─ HEAD                     # 当前分支名（文本文件）
├─ refs/heads/<branch>      # 分支 = 一个 40 字符 commit id 的文件 ⇒ 分支/切换 O(1)
└─ objects/xx/yyy...        # 内容寻址库：SHA-1 前 2 位分桶（两级哈希，同 Git）
对象格式: "type size\0content"   # blob 与 commit 同构；读回重哈希 = 自带完整性校验
```

| 组件 | 讲次知识点 | 说明 |
| --- | --- | --- |
| `ObjectStore` | L20 哈希、L37 I/O | 同内容同 ID ⇒ **去重/幂等**；防篡改（Merkle 式思想的前半） |
| `MiniGit.commit` | L07 record/Map、L23 有序快照 | parent 指针 + TreeMap 快照序列化（字典序稳定 ⇒ 可复现哈希） |
| `MiniGit.log/findFile` | L29–L30 图遍历 | 沿父链回溯（DAG 退化为链；多父合并=真正的 GITLET 难点，留扩展） |
| `branch/checkout` | L15 "成本写进 API" | 建分支/切分支只写一个小文件，不复制任何数据 |

## 编译与运行（JDK 17）

```bash
./build.sh        # 或 Windows: build.bat
javac -encoding UTF-8 -d build src/cs61b/minigit/*.java
java -cp build cs61b.minigit.Main   # 自动在系统临时目录建演示仓库并跑断言
```

## 与真实 Git 的差异（诚实清单）

1. 省略 tree 对象：commit 直挂"路径→blob"快照（GITLET 里 `git ls-tree` 层被压扁）。
2. 单父链：未实现 merge 与两个特殊父情形（LCA/findCommonAncestor）。
3. 明文对象：无 zlib 压缩与 delta 打包（`packfile` 是 L34/L37 的进阶应用）。
4. 全量快照：真实 Git 用"引用不变 + tree 共享"实现提交间 O(改变文件数) 存储——这正是 **CS61A 持久化数据结构**思想的工业版。

## 实验建议

1. 加上 tree 对象（路径按 '/' 逐级拆层——就是 L36 的 Trie），让 `findFile` 走 tree 链。
2. 支持 merge：commit 携带 `parents:` 列表，`log` 改成带 visited 集的 DFS（Lab9 代码直接复用）。
3. 用 `git init && git hash-object -w` 与本项目对拍同一文件的 ID（格式一致：`blob <len>\0`），亲眼确认"简化≠错误"。
