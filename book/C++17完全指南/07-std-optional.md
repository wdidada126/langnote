# 07 std::optional——栈上的「可能没有值」

> 覆盖原书 **Part III 第 15 章**（`std::optional`）。
> 一句话：**给「值 + 存在性」一个不需要 new、不需要哨兵值、不需要异常也能表达「没有」的栈上载体**。
> 互链：[../C++17完全指南.md](../C++17完全指南.md)｜[../C++系列·总索引.md](../C++系列·总索引.md)｜[08-std-variant与std-any与std-byte.md](08-std-variant与std-any与std-byte.md)

## 核心概念速览（中英对照）

- **可选值** — `std::optional<T>`：对象内直接存放 `T`（或无），拷贝/移动/析构语义与 `T` 一致。
- **带标签的空值** — `std::nullopt` / `std::nullopt_t`：写 `return std::nullopt;` 表示「没有值」，参与比较与构造。
- **两种访问档位** — `value()` vs `operator*`：前者无值时抛 `std::bad_optional_access`（实测消息 `bad optional access`），后者**不检查、UB**。
- **就地构造** — `emplace` / `std::in_place`：值直接长在 optional 的存储里，实测零次额外拷贝/移动。
- **安全取默认** — `value_or(d)`：无值返回 `d`，有值返回内容（实测空 optional 得 7）。
- **比较次序** — optional 的有序比较：**空值小于任何有值**；`==` 对空值恒为 false（两条实测陷阱）。
- **单播语义** — monadic operations（C++23）：`transform`/`and_then`/`or_else`，把 optional 串成表达式而不嵌套解包。
- **可期望类型** — `std::expected<T, E>`（C++23）：optional 的直接后继，把「没有」升级为「为什么没有」。

## 动机：三种老方案的共同病

| 老方案 | 病例 |
| --- | --- |
| 返回 `T` + 哨兵值（`-1`、`npos`、空字符串） | 合法值域被占用；`find` 返回 -1 分不清「没找到」和「值是 -1」 |
| 返回 `T*` / 迭代器 + 判空 | 所有权含混；指到栈对象还是堆？谁负责释放？ |
| `bool f(const T& out)` 出参 / 抛异常 | 出参绕过 const 与移动；用异常表达「查无此人」既贵又鼓励吞掉 |

`optional<T>` 是第四种：**值语义 + 显式存在性 + 无堆分配**。函数签名自己说明一切：
`std::optional<User> find_user(id_type)` 不可能被误读成「总能拿到东西」。

## 机制与实测证据

### 1. 基本行为（已实测 g++ 15.2 -std=gnu++17，输出原样记录）

```cpp
std::optional<std::string> o = "hi";
// *o == "hi"，o->size() == 2，o.has_value() == 1
std::optional<int> empty;
empty.value_or(7)        // 7（实测）
empty.value()            // 实测抛出，what(): "bad optional access"
o.emplace(3, 'a');       // 原地重构造 -> "aaa"（实测）
o.reset();               // 变空（实测 has_value()==0）
```

