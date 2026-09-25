// 07-wal-recovery : Write-Ahead Log with redo/undo crash recovery (mini-ARIES).
// CMU 15-445/645 Fall 2023 — companion to Lectures 19/20 (Logging & Recovery).
// Standard library only, C++17.
//
// Model:
//   * `log` is durable and appended in LSN order (WAL: a write is logged before applied).
//   * `mem`  is the in-memory page state; writes apply immediately (STEAL).
//   * `disk` is only advanced by flush()/checkpoint (NO-FORCE on commit).
//   * a crash() wipes mem back to disk; recover() rebuilds a consistent mem from the log:
//       REDO  committed   updates (forward, idempotent)
//       UNDO  loser (non-committed) updates (backward, using before-images)
#include <cstdint>
#include <cstdio>
#include <map>
#include <set>
#include <string>
#include <vector>

enum class RecType { Begin, Update, Commit, Abort, Checkpoint };

struct LogRecord {
  int64_t lsn;
  int tid;
  RecType type;
  int key = 0;              // for Update
  std::string before, after; // values (empty for non-Update); before="~" => key did not exist
};

class LogManager {
 public:
  int64_t Append(int tid, RecType t) {
    LogRecord r{ (int64_t)recs_.size(), tid, t };
    recs_.push_back(r); return r.lsn;
  }
  int64_t AppendUpdate(int tid, int key, std::string before, std::string after) {
    LogRecord r{ (int64_t)recs_.size(), tid, RecType::Update, key, std::move(before), std::move(after) };
    recs_.push_back(r); return r.lsn;
  }
  const std::vector<LogRecord>& Records() const { return recs_; }
 private:
  std::vector<LogRecord> recs_;
};

// KV store treated as pages (key -> string value)
using Pages = std::map<int, std::string>;

class RecoveryManager {
 public:
  RecoveryManager(LogManager* log) : log_(log) {}

  // Transaction runtime API ---------------------------------------------
  void Begin(int tid) { log_->Append(tid, RecType::Begin); active_.insert(tid); }
  void Write(int tid, int key, const std::string& val) {
    std::string before = mem_.count(key) ? mem_[key] : "~";
    log_->AppendUpdate(tid, key, before, val);     // WAL first
    mem_[key] = val;                                // then apply in memory (STEAL)
  }
  void Commit(int tid) { log_->Append(tid, RecType::Commit); active_.erase(tid); committed_.insert(tid); }
  void Abort(int tid) {
    // undo loser in memory immediately, using its own update records (reverse)
    for (auto it = log_->Records().rbegin(); it != log_->Records().rend(); ++it) {
      if (it->type == RecType::Update && it->tid == tid) {
        if (it->before == "~") mem_.erase(it->key); else mem_[it->key] = it->before;
      }
    }
    log_->Append(tid, RecType::Abort); active_.erase(tid);
  }

  void Checkpoint() {
    // no-fuzzy for simplicity: flush all dirty mem to disk, then record active txns
    disk_ = mem_;
    log_->Append(0, RecType::Checkpoint);
    ckpt_lsn_ = log_->Records().size() ? (int64_t)log_->Records().size() - 1 : 0;
  }

  void FlushToDisk() { disk_ = mem_; }

  // Simulate power loss: memory reverts to the last durable disk state.
  void Crash() { mem_ = disk_; crashed_ = true; }

  // Rebuild mem from disk + log. Returns nothing; inspect Mem().
  void Recover() {
    Pages state = disk_;
    const auto& recs = log_->Records();
    // REDO pass (forward): re-apply every committed transaction's updates.
    for (const auto& r : recs) {
      if (r.type == RecType::Update && committed_.count(r.tid)) {
        if (r.after.size()) state[r.key] = r.after;
      }
    }
    // identify losers: began but never committed/aborted by end of log
    std::set<int> maybe_loser, resolved;
    for (const auto& r : recs) {
      if (r.type == RecType::Begin) maybe_loser.insert(r.tid);
      if (r.type == RecType::Commit || r.type == RecType::Abort) resolved.insert(r.tid);
    }
    std::set<int> losers;
    for (int t : maybe_loser) if (!resolved.count(t)) losers.insert(t);

    // UNDO pass (backward): roll back loser writes.
    for (auto it = recs.rbegin(); it != recs.rend(); ++it) {
      if (it->type == RecType::Update && losers.count(it->tid)) {
        if (it->before == "~") state.erase(it->key); else state[it->key] = it->before;
      }
    }
    mem_ = state;
    disk_ = state;
    crashed_ = false;
  }

