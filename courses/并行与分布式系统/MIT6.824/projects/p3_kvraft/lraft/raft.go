// Package lraft 实现 Raft 共识算法的简化核心：
// leader 选举 + 日志复制（安全性：仅当前 term 提交、选举限制），
// 不含快照与成员变更（对应 6.824 pg2 的 A+B 范围，README 有说明）。
//
// 对应讲次：L05/L06（Raft 论文与安全性），L01（RPC），L08（Paxos 对照）。
package lraft

import (
	"math/rand"
	"sync"
	"time"
)

// ApplyMsg 是交付给状态机（上层）的一条已提交命令。
type ApplyMsg struct {
	CommandValid bool
	Command      interface{}
	CommandIndex int // 1-based（与论文日志编号一致）
	CommandTerm  int
}

// LogEntry 一条日志：任期 + 命令。Noop 条目用于新 leader 提交旧 term 日志（L06 §1）。
type LogEntry struct {
	Term    int
	Command interface{}
	IsNoop  bool
}

const (
	follower = iota
	candidate
	leader
)

// 关键时序参数（论文的 150-300ms 选举超时 + 100ms 心跳）。
var (
	HeartbeatInterval = 100 * time.Millisecond
	ElectionMin       = 150 * time.Millisecond
	ElectionMax       = 300 * time.Millisecond
	pollInterval      = 10 * time.Millisecond
)

// RequestVoteArgs / RequestVoteReply：L05 §2.2 选举 RPC。
type RequestVoteArgs struct {
	Term         int
	CandidateID  int
	LastLogIndex int // 1-based；0 表示空日志
	LastLogTerm  int
}

type RequestVoteReply struct {
	Term        int
	VoteGranted bool
}

// AppendEntriesArgs / AppendEntriesReply：L05 §2.3 日志复制 RPC（兼心跳）。
type AppendEntriesArgs struct {
	Term         int
	LeaderID     int
	PrevLogIndex int // 紧接新条目前一条（1-based；0=日志起点之前）
	PrevLogTerm  int
	Entries      []LogEntry
	LeaderCommit int
}

type AppendEntriesReply struct {
	Term    int
	Success bool
	// 简化版回退提示：只用 nextIndex-- 策略（Ongaro 论文 §3.3 的低效但正确做法）。
}

// Raft 单个节点。
type Raft struct {
	mu   sync.Mutex
	me   int
	role int
	t    *Transport

	// 持久状态（pg3 范围；这里交给我们注入的 StateStorage，默认内存版）。
	currentTerm int
	votedFor    int // -1 表示未投
	log         []LogEntry
	store       StateStorage

	// 易失状态
	commitIndex int // 已提交的最大索引（1-based；0=无）
	lastApplied int // 已交付状态机的最大索引

	// leader 易失状态
	nextIndex  []int
	matchIndex []int

	lastHeartbeat time.Time // 最近一次"认可当前 leader"的时刻
	electionTO    time.Duration
	votes         int

	applyCh chan ApplyMsg
	done    chan struct{} // Shutdown 关闭，停掉所有循环
	closeOnce sync.Once
	rng     *rand.Rand
}

// Make 创建并启动一个节点：peers 为全体节点 id（含自己）。
func Make(me int, peers []int, t *Transport, store StateStorage) *Raft {
	rf := &Raft{
		me:        me,
		role:      follower,
		t:         t,
		votedFor:  -1,
		store:     store,
		applyCh:   make(chan ApplyMsg, 1000),
		done:      make(chan struct{}),
		rng:       rand.New(rand.NewSource(int64(me)*7919+time.Now().UnixNano())),
	}
	if store != nil {
		pterm, pvote, plog := store.Read()
		rf.currentTerm, rf.votedFor, rf.log = pterm, pvote, plog
	}
	rf.resetElectionTimeout()
	rf.lastHeartbeat = time.Now()
	go rf.mainLoop()
	go rf.applyLoop()
	return rf
}

