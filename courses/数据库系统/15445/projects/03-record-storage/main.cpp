// 03-record-storage : Slotted page + a single-page heap table.
// CMU 15-445/645 Fall 2023 — companion to Lecture 04/05 (Database Storage, Storage Models).
// Standard library only, C++17.
//
// Page layout (bytes, little-endian):
//   [0..1] uint16 num_slots
//   [2..3] uint16 free_end          (lowest used data byte; grows toward 0)
//   [4.. ] slot table: num_slots * { uint16 offset, uint16 size }  (size==0xFFFF == deleted)
//   ...     free space
//   records are written from the tail of the page downwards
// A (slot_offset) pair acts as the stable tuple id (TID) inside the page.
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <optional>
#include <string>
#include <vector>

static constexpr uint16_t SLOT_DELETED = 0xFFFF;

struct Slot { uint16_t offset; uint16_t size; };

class SlottedPage {
 public:
  static constexpr int HEADER = 4;         // num_slots + free_end
  static constexpr int SLOT_BYTES = 4;     // offset + size

  explicit SlottedPage(uint16_t page_size = 128)
      : page_size_(page_size), buf_(page_size, 0), free_end_(page_size) {
    std::memset(buf_.data(), 0, page_size);
    write_u16(0, 0);      // num_slots = 0
    write_u16(2, free_end_);
  }

  // Returns slot id, or nullopt if the record does not fit.
  std::optional<int> Insert(const std::vector<uint8_t>& rec) {
    int num_slots = read_u16(0);
    int slot_table_end = HEADER + (num_slots + 1) * SLOT_BYTES;
    if (free_end_ - slot_table_end < (int)rec.size()) return std::nullopt;  // full
    uint16_t rec_off = free_end_ - (uint16_t)rec.size();
    std::memcpy(&buf_[rec_off], rec.data(), rec.size());
    free_end_ = rec_off;
    // append slot
    int idx = num_slots;
    write_u16(HEADER + idx * SLOT_BYTES + 0, rec_off);
    write_u16(HEADER + idx * SLOT_BYTES + 2, (uint16_t)rec.size());
    write_u16(0, (uint16_t)(num_slots + 1));
    write_u16(2, free_end_);
    return idx;
  }

  std::optional<std::vector<uint8_t>> Get(int slot) const {
    int num_slots = read_u16(0);
    if (slot < 0 || slot >= num_slots) return std::nullopt;
    Slot s = read_slot(slot);
    if (s.size == SLOT_DELETED) return std::nullopt;
    return std::vector<uint8_t>(buf_.begin() + s.offset, buf_.begin() + s.offset + s.size);
  }

  bool Delete(int slot) {
    int num_slots = read_u16(0);
    if (slot < 0 || slot >= num_slots) return false;
    write_u16(HEADER + slot * SLOT_BYTES + 2, SLOT_DELETED);  // mark deleted; data space not reclaimed here
    return true;
  }

  int SlotCount() const { return read_u16(0); }
  int LiveCount() const {
    int n = 0; for (int i = 0; i < SlotCount(); i++) if (read_slot(i).size != SLOT_DELETED) n++;
    return n;
  }

 private:
  uint16_t read_u16(int off) const { return buf_[off] | (buf_[off + 1] << 8); }
  void write_u16(int off, uint16_t v) { buf_[off] = v & 0xFF; buf_[off + 1] = (v >> 8) & 0xFF; }
  Slot read_slot(int slot) const {
    return { read_u16(HEADER + slot * SLOT_BYTES), read_u16(HEADER + slot * SLOT_BYTES + 2) };
  }

  uint16_t page_size_;
  std::vector<uint8_t> buf_;
  uint16_t free_end_;
};

// ---- Row = (int32 id, string name) serialized to bytes --------------------
struct Row {
  int32_t id;
  std::string name;
  std::vector<uint8_t> Serialize() const {
    std::vector<uint8_t> out(4 + name.size());
    std::memcpy(out.data(), &id, 4);
    std::memcpy(out.data() + 4, name.data(), name.size());
    return out;
  }
  static Row Deserialize(const std::vector<uint8_t>& b) {
    Row r; std::memcpy(&r.id, b.data(), 4); r.name.assign(b.begin() + 4, b.end()); return r;
  }
};

// A "table" backed by one slotted page for teaching purposes.
class HeapTable {
 public:
  explicit HeapTable(uint16_t page_size = 128) : page_(page_size) {}

  std::optional<int> Insert(const Row& r) {
    auto slot = page_.Insert(r.Serialize());
    if (slot) rows_++;
    return slot;
  }
  std::optional<Row> Get(int slot) const {
    auto b = page_.Get(slot);
    if (!b) return std::nullopt;
    return Row::Deserialize(*b);
  }
  bool Remove(int slot) { bool ok = page_.Delete(slot); if (ok) rows_--; return ok; }

  std::vector<Row> ScanAll() const {
    std::vector<Row> out;
    for (int i = 0; i < page_.SlotCount(); i++) {
      auto b = page_.Get(i);
      if (b) out.push_back(Row::Deserialize(*b));
    }
    return out;
  }
  int size() const { return rows_; }
  int freeSlotsLeaked() const { return page_.SlotCount() - page_.LiveCount(); }

 private:
  SlottedPage page_;
  int rows_ = 0;
};

// ---- Tests ----------------------------------------------------------------
static int g_fail = 0;
static void CHECK(bool c, const char* m) {
  if (!c) { printf("  [FAIL] %s\n", m); g_fail++; } else { printf("  [ ok ] %s\n", m); }
}

int main() {
  printf("=== 03 record storage (slotted page + heap) ===\n");
  HeapTable t(256);
  auto s0 = t.Insert({1, "alice"});
  auto s1 = t.Insert({2, "bob"});
  auto s2 = t.Insert({3, "carol-with-a-longer-name"});
  CHECK(s0 && s1 && s2, "three inserts return slots");
  CHECK(t.Get(*s1)->id == 2 && t.Get(*s1)->name == "bob", "point read by slot");
  CHECK(t.size() == 3, "three live rows");

  // delete middle, others unaffected; TID stable
  CHECK(t.Remove(*s1), "delete slot 1");
  CHECK(!t.Get(*s1).has_value(), "deleted row gone");
  CHECK(t.Get(*s2)->name == "carol-with-a-longer-name", "surviving row still correct after delete");
  CHECK(t.size() == 2, "live count reflects delete");
  CHECK(t.freeSlotsLeaked() == 1, "one tombstone slot remains");

  // scan
  auto all = t.ScanAll();
  CHECK(all.size() == 2 && all[0].id == 1 && all[1].id == 3, "scan returns live rows in slot order");

  // page-full behavior: tiny page cannot fit everything
  HeapTable small(32);
  int ok = 0;
  for (int i = 0; i < 20; i++) { auto s = small.Insert({i, "x"}); if (s) ok++; }
  CHECK(ok > 0 && ok < 20, "page rejects records once out of free space");

  printf("=== %s ===\n", g_fail == 0 ? "ALL TESTS PASSED" : "SOME TESTS FAILED");
  return g_fail == 0 ? 0 : 1;
}
