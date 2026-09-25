// 05-agg-sort : Blocking operators — external-style sort + hash aggregation.
// CMU 15-445/645 Fall 2023 — companion to Lecture 10 (Sorting and Aggregations).
// Standard library only, C++17. Self-contained mini volcano model.
//
//   Sort      : consumes all input, emits in key order (a pipeline breaker).
//   HashAgg   : builds an in-memory hash map group-key -> accumulator (SUM/COUNT/AVG/MIN/MAX).
// Both demonstrate the "blocking operator" concept from Lecture 12/13.
#include <algorithm>
#include <climits>
#include <cstdio>
#include <functional>
#include <map>
#include <memory>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

struct Tuple {
  std::unordered_map<std::string, long long> cols;
  Tuple() = default;
  // Enables `Tuple{{"dept",10},{"amount",100}}` without brace-elision ambiguity.
  Tuple(std::initializer_list<std::pair<const std::string, long long>> il) : cols(il) {}
};
using Table = std::vector<Tuple>;

class Executor {
 public:
  virtual ~Executor() = default;
  virtual void Init() = 0;
  virtual std::optional<Tuple> Next() = 0;
};

class MemoryScan : public Executor {
 public:
  explicit MemoryScan(const Table* t) : t_(t) {}
  void Init() override { i_ = 0; }
  std::optional<Tuple> Next() override { return i_ < (int)t_->size() ? std::optional<Tuple>((*t_)[i_++]) : std::nullopt; }
 private:
  const Table* t_; int i_ = 0;
};

// sort by one column (then a tie-breaker col for stability), asc/desc
class Sort : public Executor {
 public:
  Sort(std::unique_ptr<Executor> child, std::string key, std::string tie, bool asc)
      : child_(std::move(child)), key_(std::move(key)), tie_(std::move(tie)), asc_(asc) {}
  void Init() override {
    child_->Init(); buffer_.clear();
    while (auto t = child_->Next()) buffer_.push_back(*t);   // BLOCKING: materialize all
    std::stable_sort(buffer_.begin(), buffer_.end(), [&](const Tuple& a, const Tuple& b) {
      long long ka = a.cols.at(key_), kb = b.cols.at(key_);
      if (ka != kb) return asc_ ? ka < kb : ka > kb;
      return a.cols.at(tie_) < b.cols.at(tie_);
    });
    pos_ = 0;
  }
  std::optional<Tuple> Next() override {
    if (pos_ >= (int)buffer_.size()) return std::nullopt;
    return buffer_[pos_++];
  }
 private:
  std::unique_ptr<Executor> child_;
  std::string key_, tie_; bool asc_;
  std::vector<Tuple> buffer_; size_t pos_ = 0;
};

enum class AggFunc { Sum, Count, Avg, Min, Max };
struct AggSpec { std::string out_name; AggFunc fn; std::string on_col; };
struct Accum { long long sum = 0, count = 0, min = LLONG_MAX, max = LLONG_MIN; };

// GROUP BY group_col, apply aggregates. Emits one row per group (first-seen order).
class HashAgg : public Executor {
 public:
  HashAgg(std::unique_ptr<Executor> child, std::string group_col, std::vector<AggSpec> aggs)
      : child_(std::move(child)), group_col_(std::move(group_col)), aggs_(std::move(aggs)) {}
  void Init() override {
    child_->Init(); acc_.clear(); order_.clear();
    while (auto t = child_->Next()) {                 // BLOCKING build phase
      long long key = t->cols.at(group_col_);
      auto it = acc_.find(key);
      if (it == acc_.end()) { it = acc_.emplace(key, std::vector<Accum>(aggs_.size())).first; order_.push_back(key); }
      for (size_t i = 0; i < aggs_.size(); i++) {
        long long v = t->cols.count(aggs_[i].on_col) ? t->cols.at(aggs_[i].on_col) : 0;
        Accum& a = it->second[i];
        a.sum += v; a.count += 1; a.min = std::min(a.min, v); a.max = std::max(a.max, v);
      }
    }
    pos_ = 0;
  }
  std::optional<Tuple> Next() override {
    if (pos_ >= order_.size()) return std::nullopt;
    long long key = order_[pos_++];
    Tuple out; out.cols[group_col_] = key;
    for (size_t i = 0; i < aggs_.size(); i++) {
      Accum& a = acc_[key][i];
      long long val = 0;
      switch (aggs_[i].fn) {
        case AggFunc::Sum:   val = a.sum; break;
        case AggFunc::Count: val = a.count; break;
        case AggFunc::Avg:   val = a.count ? a.sum / a.count : 0; break;   // integer avg
        case AggFunc::Min:   val = a.count ? a.min : 0; break;
        case AggFunc::Max:   val = a.count ? a.max : 0; break;
      }
      out.cols[aggs_[i].out_name] = val;
    }
    return out;
  }
 private:
  std::unique_ptr<Executor> child_;
  std::string group_col_;
  std::vector<AggSpec> aggs_;
  std::unordered_map<long long, std::vector<Accum>> acc_;
  std::vector<long long> order_;
  size_t pos_ = 0;
};