// GetApplyChan 暴露状态机投递通道（每个节点必须有人持续读取）。
func (rf *Raft) GetApplyChan() <-chan ApplyMsg { return rf.applyCh }

// Shutdown 停止该节点（进程退出的模拟）。
func (rf *Raft) Shutdown() {
 rf.closeOnce.Do(func() { close(rf.done) })
}

func (rf *Raft) resetElectionTimeout() {
	d := ElectionMax - ElectionMin
	rf.electionTO = ElectionMin + time.Duration(rf.rng.Int63n(int64(d)))
	rf.lastHeartbeat = time.Now()
}

func (rf *Raft) persist() {
	if rf.store != nil {
		rf.store.Save(rf.currentTerm, rf.votedFor, rf.log)
	}
}

// ---------------------------------------------------------------------------
// 主循环：选举超时驱动 + 心跳驱动（一个 ticker 全包，节奏 pollInterval）。
// ---------------------------------------------------------------------------

func (rf *Raft) mainLoop() {
	for {
		select {
		case <-rf.done:
			return
		case <-time.After(pollInterval):
		}
		rf.mu.Lock()
		switch rf.role {
		case leader:
			if time.Since(rf.lastHeartbeat) >= HeartbeatInterval {
				rf.broadcastAppendEntries()
			}
		default: // follower / candidate
			if time.Since(rf.lastHeartbeat) >= rf.electionTO {
				rf.becomeCandidate()
			}
		}
		rf.mu.Unlock()
	}
}

// applyLoop：把 commitIndex 前缀中新到的非 Noop 条目交付 applyCh。
// leader 与 follower 都靠它"消费提交进度"（leader 的 commitIndex 由心跳推进）。
func (rf *Raft) applyLoop() {
	for {
		rf.mu.Lock()
		if rf.lastApplied < rf.commitIndex && rf.commitIndex <= len(rf.log) {
			start, end := rf.lastApplied+1, rf.commitIndex
			msgs := make([]ApplyMsg, 0, end-start)
			for i := start; i <= end; i++ {
				e := rf.log[i-1]
				if e.IsNoop {
					continue
				}
				msgs = append(msgs, ApplyMsg{
					CommandValid: true, Command: e.Command,
					CommandIndex: i, CommandTerm: e.Term,
				})
			}
			rf.lastApplied = end
			rf.mu.Unlock()
			for _, m := range msgs {
				select {
				case rf.applyCh <- m:
				case <-rf.done:
					return
				}
			}
			continue
		}
		rf.mu.Unlock()
		select {
		case <-rf.done:
			return
		case <-time.After(pollInterval):
		}
	}
}

// ---------------------------------------------------------------------------
// 选举（L05 §2.2 / L06 §1 安全性：投票给"日志至少一样新"的候选人）
// ---------------------------------------------------------------------------

func (rf *Raft) becomeCandidate() {
	rf.currentTerm++
	rf.role = candidate
	rf.votedFor = rf.me
	rf.votes = 1
	rf.persist()
	rf.resetElectionTimeout()

	args := RequestVoteArgs{
		Term:        rf.currentTerm,
		CandidateID: rf.me,
	}
	if n := len(rf.log); n > 0 {
		args.LastLogIndex = n
		args.LastLogTerm = rf.log[n-1].Term
	}
	peers := rf.t.PeerIDs(rf.me)
	for _, to := range peers {
		go func(to int) {
			reply := RequestVoteReply{}
			ok := rf.t.Call(to, func(s *Raft) {
				reply = s.handleRequestVote(args)
			}) == nil
			if !ok {
				return
			}
			rf.mu.Lock()
			defer rf.mu.Unlock()
			if reply.Term > rf.currentTerm {
				rf.becomeFollowerLocked(reply.Term)
				return
			}
			if rf.role == candidate && reply.Term == rf.currentTerm && reply.VoteGranted {
				rf.votes++
				if rf.votes >= rf.t.N()/2+1 {
					rf.becomeLeader()
				}
			}
		}(to)
	}
}

