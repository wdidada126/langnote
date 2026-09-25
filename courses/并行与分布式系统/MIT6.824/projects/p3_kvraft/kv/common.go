// Package kv 在 lraft（P2 的 Raft 内核，课程同款"整包复制"做法）之上
// 实现容错 KV 状态机：Put / Append / Get + 客户端去重（at-most-once 语义）。
//
// 对应讲次：L01（RPC 幂等/重试）、L05/L06（共识）、L09（面向故障）、
// L10（线性一致性：读走 Raft 才线性一致）、L14（复制状态机=事务日志重放）。
// 对应 Lab：6.824 pg2/pg3 的 kvraft 部分（单 Raft 组；分片见 pg4，README 有述）。
package kv

// ErrWrongLeader：客户端应换服务器重试（L01 的"每次调用查位置"绑定策略）。
const ErrWrongLeader = "ERRWRONGLEADER"

// ErrTimeout：leader 在等待提交/应用时超时（崩溃或分区），客户端换节点重试。
const ErrTimeout = "ERRTIMEOUT"

// Request 是一次 KV 操作（客户端 → 服务器 RPC；服务器 → Raft 的命令）。
type Request struct {
	ClientID  int64  // 去重主键 1
	RequestID int    // 去重主键 2（同一客户端内单调）
	Method    string // "PutAppend" | "Get"
	Key       string
	Value     string
	Op        string // PutAppend 时：""(=Put) | "append"
}

// Response 是 RPC 应答（注意：Response 会原样进 dup 表被重放，字段必须完整）。
type Response struct {
	Err   string // "" 表示成功
	Value string // Get 的读值
}

// Command 是进入 Raft 日志的条目内容（= Request 的可执行投影）。
type Command struct {
	ClientID  int64
	RequestID int
	Method    string
	Key       string
	Value     string
	Op        string
}
