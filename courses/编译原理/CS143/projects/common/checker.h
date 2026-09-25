#pragma once
// ============================================================================
// MiniC compiler core — stage L09-L10 material: SCOPES + STATIC TYPE CHECK.
// Course mapping: CS143 L10 (symbol table, scope stack, type rules); the
// "attribute" being computed is Expr::type — a synthesized attribute in the
// sense of L9, propagated bottom-up while the environment flows top-down.
// Two-pass design (signatures first, then bodies) is what makes recursion and
// forward references legal — see notes/L10 "函数签名的两遍法".
// Error discipline: every faulty node reports once; we still return *some*
// type for it (Ty::Unknown printed as '?') so the traversal continues — the
// "sentinel type" trick that prevents cascading error spam.
// ============================================================================
#include <string>
#include <unordered_map>
#include <vector>

#include "ast.h"

namespace minic {

class Checker {
 public:
  const std::vector<std::string>& errors() const { return errors_; }
  const std::vector<std::string>& warnings() const { return warnings_; }

  bool checkProgram(Program& p) {
    funcs_.clear();
    errors_.clear();
    warnings_.clear();
    // Pass 1: collect signatures so recursive/forward calls are visible.
    for (auto& f : p.funcs) {
      if (funcs_.count(f->name)) {
        err(f->loc.line, "duplicate function name '" + f->name + "'");
        continue;
      }
      FnSig sig;
      sig.ret = f->ret;
      for (auto& prm : f->params) sig.params.push_back(prm.type);
      funcs_[f->name] = sig;
    }
    // Pass 2: check bodies.
    for (auto& f : p.funcs) checkFunc(*f);
    return errors_.empty();
  }

 private:
  struct FnSig { Ty ret = Ty::Unknown; std::vector<Ty> params; };

  void err(int line, const std::string& msg) {
    errors_.push_back("line " + std::to_string(line) + ": " + msg);
  }
  void warn(int line, const std::string& msg) {
    warnings_.push_back("line " + std::to_string(line) + ": warning: " + msg);
  }

  Ty* lookup(const std::string& name) {
    for (auto it = scopes_.rbegin(); it != scopes_.rend(); ++it) {
      auto f = it->find(name);
      if (f != it->end()) return &f->second;
    }
    return nullptr;
  }
  bool declaredHere(const std::string& name) const {
    return !scopes_.empty() && scopes_.back().count(name) > 0;
  }

  void checkFunc(Func& f) {
    scopes_.clear();
    scopes_.emplace_back();                 // parameter scope
    for (auto& p : f.params) {
      if (declaredHere(p.name))
        err(f.loc.line, "duplicate parameter '" + p.name + "'");
      else
        scopes_.back()[p.name] = p.type;
    }
    curRet_ = f.ret;
    curFn_ = &f;
    checkBlock(*f.body);
    if (f.body->items.empty() ||
        f.body->items.back()->kind != Stmt::SReturn)
      warn(f.loc.line, "function '" + f.name +
                           "' may reach its end without 'return'; "
                           "IRGen will emit an implicit `return 0`");
    curFn_ = nullptr;
  }

  void checkBlock(BlockStmt& b) {
    scopes_.emplace_back();
    for (auto& s : b.items) checkStmt(*s);
    scopes_.pop_back();
  }

  void checkStmt(Stmt& s) {
    switch (s.kind) {
      case Stmt::SBlock: checkBlock(static_cast<BlockStmt&>(s)); break;
      case Stmt::SVar: {
        auto& d = static_cast<VarStmt&>(s);
        if (declaredHere(d.name)) {
          err(d.loc.line, "redeclaration of '" + d.name + "' in the same scope");
        } else {
          if (d.init) {
            checkExpr(*d.init);
            if (d.init->type != d.type && d.init->type != Ty::Unknown)
              err(d.loc.line, std::string("cannot initialize '") +
                                  tyName(d.type) + "' variable '" + d.name +
                                  "' with a " + tyName(d.init->type) + " value");
          }
          scopes_.back()[d.name] = d.type;  // binding visible AFTER the init
        }
        break;
      }
      case Stmt::SAssign: {
        auto& a = static_cast<AssignStmt&>(s);
        checkExpr(*a.rhs);
        Ty* t = lookup(a.name);
        if (!t)
          err(a.loc.line, "assignment to undeclared '" + a.name + "'");
        else if (a.rhs->type != *t && a.rhs->type != Ty::Unknown)
          err(a.loc.line, std::string("cannot assign ") +
                              tyName(a.rhs->type) + " to '" + a.name +
                              "' of type " + tyName(*t));
        break;
      }
      case Stmt::SPrint: {
        auto& p = static_cast<PrintStmt&>(s);
        checkExpr(*p.e);  // print accepts int or bool
        if (p.e->type == Ty::Unknown)
          err(p.loc.line, "print expects an int or bool expression");
        break;
      }
      case Stmt::SReturn: {
        auto& r = static_cast<ReturnStmt&>(s);
        if (!r.e) {
          err(r.loc.line, "MiniC requires `return <expr>;` (no void functions)");
          break;
        }
        checkExpr(*r.e);
        if (r.e->type != curRet_ && r.e->type != Ty::Unknown)
          err(r.loc.line, std::string("returning ") + tyName(r.e->type) +
                              " from function declared " + tyName(curRet_));
        break;
      }
      case Stmt::SIf: {
        auto& i = static_cast<IfStmt&>(s);
        checkExpr(*i.cond);
        if (i.cond->type != Ty::Bool && i.cond->type != Ty::Unknown)
          err(i.loc.line, "if condition must be bool");
        checkStmt(*i.thenS);
        if (i.elseS) checkStmt(*i.elseS);
        break;
      }
      case Stmt::SWhile: {
        auto& w = static_cast<WhileStmt&>(s);
        checkExpr(*w.cond);
        if (w.cond->type != Ty::Bool && w.cond->type != Ty::Unknown)
          err(w.loc.line, "while condition must be bool");
        checkStmt(*w.body);
        break;
      }
      case Stmt::SExpr: {
        auto& e = static_cast<ExprStmt&>(s);
        checkExpr(*e.e);
        if (e.e->kind != Expr::ECall)
          err(e.loc.line, "only call expressions may stand as statements");
        break;
      }
    }
  }

