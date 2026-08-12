# libdill

## 官网
https://libdill.org/

## source code
https://github.com/sustrik/libdill

## 测试代码
https://github.com/edidada/testlibdill

wget https://libdill.org/libdill-2.14.tar.gz
tar -xzf libdill-2.14.tar.gz 
cd libdill-2.14
./configure
make
sudo make install

1009 #define dns_opts(...) (&dns_quietinit((struct dns_options)DNS_OPTS_INIT(__V     A_ARGS__)))


你遇到的这个编译错误：

```
dns/dns.h:1009:24: error: lvalue required as unary ‘&’ operand
 1009 | #define dns_opts(...) (&dns_quietinit((struct dns_options)DNS_OPTS_INIT(__VA_ARGS__)))
      |                        ^
ipaddr.c:335:47: note: in expansion of macro ‘dns_opts’
  335 |         dill_dns_hosts, dill_dns_hints, NULL, dns_opts(), &rc);
      |                                               ^~~~~~~~
```

是一个在 **C语言中对临时对象（rvalue）取地址** 的语法错误。

---

## 错误分析

### 出错代码：
```c
#define dns_opts(...) (&dns_quietinit((struct dns_options)DNS_OPTS_INIT(__VA_ARGS__)))
```

### 分解一下这段宏的作用：
- `dns_quietinit(...)` 是一个函数或宏，用于初始化一个 `struct dns_options`。
- `(struct dns_options)DNS_OPTS_INIT(...)` 是一个结构体复合字面量（compound literal），创建了一个**临时结构体对象（rvalue）**。
- 然后用 `&` 对这个临时对象取地址 —— 这是非法的！

---

## ❌ 为什么不能对临时变量取地址？

在 C 中，复合字面量虽然有地址，但它的生命周期只到当前作用域结束。不过更关键的是，某些编译器版本或者特定编译器（比如 GCC 的某些模式）会对这种写法报错，尤其是当它被当作临时表达式使用时。

你的编译器不允许你对一个临时构造的结构体取地址。

---

## ✅ 解决方案

这个问题在 libdill 的较新版本中已经修复了。如果你使用的是官方发布的 `libdill-2.14.tar.gz`，那么这是一个已知的 bug。

### ✅ 方法一：打补丁（推荐）

你可以手动修改 `dns/dns.h` 文件第 1009 行的宏定义，将：

```c
#define dns_opts(...) (&dns_quietinit((struct dns_options)DNS_OPTS_INIT(__VA_ARGS__)))
```

改为：

```c
struct dns_options dns_opt_storage;
#define dns_opts(...) (dns_quietinit(&(struct dns_options){DNS_OPTS_INIT(__VA_ARGS__)}))
```

或者更稳妥一点：

```c
#define dns_opts(...) ({ \
    struct dns_options* opts = malloc(sizeof(struct dns_options)); \
    if (opts) { \
        *opts = (struct dns_options)DNS_OPTS_INIT(__VA_ARGS__); \
        dns_quietinit(opts); \
    } \
    opts; \
})
```

> ⚠️ 注意：如果使用 `malloc`，你需要确保后续释放内存，否则会泄漏。

---

### ✅ 方法二：升级到最新版源码（推荐）

libdill 的 GitHub 仓库已经修复了这个问题。建议你从 GitHub 获取最新源码：

```bash
git clone https://github.com/sustrik/libdill.git
cd libdill
./autogen.sh
./configure
make
sudo make install
```

GitHub 地址：https://github.com/sustrik/libdill

---

### ✅ 方法三：禁用 DNS 功能（临时绕过问题）

如果你不需要 libdill 的 DNS 相关功能，可以尝试在配置时禁用：

```bash
./configure --disable-dns
```

这样就不会编译涉及 DNS 的部分代码，自然也就不会触发这个错误。

---

## 验证是否解决

完成修改或更新后重新编译：

```bash
make clean
make -j$(nproc)
sudo make install
```

---

## ✅ 总结

| 问题原因 | 对临时结构体取地址 |
|----------|--------------------|
| 编译器报错 | `lvalue required as unary ‘&’ operand` |
| 解决方式 | 修改宏定义、升级源码、或禁用 DNS 模块 |

---

如果你需要我帮你生成一个完整 patch 文件或提供修改后的文件内容，请告诉我，我可以直接贴出来供你替换。

是否要我帮你写一个完整的 `dns/dns.h` 替换文件？