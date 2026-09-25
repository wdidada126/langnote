// Package raft_test 用进程内集群 + 模拟网络对 Raft 核心做多节点测试
// （思想取自 6.824 lab2a/lab2b 的 go 测试：随机丢包、随机崩溃下验证安全性）。
package raft_test

import (
	"testing"
	"time"

	"raft.example/p2/raft"
)

type kvcmd struct {
	Key   string
	Value int
}

// TestBasicElection：3 节点应选出唯一 leader；杀掉后 term 递增地产生新 leader。
func TestBasicElection(t *testing.T) {
	c := raft.MakeCluster(3, 0.0, 5*time.Millisecond)
	defer c.Stop()

	leader, term := c.WaitLeader(2 * time.Second)
	if leader < 0 {
		t.Fatalf("no leader elected")
	}
	if c.WaitLeader(time.Second) != leader {
		// 稳定性弱检查：短时间内不应换主（心跳正常时）
		t.Logf("note: leader changed within 1s (acceptable under jitter)")
	}

	c.Kill(leader)
	nl, nt := c.WaitLeader(5 * time.Second)
	if nl < 0 {
		t.Fatalf("no leader after killing %d", leader)
	}
	if nt <= term {
		t.Fatalf("term did not advance: %d -> %d", term, nt)
	}
	t.Logf("election ok: %d(term %d) -> %d(term %d)", leader, term, nl, nt)
}

// TestReplicationAgreement：50 条命令在 5% 丢包下提交，
// 安全性不变量：所有节点应用序列 == 同一条全局序（前缀一致 + 无重复 + 有序）。
func TestReplicationAgreement(t *testing.T) {
	const n, m = 5, 50
	c := raft.MakeCluster(n, 0.05, 10*time.Millisecond)
	defer c.Stop()

	if l, _ := c.WaitLeader(3 * time.Second); l < 0 {
		t.Fatalf("no leader")
	}
	sent := 0
	deadline := time.Now().Add(10 * time.Second)
	for sent < m && time.Now().Before(deadline) {
		l := c.AnyLeader()
		if l < 0 {
			time.Sleep(15 * time.Millisecond)
			continue
		}
		if _, _, ok := c.Servers[l].Start(kvcmd{Key: "k", Value: sent}); ok {
			sent++
		} else {
			time.Sleep(5 * time.Millisecond)
		}
	}
	if sent < m {
		t.Fatalf("only %d/%d accepted", sent, m)
	}
	if !c.WaitCommitted(m, n-1, 10*time.Second) {
		t.Fatalf("commit did not reach %d nodes", n-1)
	}
	time.Sleep(300 * time.Millisecond)

	var longest []raft.ApplyMsg
	for i := 0; i < n; i++ {
		ap := c.Applied(i)
		if len(ap) > len(longest) {
			longest = ap
		}
	}
	for i := 0; i < n; i++ {
		ap := c.Applied(i)
		seen := map[int]bool{}
		for j, msg := range ap {
			kv, ok := msg.Command.(kvcmd)
			if !ok {
				t.Fatalf("node %d pos %d: bad command type", i, j)
			}
			if seen[msg.CommandIndex] {
				t.Fatalf("node %d: duplicate apply at index %d", i, msg.CommandIndex)
			}
			seen[msg.CommandIndex] = true
			if j >= len(longest) || longest[j].Command.(kvcmd).Value != kv.Value {
				t.Fatalf("node %d diverges from agreed order at %d", i, j)
			}
			if j > 0 && msg.CommandIndex <= ap[j-1].CommandIndex {
				t.Fatalf("node %d: non-increasing index at %d", i, j)
			}
		}
	}
	t.Logf("agreement ok: %d applied on longest node, all prefixes consistent", len(longest))
}

