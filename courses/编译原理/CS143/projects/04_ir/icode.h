#pragma once
// ============================================================================
// MiniC stage 04 — INTERMEDIATE REPRESENTATION: three-address code generator.
// Course mapping: notes/L12 (what an IR is) + notes/L13 (translation schemes,
// backpatching, short-circuit control flow). This file is the "new material"
// of stage 04; main.cpp only wires the pipeline.
//
// IR shape (Dragon book ch8 style, one definition/line):
//   dst = imm / dst = src1 op src2 / dst = !src1 / dst = -src1
//   dst = src1                       (MOVE; dst may be a global box "$a<i>")
//   L<n>:  /  goto L<n>  /  ifz t goto L<n>  /  ifnz t goto L<n>
//   dst = call fname                 (arguments staged via "$a<i>" boxes)
//   return t / return / print t / printb t / nop
//
// Naming model — two kinds of value names:
//   * slots  "x@12": storage cells (variables/params), may be written many
//     times, i.e. "memory-like" names — exactly what mem2reg/SSA promotes
//     (see notes/L17). Scope shadowing is resolved at generation time by
//     giving every binding a FRESH slot name, so slots are already unique
//     (though not single-assignment).
//   * temps  "t7": written at most once by the generator (SSA-ish): ideal
//     food for the stage-06 optimizer.
//   * "$a<i>" are global argument boxes: a deliberate miniature of a calling
//     convention (notes/L11) — caller writes, callee copies at entry.
// ============================================================================
#include <ostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

#include "../common/ast.h"

namespace minic {

enum class IOp {
  Const, Add, Sub, Mul, Div, Mod, Neg, Not,
  Lt, Le, Gt, Ge, Eq, Ne,
  Move, Label, Jmp, Jz, Jnz, Call, Ret, Print, PrintB, Nop
};

struct Inst {
  IOp op = IOp::Nop;
  std::string dst;            // defined value name ("" if none)
  std::string src1, src2;     // read value names ("" if unused)
  long long imm = 0;          // Const payload
  int target = -1;            // jump target / Label id
  std::string fname;          // Call callee
  int line = 0;               // source line for annotations
};

struct IRFunc {
  std::string name;
  int nparams = 0;
  std::vector<Inst> code;
};

inline const char* opSymbol(IOp op, bool& isCmp) {
  isCmp = true;
  switch (op) {
    case IOp::Add: return "+";  case IOp::Sub: return "-";
    case IOp::Mul: return "*";  case IOp::Div: return "/";  case IOp::Mod: return "%";
    case IOp::Lt:  return "<";  case IOp::Le:  return "<=";
    case IOp::Gt:  return ">";  case IOp::Ge:  return ">=";
    case IOp::Eq:  return "=="; case IOp::Ne:  return "!=";
  }
  isCmp = false;
  return "";
}

inline std::string instText(const Inst& in) {
  bool cmp = false;
  const char* sym = opSymbol(in.op, cmp);
  switch (in.op) {
    case IOp::Const: return in.dst + " = " + std::to_string(in.imm);
    case IOp::Neg:   return in.dst + " = -" + in.src1;
    case IOp::Not:   return in.dst + " = !" + in.src1;
    case IOp::Move:  return in.dst + " = " + in.src1;
    case IOp::Label: return "L" + std::to_string(in.target) + ":";
    case IOp::Jmp:   return "goto L" + std::to_string(in.target);
    case IOp::Jz:    return "ifz " + in.src1 + " goto L" + std::to_string(in.target);
    case IOp::Jnz:   return "ifnz " + in.src1 + " goto L" + std::to_string(in.target);
    case IOp::Call:  return in.dst + " = call " + in.fname;
    case IOp::Ret:   return in.src1.empty() ? "return" : ("return " + in.src1);
    case IOp::Print: return "print " + in.src1;
    case IOp::PrintB: return "printb " + in.src1;
    case IOp::Nop:   return "nop";
    default:         return in.dst + " = " + in.src1 + " " + sym + " " + in.src2;
  }
}

inline void dumpIR(std::ostream& os, const std::vector<IRFunc>& prog) {
  for (const auto& fn : prog) {
    os << "--- func " << fn.name << " (" << fn.nparams << " params, "
       << fn.code.size() << " instrs) ---\n";
    for (const auto& in : fn.code) {
      os << "  " << instText(in);
      if (in.line) os << "        ; source line " << in.line;
      os << "\n";
    }
  }
}

class IRGen {
 public:
  std::vector<IRFunc> generate(Program& p) {
    std::vector<IRFunc> out;
    for (auto& f : p.funcs) out.push_back(genFunc(*f));
    return out;
  }

 private:
  std::string newTmp() { return "t" + std::to_string(++tmp_); }
  int newLabel() { return ++label_; }
  void emit(const Inst& in) { code_.push_back(in); }
  void emitLabel(int id, int line) {
    Inst l; l.op = IOp::Label; l.target = id; l.line = line; emit(l);
  }

