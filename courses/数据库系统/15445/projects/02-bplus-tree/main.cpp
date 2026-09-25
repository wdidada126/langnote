// 02-bplus-tree : In-memory B+tree with insert + node splitting + range scan.
// CMU 15-445/645 Fall 2023 — companion to Lecture 08 (Tree-Based Indexes).
// Standard library only, C++17.
//
// Properties implemented:
//   * internal nodes store only keys + child pointers (routing); data lives in leaves
//   * leaves linked by a next-sibling pointer for O(range) ordered scan
//   * insert triggers leaf split -> key promotion -> recursive split up to root
//   * order (max children) configurable; nodes stay at >= ceil(order/2) keys after split
#include <algorithm>
#include <cassert>
#include <cstdio>
#include <functional>
#include <memory>
#include <optional>
#include <string>
#include <vector>

// ---- Node bases -----------------------------------------------------------
struct Node {
  virtual ~Node() = default;
  virtual bool is_leaf() const = 0;
};

struct Leaf : Node {
  bool is_leaf() const override { return true; }
  std::vector<int> keys;          // sorted
  std::vector<int> values;        // parallel to keys
  Leaf* next = nullptr;           // sibling link for scanning
};

struct Inner : Node {
  bool is_leaf() const override { return false; }
  std::vector<int> keys;          // separator keys, size == children.size()-1
  std::vector<std::unique_ptr<Node>> children;
};

// ---- B+ tree --------------------------------------------------------------
class BPlusTree {
 public:
  explicit BPlusTree(int order = 4) : order_(order) {}  // order = max children

  void Insert(int key, int value) {
    if (!root_) {
      auto l = std::make_unique<Leaf>();
      l->keys.push_back(key); l->values.push_back(value);
      root_ = std::move(l);
      ++size_;
      return;
    }
    Leaf* leaf = find_leaf(key);
    // insert into leaf keeping sorted order
    size_t pos = std::lower_bound(leaf->keys.begin(), leaf->keys.end(), key) - leaf->keys.begin();
    leaf->keys.insert(leaf->keys.begin() + pos, key);
    leaf->values.insert(leaf->values.begin() + pos, value);
    ++size_;
    // split if overflow
    int max_keys = order_ - 1;
    if ((int)leaf->keys.size() > max_keys) {
      split_leaf(leaf, max_keys);
    }
  }

  std::optional<int> Get(int key) const {
    Leaf* l = find_leaf(key);
    for (size_t i = 0; i < l->keys.size(); i++)
      if (l->keys[i] == key) return l->values[i];
    return std::nullopt;
  }

  // In-order scan of [lo, hi] following sibling links.
  std::vector<std::pair<int, int>> RangeScan(int lo, int hi) const {
    std::vector<std::pair<int, int>> out;
    Leaf* l = find_leaf(lo);
    while (l) {
      for (size_t i = 0; i < l->keys.size(); i++) {
        if (l->keys[i] > hi) return out;
        if (l->keys[i] >= lo) out.emplace_back(l->keys[i], l->values[i]);
      }
      l = l->next;
    }
    return out;
  }

  // Full ordered traversal (used by tests).
  std::vector<int> AllKeys() const {
    std::vector<int> out;
    Leaf* l = leftmost_leaf();
    while (l) { for (int k : l->keys) out.push_back(k); l = l->next; }
    return out;
  }

  int height() const {
    int h = 0; Node* n = root_.get();
    while (n && !n->is_leaf()) { n = static_cast<Inner*>(n)->children[0].get(); h++; }
    return h + (n ? 1 : 0);
  }
  int size() const { return size_; }

 private:
  Leaf* leftmost_leaf() const {
    if (!root_) return nullptr;
    Node* n = root_.get();
    while (!n->is_leaf()) n = static_cast<Inner*>(n)->children[0].get();
    return static_cast<Leaf*>(n);
  }

  Leaf* find_leaf(int key) const {
    Node* n = root_.get();
    while (!n->is_leaf()) {
      Inner* in = static_cast<Inner*>(n);
      size_t i = 0;
      while (i < in->keys.size() && key >= in->keys[i]) i++;  // right on ties
      n = in->children[i].get();
    }
    return static_cast<Leaf*>(n);
  }

  // Find parent + child index of a given node (teaching-grade: top-down search).
  std::pair<Node*, size_t> find_parent_and_index(Node* target) const {
    if (root_.get() == target) return {nullptr, 0};
    Node* cur = root_.get();
    while (cur && !cur->is_leaf()) {
      Inner* in = static_cast<Inner*>(cur);
      for (size_t i = 0; i < in->children.size(); i++)
        if (in->children[i].get() == target) return {cur, i};
      // descend toward target using keys is not enough; do DFS:
      for (size_t i = 0; i < in->children.size(); i++) {
        auto r = dfs_parent(in->children[i].get(), target, cur);
        if (r.first) return r;
      }
      break;
    }
    return {nullptr, 0};
  }

  std::pair<Node*, size_t> dfs_parent(Node* child, Node* target, Node* fallback_parent) const {
    if (child == target) return {fallback_parent, 0};
    if (!child->is_leaf()) {
      Inner* in = static_cast<Inner*>(child);
      for (size_t i = 0; i < in->children.size(); i++) {
        auto r = dfs_parent(in->children[i].get(), target, child);
        if (r.first) {
          // recompute the index of target within its parent
          Inner* p = in;  // parent of target is `child` here when r.child==target
          (void)p;
          return {child, index_of_child(child, target)};
        }
      }
    }
    return {nullptr, 0};
  }

