// 01-buffer-pool : Buffer Pool Manager with Clock (Second-Chance) replacement + pin counts.
// CMU 15-445/645 Fall 2023 — companion to Lecture 06 (Memory Management).
// BusTub-inspired but independent; standard library only, C++17.
//
// Concepts exercised:
//   * fixed frame array + page table (pid -> frame)
//   * pin_count (a pinned frame is never evicted) and dirty flag
//   * Clock / second-chance replacement via reference bits + hand
//   * FetchPage / NewPage / WritePage / UnpinPage / FlushPage lifecycle
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <cassert>
#include <vector>
#include <unordered_map>
#include <optional>
#include <functional>

static constexpr int PAGE_SIZE = 16;   // bytes per page (small for testing)
static constexpr int NUM_FRAMES = 3;   // pool size in frames

// ---- A page is just a small POD we can inspect in tests -------------------
struct Page {
  uint8_t data[PAGE_SIZE]{};
  int Get() const { int v; memcpy(&v, data, sizeof(v)); return v; }
  void Set(int v) { memcpy(data, &v, sizeof(v)); }
};

// ---- Mock disk: pid -> page, with a read/write counter for observability ---
class DiskManager {
 public:
  std::optional<Page> Read(int pid) const {
    auto it = pages_.find(pid);
    if (it == pages_) return std::nullopt;
    return it->second;
  }
  void Write(int pid, const Page& p) { pages_[pid] = p; writes_++; }
  bool Exists(int pid) const { return pages_.count(pid) > 0; }
  int PageCount() const { return (int)pages_.size(); }
  int Writes() const { return writes_; }
  void SeedEmpty(int pid) { pages_[pid] = Page{}; }
 private:
  std::unordered_map<int, Page> pages_;
  int writes_ = 0;
};

// ---- One frame in the pool -------------------------------------------------
struct Frame {
  Page page;
  int page_id = -1;        // -1 == empty
  int pin_count = 0;
  bool is_dirty = false;
  bool ref = false;        // clock reference bit
};

// ---- Buffer pool manager ---------------------------------------------------
class BufferPoolManager {
 public:
  BufferPoolManager(DiskManager* disk) : disk_(disk), frames_(NUM_FRAMES) {
    for (int i = 0; i < NUM_FRAMES; i++) free_stack_.push_back(i);
  }

  // Returns pointer to page for pid, loading from disk if needed. nullptr if pool full.
  Page* FetchPage(int pid) {
    auto it = page_table_.find(pid);
    if (it != page_table_.end()) {
      Frame& f = frames_[it->second];
      f.pin_count++;
      f.ref = true;
      hits_++;
      return &f.page;
    }
    std::optional<int> victim = AllocateFrame();
    if (!victim) return nullptr;
    Frame& f = frames_[*victim];
    auto loaded = disk_->Read(pid);
    if (loaded) { f.page = *loaded; } else { f.page = Page{}; }  // read miss => zeroed (shouldn't happen for Fetch)
    f.page_id = pid;
    f.pin_count = 1;
    f.is_dirty = false;
    f.ref = true;
    page_table_[pid] = *victim;
    misses_++;
    return &f.page;
  }

  // Allocate a brand-new page (not read from disk) bound to pid.
  Page* NewPage(int pid) {
    std::optional<int> victim = AllocateFrame();
    if (!victim) return nullptr;
    Frame& f = frames_[*victim];
    f.page = Page{};
    f.page_id = pid;
    f.pin_count = 1;
    f.is_dirty = true;
    f.ref = true;
    page_table_[pid] = *victim;
    return &f.page;
  }

  bool UnpinPage(int pid, bool dirty) {
    auto it = page_table_.find(pid);
    if (it == page_table_.end()) return false;
    Frame& f = frames_[it->second];
    if (f.pin_count == 0) return false;   // over-unpin guard
    f.pin_count--;
    if (dirty) f.is_dirty = true;
    return true;
  }

  bool FlushPage(int pid) {
    auto it = page_table_.find(pid);
    if (it == page_table_.end()) return false;
    Frame& f = frames_[it->second];
    disk_->Write(pid, f.page);
    f.is_dirty = false;
    return true;
  }

  void FlushAll() {
    for (auto& [pid, idx] : page_table_) {
      if (frames_[idx].is_dirty) { disk_->Write(pid, frames_[idx].page); frames_[idx].is_dirty = false; }
    }
  }

