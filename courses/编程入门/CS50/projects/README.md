# Harvard CS50x（2025）— 配套项目计划（骨架）

> 本轮不写代码。主线：官方 PSET0–9 逐周完成（VS Code 云端 codespaces 或本地 csdev 环境），Final Project 收束；每行给出与讲义对应的练习与运行方式。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L0 Scratch | Scratch 3 | PS0：个人 Scratch 小游戏/动画（变量+循环+条件） | https://scratch.mit.edu 在线 |
| L1 C | C | PS1 Mario（more）：嵌套循环打印金字塔 | `make mario && ./mario` |
| L2 C | C | PS2 Cash：找零最少硬币数（规避浮点误差） | `make cash && ./cash` |
| L3 C | C | 算法实验：手写 linear/binary search + selection/bubble sort 并计时 | `make sort && ./sort` |
| L4 C | C | PS4 Filter（less/more）：BMP 灰度/模糊处理；或 Recovery 修复 JPEG | `./filter-less input.bmp output.bmp` |
| L5 C | C | 迷你散列表：链表桶 + djb2 哈希，插入/查找/删除 | `make hash && ./hash` |
| L6 Python | Python | PS6 DNA：统计序列中 STR 拷贝数（dict 应用） | `python dna.py sequences.csv person.txt` |
| L7 SQL | SQLite | PS7 数据库练习：自建歌曲/图书库 + 10 条查询（JOIN/GROUP BY） | `sqlite3 library.db < queries.sql` |
| L8 Web | HTML/CSS/JS | 个人主页三件套 + fetch 调用公开 API 展示数据 | 浏览器直接打开 / `python -m http.server` |
| L9 Flask | Python | PS9 Finance：股票买卖全栈应用（登录/持仓/报价 API） | `flask run` |
| L10 综合 | 自选 | Final Project：端到端小系统（含 DB + Web + 测试），提交设计与演示视频 | 按选题工具链 |

## 验收清单
- [ ] PS0–PS9 全部通过 submit50；
- [ ] Final Project 覆盖至少两种课内技术栈（如 C+Python 或 SQL+Flask）。
