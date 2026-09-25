// 06-mini-sql : Parse a SELECT ... FROM ... [WHERE ...] [ORDER BY ...] subset and
// execute it through a volcano operator tree.
// CMU 15-445/645 Fall 2023 — companion to Lectures 02/12/14 (SQL -> plan -> execution).
// Standard library only, C++17.
//
// Supported grammar:
//   query    := SELECT sel FROM ident [WHERE conds] [ORDER BY ident [DESC]]
//   sel      := '*' | ident (',' ident)*
//   conds    := cond (AND cond)*
//   cond     := ident op number
//   op       := '=' | '!=' | '<' | '<=' | '>' | '>='
#include <algorithm>
#include <cctype>
#include <cstdio>
#include <functional>
#include <map>
#include <memory>
#include <optional>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

// ---- Data model -----------------------------------------------------------
struct Row {
  std::unordered_map<std::string, long long> cols;
  Row() = default;
  // Enables `Row{{"id",1},{"dept",10}}` without brace-elision ambiguity.
  Row(std::initializer_list<std::pair<const std::string, long long>> il) : cols(il) {}
};
struct Table {
  std::string name;
  std::vector<std::string> cols;   // schema order
  std::vector<Row> rows;
};

// ---- Lexer ----------------------------------------------------------------
enum class TK { Ident, Number, Comma, Star, Eq, Ne, Lt, Le, Gt, Ge, End };
struct Token { TK kind; std::string text; };
static const std::map<std::string, TK> KEYWORDS = {
  {"SELECT", TK::Ident}, {"FROM", TK::Ident}, {"WHERE", TK::Ident},
  {"AND", TK::Ident}, {"ORDER", TK::Ident}, {"BY", TK::Ident}, {"DESC", TK::Ident},
};

class Lexer {
 public:
  explicit Lexer(std::string s) : s_(std::move(s)) {}
  std::vector<Token> All() {
    std::vector<Token> out;
    while (pos_ < s_.size()) {
      char c = s_[pos_];
      if (std::isspace((unsigned char)c)) { pos_++; continue; }
      if (std::isalpha((unsigned char)c) || c == '_') { out.push_back(ReadWord()); continue; }
      if (std::isdigit((unsigned char)c)) { out.push_back(ReadNum()); continue; }
      pos_++;
      switch (c) {
        case ',': out.push_back({TK::Comma, ","}); break;
        case '*': out.push_back({TK::Star, "*"}); break;
        case '=': out.push_back({TK::Eq, "="}); break;
        case '!': out.push_back({TK::Ne, "!="}); if (pos_ < s_.size() && s_[pos_] == '=') pos_++; break;
        case '<': if (peek('=')) { pos_++; out.push_back({TK::Le, "<="}); } else out.push_back({TK::Lt, "<"}); break;
        case '>': if (peek('=')) { pos_++; out.push_back({TK::Ge, ">="}); } else out.push_back({TK::Gt, ">"}); break;
        default: throw std::runtime_error(std::string("bad char ") + c);
      }
    }
    out.push_back({TK::End, ""});
    return out;
  }
 private:
  bool peek(char c) const { return pos_ < s_.size() && s_[pos_] == c; }
  Token ReadWord() {
    size_t st = pos_; while (pos_ < s_.size() && (std::isalnum((unsigned char)s_[pos_]) || s_[pos_] == '_')) pos_++;
    std::string w = s_.substr(st, pos_ - st);
    std::string up = w; for (auto& ch : up) ch = std::toupper((unsigned char)ch);
    if (KEYWORDS.count(up)) return {TK::Ident, up};
    return {TK::Ident, w};
  }
  Token ReadNum() {
    size_t st = pos_; while (pos_ < s_.size() && std::isdigit((unsigned char)s_[pos_])) pos_++;
    return {TK::Number, s_.substr(st, pos_ - st)};
  }
  std::string s_; size_t pos_ = 0;
};

// ---- AST ------------------------------------------------------------------
enum class Cmp { Eq, Ne, Lt, Le, Gt, Ge };
struct Predicate { std::string col; Cmp op; long long value; };
struct Query {
  bool star = false;
  std::vector<std::string> select_cols;
  std::string table;
  std::vector<Predicate> where;                 // AND-ed
  std::optional<std::string> order_col;
  bool order_desc = false;
};

