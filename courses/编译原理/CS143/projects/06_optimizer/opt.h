#pragma once
// ============================================================================
// MiniC stage 06 — MACHINE-INDEPENDENT OPTIMIZATION passes over three-address
// code. Course mapping: notes/L14 (frameworks) + notes/L17 (const prop /
// copy prop / DCE / SSA-adjacent reasoning).
//
// Pass inventory:
//   1. constFold   — BLOCK-LOCAL latticed constant propagation over temps:
//                    folding arithmetic and Jz/Jnz on constant conditions.
//                    The map resets at every Label (block boundary): merging
//                    paths needs the full L14 data-flow machinery, which is
//                    the honest reason this toy stays local (and why LLVM
//                    wants memory in SSA before doing it globally).
//   2. pruneJumpOver — delete straight-line runs skipped by a forward Jmp
//                    (only when no other jump targets the run). This is a
//                    miniature simplify-CFG.
//   3. copyProp    — block-local dst->src chains over single-def temps
//                    ("t_a = t_b" ⇒ later reads of t_a see t_b). Slots are
//                    excluded because they can be reassigned: this is the
//                    L12/L17 "SSA makes optimizations cheap" lesson in one
//                    line of code.
//   4. deadCode    — whole-function backward use analysis by NAME: no
//                    aliasing in MiniC, so an un-read name is provably dead.
//                    Calls are kept (side-effect conservative).
// ============================================================================
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "../04_ir/icode.h"

namespace minic {
namespace oopt {

inline bool isTemp(const std::string& n) { return !n.empty() && n[0] == 't'; }

inline bool isFoldable(IOp op) {
  switch (op) {
    case IOp::Add: case IOp::Sub: case IOp::Mul: case IOp::Div: case IOp::Mod:
    case IOp::Neg: case IOp::Not:
    case IOp::Lt: case IOp::Le: case IOp::Gt: case IOp::Ge:
    case IOp::Eq: case IOp::Ne:
      return true;
    default: return false;
  }
}

inline bool isValueDefining(IOp op) {
  return isFoldable(op) || op == IOp::Const || op == IOp::Move;
}

// Evaluation with a soft "undefined" channel (div/mod by zero refuses to fold).
inline long long eval(IOp op, long long a, long long b, bool& ok) {
  ok = true;
  switch (op) {
    case IOp::Add: return a + b;
    case IOp::Sub: return a - b;
    case IOp::Mul: return a * b;
    case IOp::Div: if (b == 0) { ok = false; return 0; } return a / b;
    case IOp::Mod: if (b == 0) { ok = false; return 0; } return a % b;
    case IOp::Neg: return -a;
    case IOp::Not: return a ? 0 : 1;
    case IOp::Lt: return a < b;
    case IOp::Le: return a <= b;
    case IOp::Gt: return a > b;
    case IOp::Ge: return a >= b;
    case IOp::Eq: return a == b ? 1 : 0;
    case IOp::Ne: return a != b ? 1 : 0;
    default: ok = false; return 0;
  }
}

}  // namespace oopt

class Optimizer {
 public:
  bool optimize(std::vector<IRFunc>& prog) {
    bool any = false;
    for (auto& fn : prog) any |= optimizeFunction(fn);
    return any;
  }

  bool optimizeFunction(IRFunc& fn) {
    bool any = false;
    for (int round = 0; round < 10; ++round) {
      bool ch = false;
      ch |= constFold(fn.code);
      ch |= pruneJumpOver(fn.code);
      ch |= copyProp(fn.code);
      ch |= deadCode(fn.code);
      if (!ch) break;
      any = true;
    }
    return any;
  }

 private:
  using Code = std::vector<Inst>;

