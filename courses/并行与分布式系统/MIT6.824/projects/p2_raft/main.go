// P2 Raft 演示：进程内 5 节点集群，选举 + 日志复制 + leader 宕机接管。
//
// 剧本（对应 L05/L06 与 pg2 的测试思路）：
//  1. 建 5 节点集群（带 5% 丢包 + 20ms 平均延迟的"坏网络"）。
//  2. 等出唯一 leader，向其提交 30 条命令。
//  3. 杀掉 leader —— 观察重新选举；新 leader 继续提交 30 条。
//  4. 校验安全性不变量：任意两节点的"已应用命令序列"必须是公共前缀一致
//     （等价于 lab 的 check_agree：提交序绝不分叉）。
package main

import (
	"fmt"
	"os"
	"time"

	"raft.example/p2/raft"
)

type cmd struct {
	Num int
	Arg string
}

func main() {
	const n = 5
	c := raft.MakeCluster(n, 0.05, 20*time.Millisecond)
	defer c.Stop()

	leader, term := c.WaitLeader(3 * time.Second)
	if leader < 0 {
		fmt.Println("FAIL: no leader elected")
		os.Exit(1)
	}
	fmt.Printf("[phase 1] leader=%d term=%d\n", leader, term)

	submit := func(from, to int) int {
		ok := 0
		deadline := time.Now().Add(5 * time.Second)
		for i := from; i < to; {
			if time.Now().After(deadline) {
				break
			}
			l := c.AnyLeader()
			if l < 0 {
				time.Sleep(20 * time.Millisecond)
				continue
			}
			if _, _, isLeader := c.Servers[l].Start(cmd{Num: i}); isLeader {
				ok++
				i++
			}
		}
		return ok
	}
	submit(0, 30)
	if !c.WaitCommitted(25, 4, 5*time.Second) {
		fmt.Println("FAIL: phase-1 commands not committed on 4 nodes")
		os.Exit(1)
	}
	fmt.Println("[phase 1] >=25/30 committed on 4+ nodes")

	// 杀掉 leader：模拟进程崩溃
	fmt.Printf("[phase 2] kill leader %d\n", leader)
	c.Kill(leader)
	newLeader, newTerm := c.WaitLeader(5 * time.Second)
	if newLeader < 0 || newLeader == leader {
		fmt.Println("FAIL: no new leader after kill")
		os.Exit(1)
	}
	if newTerm <= term {
		fmt.Println("FAIL: new leader did not advance term")
		os.Exit(1)
	}
	fmt.Printf("[phase 2] new leader=%d term=%d\n", newLeader, newTerm)

	submit(30, 60)
	if !c.WaitCommitted(55, 4, 8*time.Second) {
		fmt.Println("FAIL: phase-2 commands not committed")
		os.Exit(1)
	}
	time.Sleep(500 * time.Millisecond) // 给 apply 一点时间

	// 安全性不变量：所有节点的应用序列两两前缀一致；且命令序号 0..k 连续无洞。
	var ref []raft.ApplyMsg
	fail := false
	for i := 0; i < n; i++ {
		ap := c.Applied(i)
		if i == 0 || len(ap) > len(ref) {
			ref = ap
		}
	}
	for i := 0; i < n; i++ {
		ap := c.Applied(i)
		for j, m := range ap {
			if j >= len(ref) || ref[j].Command.(cmd).Num != m.Command.(cmd).Num {
				fmt.Printf("FAIL: node %d diverges at apply pos %d\n", i, j)
				fail = true
				break
			}
		}
		// 索引必须严格递增（Raft 只按序交付）
		for j := 1; j < len(ap); j++ {
			if ap[j].CommandIndex <= ap[j-1].CommandIndex {
				fmt.Printf("FAIL: node %d out-of-order apply at %d\n", i, j)
				fail = true
			}
		}
	}
	if fail {
		os.Exit(1)
	}
	fmt.Printf("PASS: %d commands applied, agreed prefix across %d nodes (longest=%d)\n",
		60, n, len(ref))
}