class Parser {
 public:
  explicit Parser(std::vector<Token> t) : t_(std::move(t)) {}
  Query Parse() {
    Query q;
    ExpectKw("SELECT");
    if (at(TK::Star)) { q.star = true; next(); }
    else {
      do { q.select_cols.push_back(ExpectIdent()); } while (eat(TK::Comma));
    }
    ExpectKw("FROM");
    q.table = ExpectIdent();
    if (atIdent("WHERE")) {
      next();
      do { q.where.push_back(ParseCond()); } while (atIdent("AND") && (next(), true));
    }
    if (atIdent("ORDER")) {
      next(); ExpectKw("BY");
      q.order_col = ExpectIdent();
      if (atIdent("DESC")) { q.order_desc = true; next(); }
    }
    return q;
  }
 private:
  size_t i_ = 0;
  const Token& cur() { return t_[i_]; }
  void next() { if (cur().kind != TK::End) i_++; }
  bool at(TK k) { return cur().kind == k; }
  bool atIdent(const std::string& s) { return cur().kind == TK::Ident && cur().text == s; }
  bool eat(TK k) { if (at(k)) { next(); return true; } return false; }
  void ExpectKw(const std::string& s) { if (!atIdent(s)) throw std::runtime_error("expected " + s); next(); }
  std::string ExpectIdent() {
    if (cur().kind != TK::Ident) throw std::runtime_error("expected identifier");
    std::string t = cur().text; next(); return t;
  }
  Predicate ParseCond() {
    Predicate p; p.col = ExpectIdent();
    TK k = cur().kind; next();
    switch (k) {
      case TK::Eq: p.op = Cmp::Eq; break; case TK::Ne: p.op = Cmp::Ne; break;
      case TK::Lt: p.op = Cmp::Lt; break; case TK::Le: p.op = Cmp::Le; break;
      case TK::Gt: p.op = Cmp::Gt; break; case TK::Ge: p.op = Cmp::Ge; break;
      default: throw std::runtime_error("expected comparison operator");
    }
    if (!at(TK::Number)) throw std::runtime_error("expected number literal");
    p.value = std::stoll(cur().text); next();
    return p;
  }
  std::vector<Token> t_;
};

// ---- Executor (volcano) ---------------------------------------------------
struct Tuple { std::unordered_map<std::string, long long> cols; };

class Executor {
 public:
  virtual ~Executor() = default;
  virtual void Init() = 0;
  virtual std::optional<Tuple> Next() = 0;
};

class SeqScan : public Executor {
 public:
  explicit SeqScan(const Table* t) : t_(t) {}
  void Init() override { i_ = 0; }
  std::optional<Tuple> Next() override {
    if (i_ >= (int)t_->rows.size()) return std::nullopt;
    return Tuple{ t_->rows[i_++].cols };
  }
 private:
  const Table* t_; int i_ = 0;
};

class Filter : public Executor {
 public:
  Filter(std::unique_ptr<Executor> c, std::function<bool(const Tuple&)> p) : c_(std::move(c)), p_(std::move(p)) {}
  void Init() override { c_->Init(); }
  std::optional<Tuple> Next() override { while (auto t = c_->Next()) if (p_(*t)) return t; return std::nullopt; }
 private:
  std::unique_ptr<Executor> c_; std::function<bool(const Tuple&)> p_;
};

class Project : public Executor {
 public:
  Project(std::unique_ptr<Executor> c, std::vector<std::string> cols) : c_(std::move(c)), cols_(std::move(cols)) {}
  void Init() override { c_->Init(); }
  std::optional<Tuple> Next() override {
    auto t = c_->Next(); if (!t) return std::nullopt;
    if (cols_.empty()) return t;                 // '*' passthrough
    Tuple o; for (auto& c : cols_) if (t->cols.count(c)) o.cols[c] = t->cols.at(c);
    return o;
  }
 private:
  std::unique_ptr<Executor> c_; std::vector<std::string> cols_;
};

class OrderBy : public Executor {
 public:
  OrderBy(std::unique_ptr<Executor> c, std::string col, bool desc) : c_(std::move(c)), col_(std::move(col)), desc_(desc) {}
  void Init() override {
    c_->Init(); buf_.clear();
    while (auto t = c_->Next()) buf_.push_back(*t);
    std::stable_sort(buf_.begin(), buf_.end(), [&](const Tuple& a, const Tuple& b) {
      long long ka = a.cols.count(col_) ? a.cols.at(col_) : 0;
      long long kb = b.cols.count(col_) ? b.cols.at(col_) : 0;
      return desc_ ? ka > kb : ka < kb;
    });
    pos_ = 0;
  }
  std::optional<Tuple> Next() override {
    if (pos_ >= buf_.size()) return std::nullopt; return buf_[pos_++];
  }
 private:
  std::unique_ptr<Executor> c_; std::string col_; bool desc_; std::vector<Tuple> buf_; size_t pos_ = 0;
};