  void checkExpr(Expr& e) {
    switch (e.kind) {
      case Expr::ENum: e.type = Ty::Int; break;
      case Expr::EBool: e.type = Ty::Bool; break;
      case Expr::EVar: {
        auto& v = static_cast<VarExpr&>(e);
        if (Ty* t = lookup(v.name)) v.type = *t;
        else { err(v.loc.line, "use of undeclared '" + v.name + "'"); v.type = Ty::Unknown; }
        break;
      }
      case Expr::EUnary: {
        auto& u = static_cast<UnaryExpr&>(e);
        checkExpr(*u.e);
        if (u.op == UnaryExpr::Neg) {
          if (u.e->type != Ty::Int && u.e->type != Ty::Unknown)
            err(u.loc.line, "'-' applies to int");
          u.type = Ty::Int;
        } else {
          if (u.e->type != Ty::Bool && u.e->type != Ty::Unknown)
            err(u.loc.line, "'!' applies to bool");
          u.type = Ty::Bool;
        }
        break;
      }
      case Expr::EBinary: {
        auto& b = static_cast<BinaryExpr&>(e);
        checkExpr(*b.lhs);
        checkExpr(*b.rhs);
        Ty L = b.lhs->type, R = b.rhs->type;
        bool known = (L != Ty::Unknown && R != Ty::Unknown);
        switch (b.op) {
          case BinaryExpr::Add: case BinaryExpr::Sub: case BinaryExpr::Mul:
          case BinaryExpr::Div: case BinaryExpr::Mod:
            if (known && (L != Ty::Int || R != Ty::Int))
              err(b.loc.line, std::string("'") + BinaryExpr::opName(b.op) +
                                  "' needs int operands");
            b.type = Ty::Int;
            break;
          case BinaryExpr::Lt: case BinaryExpr::Le:
          case BinaryExpr::Gt: case BinaryExpr::Ge:
            if (known && (L != Ty::Int || R != Ty::Int))
              err(b.loc.line, "ordering comparisons need int operands");
            b.type = Ty::Bool;
            break;
          case BinaryExpr::Eq: case BinaryExpr::Ne:
            if (known && L != R)
              err(b.loc.line, "'=='/'!=' needs operands of the same type");
            b.type = Ty::Bool;
            break;
          case BinaryExpr::And: case BinaryExpr::Or:
            if (known && (L != Ty::Bool || R != Ty::Bool))
              err(b.loc.line, "'&&'/'||' needs bool operands");
            b.type = Ty::Bool;
            break;
        }
        break;
      }
      case Expr::ECall: {
        auto& c = static_cast<CallExpr&>(e);
        auto it = funcs_.find(c.callee);
        if (it == funcs_.end()) {
          err(c.loc.line, "call to undefined function '" + c.callee + "'");
          for (auto& a : c.args) checkExpr(*a);
          c.type = Ty::Unknown;
          break;
        }
        if (c.args.size() != it->second.params.size()) {
          err(c.loc.line, "'" + c.callee + "' expects " +
                              std::to_string(it->second.params.size()) +
                              " argument(s), got " + std::to_string(c.args.size()));
        }
        for (size_t i = 0; i < c.args.size(); ++i) {
          checkExpr(*c.args[i]);
          if (i < it->second.params.size() &&
              c.args[i]->type != Ty::Unknown &&
              c.args[i]->type != it->second.params[i])
            err(c.loc.line, "argument " + std::to_string(i + 1) + " of '" +
                                c.callee + "' should be " +
                                tyName(it->second.params[i]));
        }
        c.type = it->second.ret;
        break;
      }
    }
  }

  std::unordered_map<std::string, FnSig> funcs_;
  std::vector<std::unordered_map<std::string, Ty>> scopes_;
  std::vector<std::string> errors_, warnings_;
  Ty curRet_ = Ty::Unknown;
  Func* curFn_ = nullptr;
};

}  // namespace minic