  bool constFold(Code& code) {
    bool changed = false;
    std::unordered_map<std::string, long long> konst;
    for (auto& in : code) {
      switch (in.op) {
        case IOp::Label:
          konst.clear();               // block boundary = merge point
          break;
        case IOp::Const:
          if (oopt::isTemp(in.dst)) konst[in.dst] = in.imm;
          break;
        case IOp::Jz: case IOp::Jnz: {
          auto it = konst.find(in.src1);
          if (it == konst.end()) break;
          bool take = (in.op == IOp::Jz) ? (it->second == 0) : (it->second != 0);
          if (take) { in.op = IOp::Jmp; in.src1.clear(); }
          else { in.op = IOp::Nop; in.src1.clear(); in.target = -1; }
          changed = true;
          break;
        }
        case IOp::Move:
          if (konst.count(in.dst)) konst.erase(in.dst);
          break;
        case IOp::Call:
          if (konst.count(in.dst)) konst.erase(in.dst);
          break;
        default:
          if (!oopt::isFoldable(in.op)) break;
          if (in.dst.empty()) { if (konst.count(in.dst)) konst.erase(in.dst); break; }
          auto i1 = konst.find(in.src1);
          auto i2 = konst.find(in.src2);
          bool unary = (in.op == IOp::Neg || in.op == IOp::Not);
          bool have = unary ? (i1 != konst.end())
                            : (i1 != konst.end() && i2 != konst.end());
          if (have) {
            bool ok = false;
            long long v = oopt::eval(in.op, i1->second,
                                     i2 != konst.end() ? i2->second : 0, ok);
            if (ok) {
              Inst c;
              c.op = IOp::Const;
              c.dst = in.dst;
              c.imm = v;
              c.line = in.line;
              in = c;
              konst[in.dst] = v;
              changed = true;
              break;
            }
          }
          konst.erase(in.dst);
          break;
      }
    }
    return changed;
  }

  bool pruneJumpOver(Code& code) {
    bool changed = false;
    for (size_t i = 0; i < code.size(); ++i) {
      if (code[i].op != IOp::Jmp || code[i].target < 0) continue;
      // Locate the target label *forward*; erase the skipped straight-line
      // run unless any label defined inside it is targeted from elsewhere.
      size_t j = i + 1;
      for (; j < code.size(); ++j)
        if (code[j].op == IOp::Label && code[j].target == code[i].target) break;
      if (j >= code.size() || j == i + 1) continue;
      std::unordered_set<int> internal;
      for (size_t k = i + 1; k < j; ++k)
        if (code[k].op == IOp::Label) internal.insert(code[k].target);
      bool externalTarget = false;
      for (size_t k = 0; k < code.size() && !externalTarget; ++k) {
        if (k > i && k < j) continue;                 // inside the run
        const Inst& t = code[k];
        if ((t.op == IOp::Jmp || t.op == IOp::Jz || t.op == IOp::Jnz) &&
            internal.count(t.target)) externalTarget = true;
      }
      if (externalTarget) continue;
      code.erase(code.begin() + i + 1, code.begin() + j);
      changed = true;
    }
    return changed;
  }

  bool copyProp(Code& code) {
    bool changed = false;
    std::unordered_map<std::string, std::string> alias;   // dst -> src (temps)
    auto resolve = [&](std::string& name) {
      if (!oopt::isTemp(name)) return;
      std::string cur = name;
      std::unordered_set<std::string> seen;
      while (true) {
        auto it = alias.find(cur);
        if (it == alias.end() || seen.count(it->second)) break;
        seen.insert(cur);
        cur = it->second;
      }
      if (cur != name) { name = cur; changed = true; }
    };
    for (auto& in : code) {
      switch (in.op) {
        case IOp::Label:
          alias.clear();
          break;
        case IOp::Move: {
          resolve(in.src1);                                // read
          if (oopt::isTemp(in.dst) && oopt::isTemp(in.src1)) {
            if (in.dst == in.src1) { in.op = IOp::Nop; changed = true; }
            else alias[in.dst] = in.src1;
          } else {
            alias.erase(in.dst);
          }
          break;
        }
        default:
          resolve(in.src1);
          resolve(in.src2);
          if (!in.dst.empty() && oopt::isTemp(in.dst)) {
            // a re-definition invalidates any older binding of dst
            // (temps are single-def in this IR, so this is belt-and-suspenders)
          }
          break;
      }
    }
    return changed;
  }

  bool deadCode(Code& code) {
    bool anyRemoved = false;
    for (;;) {
      std::unordered_set<std::string> read;
      for (const auto& in : code) {
        if (!in.src1.empty()) read.insert(in.src1);
        if (!in.src2.empty()) read.insert(in.src2);
      }
      Code kept;
      bool removed = false;
      for (const auto& in : code) {
        bool definesName = !in.dst.empty() && in.dst[0] != '$' &&
                           oopt::isValueDefining(in.op);
        if (definesName && !read.count(in.dst)) { removed = true; continue; }
        kept.push_back(in);
      }
      code.swap(kept);
      if (!removed) break;
      anyRemoved = true;
    }
    // Final tidy: drop Nops (never targeted; labels/jumps keep their ids).
    Code kept;
    for (const auto& in : code)
      if (in.op != IOp::Nop) kept.push_back(in);
    if (kept.size() != code.size()) anyRemoved = true;
    code.swap(kept);
    return anyRemoved;
  }
};

}  // namespace minic
