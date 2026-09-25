// Package mapreduce 以单进程多 goroutine 的方式模拟 MapReduce 的 master/worker 架构。
//
// 对应讲次：L01（RPC 语义：超时/幂等/at-most-once）、L02（MapReduce 论文）。
// 对应 Lab：6.824 pg1（mapreduce）。
//
// 与原版 Lab 的差异：原版要求用 net/rpc 跨进程通信；本实现把"RPC"换成
// 进程内带互斥锁的方法调用 + goroutine，但**协议结构、任务状态机、超时重做、
// 备份任务**等核心机制完整保留——它们才是论文的知识点。
package mapreduce

import (
	"errors"
	"sync"
	"time"
)

// ErrTimeout 模拟 RPC 超时（真实系统里是网络丢包/进程假死）。
var ErrTimeout = errors.New("rpc timeout")

// ErrDial 模拟连不上目标（真实系统里是进程已死）。
var ErrDial = errors.New("rpc dial failed")

// RPCTimeout 是所有"调用 master"的客户端超时（对照 L01：无超时必挂死）。
const RPCTimeout = 300 * time.Millisecond

// ---------------------------------------------------------------------------
// 进程内 RPC 总线：把 (方法, 参数) 派发给目标对象的互斥临界区，
// 并用 goroutine + channel 实现超时。等价于一次 net/rpc 调用的语义。
// ---------------------------------------------------------------------------

// Server 是一个可被 Call 的进程内 RPC 端点。
type Server struct {
	mu   sync.Mutex
	addr string
	// target 指向具体服务（*Master），调用在持有 mu 时执行，
	// 模拟"服务端按序处理请求"。
	target interface{}
}

// Addr 返回该端点的逻辑地址（仅用于日志）。
func (s *Server) Addr() string { return s.addr }

// NewServer 把服务对象（*Master 等）包装成可被 Call 的端点。
func NewServer(target interface{}, addr string) *Server {
	return &Server{target: target, addr: addr}
}

// callFn 在服务端临界区内执行 fn。
func (s *Server) invoke(fn func(target interface{})) {
	s.mu.Lock()
	defer s.mu.Unlock()
	fn(s.target)
}

// Client 模拟一次带超时的 RPC 调用。
type Client struct {
	srv *Server
	// down 为 true 时模拟"对端失联"，所有调用返回 ErrDial。
	down bool
	mu   sync.Mutex
}

// NewClient 创建指向 srv 的客户端。
func NewClient(srv *Server) *Client {
	return &Client{srv: srv}
}

// SetDown 模拟目标机器宕机/断网（worker 崩溃测试用）。
func (c *Client) SetDown(d bool) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.down = d
}

// Call 执行 RPC：fn 在 master 互斥锁内运行；超过 RPCTimeout 返回 ErrTimeout。
// args/reply 通过闭包捕获（真实 RPC 里是序列化，语义等价：请求-应答一次往返）。
func Call(c *Client, fn func(target interface{})) error {
	c.mu.Lock()
	down := c.down
	c.mu.Unlock()
	if down {
		return ErrDial
	}
	done := make(chan struct{})
	go func() {
		defer close(done)
		c.srv.invoke(fn)
	}()
	select {
	case <-done:
		return nil
	case <-time.After(RPCTimeout):
		return ErrTimeout
	}
}