  std::string slotFor(const std::string& name) {
    for (auto it = scopes_.rbegin(); it != scopes_.rend(); ++it) {
      auto f = it->find(name);
      if (f != it->end()) return f->second;
    }
    throw std::runtime_error("IRGen: undeclared '" + name +
                             "' — the checker should have caught this");
  }
  std::string bind(const std::string& name) {
    std::string slot = name + "@" + std::to_string(++slot_);
    scopes_.back()[name] = slot;
    return slot;
  }

  IRFunc genFunc(const Func& f) {
    code_.clear();
    scopes_.clear();
    scopes_.emplace_back();
    tmp_ = label_ = slot_ = 0;

    // Prologue (notes/L11): copy the global argument boxes into fresh slots.
    for (size_t i = 0; i < f.params.size(); ++i) {
      std::string slot = bind(f.params[i].name);
      Inst m;
      m.op = IOp::Move;
      m.dst = slot;
      m.src1 = "$a" + std::to_string(i);
      m.line = f.loc.line;
      emit(m);
    }

    genBlock(*f.body);

    // Safety epilogue: the checker warns when this path is reachable.
    Inst c;
    c.op = IOp::Const;
    c.dst = newTmp();
    c.imm = 0;
    emit(c);
    Inst r;
    r.op = IOp::Ret;
    r.src1 = c.dst;
    emit(r);

    IRFunc fn;
    fn.name = f.name;
    fn.nparams = static_cast<int>(f.params.size());
    fn.code = std::move(code_);
    code_.clear();
    return fn;
  }

  void genBlock(BlockStmt& b) {
    scopes_.emplace_back();
    for (auto& s : b.items) genStmt(*s);
    scopes_.pop_back();
  }

  void genStmt(Stmt& s) {
    switch (s.kind) {
      case Stmt::SBlock: genBlock(static_cast<BlockStmt&>(s)); break;

      case Stmt::SVar: {
        auto& d = static_cast<VarStmt&>(s);
        std::string init;
        if (d.init) {
          init = genExpr(*d.init);
        } else {
          Inst c;
          c.op = IOp::Const;
          c.dst = newTmp();
          c.imm = 0;
          c.line = d.loc.line;
          emit(c);
          init = c.dst;
        }
        Inst m;
        m.op = IOp::Move;
        m.dst = bind(d.name);
        m.src1 = init;
        m.line = d.loc.line;
        emit(m);
        break;
      }

      case Stmt::SAssign: {
        auto& a = static_cast<AssignStmt&>(s);
        std::string v = genExpr(*a.rhs);
        Inst m;
        m.op = IOp::Move;
        m.dst = slotFor(a.name);
        m.src1 = v;
        m.line = a.loc.line;
        emit(m);
        break;
      }

      case Stmt::SPrint: {
        auto& p = static_cast<PrintStmt&>(s);
        Inst out;
        out.op = (p.e->type == Ty::Bool) ? IOp::PrintB : IOp::Print;
        out.src1 = genExpr(*p.e);
        out.line = p.loc.line;
        emit(out);
        break;
      }

      case Stmt::SReturn: {
        auto& r = static_cast<ReturnStmt&>(s);
        Inst i;
        i.op = IOp::Ret;
        i.line = r.loc.line;
        if (r.e) i.src1 = genExpr(*r.e);
        emit(i);
        break;
      }

      case Stmt::SIf: {
        auto& f = static_cast<IfStmt&>(s);
        std::string c = genExpr(*f.cond);
        int lElse = newLabel();
        Inst jz;
        jz.op = IOp::Jz;
        jz.src1 = c;
        jz.target = lElse;
        jz.line = f.loc.line;
        emit(jz);                       // "true list" patched right here (L13)
        genStmt(*f.thenS);
        if (f.elseS) {
          int lEnd = newLabel();
          Inst jmp;
          jmp.op = IOp::Jmp;
          jmp.target = lEnd;
          jmp.line = f.loc.line;
          emit(jmp);
          emitLabel(lElse, f.loc.line);
          genStmt(*f.elseS);
          emitLabel(lEnd, f.loc.line);
        } else {
          emitLabel(lElse, f.loc.line);
        }
        break;
      }

      case Stmt::SWhile: {
        auto& w = static_cast<WhileStmt&>(s);
        int lBody = newLabel(), lCond = newLabel();
        Inst jmp;
        jmp.op = IOp::Jmp;
        jmp.target = lCond;
        jmp.line = w.loc.line;
        emit(jmp);
        emitLabel(lBody, w.loc.line);
        genStmt(*w.body);
        emitLabel(lCond, w.loc.line);
        std::string c = genExpr(*w.cond);
        Inst jnz;
        jnz.op = IOp::Jnz;
        jnz.src1 = c;
        jnz.target = lBody;
        jnz.line = w.loc.line;
        emit(jnz);                      // the "back edge" — reducible (L13)
        break;
      }

      case Stmt::SExpr: {
        auto& e = static_cast<ExprStmt&>(s);
        genExpr(*e.e);
        break;
      }
    }
  }

