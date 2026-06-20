# ds_CRDT

整一个用CRDT做分布式同步算法的数据库POC吧
CRDT（Conflict-Free Replicated Data Type）是分布式系统中处理数据同步的优雅方案。让我为你详细解析如何用CRDT实现分布式同步算法。

CRDT 核心概念

两种主要类型

// 1. 基于状态的CRDT (State-based)
type GCounter struct {
    counts map[string]int
}

// 2. 基于操作的CRDT (Op-based)  
type GSet struct {
    elements map[interface{}]bool
    ops []Operation
}


常见CRDT数据类型实现
1. G-Counter (Grow-only Counter)

type GCounter struct {
    id    string
    counts map[string]int
}

func (g *GCounter) Increment() {
    g.counts[g.id]++
}

func (g *GCounter) Value() int {
    sum := 0
    for _, v := range g.counts {
        sum += v
    }
    return sum
}

// 合并：取每个节点的最大值
func (g *GCounter) Merge(other *GCounter) {
    for id, count := range other.counts {
        if count > g.counts[id] {
            g.counts[id] = count
        }
    }
}


2. PN-Counter (Positive-Negative Counter)
type PNCounter struct {
    increments *GCounter
    decrements *GCounter
}

func (p *PNCounter) Increment() {
    p.increments.Increment()
}

func (p *PNCounter) Decrement() {
    p.decrements.Increment()
}

func (p *PNCounter) Value() int {
    return p.increments.Value() - p.decrements.Value()
}


3. G-Set (Grow-only Set)
type GSet struct {
    elements map[interface{}]bool
}

func (g *GSet) Add(element interface{}) {
    g.elements[element] = true
}

func (g *GSet) Merge(other *GSet) {
    for element := range other.elements {
        g.elements[element] = true
    }
}


4. 2P-Set (Two-Phase Set)
type TwoPhaseSet struct {
    added   *GSet
    removed *GSet
}

func (t *TwoPhaseSet) Add(element interface{}) {
    t.added.Add(element)
}

func (t *TwoPhaseSet) Remove(element interface{}) {
    if t.added.Contains(element) {
        t.removed.Add(element)
    }
}

func (t *TwoPhaseSet) Contains(element interface{}) bool {
    return t.added.Contains(element) && !t.removed.Contains(element)
}


分布式同步架构设计
基于状态的CRDT同步框架

type StateBasedCRDT interface {
    Value() interface{}
    Merge(other StateBasedCRDT)
    GetState() map[string]interface{}
    SetState(state map[string]interface{})
}

type SyncManager struct {
    crdt    StateBasedCRDT
    peers   []string
    version int
}

// 定期同步状态
func (s *SyncManager) StartSync() {
    ticker := time.NewTicker(5 * time.Second)
    go func() {
        for range ticker.C {
            s.broadcastState()
        }
    }()
}

func (s *SyncManager) broadcastState() {
    state := s.crdt.GetState()
    for _, peer := range s.peers {
        go s.sendState(peer, state, s.version)
    }
}


基于操作的CRDT同步框架
type Operation struct {
    Type string
    Data interface{}
    Timestamp int64
    ReplicaID string
}

type OpBasedCRDT struct {
    state     interface{}
    log       []Operation
    vectorClock map[string]int
}

func (o *OpBasedCRDT) Apply(op Operation) {
    // 应用操作到本地状态
    o.applyOperation(op)
    o.log = append(o.log, op)
    o.vectorClock[op.ReplicaID]++
}

func (o *OpBasedCRDT) SyncOperations(operations []Operation) {
    // 按时间戳和向量时钟排序
    sortedOps := o.sortOperations(operations)
    
    for _, op := range sortedOps {
        if !o.isOperationApplied(op) {
            o.Apply(op)
        }
    }
}


CRDT在数据库中的应用
分布式计数器场景

// 类似Redis INCR的分布式实现
type DistributedCounter struct {
    counters map[string]*PNCounter
    sync.RWMutex
}

func (d *DistributedCounter) Increment(key string, delta int) {
    d.Lock()
    defer d.Unlock()
    
    if _, exists := d.counters[key]; !exists {
        d.counters[key] = NewPNCounter()
    }
    
    if delta > 0 {
        for i := 0; i < delta; i++ {
            d.counters[key].Increment()
        }
    } else {
        for i := 0; i < -delta; i++ {
            d.counters[key].Decrement()
        }
    }
}

func (d *DistributedCounter) Merge(other *DistributedCounter) {
    d.Lock()
    defer d.Unlock()
    
    for key, counter := range other.counters {
        if existing, exists := d.counters[key]; exists {
            existing.Merge(counter)
        } else {
            d.counters[key] = counter
        }
    }
}


分布式集合操作

// 类似Redis Set的分布式实现
type DistributedSet struct {
    sets map[string]*TwoPhaseSet
}

func (d *DistributedSet) SAdd(key string, members ...interface{}) {
    if _, exists := d.sets[key]; !exists {
        d.sets[key] = NewTwoPhaseSet()
    }
    
    for _, member := range members {
        d.sets[key].Add(member)
    }
}

func (d *DistributedSet) SRem(key string, members ...interface{}) {
    if set, exists := d.sets[key]; exists {
        for _, member := range members {
            set.Remove(member)
        }
    }
}


性能优化策略

1. 增量同步
type DeltaCRDT struct {
    fullState StateBasedCRDT
    deltas    []Delta
}

type Delta struct {
    Operation string
    Data      interface{}
    Timestamp int64
}

func (d *DeltaCRDT) GetDeltaSince(timestamp int64) []Delta {
    var recentDeltas []Delta
    for _, delta := range d.deltas {
        if delta.Timestamp > timestamp {
            recentDeltas = append(recentDeltas, delta)
        }
    }
    return recentDeltas
}


2. 向量时钟优化
type CompactVectorClock struct {
    id    string
    clock int
    dots  map[string]int // 其他节点的最新版本
}

func (c *CompactVectorClock) Compare(other *CompactVectorClock) int {
    // 实现紧凑的版本比较逻辑
}


测试用例示例
func TestCRDTConvergence(t *testing.T) {
    // 创建三个节点的计数器
    counterA := NewGCounter("nodeA")
    counterB := NewGCounter("nodeB") 
    counterC := NewGCounter("nodeC")
    
    // 各节点独立操作
    counterA.Increment()
    counterA.Increment()
    counterB.Increment()
    counterC.Increment()
    counterC.Increment()
    counterC.Increment()
    
    // 合并状态
    counterA.Merge(counterB)
    counterA.Merge(counterC)
    
    assert.Equal(t, 6, counterA.Value()) // 1+1+1+3 = 6
}


实际应用场景
1. 实时协作编辑 (如 Google Docs)
2. 分布式计数器 (如点赞、浏览量统计)
3. 购物车合并 (电商分布式购物车)
4. 配置管理 (多数据中心配置同步)
5. IoT设备状态同步

CRDT的优势在于无需协调就能保证最终一致性，特别适合高延迟、易分区的网络环境。你想深入了解某个具体的CRDT类型或应用场景吗？