// P1 MapReduce：word count，单进程内模拟 master + N 个 worker。
//
// 剧本（对应 L01/L02 与 pg1 的容错测试）：
//  1. 生成 6 个输入文件（map 任务数=6，reduce 分区数=3）。
//  2. 启动 5 个 worker；其中 2 个在运行中途"宕机"（crashAfter），
//     它们的 in-progress 任务由 master 心跳超时回收、由存活 worker 重做。
//  3. 1 个 worker 被注入"极慢"（本模拟用 crashAfter 恰在收尾前触发近似），
//     master 的备份任务机制保证作业不被拖死。
//  4. 结束后校验：输出总词数 == 单机直接统计结果（正确性不变量）。
package main

import (
	"fmt"
	"os"
	"strings"
	"sync"
	"time"

	"mapreduce.example/p1/mapreduce"
)

func wcMap(_ string, contents string) []mapreduce.KeyValue {
	var out []mapreduce.KeyValue
	for _, line := range strings.Split(contents, "\n") {
		for _, w := range strings.Fields(line) {
			w = strings.ToLower(strings.Trim(w, ".,!?\"'"))
			if w != "" {
				out = append(out, mapreduce.KeyValue{Key: w, Value: "1"})
			}
		}
	}
	return out
}

func wcReduce(key string, values []string) string {
	return fmt.Sprintf("%d", len(values))
}

func generateInputs(dir string, n int) []string {
	lorem := "the quick brown fox jumps over the lazy dog distributed systems fault tolerance consensus replication linearizability mapreduce the log the shard"
	var files []string
	for i := 0; i < n; i++ {
		p := fmt.Sprintf("%s/input-%02d.txt", dir, i)
		var b strings.Builder
		for j := 0; j < 40; j++ {
			b.WriteString(lorem)
			b.WriteString(fmt.Sprintf(" filler%03d word%d unique%d\n", i*100+j, j%7, i))
		}
		if err := os.WriteFile(p, []byte(b.String()), 0o644); err != nil {
			panic(err)
		}
		files = append(files, p)
	}
	return files
}

// 单机直接统计（校验基准）。
func referenceCount(files []string) map[string]int {
	ref := map[string]int{}
	for _, f := range files {
		data, err := os.ReadFile(f)
		if err != nil {
			panic(err)
		}
		for _, line := range strings.Split(string(data), "\n") {
			for _, w := range strings.Fields(line) {
				ref[strings.ToLower(strings.Trim(w, ".,!?\"'"))]++
			}
		}
	}
	return ref
}

func readOutput(job string, nReduce int) map[string]int {
	got := map[string]int{}
	for i := 0; i < nReduce; i++ {
		p := fmt.Sprintf("%s-%05d", job, i)
		data, err := os.ReadFile(p)
		if err != nil {
			continue
		}
		for _, line := range strings.Split(string(data), "\n") {
			kv := strings.SplitN(line, "\t", 2)
			if len(kv) != 2 {
				continue
			}
			var v int
			fmt.Sscanf(kv[1], "%d", &v)
			got[kv[0]] = v
		}
	}
	return got
}

func main() {
	dir, err := os.MkdirTemp("", "mr")
	if err != nil {
		panic(err)
	}
	if err := os.Chdir(dir); err != nil { // 中间/输出文件都写进临时目录
		panic(err)
	}
	const nMap, nReduce, nWorkers = 6, 3, 5
	files := generateInputs(dir, nMap)

	mapreduce.SetMapF(wcMap)
	mapreduce.SetReduceF(wcReduce)

	const job = "wc"
	master := mapreduce.NewMaster(job, files, nReduce,
		700*time.Millisecond, // 心跳超时 → 重做
		1500*time.Millisecond) // straggler → 备份
	srv := mapreduce.NewServer(master, "master")

	stop := make(chan struct{})
	var wg sync.WaitGroup
	wg.Add(1)
	go func() { defer wg.Done(); mapreduce.BackupWatch(master, stop) }()

	for i := 0; i < nWorkers; i++ {
		crash := time.Duration(0)
		switch i {
		case 1:
			crash = 900 * time.Millisecond // 中途宕机 → 触发超时重做
		case 3:
			crash = 2200 * time.Millisecond // 晚些宕机，再触发一次重做
		}
		w := &mapreduce.Worker{
			ID: i, Job: job, Client: mapreduce.NewClient(srv),
			NReduce: nReduce, CrashAfter: crash,
		}
		wg.Add(1)
		go func(ww *mapreduce.Worker) {
			defer wg.Done()
			ww.Run(stop)
		}(w)
	}

	master.WaitForCompletion()
	close(stop)
	// 等所有 map 任务完成后再让 worker 退出（reduce 依赖 map done，master 已门控）。
	done := make(chan struct{})
	go func() { wg.Wait(); close(done) }()
	select {
	case <-done:
	case <-time.After(5 * time.Second):
		fmt.Println("warn: some workers still running (crashed goroutines exit on their own)")
	}

	finished, redone, backups, elapsed := master.Done()
	ref := referenceCount(files)
	got := readOutput(job, nReduce)

	mismatch := 0
	for k, v := range ref {
		if got[k] != v {
			mismatch++
		}
	}
	for k := range got {
		if _, ok := ref[k]; !ok {
			mismatch++
		}
	}

	fmt.Printf("job=%s finished=%v elapsed=%v redo=%d backups=%d\n",
		job, finished, elapsed.Round(time.Millisecond), redone, backups)
	fmt.Printf("distinct words=%d (reference=%d) mismatches=%d\n",
		len(got), len(ref), mismatch)
	if mismatch == 0 && finished {
		fmt.Println("PASS: distributed result == single-machine reference")
	} else {
		fmt.Println("FAIL")
		os.Exit(1)
	}
}
