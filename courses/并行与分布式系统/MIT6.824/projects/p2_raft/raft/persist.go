package raft

import "sync"

// StateStorage 抽象"写盘"（pg3 的边界：把易失内存状态变成崩溃后仍在的状态）。
// Raft 核心只在三个地方调用 Save：term/vote 变更、日志追加、日志截断。
// 这正是 L06 所讲的"先落盘再动作 = WAL 纪律"（与 6.S081 日志文件系统同构）。
type StateStorage interface {
	// Read 返回 (currentTerm, votedFor, log)。新实例返回 (0, -1, nil)。
	Read() (int, int, []LogEntry)
	// Save 必须做拷贝存储（调用方可能继续原地修改）。
	Save(currentTerm, votedFor int, log []LogEntry)
}

// MemoryStore 是内存实现（本轮无磁盘；pg3 对应 FileStorage，见 README 讨论）。
type MemoryStore struct {
	mu       sync.Mutex
	term     int
	votedFor int
	log      []LogEntry
}

// NewMemoryStore 空存储。
func NewMemoryStore() *MemoryStore { return &MemoryStore{votedFor: -1} }

// Read 实现 StateStorage。
func (s *MemoryStore) Read() (int, int, []LogEntry) {
	s.mu.Lock()
	defer s.mu.Unlock()
	cp := append([]LogEntry(nil), s.log...)
	return s.term, s.votedFor, cp
}

// Save 实现 StateStorage。
func (s *MemoryStore) Save(currentTerm, votedFor int, log []LogEntry) {
	cp := append([]LogEntry(nil), log...)
	s.mu.Lock()
	defer s.mu.Unlock()
	s.term, s.votedFor, s.log = currentTerm, votedFor, cp
}

// 扩展练习（pg3）：再写一个 FileStorage（encoding/gob 单文件即可），
// 让 Cluster.Kill/Recover 走"真崩溃 + 重读盘"路径——接口已为此预留。