static std::vector<Tuple> Run(Executor* r) { r->Init(); std::vector<Tuple> o; while (auto t = r->Next()) o.push_back(*t); return o; }

static int g_fail = 0;
static void CHECK(bool c, const char* m) {
  if (!c) { printf("  [FAIL] %s\n", m); g_fail++; } else { printf("  [ ok ] %s\n", m); }
}

int main() {
  printf("=== 05 aggregation + sort operators ===\n");
  // sales(dept, amount)
  Table sales = {
    {{ "dept", 10 }, { "amount", 100 } },
    {{ "dept", 20 }, { "amount", 200 } },
    {{ "dept", 10 }, { "amount", 50  } },
    {{ "dept", 20 }, { "amount", 300 } },
    {{ "dept", 30 }, { "amount", 70  } },
    {{ "dept", 10 }, { "amount", 25  } },
  };

  // Sort by dept asc, tie by amount desc
  {
    auto s = std::make_unique<Sort>(std::make_unique<MemoryScan>(&sales), "dept", "amount", true);
    auto out = Run(s.get());
    CHECK(out.size() == 6, "sort emits all rows");
    CHECK(out[0].cols.at("dept") == 10, "smallest dept first");
    bool nondec = true; for (size_t i = 1; i < out.size(); i++) if (out[i].cols.at("dept") < out[i-1].cols.at("dept")) nondec = false;
    CHECK(nondec, "dept keys non-decreasing");
  }

  // SELECT dept, SUM(amount), COUNT(*), AVG(amount), MIN, MAX GROUP BY dept
  {
    auto agg = std::make_unique<HashAgg>(std::make_unique<MemoryScan>(&sales), "dept",
        std::vector<AggSpec>{ {"sum", AggFunc::Sum, "amount"}, {"cnt", AggFunc::Count, "amount"},
                              {"avg", AggFunc::Avg, "amount"}, {"mn", AggFunc::Min, "amount"},
                              {"mx", AggFunc::Max, "amount"} });
    auto out = Run(agg.get());
    std::map<long long, Tuple> by;
    for (auto& r : out) by[r.cols.at("dept")] = r;
    CHECK(out.size() == 3, "three groups (10,20,30)");
    CHECK(by[10].cols.at("sum") == 175, "dept 10 sum = 100+50+25");
    CHECK(by[10].cols.at("cnt") == 3, "dept 10 count = 3");
    CHECK(by[10].cols.at("avg") == 58, "dept 10 int avg = 175/3");
    CHECK(by[20].cols.at("max") == 300 && by[20].cols.at("min") == 200, "dept 20 min/max");
    CHECK(by[30].cols.at("sum") == 70, "dept 30 sum");
  }

  // GROUP BY dept then ORDER BY dept desc (composition of two operators)
  {
    auto agg = std::make_unique<HashAgg>(std::make_unique<MemoryScan>(&sales), "dept",
        std::vector<AggSpec>{ {"sum", AggFunc::Sum, "amount"} });
    auto sor = std::make_unique<Sort>(std::move(agg), "sum", "dept", false);  // order by sum desc
    auto out = Run(sor.get());
    CHECK(out.size() == 3 && out[0].cols.at("sum") == 500, "sorted desc: dept20 sum 500 first");
    CHECK(out[2].cols.at("sum") == 70, "smallest sum last");
  }

  printf("=== %s ===\n", g_fail == 0 ? "ALL TESTS PASSED" : "SOME TESTS FAILED");
  return g_fail == 0 ? 0 : 1;
}
