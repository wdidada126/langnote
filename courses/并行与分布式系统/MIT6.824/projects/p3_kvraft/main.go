// P3 容错分布式 KV 演示：3 节点 Raft 集群 + Put/Append/Get 客户端，
// 依次杀掉 leader 与一个 follower，验证客户端无感切换 + 副本状态一致。
//
// 对应讲次：L05/L06（共识内核）、L01（客户端幂等重试）、L09（面向故障）、L10（读一致性）。
package main

import (
	"fmt"
	"os"
	"reflect"
	"sync"
	"time"

	"kv.example/p3/kv"
)

func main() {
	kc := kv.MakeKVCluster(3, 0.02, 10*time.Millisecond)
	if _, ok := waitLeader(kc, 3*time.Second); !ok {
		fmt.Println("FAIL: no leader")
		os.Exit(1)
	}

	ck := kv.MakeClerk(kc.Servers)

	// --- 1. 基础语义 ---
	ck.Put("greeting", "hello")
	ck.Append("greeting", " world")
	if v := ck.Get("greeting"); v != "hello world" {
		fmt.Printf("FAIL: got %q want %q\n", v, "hello world")
		os.Exit(1)
	}
	fmt.Println("[1] Put/Append/Get semantics OK")

	// --- 2. 杀掉 leader：客户端超时/被拒 → 换节点重试，新 leader 上任后继续 ---
	oldLeader := kc.AnyLeaderServer()
	kc.Kill(oldLeader)
	if _, ok := waitLeader(kc, 5*time.Second); !ok {
		fmt.Println("FAIL: no re-election after killing leader")
		os.Exit(1)
	}
	ck.Put("phase", "after-leader-death") // 内含重试：Handler 返回 WrongLeader/Timeout 时换服务器
	fmt.Printf("[2] writes survive leader death (killed %d, client auto-switched)\n", oldLeader)

	// --- 3. 再杀一个 follower（集群 3 存 2，仍是多数派）---
	for i := range kc.Servers {
		if i != oldLeader && kc.RaftClus.T.Alive(i) {
			kc.Kill(i)
			fmt.Printf("[3] also killed follower %d\n", i)
			break
		}
	}
	ck.Append("phase", "|still-alive")
	if v := ck.Get("phase"); v != "after-leader-death|still-alive" {
		fmt.Printf("FAIL: phase = %q\n", v)
		os.Exit(1)
	}
	fmt.Println("[3] writes survive two node deaths (majority held)")

	// --- 4. 并发压测：4 个客户端各写独立 key ---
	var wg sync.WaitGroup
	for g := 0; g < 4; g++ {
		wg.Add(1)
		go func(g int) {
			defer wg.Done()
			c2 := kv.MakeClerk(kc.Servers) // 独立客户端（独立会话/去重域）
			for i := 0; i < 10; i++ {
				k := fmt.Sprintf("g%d-k%d", g, i)
				c2.Put(k, "v")
				c2.Append(k, fmt.Sprintf("%d", i))
				if v := c2.Get(k); v != fmt.Sprintf("v%d", i) {
					fmt.Printf("FAIL: %s = %q\n", k, v)
					os.Exit(1)
				}
			}
		}(g)
	}
	wg.Wait()
	fmt.Println("[4] concurrent clients OK")

	// --- 5. 安全性校验：所有存活副本状态机一致（复制状态机的定义） ---
	time.Sleep(500 * time.Millisecond) // 给刚恢复节点一点追赶时间
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
		if !reflect.DeepEqual(ref, st) {
			fmt.Printf("FAIL: replica %d diverges from agreed state\n", i)
			os.Exit(1)
		}
	}
	fmt.Printf("PASS: replicated KV consistent, %d keys, alive replicas agree\n", len(ref))
}

func waitLeader(kc *kv.KVCluster, timeout time.Duration) (int, bool) {
	deadline := time.Now().Add(timeout)
	for time.Now().Before(deadline) {
		if l := kc.AnyLeaderServer(); l >= 0 {
			return l, true
		}
		time.Sleep(20 * time.Millisecond)
	}
	return -1, false
}
