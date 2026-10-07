# TypeScript 系列·Runtime vs Type System 专题（type erasure）

> 2026-10-07 建。本档是 TypeScript 系列的**独立专题档**（用户书目粘贴中特别点名：TS 与 Java/Kotlin/C++ 的根本分歧=类型擦除后运行时裸 JS）。
> 证据三态：✅=本会话本机实测（node v22.14，`--experimental-strip-types`）｜⚠️=书目说法/记忆归纳｜🔧=可复演实验位。
> 实验脚本位：`/tmp/tsexp/`（会话临时）——第 2 波起将样例固化到本目录 `exp/` 子夹。

## 一、一句话公理

**TS = JS + 一层编译期即全数剥除的类型注解。** 类型不存在于任何运行时结构中：没有类型对象、没有反射入口、没有类型分派——程序运行时是纯 JS，类型对它的唯一影响是「你写它时编辑器有没有红波浪线」。这与三兄弟语言的根本差异构成下表。

## 二、四语言擦除程度对照（本专题核心表）

| 语言 | 泛型/类型参数运行时留存 | 具体形态 |
|---|---|---|
| **TypeScript** | **零留存**（全类型层擦除）✅ | 注解、interface、type、`implements`、类型谓词全数删除，产物=等价 JS；`private`（TS 关键字）也仅类型层 ✅实测 |
| Java | 类型参数擦除，但**类/接口元数据全在** | `List<T>` 擦除为 `List`+桥方法；`instanceof`/反射/注解运行时可见——擦的是泛型不是类型系统 |
| Kotlin | 泛型擦除（同 Java），但 **inline/value class 可 reified** | `reified T` 借内联逃逸擦除；`@JvmStatic` 等映射层留存 |
| C++ | **不擦除而是消灭**：模板单态化生成真实代码 | 运行时无统一类型对象（RTTI 另议）；类型在编译期直接变成机器码形状 |

⚠️ Java/Kotlin/C++ 三列为既有书档归纳（`深入解析Java虚拟机HotSpot.md`、`C++语言的设计与演化.md`、Kotlin 系列 KiA2e 泛型/内联章），非本会话实测；对照表引用时按各书档口径。

## 三、本机实测记录（✅ 2026-10-07）

实验 A：`erasure.ts`（`node --experimental-strip-types`，exit=0）

```ts
type Shape = { kind: "circle"; r: number } | { kind: "square"; s: number };
interface Named { name: string }
class A implements Named { name = "a"; private secret = 42; #hard = 7; }
const f = (x: Shape & Named): string => x.kind;
```

输出与解读：

- `runtime keys: [ 'name', 'secret' ]` —— **TS `private` 运行时字段照在**：它是纯类型层访问标记，编译后无任何封装效果。
- `"secret" in new A()` → `true`；`Object.getOwnPropertyNames` 含 `secret` 不含 `#hard` —— **TS `private` ≠ JS `#`**：前者编译期礼貌，后者运行时硬墙。类设计条目重灾区。
- `f.length = 1` —— 类型交集/联合注解不改变任何 JS 反射事实。
- `type/interface/implements` 全部：运行时零痕迹 ✅。

实验 B：`notypecheck.ts`

```ts
const n: number = "not a number";
console.log("node ran it anyway, n =", n, typeof n);
```

输出：`node ran it anyway, n = not a number string`（exit=0）—— **删注解≠查类型**。校验完全发生在 `tsc`/编辑器的编译期；一旦产物落地运行时，`number` 里装着 string 无人报警。

## 四、推论与工程戒律（各书 Item 的统一底层）

1. 一切「类型安全」预算都花在编译期：CI 无 `tsc --noEmit` = 裸奔（TS 侧对应 Java 不编译直接跑字节码的荒谬度）。⚠️ 书目共识，非实测。
2. 断言 `as` 是**向编译器撒谎**，运行时不产生转换、不产生检查——与 Java 强转（运行时 checkcast 真拦截）语义断裂最大的一处。✅ 撒谎面即实验 B 机理。
3. 需要运行时类型信息时只能**自己编码进值里**：判别联合的 `kind` 字段、`zod` 式 schema-first——TS 生态把「类型」重造为「值」的库群由此公理解释。⚠️ 归纳。
4. `enum`/参数属性/装饰器是**少数会产码的类型层语法**（违背纯擦除，strip 模式拒跑即界碑 ✅ 已实测：`--experimental-strip-types` 拒载 enum/namespace，`--experimental-transform-types` 放行产码），satisfies/`as const` 则纯类型层——混合带是迁移脚本兼容地雷位。
5. 与 Kotlin `data class`（真生成 equals/hashCode）对照：**TS 的结构相等要手写或借库**——「形状相同即相等」是类型层的，运行时无相等协议。⚠️。

## 五、🔧 待补实验清单（第 2 波销账）

- 装 `typescript`（本地 devDependency 或全局，待用户授权口径）后补：`tsc --strict` 下实验 A/B 的报错矩阵、`private` 越权访问报错、enum 转译产物阅读。
- ✅ **已销（2026-10-07 泳群复演+主代理独立复现）**：`enum`/`namespace` 在 `--experimental-strip-types` 下拒载（`ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX`，exit=1），加 `--experimental-transform-types` 即放行运行（exit=0，`E.A=0`、`NS.x=1` 可见产物）——「非纯擦除语法界碑」实锤；另实测 2012 式尖括号断言 `<string>expr` 在今 strip 面**直接拒载**＝语法平面硬断层（详见 `Pro_TypeScript/02-2012vs202x差异年表.md`）。
- 判别联合运行时收窄 vs `as` 强转的 crash 位点对照。

## 盘谱登记

- 各书对位章：Tackling TS Ⅰ 段（论述本）、Programming TS Ⅰ/附录（机制本）、50 Lessons Ⅳ 部（配置本）、Type-Level Ⅰ 段（类型=集合观）。
- JVM 对照档：`../Java_to_Kotlin/`、`../深入解析Java虚拟机HotSpot.md`（泛型擦除章）；C++ 对照：`../C++20模板元编程/`。
