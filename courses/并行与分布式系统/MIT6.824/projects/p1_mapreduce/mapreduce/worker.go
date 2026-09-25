package mapreduce

import (
	"fmt"
	"os"
	"sort"
	"strings"
	"time"
)

// KeyValue 是 map/reduce 之间的记录类型（论文：value 对 MapReduce 不透明，这里是字符串）。
type KeyValue struct {
	Key   string
	Value string
}

// MapF / ReduceF：用户函数签名（论文 §2 的 map/reduce 接口）。
type MapF func(filename string, contents string) []KeyValue
type ReduceF func(key string, values []string) string

// ---------------------------------------------------------------------------
// 小工具（避免额外 import 负担）
// ---------------------------------------------------------------------------

func splitLines(s string) []string {
	return strings.Split(s, "\n")
}

func cutKV(line string) (string, string, bool) {
	i := strings.Index(line, "\t")
	if i < 0 {
		return "", "", false
	}
	return line[:i], line[i+1:], true
}

// 文件命名约定：map 输出按 (mapID, reduceID) 分区落盘，rename 原子发布；
// reduce 读取全部 mapID 中自己分区的文件（对应论文 "intermediate files on local disk"）。
func mapPartitionFile(job string, mapID, partID int) string {
	return fmt.Sprintf("mrapps.%s.map-%05d-part-%05d", job, mapID, partID)
}

func finalOutputFile(job string, reduceID int) string {
	return fmt.Sprintf("%s-%05d", job, reduceID)
}

// ---------------------------------------------------------------------------
// Worker
// ---------------------------------------------------------------------------

// Worker 轮询 master 领取任务并执行；参数控制其"故障剧本"。
type Worker struct {
	ID      int
	Job     string
	Client  *Client // 指向 master 的 RPC 客户端
	NReduce int

	// CrashAfter > 0：worker 启动后运行该时长即"宕机"（goroutine 直接退出，
	// 停止心跳 → master 超时回收其任务 → 其他 worker 重做）。
	CrashAfter time.Duration
}

// Run 是 worker 主循环（被 go 起来）。返回时模拟进程退出。
func (w *Worker) Run(done <-chan struct{}) {
	deadline := time.Now().Add(w.CrashAfter)
	for {
		select {
		case <-done:
			return
		default:
		}
		if w.CrashAfter > 0 && time.Now().After(deadline) {
			return // 宕机：不回心跳、不发布结果
		}
		if worked := w.tryMapTask(); worked {
			continue
		}
		if worked := w.tryReduceTask(); worked {
			continue
		}
		time.Sleep(15 * time.Millisecond) // idle 心跳间隔（轮询即心跳，对照 lab2 注释）
	}
}

// tryMapTask 领取并执行一个 map 任务。
func (w *Worker) tryMapTask() bool {
	var mapID int
	var inFile string
	ok := false
	err := Call(w.Client, func(t interface{}) {
		m := t.(*Master)
		mapID, inFile, ok = m.acquireMapTask(w.ID)
	})
	if err != nil || !ok {
		return false
	}
	contents, ferr := os.ReadFile(inFile)
	if ferr != nil {
		// 输入坏了：释放任务，等超时重做（真实系统里是报错重排）。
		w.report("map", mapID)
		return true
	}
	kvs := w.callMapF(inFile, string(contents))
	// 按 reduce 分区写中间文件（论文：partition = hash(key) mod R）。
	buckets := make([][]KeyValue, w.NReduce)
	for _, kv := range kvs {
		p := strings.ToLower(kv.Key)
		h := 0
		for i := 0; i < len(p); i++ {
			h = (h*31 + int(p[i])) & 0x7fffffff
		}
		pid := h % w.NReduce
		buckets[pid] = append(buckets[pid], kv)
	}
	for pid, b := range buckets {
		path := mapPartitionFile(w.Job, mapID, pid)
		if werr := writeKVFile(path, b); werr != nil {
			w.report("map", mapID)
			return true
		}
	}
	w.report("map", mapID)
	return true
}

// tryReduceTask 领取并执行一个 reduce 任务（仅当全部 map 完成后 master 才派发）。
func (w *Worker) tryReduceTask() bool {
	var redID int
	var outName string
	ok := false
	err := Call(w.Client, func(t interface{}) {
		m := t.(*Master)
		redID, outName, ok = m.acquireReduceTask(w.ID)
	})
	if err != nil || !ok {
		return false
	}
	// 收集所有 map 的本分区中间文件（mapID 从 master 拿布局）。
	var nMap int
	Call(w.Client, func(t interface{}) {
		m := t.(*Master)
		_, nMap = m.jobLayout()
	})
	kvs := make(map[string][]string)
	for mid := 0; mid < nMap; mid++ {
		path := mapPartitionFile(w.Job, mid, redID)
		recs, rerr := readKVFile(path)
		if rerr != nil {
			continue // 该 map 输出为空
		}
		for _, r := range recs {
			kvs[r.Key] = append(kvs[r.Key], r.Value)
		}
	}
	keys := make([]string, 0, len(kvs))
	for k := range kvs {
		keys = append(keys, k)
	}
	sort.Strings(keys) // 论文：reduce 前按 key 排序（保证输出确定性与归并便利）
	var out []KeyValue
	for _, k := range keys {
		out = append(out, KeyValue{Key: k, Value: w.callReduceF(k, kvs[k])})
	}
	writeKVFile(finalOutputFile(w.Job, redID), out)
	w.report("reduce", redID)
	return true
}

// report 向 master 上报任务完成（RPC 可能失败：失败无所谓——
// 心跳超时会回收重做，完成上报本身幂等）。
func (w *Worker) report(kind string, id int) {
	_ = Call(w.Client, func(t interface{}) {
		m := t.(*Master)
		m.releaseTask(kind, id, w.ID)
	})
}

// callMapF/callReduceF：在 worker 本地执行用户函数（原版经 RPC 回传给
// 注册了函数的"协调进程"；同进程内直接闭包共享）。
func (w *Worker) callMapF(f string, c string) []KeyValue { return globalMapF(f, c) }
func (w *Worker) callReduceF(k string, v []string) string {
	return globalReduceF(k, v)
}

// 用户函数的进程内注册表（对应原版 "函数随任务经 RPC 传递/注册" 的简化）。
var (
	globalMapF    MapF
	globalReduceF ReduceF
)

// SetMapF/SetReduceF 在启动 worker 前注册用户函数。
func SetMapF(f MapF) { globalMapF = f }
func SetReduceF(f ReduceF) {
	globalReduceF = f
}

// BackupWatch 后台驱动 straggler 检测（main 启动一次即可）。
func BackupWatch(m *Master, stop <-chan struct{}) {
	for {
		select {
		case <-stop:
			return
		case <-time.After(50 * time.Millisecond):
			m.maybeBackupStragglers()
		}
	}
}
