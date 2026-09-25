#pragma once
// ============================================================================
// MiniC stage 05 — BACK END as a three-address VIRTUAL MACHINE.
// Course mapping: notes/L11 (activation records), notes/L15 (why a real PA5
// emits MIPS/x86 instead — this stage's README shows the asm-style rendering).
//
// The machine keeps an explicit frame stack (one Frame per live call — a
// literal stack of activation records), a shared global box map for the
// "$a<i>" argument cells (our toy calling convention), and a step budget
// that catches infinite loops.
// ============================================================================
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

#include "../04_ir/icode.h"

namespace minic {

class Machine {
 public:
  static constexpr size_t kMaxSteps = 100000000;  // 1e8 — runaway guard

  explicit Machine(const std::vector<IRFunc>& prog, std::ostream& out = std::cout)
      : prog_(prog), out_(out) {
    for (const auto& f : prog_) byName_[f.name] = &f;
  }

  // Call `entry` with empty argument boxes; returns its value.
  long long run(const std::string& entry) {
    const IRFunc* fn = findFunc(entry);
    frames_.clear();
    gbox_.clear();
    frames_.push_back(Frame{fn, 0, {}, ""});

    size_t steps = 0;
    long long programResult = 0;
    bool finished = false;

    while (!finished) {
      if (++steps > kMaxSteps)
        throw std::runtime_error("step limit exceeded (infinite loop?)");

      Frame& fr = frames_.back();
      if (fr.pc >= fr.fn->code.size())
        throw std::runtime_error("fell off the end of function " + fr.fn->name);
      const Inst in = fr.fn->code[fr.pc];   // copy: stack ops may invalidate fr
      ++fr.pc;                              // default advance; jumps override

      switch (in.op) {
        case IOp::Nop: case IOp::Label: break;

        case IOp::Const: write(fr, in.dst, in.imm); break;

        case IOp::Neg: write(frames_.back(), in.dst, -read(frames_.back(), in.src1)); break;
        case IOp::Not: write(frames_.back(), in.dst, read(frames_.back(), in.src1) ? 0 : 1); break;

        case IOp::Add: case IOp::Sub: case IOp::Mul: case IOp::Div: case IOp::Mod:
        case IOp::Lt: case IOp::Le: case IOp::Gt: case IOp::Ge:
        case IOp::Eq: case IOp::Ne: {
          Frame& cur = frames_.back();
          long long a = read(cur, in.src1), b = read(cur, in.src2);
          write(cur, in.dst, evalArith(in.op, a, b));
          break;
        }

        case IOp::Move: {
          Frame& cur = frames_.back();
          long long v = read(cur, in.src1);
          write(cur, in.dst, v);
          break;
        }

        case IOp::Jmp:
          frames_.back().pc = labelAt(frames_.back().fn, in.target);
          break;
        case IOp::Jz:
          if (read(frames_.back(), in.src1) == 0)
            frames_.back().pc = labelAt(frames_.back().fn, in.target);
          break;
        case IOp::Jnz:
          if (read(frames_.back(), in.src1) != 0)
            frames_.back().pc = labelAt(frames_.back().fn, in.target);
          break;

        case IOp::Call: {
          const IRFunc* callee = findFunc(in.fname);
          Frame nf;
          nf.fn = callee;
          nf.pc = 0;
          nf.retDest = in.dst;              // where the result lands in caller
          frames_.push_back(std::move(nf)); // "$a<i)" boxes already staged
          break;
        }
        case IOp::Ret: {
          Frame& cur = frames_.back();
          long long v = in.src1.empty() ? 0 : read(cur, in.src1);
          std::string dst = cur.retDest;
          frames_.pop_back();
          if (frames_.empty()) {            // entry frame returned: halt
            programResult = v;
            finished = true;
          } else if (!dst.empty()) {
            write(frames_.back(), dst, v);
          }
          break;
        }

        case IOp::Print:  out_ << read(frames_.back(), in.src1) << "\n"; break;
        case IOp::PrintB:
          out_ << (read(frames_.back(), in.src1) ? "true" : "false") << "\n";
          break;
      }
    }
    return programResult;
  }

 private:
  struct Frame {
    const IRFunc* fn = nullptr;
    size_t pc = 0;
    std::unordered_map<std::string, long long> locals;
    std::string retDest;                    // caller-side temp for the result
  };

  const IRFunc* findFunc(const std::string& name) {
    auto it = byName_.find(name);
    if (it == byName_.end())
      throw std::runtime_error("no such function: " + name);
    return it->second;
  }

  static long long evalArith(IOp op, long long a, long long b) {
    switch (op) {
      case IOp::Add: return a + b;
      case IOp::Sub: return a - b;
      case IOp::Mul: return a * b;
      case IOp::Div:
        if (b == 0) throw std::runtime_error("division by zero");
        return a / b;
      case IOp::Mod:
        if (b == 0) throw std::runtime_error("modulo by zero");
        return a % b;
      case IOp::Lt: return a < b;
      case IOp::Le: return a <= b;
      case IOp::Gt: return a > b;
      case IOp::Ge: return a >= b;
      case IOp::Eq: return a == b;
      case IOp::Ne: return a != b;
      default: return 0;
    }
  }

  long long read(const Frame& fr, const std::string& name) {
    if (!name.empty() && name[0] == '$') {
      auto it = gbox_.find(name);
      if (it == gbox_.end())
        throw std::runtime_error("read of uninitialized argument box " + name);
      return it->second;
    }
    auto it = fr.locals.find(name);
    if (it == fr.locals.end())
      throw std::runtime_error("read of uninitialized " + name +
                               " in " + fr.fn->name);
    return it->second;
  }

  void write(Frame& fr, const std::string& name, long long v) {
    if (name.empty()) return;               // e.g. statement-level `return`
    if (name[0] == '$') {                   // calling-convention box
      gbox_[name] = v;
      return;
    }
    fr.locals[name] = v;                    // ordinary local slot
  }

  size_t labelAt(const IRFunc* fn, int id) {
    auto perFn = labels_.find(fn);
    if (perFn == labels_.end()) {
      std::unordered_map<int, size_t> m;
      for (size_t i = 0; i < fn->code.size(); ++i)
        if (fn->code[i].op == IOp::Label) m[fn->code[i].target] = i;
      perFn = labels_.emplace(fn, std::move(m)).first;
    }
    auto it = perFn->second.find(id);
    if (it == perFn->second.end())
      throw std::runtime_error("jump to missing label in " + fn->name);
    return it->second;
  }

  const std::vector<IRFunc>& prog_;
  std::ostream& out_;
  std::unordered_map<std::string, const IRFunc*> byName_;
  std::unordered_map<const IRFunc*, std::unordered_map<int, size_t>> labels_;
  std::unordered_map<std::string, long long> gbox_;
  std::vector<Frame> frames_;
};

}  // namespace minic
