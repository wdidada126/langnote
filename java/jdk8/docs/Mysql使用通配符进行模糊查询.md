Mysql 使用通配符进行模糊查询

Mysql| 使用通配符进行模糊查询(like,%,_)
通配符的分类: 
%百分号通配符: 表示任何字符出现任意次数(可以是0次). 
_下划线通配符:表示只能匹配单个字符,不能多也不能少,就是一个字符.
like操作符: 
LIKE作用是指示mysql后面的搜索模式是利用通配符而不是直接相等匹配进行比较. 
注意: 如果在使用like操作符时,后面的没有使用通用匹配符效果是和=一致的,SELECT * FROM products WHERE products.prod_name like '1000';只能匹配的结果为1000,而不能匹配像JetPack 1000这样的结果.
1)%通配符使用: 
匹配以"yves"开头的记录:(包括记录"yves") 
SELECT * FROM products WHERE products.prod_name like 'yves%';
匹配包含"yves"的记录(包括记录"yves") 
SELECT * FROM products WHERE products.prod_name like '%yves%';
匹配以"yves"结尾的记录(包括记录"yves",不包括记录"yves ",也就是yves后面有空格的记录,这里需要注意) 
SELECT * FROM products WHERE products.prod_name like '%yves';
2)_通配符使用: 
SELECT * FROM products WHERE products.prod_name like '_yves'; 
匹配结果为: 像"yyves"这样记录.
SELECT * FROM products WHERE products.prod_name like 'yves__'; 
匹配结果为: 像"yvesHe"这样的记录.(一个下划线只能匹配一个字符,不能多也不能少)
注意事项:
注意大小写,在使用模糊匹配时,也就是匹配文本时,mysql是可能区分大小的,也可能是不区分大小写的,这个结果是取决于用户对MySQL的配置方式.如果是区分大小写,那么像YvesHe这样记录是不能被"yves__"这样的匹配条件匹配的.
注意尾部空格,"%yves"是不能匹配"heyves "这样的记录的.
注意NULL,%通配符可以匹配任意字符,但是不能匹配NULL,也就是说SELECT * FROM products WHERE products.prod_name like '%;是匹配不到products.prod_name为NULL的的记录.
技巧与建议: 
正如所见， MySQL的通配符很有用。但这种功能是有代价的：通配符搜索的处理一般要比前面讨论的其他搜索所花时间更长。这里给出一些使用通配符要记住的技巧。
不要过度使用通配符。如果其他操作符能达到相同的目的，应该 使用其他操作符。
在确实需要使用通配符时，除非绝对有必要，否则不要把它们用 在搜索模式的开始处。把通配符置于搜索模式的开始处，搜索起 来是最慢的。
仔细注意通配符的位置。如果放错地方，可能不会返回想要的数.

- javaagent:E:\apache-skywalking-apm-incubating\agent\skywalking-agent.jar
 
eclipse提示快捷键
ALT + /

购买DDoS高防IP服务后，把域名解析到高防IP（Web业务把域名解析指向高防IP；非Web业务，把业务IP替换成高防IP），并配置源站IP。所有公网流量都经过高防IP机房，通过端口协议转发的方式将访问流量通过高防IP转发到源站IP，同时将恶意攻击流量在高防IP上进行清洗过滤后将正常流量返回给源站IP，从而确保源站IP稳定访问。
配置DDoS高防IP服务后，当您遭受DDoS攻击时，无需额外做流量牵引和回注。