// ---- Planner: AST -> operator tree ---------------------------------------
static bool cmp_eval(Cmp op, long long l, long long r) {
  switch (op) { case Cmp::Eq: return l == r; case Cmp::Ne: return l != r;
    case Cmp::Lt: return l < r; case Cmp::Le: return l <= r; case Cmp::Gt: return l > r; case Cmp::Ge: return l >= r; }
  return false;
}

class Planner {
 public:
  explicit Planner(std::map<std::string, Table>* db) : db_(db) {}
  std::unique_ptr<Executor> Plan(const Query& q) {
    auto it = db_->find(q.table);
    if (it == db_->end()) throw std::runtime_error("no such table: " + q.table);
    std::unique_ptr<Executor> node = std::make_unique<SeqScan>(&it->second);
    if (!q.where.empty()) {
      auto preds = q.where;
      node = std::make_unique<Filter>(std::move(node), [preds](const Tuple& t) {
        for (auto& p : preds) { long long v = t.cols.count(p.col) ? t.cols.at(p.col) : 0; if (!cmp_eval(p.op, v, p.value)) return false; }
        return true;
      });
    }
    if (q.order_col) node = std::make_unique<OrderBy>(std::move(node), *q.order_col, q.order_desc);
    node = std::make_unique<Project>(std::move(node), q.star ? std::vector<std::string>{} : q.select_cols);
    return node;
  }
 private:
  std::map<std::string, Table>* db_;
};

// ---- Tests ----------------------------------------------------------------
static int g_fail = 0;
static void CHECK(bool c, const char* m) {
  if (!c) { printf("  [FAIL] %s\n", m); g_fail++; } else { printf("  [ ok ] %s\n", m); }
}

static std::vector<Tuple> Exec(const std::string& sql, Planner& pl) {
  Lexer lx(sql); Query q = Parser(lx.All()).Parse();
  auto tree = pl.Plan(q);
  tree->Init(); std::vector<Tuple> out; while (auto t = tree->Next()) out.push_back(*t);
  return out;
}

int main() {
  printf("=== 06 mini-sql parser + executor ===\n");
  std::map<std::string, Table> db;
  Table emp{"emp", {"id","name","dept","salary"}, {}};
  emp.rows = {
    {{"id",1},{"dept",10},{"salary",5000}},
    {{"id",2},{"dept",20},{"salary",8000}},
    {{"id",3},{"dept",10},{"salary",6000}},
    {{"id",4},{"dept",30},{"salary",9000}},
    {{"id",5},{"dept",20},{"salary",7000}},
  };
  db["emp"] = emp;
  Planner pl(&db);

  // SELECT id,salary FROM emp WHERE dept = 10
  {
    auto r = Exec("SELECT id,salary FROM emp WHERE dept = 10", pl);
    CHECK(r.size() == 2, "dept=10 -> 2 rows");
    CHECK(r[0].cols.count("id") && !r[0].cols.count("dept"), "projection drops unselected cols");
  }
  // SELECT * FROM emp WHERE salary >= 7000
  {
    auto r = Exec("SELECT * FROM emp WHERE salary >= 7000", pl);
    CHECK(r.size() == 3, "salary>=7000 -> 3 rows");
    CHECK(r[0].cols.size() == 4, "star keeps all columns");
  }
  // SELECT id FROM emp WHERE dept != 10 AND salary < 8000 ORDER BY id DESC
  {
    auto r = Exec("SELECT id FROM emp WHERE dept != 10 AND salary < 8000 ORDER BY id DESC", pl);
    CHECK(r.size() == 2, "compound AND filter");
    CHECK(r[0].cols.at("id") == 5 && r[1].cols.at("id") == 2, "order by id desc");
  }
  // parse error path
  {
    bool threw = false;
    try { Exec("SELECT id emp WHERE", pl); } catch (...) { threw = true; }
    CHECK(threw, "malformed query raises");
  }

  printf("=== %s ===\n", g_fail == 0 ? "ALL TESTS PASSED" : "SOME TESTS FAILED");
  return g_fail == 0 ? 0 : 1;
}
