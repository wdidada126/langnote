// kv 层多节点测试：语义、并发、崩溃切换、请求去重。
// 思想取自 6.824 pg2/pg3 的 kill/misbehave 测试矩阵（此处仅崩溃模型）。
package kv_test

import (
	"fmt"
	"sync"
	"testing"
	"time"

	"kv.example/p3/kv"
)

func startCluster(t *testing.T, n int) *kv.KVCluster {
	t.Helper()
	kc := kv.MakeKVCluster(n, 0.05, 8*time.Millisecond)
	deadline := time.Now().Add(5 * time.Second)
	for time.Now().Before(deadline) {
		if kc.AnyLeaderServer() >= 0 {
			return kc
		}
		time.Sleep(10 * time.Millisecond)
	}
	t.Fatalf("no leader in fresh cluster")
	return nil
}

// TestBasicSemantics：Put 覆盖、Append 追加、Get 读己之写。
func TestBasicSemantics(t *testing.T) {
	kc := startCluster(t, 3)
	defer kc.RaftClus.Stop()
	ck := kv.MakeClerk(kc.Servers)

	ck.Put("k", "1")
	ck.Append("k", "2")
	ck.Append("k", "3")
	if v := ck.Get("k"); v != "123" {
		t.Fatalf("k=%q want 123", v)
	}
	ck.Put("k", "x") // Put 应覆盖
	if v := ck.Get("k"); v != "x" {
		t.Fatalf("after Put k=%q want x", v)
	}
	if v := ck.Get("missing"); v != "" {
		t.Fatalf("missing key = %q want empty", v)
	}
}

// TestConcurrentClients：多客户端交叉写，副本收敛到同一状态机。
func TestConcurrentClients(t *testing.T) {
	kc := startCluster(t, 5)
	defer kc.RaftClus.Stop()

	var wg sync.WaitGroup
	for g := 0; g < 6; g++ {
		wg.Add(1)
		go func(g int) {
			defer wg.Done()
			ck := kv.MakeClerk(kc.Servers)
			for i := 0; i < 8; i++ {
				key := fmt.Sprintf("c%d-k%d", g, i)
				ck.Put(key, "a")
				ck.Append(key, "b")
				if v := ck.Get(key); v != "ab" {
					t.Errorf("%s=%q want ab", key, v)
					return
				}
			}
		}(g)
	}
	wg.Wait()
	time.Sleep(400 * time.Millisecond)

	var ref map[string]string
	for i, sv := range kc.Servers {
		if !kc.RaftClus.T.Alive(i) {
			continue
		}
		st := sv.StateSnapshot()
		if ref == nil {
			ref = st
			continue
		}
		for k, v := range ref {
			if st[k] != v {
				t.Fatalf("replica %d diverges on %s: %q vs %q", i, k, st[k], v)
			}
		}
	}
}

// TestLeaderFailover：写若干轮，每轮随机杀 leader；最终数据完整且副本一致。
func TestLeaderFailover(t *testing.T) {
	kc := startCluster(t, 5)
	defer kc.RaftClus.Stop()
	ck := kv.MakeClerk(kc.Servers)

	for r := 0; r < 4; r++ {
		ck.Put(fmt.Sprintf("r%d", r), fmt.Sprintf("v%d", r))
		// 只杀两轮 leader：5 节点最多损失 2，多数派常在，最终读才安全
		if l := kc.AnyLeaderServer(); l >= 0 && r < 2 {
			kc.Kill(l)
			time.Sleep(200 * time.Millisecond)
		}
	}
	// 最后一轮全部可查
	time.Sleep(500 * time.Millisecond)
	for r := 0; r < 4; r++ {
		if v := ck.Get(fmt.Sprintf("r%d", r)); v != fmt.Sprintf("v%d", r) {
			t.Fatalf("r%d lost/changed after failover: %q", r, v)
		}
	}
}

// TestDedupIdempotence：同一 (clientID, requestID) 的重复投递只执行一次。
// 直接模拟"客户端重试撞上双份提交"：对同一请求连发两次 Handler。
func TestDedupIdempotence(t *testing.T) {
	kc := startCluster(t, 3)
	defer kc.RaftClus.Stop()

	// 定位 leader，向它直投两次相同去重键的 Append
	l := kc.AnyLeaderServer()
	req := kv.Request{
		ClientID: 424242, RequestID: 7,
		Method: "PutAppend", Key: "dup", Value: "X", Op: "append",
	}
	r1 := kc.Servers[l].Handler(req)
	if r1.Err != "" {
		t.Fatalf("first handler call err: %q", r1.Err)
	}
	r2 := kc.Servers[l].Handler(req) // 同 requestID → 应重放旧结果而非再执行
	if r2.Err != "" {
		t.Fatalf("second handler call err: %q", r2.Err)
	}
	if v := kc.Servers[kc.AnyLeaderServer()].StateSnapshot()["dup"]; v != "X" {
		t.Fatalf("dedup failed: value=%q want single X", v)
	}
}