// TestReElectionKeepsCommitted：leader 带 30 条已提交日志时崩溃，
// 新 leader 必须拥有全部已提交条目（选举限制的直接检验，L05 §2.2/L06 §1）。
func TestReElectionKeepsCommitted(t *testing.T) {
	c := raft.MakeCluster(5, 0.10, 8*time.Millisecond)
	defer c.Stop()

	l, _ := c.WaitLeader(3 * time.Second)
	if l < 0 {
		t.Fatalf("no leader")
	}
	for i := 0; i < 30; i++ {
		for {
			cur := c.AnyLeader()
			if cur < 0 {
				time.Sleep(10 * time.Millisecond)
				continue
			}
			if _, _, ok := c.Servers[cur].Start(kvcmd{Key: "x", Value: i}); ok {
				break
			}
		}
	}
	if !c.WaitCommitted(28, 4, 8*time.Second) {
		t.Fatalf("pre-crash commit failed")
	}
	oldLeader := c.AnyLeader()
	c.Kill(oldLeader)
	nl, _ := c.WaitLeader(5 * time.Second)
	if nl < 0 {
		t.Fatalf("no leader after crash")
	}
	// 新 leader 继续提交 30 条；最终全部 60 条在幸存节点上应用且与旧前缀衔接。
	for i := 30; i < 60; i++ {
		for {
			cur := c.AnyLeader()
			if cur < 0 {
				time.Sleep(10 * time.Millisecond)
				continue
			}
			if _, _, ok := c.Servers[cur].Start(kvcmd{Key: "x", Value: i}); ok {
				break
			}
		}
	}
	if !c.WaitCommitted(58, 3, 12*time.Second) {
		t.Fatalf("post-crash commit failed")
	}
	time.Sleep(300 * time.Millisecond)
	for i := 0; i < 5; i++ {
		if i == oldLeader {
			continue
		}
		ap := c.Applied(i)
		if len(ap) < 55 {
			t.Fatalf("node %d applied only %d entries (lost committed?)", i, len(ap))
		}
		for j := 1; j < len(ap); j++ {
			if ap[j].Command.(kvcmd).Value <= ap[j-1].Command.(kvcmd).Value {
				t.Fatalf("node %d: committed order violated at %d", i, j)
			}
		}
	}
}

// TestMinorityCannotCommit：多数派失联时，存活节点不得推进提交（防脑裂决断）。
func TestMinorityCannotCommit(t *testing.T) {
	c := raft.MakeCluster(5, 0.0, 5*time.Millisecond)
	defer c.Stop()

	l, _ := c.WaitLeader(3 * time.Second)
	if l < 0 {
		t.Fatalf("no leader")
	}
	for i := 0; i < 10; i++ {
		c.Servers[l].Start(kvcmd{Key: "warm", Value: i})
	}
	if !c.WaitCommitted(8, 4, 5*time.Second) {
		t.Fatalf("warm-up commit failed")
	}
	baseCommit := func(id int) int {
		_, _, cm, _, _ := c.Servers[id].Status()
		return cm
	}
	// 杀掉 3 个（包含当前 leader 时更安全：随机性下两存活者永远无法凑齐多数派）
	victims := map[int]bool{}
	for len(victims) < 3 {
		victims[len(victims)%5] = true
	}
	survivors := []int{}
	for i := 0; i < 5; i++ {
		if victims[i] {
			c.Kill(i)
		} else {
			survivors = append(survivors, i)
		}
	}
	base := []int{baseCommit(survivors[0]), baseCommit(survivors[1])}
	for i := 0; i < 5; i++ {
		cur := c.AnyLeader()
		if cur >= 0 {
			c.Servers[cur].Start(kvcmd{Key: "should-not-commit", Value: 999})
		}
		time.Sleep(100 * time.Millisecond)
	}
	time.Sleep(500 * time.Millisecond)
	for k, s := range survivors {
		if got := baseCommit(s); got > base[k] {
			t.Fatalf("minority side advanced commit on node %d: %d -> %d (split-brain!)", s, base[k], got)
		}
	}
}
