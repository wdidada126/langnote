# ch2_dns_query —— 手工 DNS 报文查询器（A/NS/CNAME/AAAA）

## 对应章节

- 教材：§2.3（DNS：报文格式、名字服务器、资源记录、攻击面）、§2.4（UDP socket）
- 笔记：`notes/ch2-03-dns.md`（第 6 讲）

## 协议要点

1. 查询报文 = 12B 头（`!HHHHHH`：ID/FLAGS/四个计数）+ 问题段（QNAME 长度前缀编码 + QTYPE/QCLASS）。
2. **压缩指针 `0xC0`** 是本项目的灵魂：回答里的名字常以 2 字节指针指向先前出现的位置；
   解析器必须区分"普通 label（1 长度字节）"与"指针（高 2 位=11）"，并正确处理"名中指针"（读完后跳回结束位置）。
3. RR 解析：A(1)/NS(2)/CNAME(5)/AAAA(28) + TTL；AUTHORITY 段展示 referral（NS 引路）。
4. ID 校验失败即断言——对应 §2.3 "ID 爆破/投毒"攻击的客户端自检。
5. 与 `socket.getaddrinfo` 对比：后者=完整解析器（hosts、NSS、缓存、双栈排序），前者=裸协议一次往返。

## 运行

```
python dns_query.py                    # 默认 www.google.com A via 8.8.8.8
python dns_query.py example.com --type NS --server 1.1.1.1
./run.sh                                # 含 py_compile 自检
```

观察点：A 记录的 TTL（缓存策略）、CNAME 链（CDN 常用）、rcode=3（NXDOMAIN 负缓存）。
配合 Wireshark `udp.port==53` 抓同一查询，对照十六进制与解析结果。
