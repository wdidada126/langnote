# ch5_ethernet_sim —— 以太网帧 + CRC + 交换机自学习模拟

## 对应章节

- 教材：§6.2（差错检测：CRC 手算）、§6.4（以太网帧格式、交换机自学习与泛洪）
- 笔记：`notes/ch6-01-link-error-access.md`（第 20 讲）、`notes/ch6-02-ethernet-switch.md`（第 21 讲）

## 要点

1. **课堂版 CRC（小多项式）**：`G(x)=x^3+x+1` 的模 2 长除法逐步演示；
   验证"发送串整除 G ⇒ 余 0"，并演示单比特错必检（G 含 ≥3 项的性质）。
2. **以太网 II 帧**：`dst|src|type|payload(≥46 补零)|FCS`；FCS 用反射 CRC-32
   （0xEDB88320，与 `zlib.crc32` 同族，取反小端打包）；>1500 直接报错——
   **以太网永不分片，那是 IP 的事（§4.4 呼应）**。
3. **交换机**：三行核心逻辑——源 MAC 学习、目的 MAC 查表、未知/广播泛洪；
   同口帧丢弃；表项带时间戳可演示老化（aging 参数）。
4. 前导码/SFD 属物理层，不进入帧内存——与笔记第 20 讲"物理层协作区"一致。

## 运行

```
python ethernet_sim.py     # 或 ./run.sh（py_compile 自检）
```

输出三个场景的逐帧日志与最终 MAC 表。

## 实验建议

- 在 Switch.handle 里加 `now - last_seen > aging` 的清扫，重跑场景 ③ 观察再次泛洪。
- 扩展 VLAN：type 0x8100 后插 4 字节 TCI，学习键改为 (vlan, mac)——单机版"广播域收缩"。
- 用 Wireshark 抓真实帧对比本模拟的 hex（`frame.len`、FCS 校验勾选 capture 选项）。
