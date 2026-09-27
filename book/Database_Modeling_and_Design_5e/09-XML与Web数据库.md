# 09 · XML 与 Web 数据库（第 9 章 XML and Web Databases, pp.161-187）

> 本章文件为**精读重构**，非原书文本。章题与页区间 ✅ Crossref 实抓；27 页，全书"半结构化转向"的中心。⚠️ 原书小节与 SQL/XML 语法版本细节未能实抓，按 W3C/ISO 公开标准口径转述。

## 一、本章定位：ER 遇到"树"

前面八章的世界是"型先行"（schema-first）：先定义实体集再放对象。Web 数据反着来：**结构长在数据里**（self-describing），标签即语义，文档即实例图。本章用 27 页回答建模者三连问：XML 能表达什么数据语义？关系/ER 模型与树模型如何互译（映射与 shredding）？查询语言（XPath/XQuery）与 SQL 各擅胜场在哪？——并诚实留下 2011 年的开放问题：**模式治理松动的代价由谁付**。

## 二、XML 技术栈（标准口径，✅ 组织与标准名公开可查）

| 层 | 标准 | 建模含义 |
|---|---|---|
| 语法 | XML 1.0（W3C Recommendation） | 标签/属性/文本节点；命名空间解异名 |
| 模式 | XML Schema (XSD)、DTD | 元素/属性类型、出现约束（minOccurs/maxOccurs≈参与/基数） |
| 结构约束 | ID/IDREF、Key/Keyref（XSD） | **关系外键的树内对应物**——本章点破：树模型并不比关系少约束语法，少的是执行担保 |
| 查询 | XPath、XQuery、XSLT | 路径表达式定位+构造结果 |
| 序列化交换 | SOAP/REST+XML、后来的 JSON | Web 服务载荷时代底色 |

## 三、ER ↔ XML 的双向映射（本章技术核心，重构 ⚠️）

**ER→XML**：实体集→元素；属性→属性或子元素（选择判据：会被独立寻址吗）；1:N→嵌套；M:N→IDREF 或重复元素+引用；ISA→XSD 派生类型（restriction/extension）；弱实体→必须嵌在识别者文档内（局部键只在全局文档内唯一——**弱实体语义在树模型里"天然正确"**，这是本章最漂亮的一处对照）。
**XML→ER/关系**：文档→树实例；元素类型→实体集；"多值/可选"爆炸→列稀疏或表爆炸——**shredding（撕碎入库）**：把 XSD 约束的树映射成关系表集合（SQL/XML 的 XMLTABLE、各厂商 annotated schema 机制 ⚠️ 转述），保留 PATH 列可再重建文档（serialize）。

## 四、混合形态：SQL/XML 与"列存 XML 类型"

- Oracle XMLType / DB2 pureXML：列类型为 XML，函数面 `extract/queryvalue`、XQuery 引擎内嵌（2011 口径 ⚠️ 转述）；
- 价值主张：**关系管治理（键/事务/并发），XML 管柔性（结构演进/异构交换）**——一个订单库最自然的切分：抬头进关系表，明细快照进 XML 文档列；
- 本章立场与第 8 章一致：扩展是逃生舱——"能用关系映射解决的，别上 XML"。

## 五、Web 数据库议题（章题后半，重构 ⚠️）

- 数据规模与模式异构：Web 数据"缺全局 ER 图"的困境 → 本章给的是 XSD 局部自治 + 命名空间治理，而非全局概念模型；
- 数据集成：以交换格式（XML→后来的 JSON）为货币的 schema 映射，是第 4 章视图集成的互联网尺度重演；
- RDF/语义网仅点到（2011 时机）：链接数据作为"标签即全局 ID"的另一路线，本目录在 12 附录文件与论文线外不再展开 ⚠️。

## 六、易错点与自测

