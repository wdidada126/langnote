package mapreduce

import (
	"crypto/rand"
	"fmt"
	"math/big"
	"os"
	"path/filepath"
	"sync"
	"time"
)

// TaskState 是单个任务的生命周期状态（论文 §2.2 的 master 数据结构）。
type TaskState int

const (
	TaskWaiting    TaskState = iota // 未分配
	TaskInProgress                  // 已分配给某 worker
	TaskDone                        // 已完成（结果可用）
)

// task 描述一个 map 或 reduce 任务。
type task struct {
	state   TaskState
	worker  int    // 当前负责的 worker 编号（-1 表示无）
	inFile  string // map 任务：输入分片；reduce 任务为空
	outName string // 逻辑输出名（map: 中间文件前缀; reduce: 最终文件）
	// 备份执行（L02 §3：对付 straggler）：记录首次派发时间。
	started time.Time
	backup  bool // 是否已派发过备份
}

// Master 是调度器：分配任务、跟踪心跳/超时、重做失败任务、派发备份任务。
// 注意 master 自身不做故障转移——MapReduce 论文的诚实取舍：
// master 挂 = 作业重跑（对照 L05：要真容错请上共识）。
type Master struct {
	name      string
	mu        sync.Mutex
	mapTasks  []*task
	redTasks  []*task
	nReduce   int
	startTime time.Time
	// heartbeatTimeout：worker 超过该时间没有"心跳"（= 任何对 master 的调用）
	// 则判定失活，其 in-progress 任务回炉（论文 §2.4 / §2.5）。
	heartbeatTimeout time.Duration
	// stragglerAfter：任务运行超过该值仍未完成 → 派发备份任务（§3 末节）。
	stragglerAfter time.Duration

	// 统计
	redone   int // 被重做的任务数（超时/崩溃）
	backups  int // 备份派发数
	done     bool
	finished time.Time
}

// NewMaster 创建并启动一个作业的调度器。
func NewMaster(name string, files []string, nReduce int, hbTimeout, straggler time.Duration) *Master {
	m := &Master{
		name:             name,
		nReduce:          nReduce,
		heartbeatTimeout: hbTimeout,
		stragglerAfter:   straggler,
		startTime:        time.Now(),
	}
	for _, f := range files {
		m.mapTasks = append(m.mapTasks, &task{state: TaskWaiting, worker: -1, inFile: f})
	}
	for i := 0; i < nReduce; i++ {
		m.redTasks = append(m.redTasks, &task{
			state: TaskWaiting, worker: -1,
			outName: fmt.Sprintf("%s-%05d", name, i),
		})
	}
	return m
}

// checkTimeouts 回收"心跳超时"的 worker 的任务并回炉重做。
// 在每次可能改变状态的操作前惰性执行（也靠后台协程驱动，双保险）。
// m.mu 必须已持有。
func (m *Master) checkTimeouts() {
	now := time.Now()
	revive := func(tasks []*task) {
		for _, t := range tasks {
			if t.state == TaskInProgress && now.Sub(t.started) > m.heartbeatTimeout {
				// worker 疑似已死：任务作废重排（结果不可信，因输出未完成）。
				t.state = TaskWaiting
				t.worker = -1
				t.backup = false
				m.redone++
			}
		}
	}
	revive(m.mapTasks)
	revive(m.redTasks)
}

// acquireMapTask 返回 (mapID, 输入文件名, ok)。
func (m *Master) acquireMapTask(worker int) (int, string, bool) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.checkTimeouts()
	for i, t := range m.mapTasks {
		if t.state == TaskWaiting {
			t.state = TaskInProgress
			t.worker = worker
			t.started = time.Now()
			return i, t.inFile, true
		}
	}
	return -1, "", false
}

// acquireReduceTask 返回 (reduceID, 输出名, ok)。
// 论文纪律：所有 map 任务完成之前不派发 reduce（否则中间文件不全）。
func (m *Master) acquireReduceTask(worker int) (int, string, bool) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.checkTimeouts()
	for _, t := range m.mapTasks {
		if t.state != TaskDone {
			return -1, "", false
		}
	}
	for i, t := range m.redTasks {
		if t.state == TaskWaiting {
			t.state = TaskInProgress
			t.worker = worker
			t.started = time.Now()
			return i, t.outName, true
		}
	}
	return -1, "", false
}

