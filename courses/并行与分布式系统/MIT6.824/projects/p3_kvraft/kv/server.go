package kv

import (
	"sync"
	"time"

	"kv.example/p3/lraft"
)

// Server 把一个 lraft 节点包成 KV 服务器：Raft 日志 → 状态机 → 去重表。
type Server struct {
	Me      int
	Raft    *lraft.Raft
	ApplyCh <-chan lraft.ApplyMsg

	mu        sync.Mutex
	state     map[string]string
	applied   int                    // 已应用到状态机的 Raft 索引
	dup       map[int64]map[int]Response // clientID -> requestID -> 应答（重放用）
	notify    chan struct{}          // 广播 applied 前进（唤醒等待者）
	closeOnce sync.Once
}

// NewServer 创建 KV 服务器并启动"应用循环"（Raft 提交 → 执行命令 → 推进 applied）。
func NewServer(me int, rf *lraft.Raft, applyCh <-chan lraft.ApplyMsg) *Server {
	sv := &Server{
		Me: me, Raft: rf, ApplyCh: applyCh,
		state:  map[string]string{},
		dup:    map[int64]map[int]Response{},
		notify: make(chan struct{}, 1),
	}
	go sv.applier()
	return sv
}

// applier：单线程消费 applyCh —— 复制状态机一致性的根（所有节点按同序执行同命令）。
func (sv *Server) applier() {
	for m := range sv.ApplyCh {
		if !m.CommandValid {
			continue // 快照消息（pg3 范围）本实现不产生
		}
		cmd := m.Command.(Command)
		sv.mu.Lock()
		// 去重：同一 (clientID, requestID) 只执行一次（L01 at-most-once 的拼图）。
		if _, done := sv.lookupDupLocked(cmd.ClientID, cmd.RequestID); !done {
			resp := sv.executeLocked(cmd)
			sv.recordDupLocked(cmd.ClientID, cmd.RequestID, resp)
		}
		sv.applied = m.CommandIndex
		sv.mu.Unlock()
		sv.broadcast()
	}
}

func (sv *Server) lookupDupLocked(cid int64, rid int) (Response, bool) {
	if byReq, ok := sv.dup[cid]; ok {
		if r, ok := byReq[rid]; ok {
			return r, true
		}
	}
	return Response{}, false
}

func (sv *Server) recordDupLocked(cid int64, rid int, r Response) {
	if sv.dup[cid] == nil {
		sv.dup[cid] = map[int]Response{}
	}
	sv.dup[cid][rid] = r
}

// executeLocked：状态机本体（Put 覆盖 / Append 追加 / Get 读快照）。
func (sv *Server) executeLocked(cmd Command) Response {
	switch cmd.Method {
	case "Get":
		return Response{Value: sv.state[cmd.Key]}
	case "PutAppend":
		if cmd.Op == "append" {
			sv.state[cmd.Key] += cmd.Value
		} else {
			sv.state[cmd.Key] = cmd.Value
		}
		return Response{}
	}
	return Response{Err: "unknown method"}
}

func (sv *Server) broadcast() {
	select {
	case sv.notify <- struct{}{}:
	default:
	}
}

// Handler 是客户端 RPC 入口。
// 流程 = 经典 kvraft：
//  1. 命令进 Raft（非 leader 立即返回 ErrWrongLeader → 客户端换节点）；
//  2. 等待本条命令被应用到状态机（leader 崩溃则超时）；
//  3. 从去重表取本次执行结果返回。
//
// 注意：**Get 也走一遍 Raft** —— 这是"用共识做线性一致读"的朴素解
// （ReadIndex/LeaseRead 优化见 README，L06 §4）。
func (sv *Server) Handler(req Request) Response {
	cmd := Command{
		ClientID: req.ClientID, RequestID: req.RequestID,
		Method: req.Method, Key: req.Key, Value: req.Value, Op: req.Op,
	}
	index, _, isLeader := sv.Raft.Start(cmd)
	if !isLeader {
		return Response{Err: ErrWrongLeader}
	}

	// 等 applied >= index（带超时：leader 中途换人时旧命令可能永不应用）。
	deadline := time.Now().Add(2 * time.Second)
	for {
		sv.mu.Lock()
		if sv.applied >= index {
			resp, done := sv.lookupDupLocked(req.ClientID, req.RequestID)
			sv.mu.Unlock()
			if done {
				return resp
			}
			// index 处被"别人家的命令"占用了：本条已被新 leader 覆盖/截断，
			// 绝不能假报成功（kvraft 的经典 bug！）→ 让客户端重试。
			return Response{Err: ErrWrongLeader}
		}
		sv.mu.Unlock()
		if time.Now().After(deadline) {
			return Response{Err: ErrTimeout}
		}
		select {
		case <-sv.notify:
		case <-time.After(50 * time.Millisecond):
		}
	}
}

// WaitReady 等该节点首次能服务（等选举结束，main/tests 启动用）。
func (sv *Server) WaitReady(timeout time.Duration) bool {
	deadline := time.Now().Add(timeout)
	for time.Now().Before(deadline) {
		role, _, _, _, _ := sv.Raft.Status()
		if role == "leader" {
			return true
		}
		time.Sleep(20 * time.Millisecond)
	}
	return false
}

// StateSnapshot 导出状态机（测试用于校验副本一致）。
func (sv *Server) StateSnapshot() map[string]string {
	sv.mu.Lock()
	defer sv.mu.Unlock()
	out := make(map[string]string, len(sv.state))
	for k, v := range sv.state {
		out[k] = v
	}
	return out
}

// ---------------------------------------------------------------------------
// KVCluster：n 个 KVServer + 底层 lraft 集群（进程内模拟，多节点测试入口）。
// ---------------------------------------------------------------------------

// KVCluster 一套可测的 KV 集群。
type KVCluster struct {
	Servers  []*Server
	RaftClus *lraft.Cluster
}

// MakeKVCluster 启动 n 节点集群；dropP/latency 控制"网络脾气"。
func MakeKVCluster(n int, dropP float64, latency time.Duration) *KVCluster {
	rc := lraft.MakeCluster(n, dropP, latency)
	kc := &KVCluster{RaftClus: rc}
	for i := 0; i < n; i++ {
		kc.Servers = append(kc.Servers, NewServer(i, rc.Servers[i], rc.Servers[i].GetApplyChan()))
	}
	return kc
}

// Kill 崩溃一个节点（Raft 侧网络失联 + 停心跳；KV 层随之不可用）。
func (kc *KVCluster) Kill(i int) { kc.RaftClus.Kill(i) }

// AnyLeaderServer 返回当前 leader 的 KVServer id（无则 -1）。
func (kc *KVCluster) AnyLeaderServer() int { return kc.RaftClus.AnyLeader() }
