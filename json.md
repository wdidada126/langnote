# json

## json格式化时间需要注意时区
格式化后的值跟数据库里面的值相差8小时
小时 13 -> 1 是12小时制 24小时制

pljson库 支持pl/sql

https://www.json.org/json-zh.html
### json格式化工具
网页版
工具
Hijson
IDEA快捷键

JavaScript Object Notion


xml
yaml


fastjson

枚举有bug



jackson





Unicode 标准

UTF-8实现


https://www.cnblogs.com/daguozb/p/7989706.html

{name:"dd"} 不对


{name:"dd"} 

## json schema详解

JSON Schema是一种用于描述JSON数据格式的语言，它可以用来验证JSON数据的有效性和完整性。JSON Schema可以定义JSON数据的结构、类型、限制等信息，使得开发人员可以更加方便地处理和验证JSON数据。

JSON Schema的基本语法包括以下几种：

1. type：指定JSON数据的类型，如字符串、数字、布尔值、数组、对象等。
2. properties：定义JSON对象的属性及其类型、限制等信息。
3. items：定义JSON数组中的元素及其类型、限制等信息。
4. required：指定JSON数据必须包含哪些属性。
5. additionalProperties：定义JSON对象的额外属性及其类型、限制等信息。
6. minItems和maxItems：定义JSON数组的最小和最大元素个数。
7. minLength和maxLength：定义字符串的最小和最大长度。
8. pattern：定义字符串的正则表达式匹配规则。
9. enum：定义字符串的可选值列表。
10. allOf和anyOf：定义多个JSON Schema之间的逻辑关系。
11. oneOf：定义多个JSON Schema之间的互斥关系。
12. not：定义JSON Schema的取反关系。
13. $ref：引用其他JSON Schema定义的属性或元素。

下面是一个示例的JSON Schema：

```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 50
    },
    "age": {
      "type": "integer",
      "minimum": 18,
      "maximum": 100
    },
    "email": {
      "type": "string",
      "format": "email"
    }
  },
  "required": ["name", "email"]
}
```

上述示例中，我们定义了一个名为“person”的对象，其中包含了三个属性：“name”、“age”和“email”。每个属性都有其对应的类型、限制等信息。同时，我们还指定了“name”和“email”是必需的属性。