func (rf *Raft) becomeLeader() {
	rf.role = leader
	rf.nextIndex = make([]int, rf.t.N())
	rf.matchIndex = make([]int, rf.t.N())
	for i := range rf.nextIndex {
		rf.nextIndex[i] = len(rf.log) + 1
	}
	rf.resetElectionTimeout() // 复用时间戳字段：心跳节拍
	// 新 leader 追加 Noop：间接提交旧 term 条目（L06 §1 图 4.3 的解法）。
	noop := LogEntry{Term: rf.currentTerm, Command: nil, IsNoop: true}
	rf.log = append(rf.log, noop)
	rf.persist()
	rf.broadcastAppendEntries()
}

func (rf *Raft) handleRequestVote(args RequestVoteArgs) RequestVoteReply {
	rf.mu.Lock()
	defer rf.mu.Unlock()
	reply := RequestVoteReply{Term: rf.currentTerm}
	if args.Term < rf.currentTerm {
		return reply
	}
	if args.Term > rf.currentTerm {
		rf.becomeFollowerLocked(args.Term)
		reply.Term = rf.currentTerm
	}
	// 日志新旧比较（选举限制，L05 §2.2 图 2）
	lastIdx, lastTerm := len(rf.log), 0
	if lastIdx > 0 {
		lastTerm = rf.log[lastIdx-1].Term
	}
	upToDate := args.LastLogTerm > lastTerm ||
		(args.LastLogTerm == lastTerm && args.LastLogIndex >= lastIdx)
	if upToDate && (rf.votedFor == -1 || rf.votedFor == args.CandidateID) {
		rf.votedFor = args.CandidateID
		rf.persist()
		rf.lastHeartbeat = time.Now() // 投出去也算"听到"有效领导者活动
		reply.VoteGranted = true
		reply.Term = rf.currentTerm
	}
	return reply
}

// becomeFollowerLocked：调用者已持锁。转 follower 并记录新 term（持久化）。
func (rf *Raft) becomeFollowerLocked(term int) {
	rf.role = follower
	rf.currentTerm = term
	rf.votedFor = -1
	rf.persist()
	rf.resetElectionTimeout()
}

// ---------------------------------------------------------------------------
// 日志复制（L05 §2.3；回退策略：nextIndex--，简单正确）
// ---------------------------------------------------------------------------

func (rf *Raft) broadcastAppendEntries() {
	entries := append([]LogEntry(nil), rf.log...)
	for _, to := range rf.t.PeerIDs(rf.me) {
		next := rf.nextIndex[to]
		if next < 1 {
			next = 1
		}
		if next > len(entries)+1 {
			next = len(entries) + 1
		}
		args := AppendEntriesArgs{
			Term:         rf.currentTerm,
			LeaderID:     rf.me,
			PrevLogIndex: next - 1,
			LeaderCommit: rf.commitIndex,
		}
		if next-1 > 0 {
			args.PrevLogTerm = entries[next-2].Term
		}
		if next-1 < len(entries) {
			args.Entries = append([]LogEntry(nil), entries[next-1:]...)
		}
		go func(to int, args AppendEntriesArgs) {
			reply := AppendEntriesReply{}
			ok := rf.t.Call(to, func(s *Raft) {
				reply = s.handleAppendEntries(args)
			}) == nil
			if !ok {
				return
			}
			rf.mu.Lock()
			defer rf.mu.Unlock()
			if rf.role != leader {
				return
			}
			if reply.Term > rf.currentTerm {
				rf.becomeFollowerLocked(reply.Term)
				return
			}
			if reply.Success {
				rf.matchIndex[to] = args.PrevLogIndex + len(args.Entries)
				rf.nextIndex[to] = rf.matchIndex[to] + 1
				rf.tryAdvanceCommit()
			} else {
				if rf.nextIndex[to] > 1 {
					rf.nextIndex[to]--
				}
			}
		}(to, args)
	}
	rf.lastHeartbeat = time.Now()
}

