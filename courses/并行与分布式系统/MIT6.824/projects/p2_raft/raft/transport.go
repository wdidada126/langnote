package raft

import (
	"errors"
	"math/rand"
	"sync"
	"time"
)

// ErrUnreachable：目标宕机/被丢弃（L01：RPC 必须显式处理失败）。
var ErrUnreachable = errors.New("raft: unreachable")

// Transport 是进程内 RPC 网络模拟：
//   - 宕机（Kill）→ 所有消息 ErrUnreachable；
//   - 延迟：每次调用随机 sleep（模拟网络 RTT）；
//   - dropP：按概率丢包（逼出超时/重试逻辑，对照 pg 的 "labgob" 防死锁纪律）。
//
// Call 语义：在随机延迟后，把闭包 fn 交给目标节点执行（同步拿到结果）。
// 这等价于"net/rpc 一次请求-应答"，但跨进程序列化被省略（README 说明）。
type Transport struct {
	mu      sync.Mutex
	servers map[int]*Raft
	alive   map[int]bool
	dropP   float64
	latency time.Duration
	rng     *rand.Rand
}

// NewTransport 创建网络；dropP ∈ [0,1) 为丢包概率，latency 为平均延迟。
func NewTransport(dropP float64, latency time.Duration) *Transport {
	return &Transport{
		servers: map[int]*Raft{},
		alive:   map[int]bool{},
		dropP:   dropP,
		latency: latency,
		rng:     rand.New(rand.NewSource(time.Now().UnixNano())),
	}
}

// Register 挂入一个节点（id 必须是 0..N-1 连续）。
func (t *Transport) Register(id int, rf *Raft) {
	t.mu.Lock()
	defer t.mu.Unlock()
	t.servers[id] = rf
	t.alive[id] = true
}

// N 集群规模。
func (t *Transport) N() int {
	t.mu.Lock()
	defer t.mu.Unlock()
	return len(t.servers)
}

// PeerIDs 返回除 me 以外的全部节点 id。
func (t *Transport) PeerIDs(me int) []int {
	t.mu.Lock()
	defer t.mu.Unlock()
	var out []int
	for id := range t.servers {
		if id != me {
			out = append(out, id)
		}
	}
	return out
}

// Kill 使节点在网络上"消失"（进程崩溃的最简模拟；内存状态保留=无盘重启语义
// 见 Cluster.Recover 的说明）。
func (t *Transport) Kill(id int) {
	t.mu.Lock()
	defer t.mu.Unlock()
	t.alive[id] = false
}

// Recover 恢复节点（重挂网络；若配持久存储即"带盘重启"）。
func (t *Transport) Recover(id int) {
	t.mu.Lock()
	defer t.mu.Unlock()
	t.alive[id] = true
}

// Alive 查询。
func (t *Transport) Alive(id int) bool {
	t.mu.Lock()
	defer t.mu.Unlock()
	return t.alive[id]
}

// Call 执行一次模拟 RPC。fn 在目标 *Raft 上运行（结果由闭包捕获）。
func (t *Transport) Call(to int, fn func(*Raft)) error {
	t.mu.Lock()
	srv, ok := t.servers[to]
	alive := t.alive[to]
	drop := t.rng.Float64() < t.dropP
	lat := t.latency
	t.mu.Unlock()

	if !ok || !alive || drop {
		return ErrUnreachable
	}
	// 抖动：0.5x–1.5x 延迟
	jitter := time.Duration(0.5*float64(lat) + t.rng.Float64()*float64(lat))
	time.Sleep(jitter)

	// 复查存活（sleep 期间可能刚被 Kill——真实网络同样不确定）
	t.mu.Lock()
	alive = t.alive[to]
	t.mu.Unlock()
	if !alive {
		return ErrUnreachable
	}
	fn(srv)
	return nil
}

// ---------------------------------------------------------------------------
// Cluster：把 n 个 Raft 组装成可测集群，并可选给每个节点挂"状态机投递记录器"
// （测试断言"已提交前缀一致"的不变量时用它）。
// ---------------------------------------------------------------------------

// Cluster 一个进程内 Raft 集群。
type Cluster struct {
	T       *Transport
	Servers []*Raft
	Stores  []*MemoryStore
	rec     []*Recorder
}