  const Pages& Mem() const { return mem_; }
  const Pages& Disk() const { return disk_; }

 private:
  LogManager* log_;
  Pages mem_, disk_;
  std::set<int> active_, committed_;
  bool crashed_ = false;
  int64_t ckpt_lsn_ = -1;
};

// ---- Tests ----------------------------------------------------------------
static int g_fail = 0;
static void CHECK(bool c, const char* m) {
  if (!c) { printf("  [FAIL] %s\n", m); g_fail++; } else { printf("  [ ok ] %s\n", m); }
}

static std::string get(const Pages& p, int k) { auto it = p.find(k); return it == p.end() ? "<absent>" : it->second; }

int main() {
  printf("=== 07 WAL redo/undo recovery ===\n");

  // Scenario A: committed txn flushed (no redo needed), loser present (undo needed).
  {
    LogManager log; RecoveryManager rm(&log);
    rm.Begin(1); rm.Write(1, 10, "v1"); rm.Commit(1);   // committed
    rm.FlushToDisk();                                     // durable to disk
    rm.Begin(2); rm.Write(2, 20, "bad");                 // stole to disk? No: only mem. Not committed.
    rm.Crash();
    rm.Recover();
    CHECK(get(rm.Mem(), 10) == "v1", "committed+flushed value survives");
    CHECK(get(rm.Mem(), 20) == "<absent>", "uncommitted steal write undone after crash");
  }

  // Scenario B: committed txn NOT flushed (NO-FORCE) -> redo must restore it.
  {
    LogManager log; RecoveryManager rm(&log);
    rm.Begin(1); rm.Write(1, 1, "a"); rm.Commit(1);      // committed but not flushed
    rm.Begin(2); rm.Write(2, 2, "b"); rm.Commit(2);
    rm.Crash();                                            // disk still empty
    CHECK(get(rm.Mem(), 1) == "<absent>", "crash wiped unflushed mem");
    rm.Recover();
    CHECK(get(rm.Mem(), 1) == "a" && get(rm.Mem(), 2) == "b", "redo restored committed writes from log");
  }

  // Scenario C: mixed committed + loser + overwrite of same key.
  {
    LogManager log; RecoveryManager rm(&log);
    rm.Begin(1); rm.Write(1, 5, "one"); rm.Commit(1);
    rm.Begin(2); rm.Write(2, 5, "two");                   // overwrite key 5 (loser)
    rm.Begin(3); rm.Write(3, 7, "three"); rm.Commit(3);
    rm.Crash();
    rm.Recover();
    CHECK(get(rm.Mem(), 5) == "one", "loser overwrite of key5 rolled back to committed value");
    CHECK(get(rm.Mem(), 7) == "three", "other committed txn present");
  }

  // Scenario D: explicit abort in memory (no crash).
  {
    LogManager log; RecoveryManager rm(&log);
    rm.Begin(1); rm.Write(1, 9, "keep"); rm.Commit(1);
    rm.Begin(2); rm.Write(2, 8, "temp"); rm.Abort(2);
    CHECK(get(rm.Mem(), 9) == "keep", "committed kept");
    CHECK(get(rm.Mem(), 8) == "<absent>", "aborted write rolled back immediately");
  }

  printf("=== %s ===\n", g_fail == 0 ? "ALL TESTS PASSED" : "SOME TESTS FAILED");
  return g_fail == 0 ? 0 : 1;
}
