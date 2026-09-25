# ch07-linking —— 链接、符号解析与库组织实验

**关联讲次**：L12（目标文件/符号解析/重定位）、L13（共享库与装载）。

## 文件

| 文件 | 作用 |
| --- | --- |
| `src/main.c` | 主驱动：调用静态库函数、弱符号、跨库依赖 |
| `src/vec.c` | 编入 `libvec.a`（演示 ar 归档按需抽取） |
| `src/weakdemo.c` | `int shared_counter;` 暂定义（规则 2/3 道具） |
| `src/strongdef.c` | `int shared_counter = 100;` 强定义（规则 2 道具） |
| `src/foo.c` + `src/bar.c` | 分装 `liba.a`/`libb.a`：库依赖顺序道具 |
| `src/dynlib.c` | 共享库源码（`-fPIC -shared` / `cl /LD`） |
| `src/dynload.c` | `dlopen`（POSIX）/ `LoadLibrary`（Windows）双版运行期装载 |

## 构建

```sh
make            # static + order + dyn 三件套
make weak_demo  # 实验①：强/弱符号
make run
# 或直接 ./build.sh
```
```bat
:: Windows：先 call vcvarsall.bat x64
build.bat
```

## 实验①：符号解析规则（L12 核心）

```sh
# 1) 只有暂定义 → 输出 0
gcc -O1 src/main.c src/weakdemo.c src/vec.c src/foo.c src/bar.c -o bin/t1
# 2) 暂定义 + 强定义，-fcommon（老规则）→ 强胜弱，输出 100
gcc -O1 -fcommon ... src/strongdef.c -o bin/t2
# 3) 同 2 但默认 -fno-common（GCC≥10）→ 链接期 multiple definition 报错
```
亲手看到"当年能链过、现在报错"——就是 CSAPP 规则 3 在现代被收紧的现实版本。

## 实验②：静态库顺序

```sh
make order_ok   # liba.a(依赖方) 在前 → 成功
make order_bad  # 故意反序 → 预期 "undefined reference to 'foo'"
```
链接器对归档**一次扫描即弃**：被依赖的库必须放在依赖者右边。

## 实验③：共享库与运行期装载（L13）

```sh
readelf -d bin/dynload | head       # DT_NEEDED 里没有 libdyn → dlopen 是"自己调 dlopen"
nm -D bin/libdyn.so                 # 动态符号表
LD_DEBUG=bindings ./bin/dynload     # 观察符号绑定过程（GOT 填充）
```
Windows：`dumpbin /exports bin\dyn.dll` 对应 `nm -D`。

## 观察点小结

- `.text/.data/.bss` 归属（`size`/`readelf -S`）。
- `ar r` 归档成员抽取粒度 = 目标文件。
- dlopen 的程序把"链接期"推迟到"运行期"（L13 装载时刻表的最后一段）。