  int Hits() const { return hits_; }
  int Misses() const { return misses_; }
  int Evictions() const { return evictions_; }

 private:
  // Find a frame we can reuse, evicting via clock if none is free.
  std::optional<int> AllocateFrame() {
    if (!free_stack_.empty()) { int i = free_stack_.back(); free_stack_.pop_back(); return i; }
    // clock sweep
    for (int tries = 0; tries < (int)frames_.size() * 2; tries++) {
      Frame& f = frames_[hand_ % frames_.size()];
      int idx = hand_ % frames_.size();
      hand_ = (hand_ + 1) % (int)frames_.size();
      if (f.pin_count == 0) {
        if (f.ref) { f.ref = false; continue; }  // second chance
        // evict idx
        if (f.is_dirty) { disk_->Write(f.page_id, f.page); }
        page_table_.erase(f.page_id);
        evictions_++;
        return idx;
      }
    }
    return std::nullopt;  // all pinned
  }

  DiskManager* disk_;
  std::vector<Frame> frames_;
  std::unordered_map<int, int> page_table_;   // pid -> frame idx
  std::vector<int> free_stack_;               // unused frame indices
  int hand_ = 0;                              // clock hand
  int hits_ = 0, misses_ = 0, evictions_ = 0;
};

// ---- Tests (a tiny assert-based harness) ----------------------------------
static int g_fail = 0;
static void CHECK(bool cond, const char* msg) {
  if (!cond) { printf("  [FAIL] %s\n", msg); g_fail++; }
  else       { printf("  [ ok ] %s\n", msg); }
}

static void test_basic_fetch_and_pin() {
  printf("test_basic_fetch_and_pin\n");
  DiskManager disk;
  disk.SeedEmpty(0); disk.SeedEmpty(1);
  BufferPoolManager bpm(&disk);
  Page* p0 = bpm.FetchPage(0);
  CHECK(p0 != nullptr, "fetch page 0");
  p0->Set(42);
  CHECK(bpm.UnpinPage(0, true), "unpin dirty page 0");
  Page* p0b = bpm.FetchPage(0);
  CHECK(p0b->Get() == 42, "re-fetch sees in-memory value");
  bpm.UnpinPage(0, false);
}

static void test_eviction_and_flush() {
  printf("test_eviction_and_flush\n");
  DiskManager disk;
  for (int i = 0; i < 10; i++) disk.SeedEmpty(i);
  BufferPoolManager bpm(&disk);
  // Touch more distinct pages than frames to force eviction + dirty flushes.
  for (int round = 0; round < 2; round++) {
    for (int pid = 0; pid < 6; pid++) {
      Page* p = bpm.FetchPage(pid);
      if (p) { p->Set(pid * 100 + round); bpm.UnpinPage(pid, true); }
    }
  }
  CHECK(bpm.Evictions() > 0, "at least one eviction happened");
  CHECK(disk.Writes() > 0, "dirty pages were written back to disk");
  // After flushing everything, disk page 5 should hold the last round's value.
  bpm.FlushAll();
  auto pg = disk.Read(5);
  CHECK(pg && pg->Get() == 500 + 1, "disk page 5 reflects most recent set");
}

static void test_all_pinned_blocks_eviction() {
  printf("test_all_pinned_blocks_eviction\n");
  DiskManager disk;
  for (int i = 0; i < 10; i++) disk.SeedEmpty(i);
  BufferPoolManager bpm(&disk);
  // Pin every frame; the next fetch of a new page must fail (pool exhausted).
  for (int pid = 0; pid < NUM_FRAMES; pid++) {
    Page* p = bpm.FetchPage(pid);
    CHECK(p != nullptr, "fetch fills a frame");
    // leave pinned on purpose
  }
  Page* over = bpm.FetchPage(99);
  CHECK(over == nullptr, "cannot evict fully-pinned pool");
}

int main() {
  printf("=== 01 buffer pool (clock replacement) ===\n");
  test_basic_fetch_and_pin();
  test_eviction_and_flush();
  test_all_pinned_blocks_eviction();
  printf("=== %s ===\n", g_fail == 0 ? "ALL TESTS PASSED" : "SOME TESTS FAILED");
  return g_fail == 0 ? 0 : 1;
}