// MakeCluster 建 n 节点集群并启动全部服务；dropP/latency 控制网络脾气。
func MakeCluster(n int, dropP float64, latency time.Duration) *Cluster {
	c := &Cluster{T: NewTransport(dropP, latency)}
	peers := make([]int, n)
	for i := range peers {
		peers[i] = i
	}
	for i := 0; i < n; i++ {
		store := NewMemoryStore()
		rf := Make(i, peers, c.T, store)
		c.T.Register(i, rf)
		c.Servers = append(c.Servers, rf)
		c.Stores = append(c.Stores, store)
		rec := NewRecorder(rf)
		c.rec = append(c.rec, rec)
	}
	return c
}

// Kill 崩溃节点 i（停心跳 + 网络失联，但保留内存存储 → Recover 即"带盘重启"）。
func (c *Cluster) Kill(i int) {
	c.T.Kill(i)
	c.Servers[i].Shutdown()
}

// Partition 保留给读者练习（pg2 challenge）：只切断 i 与其余节点的双向消息。
// （实现提示：在 Transport 里加 pair 级黑名单。）

// WaitLeader 轮询直到"恰好一个 leader"，返回 (id, term)。超时返回 (-1, 0)。
func (c *Cluster) WaitLeader(timeout time.Duration) (int, int) {
	deadline := time.Now().Add(timeout)
	for time.Now().Before(deadline) {
		leader, term, cnt := -1, 0, 0
		for i, rf := range c.Servers {
			if !c.T.Alive(i) {
				continue
			}
			role, t, _, _, _ := rf.Status()
			if role == "leader" {
				leader, term, cnt = i, t, cnt+1
			}
		}
		if cnt == 1 {
			return leader, term
		}
		time.Sleep(10 * time.Millisecond)
	}
	return -1, 0
}

// AnyLeader 返回当前存活 leader（可能为 -1）。
func (c *Cluster) AnyLeader() int {
	for i, rf := range c.Servers {
		if c.T.Alive(i) {
			if role, _, _, _, _ := rf.Status(); role == "leader" {
				return i
			}
		}
	}
	return -1
}

// Applied 返回节点 i 记录到的已应用命令序列（下标即 apply 顺序）。
func (c *Cluster) Applied(i int) []ApplyMsg { return c.rec[i].Snapshot() }

// WaitCommitted 等待集群"至少 k 个存活节点提交了 n 条命令"，成功返回 true。
func (c *Cluster) WaitCommitted(n, k int, timeout time.Duration) bool {
	deadline := time.Now().Add(timeout)
	for time.Now().Before(deadline) {
		ok := 0
		for i, rf := range c.Servers {
			if !c.T.Alive(i) {
				continue
			}
			_, _, commit, _, _ := rf.Status()
			if commit >= n {
				ok++
			}
		}
		if ok >= k {
			return true
		}
		time.Sleep(10 * time.Millisecond)
	}
	return false
}

// Stop 关停所有节点。
func (c *Cluster) Stop() {
	for _, rf := range c.Servers {
		rf.Shutdown()
	}
}

// ---------------------------------------------------------------------------
// Recorder：持续消费 applyCh 的"状态机"桩，记录交付序列供断言。
// ---------------------------------------------------------------------------

// Recorder 模拟一个只记录不上层逻辑的状态机。
type Recorder struct {
	mu   sync.Mutex
	msgs []ApplyMsg
	idx  map[int]int // index -> 第几次 apply（检测重复交付）
	rf   *Raft
}

// NewRecorder 启动一个记录协程。
func NewRecorder(rf *Raft) *Recorder {
	r := &Recorder{idx: map[int]int{}, rf: rf}
	go func() {
		for m := range rf.GetApplyChan() {
			r.mu.Lock()
			r.msgs = append(r.msgs, m)
			r.idx[m.CommandIndex]++
			r.mu.Unlock()
		}
	}()
	return r
}

// Snapshot 拷贝当前已交付序列。
func (r *Recorder) Snapshot() []ApplyMsg {
	r.mu.Lock()
	defer r.mu.Unlock()
	out := make([]ApplyMsg, len(r.msgs))
	copy(out, r.msgs)
	return out
}