### 2. 拷贝/移动计数（编译器外置 counter，实测数字）

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17
std::optional<M> a{std::in_place, 1};   // 就地构造：0 拷贝 0 移动
std::optional<M> b = a;                 // 左值 -> 拷贝 1 次
std::optional<M> c = std::move(b);      // 右值 -> 移动 1 次
M m = std::move(*c);                    // 从 optional 里搬走 -> 再移动 1 次
// 实测合计：copies=1 moves=2
```

**两个实测细节**：
- `std::move(*c)` 之后 `c` 仍然 `has_value()==1`（里面的 `M` 处于「被移动后」状态）——**optional 本身不会因移出内容而变空**；要变空必须 `c.reset()`。
- 把**有值** optional 移动赋给**空** optional：实测源 `c` 依旧有值（`copies=1 moves=3 c有值=1 d有值=1`）——别指望 `std::move` 帮你清源。

### 3. 内存布局与比较（实测）

```cpp
sizeof(std::optional<int>)     // 8（int 4B + 判别 1B + 对齐填充；布局是实现细节，别当契约 ⚠️）
sizeof(std::optional<std::string>) // 40，而 sizeof(std::string)==32（MinGW libstdc++ 15 实测）
```

比较陷阱（实测原样输出）：

```cpp
std::optional<int> o;                      // 空
(o == 42)   // 0 ——「空值不等于任何值」，哪怕你想表达的是「值等于 42」
(o < 42)    // 1 ——空值排在一切有值之前；排序时 optional 的序是「先有无、再大小」
std::optional<bool> ob = false;
(bool)ob    // 1 ——operator bool 测「有值」，不是「值为真」！
```

最后一行是真实生产事故源：`if (parse_flag(input))` 在 `parse_flag` 返回 `optional<bool>` 时，
**有值且为 false 也会进分支**。必须写 `if (ob && *ob)`（实测确认此语义）。

### 4. 引用装不下（实测负例）

```cpp
// 🔧 已实测 g++ 15.2：-std=gnu++17 与 -std=gnu++26 均拒绝
std::optional<int&> r = x;
// 错误原文（片段）：non-static data member '..._M_value' in a union may not have reference type 'int&'
```

C++26 的 **P2988「Add support for optional references」**（wg21.link/p2988 实测可达，当前修订 R12 ✅）
会把 `optional<T&>` 变成合法——但本机 GCC 15.2 的 C++26 档位**尚未实现**，引用需求目前仍用
`std::optional<std::reference_wrapper<T>>` 或裸指针过渡。

## 权衡

| 决策点 | optional<T> | T* / bool+出参 / 异常 |
| --- | --- | --- |
| 表达「没有」 | ✅ 类型自明 | 指针混淆所有权；异常诱导 `catch(...)` |
| 栈上、无分配 | ✅（含值内嵌） | `new` 方案有分配；出参要求预构造 |
| 链式组合 | C++17 只能手写 `if (o) ...`；C++23 起 `transform/and_then/or_else`（实测 17 无此成员） | — |
| 表达「为什么没有」 | ❌ 只能表达「没有」 | 这正是 C++23 `expected<T,E>` 的空位（见下） |
| 放进容器 | 可以，但 `vector<optional<T>>` 的空间代价 = sizeof(T)+判别字节 | 哨兵值更省但更易错 |

## 相邻概念对比

- **vs `std::variant<T, std::monostate>`**：效果近似「optional 的变体实现」，语义上 variant 是「若干类型之一」，
  optional 是「T 或没有」；要访问「没有」时 `index()` 与 `has_value()` 各管各（见 `08`）。
- **vs `std::expected<T, E>`（C++23）**：optional 是 `expected<T, void>` 精神的子集。错误处理场景今天直接选
  expected（P0323R12，✅ 可达；本机实测 `-std=gnu++23` 下 `<expected>` 可用）。
- **vs `std::shared_ptr` 判空**：`shared_ptr` 的「空」携带所有权语义，optional 的「空」不携带任何资源。
- **值语义光谱**：`optional`（可能没有）→ `variant`（几种之一）→ `any`（任意可拷贝之一）→ `string_view`（值是别人的）——见 `08`/`09`。

## 最新演进与工业实践

**标准之后**
- **constexpr**：实测 `static_assert(std::optional<int>(5).value() == 5)` 在 **gnu++17 即通过**
  （optional 多数操作 C++17 起 constexpr；variant 同型断言也通过）。
- **C++20**：更严格的 constexpr 容器要求逐步补齐（P0798R8 本体是 C++23 的 monadic，见下；C++20 主要是
  把可选的 `emplace` 等进一步 constexpr 化 ⚠️ 逐条提案未核，口径以 cppreference 特性表为准）。
- **C++23 单播操作**：**P0798R8「Monadic operations for std::optional」**（wg21 可达 ✅，标题实测抓取）。
  实测本机：`-std=gnu++17` 报 `'class std::optional<int>' has no member named 'transform'`；
  `-std=gnu++23` 通过，`transform([](int v){return v*2;})` → `and_then` → `or_else` 链式跑通（输出 `42 42 -1`）。
- **C++23 expected**：P0323R12（✅），且 **P2505R5**（✅ 可达）为 expected 配同款 monadic 接口。
- **C++26**：P2988（✅ 可达）补 `optional<T&>`；`optional<optional<T>>` 的递归解除亦有提案在推进 ⚠️ 未核编号。

**工业实践与开源口径**
- **Abseil**：`absl::optional` 早于标准多年、现是标准别名的转发实现；其 `absl::StatusOr<T>` 走的是
  expected 路线——与本章「optional 只表达『没有』」的边界一致（`abseil/abseil-cpp`，00 当日实测 ≈18.1k★）。
- **`TartanLlama/expected`**（00 当日实测 ≈1.9k★）：C++17 项目里 optional 的常见替补。
- 纪律：**接口返回值优先 optional；需要错误原因直接上 expected**（C++17 项目用 `expected<T,E>` 库或
  `std::pair<T, error_code>`——后者见 `10` 的 filesystem error_code 风格）。

## 常见误区（实测）

1. **`std::move(opt)` 会清空 opt——错**：实测移动后源仍 `has_value()==1`；清空只有 `reset()`。
2. **`(bool)optional<bool>{false}` 是 false——错**：实测为 1；`operator bool` 测存在性。
3. **空 optional `== 42` 值得 false 说明「值不等于 42」——语义错**：它只说明「没有值」。判值先判存在。
4. **`*empty_opt` 会抛——错**：不抛、直接 UB（实测刻意未触发）；要带检查就 `value()`。
5. **`optional<T&>` 忘了它不存在——17/26 实测均被拒**：引用载荷用 `reference_wrapper`。
6. **拿 `sizeof(optional<T>)` 当 ABI 契约——错**：8/40 是本机构架实测值，判别字节位置是实现自由 ⚠️。

## 与其他章 / 其他笔记的联系

- ← 本目录 `03`：强制拷贝消除让 `return Inc{42};` 塞进 optional 的路径更省；in-place 是共同基座。
- → 本目录 `08`：`variant<T, monostate>` 与 optional 的关系；`visit` 对 optional 风格类型的替代。
- → 本目录 `12`：`to_chars`/`from_chars` 用 `errc` 而非 optional 报告失败——「为什么失败」派的做法。
- → [../C++标准库/08-特殊容器与字符串.md](../C++标准库/08-特殊容器与字符串.md)：同一作者的 C++11 版没有这些组件，对照读差异。
- → [../Effective_Modern_C++/03-转向现代C++.md](../Effective_Modern_C++/03-转向现代C++.md)：「返回对象而非出参」的条款论证。
- → [../现代C++实战30讲/05-异常与错误处理的现代化.md](../现代C++实战30讲/05-异常与错误处理的现代化.md)：optional 在错误处理谱系中的位置。

## 思考题

1. `std::optional<double> temp;` 存「传感器可能没读数」。写出「没读数就不参与均值」的循环，并解释为什么 `if (temp)` 在这里是对的、在 `optional<bool>` 场景却是错的。
2. 实测：`std::optional<std::string> o = std::nullopt; o->size();` 会发生什么？为什么「它看起来没崩」不能作为通过理由？（提示：本章误区 4 + `09` 的悬垂同构。）
3. 把 `find_user` 的返回从 `optional<User>` 改成 `expected<User, DbError>`，列出你的调用点代码会新增哪三种分支？（对照 C++23 P0323/P2505 的接口。）