  std::string genExpr(Expr& e) {
    switch (e.kind) {
      case Expr::ENum: {
        Inst c;
        c.op = IOp::Const;
        c.dst = newTmp();
        c.imm = static_cast<const NumExpr&>(e).v;
        c.line = e.loc.line;
        emit(c);
        return c.dst;
      }
      case Expr::EBool: {
        Inst c;
        c.op = IOp::Const;
        c.dst = newTmp();
        c.imm = static_cast<const BoolExpr&>(e).v ? 1 : 0;
        c.line = e.loc.line;
        emit(c);
        return c.dst;
      }
      case Expr::EVar:
        return slotFor(static_cast<const VarExpr&>(e).name);

      case Expr::EUnary: {
        auto& u = static_cast<UnaryExpr&>(e);
        std::string v = genExpr(*u.e);
        Inst i;
        i.op = (u.op == UnaryExpr::Neg) ? IOp::Neg : IOp::Not;
        i.dst = newTmp();
        i.src1 = v;
        i.line = u.loc.line;
        emit(i);
        return i.dst;
      }

      case Expr::ECall: {
        auto& c = static_cast<CallExpr&>(e);
        // Evaluate ALL arguments first, then stage them into the "$a<i>"
        // boxes atomically right before Call — otherwise an inner call in a
        // later argument would clobber the boxes (a real ABI avoids this by
        // pushing onto the caller's stack; notes/L11).
        std::vector<std::string> vals;
        vals.reserve(c.args.size());
        for (auto& a : c.args) vals.push_back(genExpr(*a));
        for (size_t i = 0; i < vals.size(); ++i) {
          Inst m;
          m.op = IOp::Move;
          m.dst = "$a" + std::to_string(i);
          m.src1 = vals[i];
          m.line = c.loc.line;
          emit(m);                      // caller-side staging (notes/L11)
        }
        Inst call;
        call.op = IOp::Call;
        call.dst = newTmp();
        call.fname = c.callee;
        call.line = c.loc.line;
        emit(call);
        return call.dst;
      }

      case Expr::EBinary: {
        auto& b = static_cast<BinaryExpr&>(e);
        if (b.op == BinaryExpr::And || b.op == BinaryExpr::Or) {
          // Short-circuit template (notes/L13 "布尔表达式的翻译模式"):
          //   a = lhs ; t = a ; ifz a goto Lend (&&) / ifnz (||)
          //   rhs -> v ; t = v ; Lend:
          std::string a = genExpr(*b.lhs);
          std::string t = newTmp();
          Inst mv1;
          mv1.op = IOp::Move;
          mv1.dst = t;
          mv1.src1 = a;
          mv1.line = b.loc.line;
          emit(mv1);
          int lEnd = newLabel();
          Inst jz;
          jz.op = (b.op == BinaryExpr::And) ? IOp::Jz : IOp::Jnz;
          jz.src1 = a;
          jz.target = lEnd;
          jz.line = b.loc.line;
          emit(jz);
          std::string v = genExpr(*b.rhs);
          Inst mv2;
          mv2.op = IOp::Move;
          mv2.dst = t;
          mv2.src1 = v;
          mv2.line = b.loc.line;
          emit(mv2);
          emitLabel(lEnd, b.loc.line);
          return t;
        }
        std::string l = genExpr(*b.lhs);
        std::string r = genExpr(*b.rhs);
        Inst i;
        switch (b.op) {
          case BinaryExpr::Add: i.op = IOp::Add; break;
          case BinaryExpr::Sub: i.op = IOp::Sub; break;
          case BinaryExpr::Mul: i.op = IOp::Mul; break;
          case BinaryExpr::Div: i.op = IOp::Div; break;
          case BinaryExpr::Mod: i.op = IOp::Mod; break;
          case BinaryExpr::Lt:  i.op = IOp::Lt;  break;
          case BinaryExpr::Le:  i.op = IOp::Le;  break;
          case BinaryExpr::Gt:  i.op = IOp::Gt;  break;
          case BinaryExpr::Ge:  i.op = IOp::Ge;  break;
          case BinaryExpr::Eq:  i.op = IOp::Eq;  break;
          case BinaryExpr::Ne:  i.op = IOp::Ne;  break;
          default: i.op = IOp::Nop; break;       // And/Or handled above
        }
        i.dst = newTmp();
        i.src1 = l;
        i.src2 = r;
        i.line = b.loc.line;
        emit(i);
        return i.dst;
      }
    }
    return "";
  }

  std::vector<Inst> code_;
  std::vector<std::unordered_map<std::string, std::string>> scopes_;
  int tmp_ = 0, label_ = 0, slot_ = 0;
};

}  // namespace minic