**易错**：① 属性 vs 子元素随手选（丢独立寻址/多值扩展位）；② 拿 DTD 做类型约束（表达能力弱一档，XSD 才有类型系统）；③ shredding 后丢 PATH 保真（重建文档结构走样）；④ 用 XML 表达 M:N（嵌套爆炸，应引用化）；⑤ 以为有 Keyref 就有引用完整性运维（无级联无孤儿扫描默认 ⚠️）。

**自测五问**：① XSD 的 min/maxOccurs 与 ER 参与/基数的对应表；② 弱实体为何在文档模型里更自然；③ shredding 的"保真三件套"（键、序、PATH）；④ XML 列与 JSON 列的取舍在 2026 怎么看；⑤ XPath 谓词与 SQL WHERE 的表达力边界差异。

## 补充一、XSD 迷你样本走查（把约束逐条翻译成 ER 词汇）

```xml
<xs:element name="order">
  <xs:complexType>
    <xs:sequence>
      <xs:element name="customerId" type="xs:IDREF"/>       <!-- 引用完整性：Keyref 兜底 -->
      <xs:element name="item" maxOccurs="unbounded">        <!-- 1:N → 嵌套；多值属性 -->
        <xs:complexType>
          <xs:sequence>
            <xs:element name="sku" type="xs:string"/>
            <xs:element name="qty" type="xs:positiveInteger"/>
          </xs:sequence>
          <xs:attribute name="gift" type="xs:boolean" use="optional"/> <!-- 可空列 -->
        </xs:complexType>
      </xs:element>
    </xs:sequence>
    <xs:attribute name="id" type="xs:ID" use="required"/>   <!-- 主键承诺 -->
  </xs:complexType>
</xs:element>
```

- 逐行读法：`maxOccurs="unbounded"`=1:N 嵌套（ER 的 R6 内嵌变体）；`use="optional"`=可空；`ID/IDREF`=实体标识与引用，但**无级联无孤儿守护**（语法齐、执行缺）；
- 把这段 schema 画回 ER：ORDER 弱实体（识别于客户文档）、LINE 子元素=属性族、customerId 是跨文档联系——树与图的互译在一次走查里同时成立。

## 补充二、shredding 工程清单（撕碎文档前要定的六件事）

1. **键保真**：文档内 ID→业务主键；全局唯一性谁担保（Keyref 校验批处理）；
2. **序保真**：序列内元素顺序→序号列（XML 的文档序是语义，关系无序是定律）；
3. **PATH 保真**：每行存来源路径，保 serialize 重建不走样；
4. **稀疏处理**：optional 元素→NULL 列还是缺行？聚合语义先定；
5. **版本共存**：XSD 演化（1.0/1.1 文档同库）→命名空间列+校验器路由；
6. **混合查询**：哪些查询走关系表、哪些走 XML 列函数——划界表进设计文档（否则"混合"退化成"两份真相"）。

## 补充三、本章的 2026 重读法（教师视角三条）

- 把"XML"整体读作"半结构化数据"，技术名词做同构替换（XSD→JSON Schema、XPath→JSONPath、XMLTABLE→JSON_TABLE），方法论完整存活；
- 保留两处 XML 原生场景再讲深：文档为中心的应用（出版/法务，文档即产品）与强交换约束（签名/合规），它们解释了"为什么 XML 没死透"；
- 本章真正的考题是**治理光谱**：schema-first（ER/关系）↔ schema-later（文档/列式 variant）——让学生在自己项目里定位，并说出该位置为"结构演进自由"付了什么约束担保的代价。

## 补充四、本章一页总结

- XML 技术的建模本质：**结构与数据同体**——这既是自由（演进不锁模式）也是代价（完整性担保外包）；
- ER↔XML 双向映射证明：树模型不比关系模型"少约束语法"（XSD 的 IDREF/Key 一应俱全），少的是**执行与运维承诺**；
- shredding 三保真（键/序/PATH）是半结构化入仓工程量的真正来源，任何"一键导入"话术都要用这三问戳穿；
- 本章的长期价值不在 XML 本身，而在它是全书第一次系统处理"模式弹性 vs 治理刚性"的章节——JSON 与湖仓时代每一场架构辩论都还在用它的题目。

