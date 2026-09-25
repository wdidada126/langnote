#pragma once
// ============================================================================
// MiniC compiler core — stage L05-L08 material: the AST (parse trees).
// Course mapping: CS143 L5 (CFGs & parse trees), L9 (attributes live here too:
// Expr::type is an *attribute slot* filled by the stage-03 checker and read
// by the stage-04 IR generator — a miniature of synthesized attributes).
// Convention: every node owns its children through std::unique_ptr; the tree
// is a strict hierarchy (exactly one owner), mirroring the parse trees of
// L5. Visitors = the virtual-free approach: switch on `kind` (like COOL's
// visitor pattern, minus the pattern).
// ============================================================================
#include <memory>
#include <string>
#include <vector>

namespace minic {

enum class Ty { Int, Bool, Unknown };
inline const char* tyName(Ty t) {
  return t == Ty::Int ? "int" : t == Ty::Bool ? "bool" : "?";
}

struct Loc { int line = 0; int col = 0; };

// ---------------- expressions ----------------------------------------------
struct Expr {
  enum Kind { ENum, EBool, EVar, ECall, EBinary, EUnary };
  Kind kind;
  Loc loc;
  Ty type = Ty::Unknown;   // filled by the semantic checker (stage 03)
  virtual ~Expr() = default;
 protected:
  explicit Expr(Kind k) : kind(k) {}
};

struct NumExpr : Expr {
  long long v;
  explicit NumExpr(long long x) : Expr(ENum), v(x) { type = Ty::Int; }
};

struct BoolExpr : Expr {
  bool v;
  explicit BoolExpr(bool x) : Expr(EBool), v(x) { type = Ty::Bool; }
};

struct VarExpr : Expr {
  std::string name;
  explicit VarExpr(std::string n) : Expr(EVar), name(std::move(n)) {}
};

struct CallExpr : Expr {
  std::string callee;
  std::vector<std::unique_ptr<Expr>> args;
  CallExpr() : Expr(ECall) {}
};

struct BinaryExpr : Expr {
  enum Op { Add, Sub, Mul, Div, Mod, Lt, Le, Gt, Ge, Eq, Ne, And, Or };
  Op op;
  std::unique_ptr<Expr> lhs, rhs;
  explicit BinaryExpr(Op o) : Expr(EBinary), op(o) {}
  static const char* opName(Op x) {
    switch (x) {
      case Add: return "+"; case Sub: return "-"; case Mul: return "*";
      case Div: return "/"; case Mod: return "%"; case Lt: return "<";
      case Le: return "<="; case Gt: return ">";  case Ge: return ">=";
      case Eq: return "=="; case Ne: return "!="; case And: return "&&";
      case Or: return "||";
    }
    return "?";
  }
};

struct UnaryExpr : Expr {
  enum Op { Neg, LNot };
  Op op;
  std::unique_ptr<Expr> e;
  explicit UnaryExpr(Op o) : Expr(EUnary), op(o) {}
};

// ---------------- statements -----------------------------------------------
struct Stmt {
  enum Kind { SExpr, SAssign, SVar, SPrint, SReturn, SIf, SWhile, SBlock };
  Kind kind;
  Loc loc;
  virtual ~Stmt() = default;
 protected:
  explicit Stmt(Kind k) : kind(k) {}
};

struct ExprStmt : Stmt {
  std::unique_ptr<Expr> e;
  ExprStmt() : Stmt(SExpr) {}
};

struct AssignStmt : Stmt {
  std::string name;
  std::unique_ptr<Expr> rhs;
  AssignStmt() : Stmt(SAssign) {}
};

struct VarStmt : Stmt {
  Ty type = Ty::Int;
  std::string name;
  std::unique_ptr<Expr> init;   // null when written as `int x;`
  VarStmt() : Stmt(SVar) {}
};

struct PrintStmt : Stmt {
  std::unique_ptr<Expr> e;
  PrintStmt() : Stmt(SPrint) {}
};

struct ReturnStmt : Stmt {
  std::unique_ptr<Expr> e;      // null for bare `return;` (accepted, checked)
  ReturnStmt() : Stmt(SReturn) {}
};

struct IfStmt : Stmt {
  std::unique_ptr<Expr> cond;
  std::unique_ptr<Stmt> thenS, elseS;   // elseS null when absent
  IfStmt() : Stmt(SIf) {}
};

struct WhileStmt : Stmt {
  std::unique_ptr<Expr> cond;
  std::unique_ptr<Stmt> body;
  WhileStmt() : Stmt(SWhile) {}
};

struct BlockStmt : Stmt {
  std::vector<std::unique_ptr<Stmt>> items;
  BlockStmt() : Stmt(SBlock) {}
};

// ---------------- declarations ---------------------------------------------
struct Param {
  Ty type = Ty::Int;
  std::string name;
};

struct Func {
  Ty ret = Ty::Int;
  std::string name;
  std::vector<Param> params;
  std::unique_ptr<BlockStmt> body;
  Loc loc;
};

struct Program {
  std::vector<std::unique_ptr<Func>> funcs;
};

}  // namespace minic