// jobLayout 返回 (map 任务数, reduce 任务数)，reduce worker 用它拼中间文件名。
func (m *Master) jobLayout() (int, int) {
	m.mu.Lock()
	defer m.mu.Unlock()
	return len(m.mapTasks), m.nReduce
}

// checkIfDone：所有 map 与 reduce 均 TaskDone 时置标志。
func (m *Master) checkIfDone() {
	if m.done {
		return
	}
	for _, t := range m.mapTasks {
		if t.state != TaskDone {
			return
		}
	}
	for _, t := range m.redTasks {
		if t.state != TaskDone {
			return
		}
	}
	m.done = true
	m.finished = time.Now()
}

// releaseTask：worker 完成任务（幂等！重复完成返回 ok=false 也无害——
// 这正是论文"两个实例同时跑同一任务结果不变"的基础）。
func (m *Master) releaseTask(kind string, id int, worker int) bool {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.checkTimeouts()
	tasks := m.mapTasks
	if kind == "reduce" {
		tasks = m.redTasks
	}
	if id < 0 || id >= len(tasks) {
		return false
	}
	t := tasks[id]
	if t.state == TaskDone {
		return false // 备份任务先到者赢；迟到者无害（幂等）
	}
	if t.worker != worker && t.backup {
		// 备份实例完成：正常（另一个实例可能仍在跑，结果等价）。
	}
	t.state = TaskDone
	m.checkIfDone()
	return true
}

// maybeBackupStragglers：慢任务（超过 stragglerAfter 未完成）再放一份回队列，
// 谁先算完谁发布（releaseTask 先到者赢 + 输出 rename 原子 → 幂等）。
// 对应论文 §3 "对最慢的少数任务启动备份实例"。
func (m *Master) maybeBackupStragglers() []int {
	m.mu.Lock()
	defer m.mu.Unlock()
	now := time.Now()
	var dispatched []int
	for i, t := range m.mapTasks {
		if t.state == TaskInProgress && !t.backup && now.Sub(t.started) > m.stragglerAfter {
			t.backup = true
			t.state = TaskWaiting // 允许他人再领一次；先到者 complete
			t.worker = -1
			// 保留原 worker 仍在计算的输出文件（rename 先到者赢）
			m.backups++
			dispatched = append(dispatched, i)
		}
	}
	return dispatched
}

// Done 报告作业是否结束，并返回统计。
func (m *Master) Done() (bool, int, int, time.Duration) {
	m.mu.Lock()
	defer m.mu.Unlock()
	d := m.done
	var el time.Duration
	if d {
		el = m.finished.Sub(m.startTime)
	}
	return d, m.redone, m.backups, el
}

// WaitForCompletion 阻塞直到作业完成（main 用）。
func (m *Master) WaitForCompletion() {
	for {
		if d, _, _, _ := m.Done(); d {
			return
		}
		time.Sleep(20 * time.Millisecond)
	}
}

// ---------------------------------------------------------------------------
// 中间文件与输出文件（论文：map 输出按 reduce 分区写本地临时文件；
// reduce 输出先写临时文件再 rename 原子发布，保证幂等）。
// ---------------------------------------------------------------------------

var tmpSeq uint64
var tmpMu sync.Mutex

func nextSeq() uint64 {
	tmpMu.Lock()
	defer tmpMu.Unlock()
	tmpSeq++
	return tmpSeq
}

func randSuffix() string {
	n, _ := rand.Int(rand.Reader, big.NewInt(1<<40))
	return fmt.Sprintf("%010x", n)
}

// writeKVFile 把 []KeyValue 写入 path（每行 key\tvalue，kv 内已含换行的除外）。
func writeKVFile(path string, kvs []KeyValue) error {
	tmp := filepath.Join(filepath.Dir(path), fmt.Sprintf(".tmp.%s.%d", randSuffix(), nextSeq()))
	f, err := os.Create(tmp)
	if err != nil {
		return err
	}
	for _, kv := range kvs {
		if _, err := fmt.Fprintf(f, "%s\t%s\n", kv.Key, kv.Value); err != nil {
			f.Close()
			return err
		}
	}
	if err := f.Sync(); err != nil {
		f.Close()
		return err
	}
	f.Close()
	return os.Rename(tmp, path) // 原子发布
}

func readKVFile(path string) ([]KeyValue, error) {
	var out []KeyValue
	// 逐行读 key\tvalue
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	for _, line := range splitLines(string(data)) {
		k, v, ok := cutKV(line)
		if !ok {
			continue
		}
		out = append(out, KeyValue{Key: k, Value: v})
	}
	return out, nil
}