### 三分钟口试（自问自答）

0. 名词定位：DTD（实体声明+浅类型）、XSD（类型系统+约束）、XSLT（变换）、XQuery（查询+构造）——四件武器各解哪类问题，一句一个；

1. XSD 的 maxOccurs 对应 ER 的哪两个构造？各映射到哪条 SQL 规则？
2. 为什么弱实体在文档模型里"免费"，在关系模型里要 CASCADE？
3. JSON_TABLE 之于 JSON，相当于本章哪个工具之于 XML？
4. 交换格式选型（XML vs JSON）在 2026 的三个真实判据？（签名规范/嵌套深度/解析器生态 ⚠️ 经验口径）

## 核心概念速览（中英对照）

1. **半结构化数据** — semistructured data：结构自描述、可不遵循固定模式的数据
2. **自描述** — self-describing：标签与值同体携带结构信息
3. **元素/属性** — element/attribute：XML 节点两类，建模语义有别
4. **XML Schema (XSD)** — XML Schema：类型与出现约束语言
5. **IDREF/Keyref** — ID/IDREF, key/keyref：树内引用约束，≈外键语法
6. **XPath** — XPath：轴+节点测试的路径定位语言
7. **XQuery** — XQuery：XML 的图灵完备查询与构造语言
8. **shredding** — shredding：XML 文档撕碎映射为关系表
9. **SQL/XML** — SQL/XML standard：XML 列型与 XMLTABLE 等桥梁函数
10. **serialize** — serialization：关系行重建为文档
11. **命名空间** — namespace：跨源异名治理
12. **混合持久化** — hybrid persistence：关系骨架+文档字段的共存设计

## 最新演进与工业实践

- **标准寿命（2024-2026）**：XSD/XPath 1.0 仍广泛存在于存量交换（政府表单、出版、金融报文）；新系统交换层几乎整体转 JSON（REST→OpenAPI、gRPC 用 protobuf 而非 XML——REST 兼容实现以 JSON 为默认 ⚠️ 生态综述）。
- **本章的"文档列"预言成真**：四大关系库都把半结构化列做进主线——PG jsonb（GIN 索引可查）、Oracle 2025 原生 JSON 类型、SQL Server JSON 类型、DB2 JSON 表（各厂商文档 ⚠️ 转述，版本细节未逐一核验）；XMLType 阵营收缩但金融/电信存量长命。
- **XPath→JSONPath/JSON Pointer**：路径语言血统平移（RFC 9535 JSONPath 2024 ✅ IETF 公开标准，未做 DOI 校验，按公开口径引用）；SQL/JSON 子句族（JSON_TABLE≈XMLTABLE 的镜像桥）进 PG/Oracle/MySQL——本章 shredding 方法论以 JSON 词汇重播。
- **开源标本**：libxml2、Saxon（XQuery）仍维护 ⚠️ 仓库名登记（GitHub 本机不可达）；XML 数据库（eXist、MarkLogic） niche 化——MarkLogic 转向多模型文档库叙事 ⚠️。
- 🔧 **本机可演示**：SQLite 3.45.3 无 XQuery，但"XMLTABLE 思想"可用 json_each 平替演示（同 08 文件方法，结果核验见 12 文件汇总）；XSD 校验用 xmllint/lxml 离线可跑（Python lxml 需 pip 安装，本机未预装则跳过 ⚠️ 未实测不标 🔧）。
- **与 repo 衔接**：文档模型的写侧代价与模式演化，读 [../设计数据密集型应用.md](../设计数据密集型应用.md)；湖仓里半结构化的第三段旅程（variant 类型）见 [../The_Data_Lakehouse/00-总览与阅读地图.md](../The_Data_Lakehouse/00-总览与阅读地图.md)。