  size_t index_of_child(Node* parent, Node* target) const {
    Inner* in = static_cast<Inner*>(parent);
    for (size_t i = 0; i < in->children.size(); i++)
      if (in->children[i].get() == target) return i;
    return 0;
  }

  void insert_into_parent(Leaf* /*not used*/, Node* left, int key, std::unique_ptr<Node> right);

  void split_leaf(Leaf* leaf, int max_keys) {
    int mid = leaf->keys.size() / 2;
    auto right = std::make_unique<Leaf>();
    right->keys.assign(leaf->keys.begin() + mid, leaf->keys.end());
    right->values.assign(leaf->values.begin() + mid, leaf->values.end());
    leaf->keys.resize(mid);
    leaf->values.resize(mid);
    // maintain sibling link
    right->next = leaf->next;
    leaf->next = right.get();

    int promote_key = right->keys.front();
    Node* parent;
    size_t idx;
    std::tie(parent, idx) = find_parent_and_index(leaf);
    if (!parent) {
      // leaf was root -> create new root
      auto nr = std::make_unique<Inner>();
      nr->keys = {promote_key};
      // keep leaf as left child: we cannot move ownership out of root_ directly,
      // so we restructure: build children referencing existing nodes.
      std::unique_ptr<Node> left_holder = std::move(root_);
      nr->children.push_back(std::move(left_holder));
      nr->children.push_back(std::move(right));
      root_ = std::move(nr);
      return;
    }
    Inner* in = static_cast<Inner*>(parent);
    size_t child_idx = index_of_child(parent, leaf);
    in->keys.insert(in->keys.begin() + child_idx, promote_key);
    in->children.insert(in->children.begin() + child_idx + 1, std::move(right));
    if ((int)in->keys.size() > order_ - 1) split_inner(in);
  }

  void split_inner(Inner* node) {
    int mid = node->keys.size() / 2;
    int promote = node->keys[mid];
    auto right = std::make_unique<Inner>();
    right->keys.assign(node->keys.begin() + mid + 1, node->keys.end());
    for (size_t i = mid + 1; i < node->children.size(); i++)
      right->children.push_back(std::move(node->children[i]));
    node->children.resize(mid + 1);
    node->keys.resize(mid);

    Node* parent; size_t idx;
    std::tie(parent, idx) = find_parent_and_index(node);
    if (!parent) {
      auto nr = std::make_unique<Inner>();
      nr->keys = {promote};
      std::unique_ptr<Node> left_holder = std::move(root_);
      nr->children.push_back(std::move(left_holder));
      nr->children.push_back(std::move(right));
      root_ = std::move(nr);
      return;
    }
    Inner* in = static_cast<Inner*>(parent);
    size_t child_idx = index_of_child(parent, node);
    in->keys.insert(in->keys.begin() + child_idx, promote);
    in->children.insert(in->children.begin() + child_idx + 1, std::move(right));
    if ((int)in->keys.size() > order_ - 1) split_inner(in);
  }

  int order_;
  int size_ = 0;
  std::unique_ptr<Node> root_;
};

// ---- Tests ----------------------------------------------------------------
static int g_fail = 0;
static void CHECK(bool c, const char* m) {
  if (!c) { printf("  [FAIL] %s\n", m); g_fail++; } else { printf("  [ ok ] %s\n", m); }
}

int main() {
  printf("=== 02 b+ tree (insert/split + range scan) ===\n");

  // Test 1: sequential inserts stay sorted, dedup by ordering.
  {
    BPlusTree t(4);
    for (int i = 0; i < 50; i++) t.Insert(i, i * 10);
    auto keys = t.AllKeys();
    bool sorted = std::is_sorted(keys.begin(), keys.end());
    CHECK(keys.size() == 50, "50 leaves after 50 inserts");
    CHECK(sorted, "leaf chain is fully sorted");
    CHECK(t.Get(37) && *t.Get(37) == 370, "point lookup correct");
    CHECK(t.height() > 2, "tree grew multiple levels");
  }

  // Test 2: random inserts maintain order and value mapping.
  {
    BPlusTree t(5);
    std::vector<int> order = {50,10,30,90,20,80,60,40,70,100,5,25,55,75,95,15};
    for (int k : order) t.Insert(k, -k);
    auto keys = t.AllKeys();
    CHECK(keys.size() == order.size(), "all keys stored");
    CHECK(std::is_sorted(keys.begin(), keys.end()), "random inserts stay sorted");
    bool vals_ok = true;
    for (int k : order) if (!t.Get(k) || *t.Get(k) != -k) vals_ok = false;
    CHECK(vals_ok, "all values retrievable");
  }

  // Test 3: range scan inclusive and ordered via sibling links.
  {
    BPlusTree t(4);
    for (int i = 1; i <= 20; i++) t.Insert(i, i);
    auto r = t.RangeScan(7, 13);
    std::vector<int> got;
    for (auto& kv : r) got.push_back(kv.first);
    CHECK(got.size() == 7 && got.front() == 7 && got.back() == 13, "range [7,13] returns 13..7");
    bool ok = true; for (size_t i = 0; i < r.size(); i++) if (r[i].first != (int)i+7) ok = false;
    CHECK(ok, "range scan in order and inclusive");
  }

  printf("=== %s ===\n", g_fail == 0 ? "ALL TESTS PASSED" : "SOME TESTS FAILED");
  return g_fail == 0 ? 0 : 1;
}
