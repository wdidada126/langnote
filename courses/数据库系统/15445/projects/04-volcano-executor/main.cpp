// 04-volcano-executor : Tuple-at-a-time (Volcano / iterator) execution engine.
// CMU 15-445/645 Fall 2023 — companion to Lecture 12 (Query Execution I).
// Standard library only, C++17.
//
// Operators implement Init()/Next() pull model:
//   SeqScan  -> reads a materialized in-memory table
//   Filter   -> predicate (pass-through pipeline operator)
//   Project  -> column subset (pipeline operator)
//   Values   -> constant rows (leaf)
//   Limit    -> early stop (demonstrates pipeline-friendly halting)
// A driver repeatedly calls root->Next() until nullopt.
#include <cstdio>
#include <functional>
#include <memory>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

using Value = int;
struct Tuple {
  std::vector<Value> cols;                       // positional
  std::unordered_map<std::string, Value> named;  // for readability by column name
};

struct Schema { std::vector<std::string> cols; };

// ---- abstract iterator ----------------------------------------------------
class Executor {
 public:
  virtual ~Executor() = default;
  virtual void Init() = 0;
  virtual std::optional<Tuple> Next() = 0;
  virtual std::string name() const = 0;
  int tuples_out = 0, tuples_in = 0;   // simple stats
};

using Table = std::vector<Tuple>;

class SeqScan : public Executor {
 public:
  SeqScan(const Table* tbl, Schema schema) : tbl_(tbl), schema_(std::move(schema)) {}
  void Init() override { pos_ = 0; }
  std::optional<Tuple> Next() override {
    if (pos_ >= (int)tbl_->size()) return std::nullopt;
    tuples_out++;
    return (*tbl_)[pos_++];
  }
  std::string name() const override { return "SeqScan"; }
 private:
  const Table* tbl_;
  Schema schema_;
  int pos_ = 0;
};

class Values : public Executor {
 public:
  explicit Values(std::vector<Tuple> rows) : rows_(std::move(rows)) {}
  void Init() override { pos_ = 0; }
  std::optional<Tuple> Next() override {
    if (pos_ >= (int)rows_.size()) return std::nullopt;
    return rows_[pos_++];
  }
  std::string name() const override { return "Values"; }
 private:
  std::vector<Tuple> rows_;
  int pos_ = 0;
};

// predicate: given a tuple, true keeps it
class Filter : public Executor {
 public:
  Filter(std::unique_ptr<Executor> child, std::function<bool(const Tuple&)> pred)
      : child_(std::move(child)), pred_(std::move(pred)) {}
  void Init() override { child_->Init(); }
  std::optional<Tuple> Next() override {
    while (auto t = child_->Next()) {
      tuples_in++;
      if (pred_(*t)) { tuples_out++; return t; }
    }
    return std::nullopt;
  }
  std::string name() const override { return "Filter"; }
 private:
  std::unique_ptr<Executor> child_;
  std::function<bool(const Tuple&)> pred_;
};

class Project : public Executor {
 public:
  Project(std::unique_ptr<Executor> child, std::vector<std::string> keep)
      : child_(std::move(child)), keep_(std::move(keep)) {}
  void Init() override { child_->Init(); }
  std::optional<Tuple> Next() override {
    auto t = child_->Next();
    if (!t) return std::nullopt;
    tuples_in++;
    Tuple out;
    for (auto& c : keep_) if (t->named.count(c)) out.named[c] = t->named[c];
    tuples_out++;
    return out;
  }
  std::string name() const override { return "Project"; }
 private:
  std::unique_ptr<Executor> child_;
  std::vector<std::string> keep_;
};

class Limit : public Executor {
 public:
  Limit(std::unique_ptr<Executor> child, int n) : child_(std::move(child)), n_(n) {}
  void Init() override { child_->Init(); seen_ = 0; }
  std::optional<Tuple> Next() override {
    if (seen_ >= n_) return std::nullopt;
    auto t = child_->Next();
    if (t) seen_++;
    return t;
  }
  std::string name() const override { return "Limit"; }
 private:
  std::unique_ptr<Executor> child_;
  int n_, seen_ = 0;
};

// ---- driver ---------------------------------------------------------------
static std::vector<Tuple> Run(Executor* root) {
  root->Init();
  std::vector<Tuple> out;
  while (auto t = root->Next()) out.push_back(*t);
  return out;
}

static Tuple mk(int id, std::string name, int age, int dept) {
  Tuple t;
  t.named["id"] = id; t.named["name"] = 0;   // (name kept only as label below)
  t.named["age"] = age; t.named["dept"] = dept; t.named["id"] = id;
  (void)name;
  return t;
}

// ---- Tests ----------------------------------------------------------------
static int g_fail = 0;
static void CHECK(bool c, const char* m) {
  if (!c) { printf("  [FAIL] %s\n", m); g_fail++; } else { printf("  [ ok ] %s\n", m); }
}

int main() {
  printf("=== 04 volcano executor (scan/filter/project) ===\n");
  // employee(id, age, dept)
  Table emp = { mk(1, "a", 30, 10), mk(2, "b", 45, 20), mk(3, "c", 25, 10),
                mk(4, "d", 50, 30), mk(5, "e", 35, 20) };

  // SELECT id FROM emp WHERE dept = 10
  {
    auto scan = std::make_unique<SeqScan>(&emp, Schema{{"id","age","dept"}});
    auto filt = std::make_unique<Filter>(std::move(scan), [](const Tuple& t){ return t.named.at("dept") == 10; });
    Executor* fptr = filt.get();   // keep raw handle; unique_ptr is moved into proj next
    auto proj = std::make_unique<Project>(std::move(filt), std::vector<std::string>{"id"});
    auto res = Run(proj.get());
    CHECK(res.size() == 2, "dept=10 has 2 employees");
    bool only_id = true; for (auto& r : res) if (r.named.size() != 1 || !r.named.count("id")) only_id = false;
    CHECK(only_id, "projection keeps only id column");
    CHECK(fptr->tuples_in == 5, "filter pulled all 5 tuples");
  }

  // SELECT id,age FROM emp WHERE age > 30 LIMIT 2
  {
    auto scan = std::make_unique<SeqScan>(&emp, Schema{{"id","age","dept"}});
    auto filt = std::make_unique<Filter>(std::move(scan), [](const Tuple& t){ return t.named.at("age") > 30; });
    auto lim  = std::make_unique<Limit>(std::move(filt), 2);
    auto proj = std::make_unique<Project>(std::move(lim), std::vector<std::string>{"id","age"});
    auto res = Run(proj.get());
    CHECK(res.size() == 2, "limit yields 2 rows");
    CHECK(proj->tuples_in == 2, "pipeline halted early: projection saw only 2 tuples");
  }

  // Values leaf
  {
    std::vector<Tuple> vs = { mk(7, "x", 1, 1) };
    auto v = std::make_unique<Values>(vs);
    auto res = Run(v.get());
    CHECK(res.size() == 1, "values emits its constant row");
  }

  printf("=== %s ===\n", g_fail == 0 ? "ALL TESTS PASSED" : "SOME TESTS FAILED");
  return g_fail == 0 ? 0 : 1;
}