func (rf *Raft) handleAppendEntries(args AppendEntriesArgs) AppendEntriesReply {
	rf.mu.Lock()
	defer rf.mu.Unlock()
	reply := AppendEntriesReply{Term: rf.currentTerm}
	if args.Term < rf.currentTerm {
		return reply
	}
	if args.Term > rf.currentTerm {
		rf.becomeFollowerLocked(args.Term)
	}
	rf.role = follower // candidate 收到合法 AE 即臣服
	rf.lastHeartbeat = time.Now()

	// 一致性检查：PrevLogIndex 处必须存在且 term 匹配（0 视为恒真）。
	if args.PrevLogIndex > len(rf.log) {
		return AppendEntriesReply{Term: rf.currentTerm, Success: false}
	}
	if args.PrevLogIndex > 0 && rf.log[args.PrevLogIndex-1].Term != args.PrevLogTerm {
		// 冲突：删除该位置起的后缀（仅未提交部分可能与 leader 冲突，
		// 已提交前缀由安全性论证保证一致——见 L06 §1）。
		rf.log = rf.log[:args.PrevLogIndex-1]
		rf.persist()
		return AppendEntriesReply{Term: rf.currentTerm, Success: false}
	}
	if len(args.Entries) > 0 {
		// 追加（若已有相同 term/index 的条目，视为一致前缀，直接补齐尾部）。
		if args.PrevLogIndex < len(rf.log) {
			rf.log = rf.log[:args.PrevLogIndex] // 防御性截断
		}
		rf.log = append(rf.log, args.Entries...)
		rf.persist()
	}
	if args.LeaderCommit > rf.commitIndex {
		rf.commitIndex = args.LeaderCommit
		if rf.commitIndex > len(rf.log) {
			rf.commitIndex = len(rf.log)
		}
	}
	return AppendEntriesReply{Term: rf.currentTerm, Success: true}
}

// tryAdvanceCommit：leader 推进提交（L06 规则：只直接提交当前 term 条目）。
// rf.mu 必须已持有。
func (rf *Raft) tryAdvanceCommit() {
	if rf.role != leader {
		return
	}
	majority := rf.t.N()/2 + 1
	for n := rf.commitIndex + 1; n <= len(rf.log); n++ {
		if rf.log[n-1].Term != rf.currentTerm {
			continue // 旧 term 条目由"提交更新的当前 term 条目"间接提交
		}
		cnt := 1 // 自己
		for i := range rf.matchIndex {
			if i != rf.me && rf.matchIndex[i] >= n {
				cnt++
			}
		}
		if cnt >= majority {
			rf.commitIndex = n
		} else {
			break
		}
	}
}

// ---------------------------------------------------------------------------
// 客户端入口
// ---------------------------------------------------------------------------

// Start 把命令交给 Raft：leader 返回 (日志索引, term, true)。
// 非 leader 返回 isLeader=false（上层重试/重定向——L01 绑定策略）。
func (rf *Raft) Start(command interface{}) (int, int, bool) {
	rf.mu.Lock()
	defer rf.mu.Unlock()
	if rf.role != leader {
		return -1, rf.currentTerm, false
	}
	entry := LogEntry{Term: rf.currentTerm, Command: command}
	rf.log = append(rf.log, entry)
	rf.persist()
	rf.broadcastAppendEntries() // 立即推一把（原版靠心跳循环，这里降延迟）
	return len(rf.log), rf.currentTerm, true
}

// Status 暴露内省信息（测试/demo 用）。
func (rf *Raft) Status() (role string, term int, commit int, lastApplied int, logLen int) {
	rf.mu.Lock()
	defer rf.mu.Unlock()
	switch rf.role {
	case leader:
		role = "leader"
	case candidate:
		role = "candidate"
	default:
		role = "follower"
	}
	return role, rf.currentTerm, rf.commitIndex, rf.lastApplied, len(rf.log)
}
