package kv

import (
	"math/rand"
	"sync/atomic"
	"time"
)

// Clerk 是 KV 客户端：把"不可靠网络 + 会崩溃的 leader"调教成
// 单一可靠服务（L01 §2.2 的核心工程：超时重试 + 幂等/去重 + 重新绑定）。
//
// 进程内实现：servers 是直连的 *Server（等价于一次不会真丢包的 RPC；
// "leader 会死"的不确定性由服务器端的超时/覆盖检测承担）。
type Clerk struct {
	servers   []*Server
	clientID  int64 // 进程生命周期内唯一（真实实现：uuid/时间戳+随机）
	requestID atomic.Int64
	primary   atomic.Int64 // "主存感知"：上次成功响应的服务器，下次先问它
}

// MakeClerk 创建客户端。
func MakeClerk(servers []*Server) *Clerk {
	return &Clerk{
		servers:  servers,
		clientID: time.Now().UnixNano() ^ rand.Int63(),
	}
}

// request 发送一次逻辑操作：无限重试直到拿到非错误应答。
// 关键：重试使用**相同**的 (clientID, requestID) → 服务器去重表保证
// 命令至多执行一次（对照 L02 MapReduce 的幂等重做）。
func (ck *Clerk) request(req Request) Response {
	req.ClientID = ck.clientID
	for {
		// 先验主，再随机轮询其余（pg4 的 config/primary 查询机制的最小前身）
		order := ck.serverOrder()
		var resp Response
		failed := true
		for _, i := range order {
			sv := ck.servers[i]
			r := sv.Handler(req)
			if r.Err == ErrWrongLeader || r.Err == ErrTimeout {
				continue // 换下一个候选
			}
			resp = r
			failed = false
			ck.primary.Store(int64(i))
			break
		}
		if !failed {
			return resp
		}
		// 全集群不可用（分区/多数派死亡）：退避后继续——线性一致的活性
		// 依赖多数派恢复（CAP 之 CP 的代价，L09/L10）。
		time.Sleep(100 * time.Millisecond)
	}
}

func (ck *Clerk) serverOrder() []int {
	n := len(ck.servers)
	order := make([]int, 0, n)
	if p := int(ck.primary.Load()); p >= 0 && p < n {
		order = append(order, p)
	}
	for _, i := range rand.Perm(n) { // 全局 rand 带锁，多 goroutine 共用 Clerk 也安全
		if i != int(ck.primary.Load()) {
			order = append(order, i)
		}
	}
	return order
}

// Put / Append / Get：论文 API 的三原语。
func (ck *Clerk) Put(key, value string) {
	ck.request(Request{RequestID: int(ck.requestID.Add(1)), Method: "PutAppend", Key: key, Value: value})
}

func (ck *Clerk) Append(key, value string) {
	ck.request(Request{RequestID: int(ck.requestID.Add(1)), Method: "PutAppend", Key: key, Value: value, Op: "append"})
}

func (ck *Clerk) Get(key string) string {
	r := ck.request(Request{RequestID: int(ck.requestID.Add(1)), Method: "Get", Key: key})
	return r.Value
}
