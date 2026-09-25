#pragma once
// ============================================================================
// MiniC compiler core — stage L05-L08 material: the RECURSIVE DESCENT PARSER.
// Course mapping: CS143 L5/L6 (hand-written top-down parsing). MiniC's grammar
// (also printed by stage 02's main):
//
//   program := { func }
//   func    := type IDENT '(' [ type IDENT { ',' type IDENT } ] ')' block
//   type    := 'int' | 'bool'
//   block   := '{' { decl | stmt } '}'
//   decl    := type IDENT [ '=' expr ] ';'
//   stmt    := block
//            | 'if' '(' expr ')' stmt [ 'else' stmt ]
//            | 'while' '(' expr ')' stmt
//            | 'return' [ expr ] ';' | 'print' expr ';'
//            | IDENT '=' expr ';' | expr ';'
//   expr    := precedence climbing over
//            || (1)  && (2)  < <= > >= == != (3)  + - (4)  * / % (5)
//            prefix: ! -  ; primary: NUM true false IDENT call (expr)
//
// Why recursion works without eliminating left recursion: binary chains are
// parsed as *loops* inside one procedure (the classic rewrite of
//   E -> E + T | T   into   p = T; while '+' { q = T; p = E+E }
// — see notes/L06 "实战绕过 LL(1) 限制"). Error strategy: panic mode with
// statement-level sync sets, exactly as advocated in L6/L8.
// ============================================================================
#include <string>
#include <vector>
#include <memory>

#include "ast.h"
#include "lexer.h"

namespace minic {

class Parser {
 public:
  explicit Parser(std::vector<Token> toks) : toks_(std::move(toks)) {
    if (toks_.empty() || toks_.back().kind != Tok::Eof)
      toks_.push_back({Tok::Eof, "<eof>", 0, 1, 1});
  }

  const std::vector<std::string>& errors() const { return errors_; }

  std::unique_ptr<Program> parseProgram() {
    auto p = std::make_unique<Program>();
    while (!check(Tok::Eof)) {
      if (!check(Tok::IntKw) && !check(Tok::BoolKw)) {
        error("expected 'int' or 'bool' to start a function definition");
        advance();                       // simple program-level recovery
        continue;
      }
      auto f = parseFunc();
      if (f) p->funcs.push_back(std::move(f));
    }
    return p;
  }

 private:
  // ---------------- token helpers ----------------
  const Token& peek(size_t k = 0) const {
    size_t i = idx_ + k;
    return i < toks_.size() ? toks_[i] : toks_.back();
  }
  bool check(Tok t, size_t k = 0) const { return peek(k).kind == t; }
  const Token& advance() {
    const Token& t = peek();
    if (idx_ + 1 < toks_.size()) ++idx_;
    return t;
  }
  bool accept(Tok t) {
    if (check(t)) { advance(); return true; }
    return false;
  }
  const Token& expect(Tok t, const char* what) {
    if (check(t)) return advance();
    error(std::string("expected ") + what + " but found '" + peek().text + "'");
    throw Loc{};                          // caller-level recovery below
  }
  void error(const std::string& msg) {
    errors_.push_back("line " + std::to_string(peek().line) + ", col " +
                      std::to_string(peek().col) + ": " + msg);
  }

  // Panic mode (L6): drop tokens until a plausible statement start or '}'.
  void skipToSync() {
    for (;;) {
      if (check(Tok::Eof) || check(Tok::RBrace)) return;
      switch (peek().kind) {
        case Tok::Semi: advance(); return;      // consume the ';' we reached
        case Tok::IfKw: case Tok::WhileKw: case Tok::ReturnKw:
        case Tok::PrintKw: case Tok::IntKw: case Tok::BoolKw:
        case Tok::LBrace:
          return;
        default: advance();
      }
    }
  }

  // ---------------- declarations ----------------
  Ty parseType() {
    if (accept(Tok::IntKw)) return Ty::Int;
    expect(Tok::BoolKw, "'bool'");
    return Ty::Bool;
  }

  std::unique_ptr<Func> parseFunc() {
    auto f = std::make_unique<Func>();
    f->loc.line = peek().line; f->loc.col = peek().col;
    try {
      f->ret = parseType();
      f->name = expect(Tok::Ident, "function name").text;
      expect(Tok::LParen, "'('");
      if (!check(Tok::RParen)) {
        do {
          Param p;
          p.type = parseType();
          p.name = expect(Tok::Ident, "parameter name").text;
          f->params.push_back(std::move(p));
        } while (accept(Tok::Comma));
      }
      expect(Tok::RParen, "')'");
      f->body = parseBlock();
    } catch (const Loc&) {
      // resume at the next top-level type keyword
      while (!check(Tok::Eof) && !check(Tok::IntKw) && !check(Tok::BoolKw))
        advance();
      return nullptr;
    }
    return f;
  }

  // ---------------- statements ----------------
  std::unique_ptr<BlockStmt> parseBlock() {
    auto b = std::make_unique<BlockStmt>();
    expect(Tok::LBrace, "'{'");
    while (!check(Tok::RBrace) && !check(Tok::Eof)) {
      auto s = parseDeclOrStmt();
      if (s) b->items.push_back(std::move(s));
    }
    expect(Tok::RBrace, "'}'");
    return b;
  }

  std::unique_ptr<Stmt> parseBlockAsStmt() { return parseBlock(); }

  std::unique_ptr<Stmt> parseDeclOrStmt() {
    try {
      switch (peek().kind) {
        case Tok::IntKw: case Tok::BoolKw: return parseVarDecl();
        case Tok::LBrace:   return parseBlockAsStmt();
        case Tok::IfKw:     return parseIf();
        case Tok::WhileKw:  return parseWhile();
        case Tok::ReturnKw: return parseReturn();
        case Tok::PrintKw:  return parsePrint();
        default: break;
      }
      // IDENT '=' expr  →  assignment (2-token lookahead, still "LL-ish")
      if (check(Tok::Ident) && check(Tok::Assign, 1)) {
        auto a = std::make_unique<AssignStmt>();
        a->loc.line = peek().line;
        a->name = advance().text;
        advance();                       // '='
        a->rhs = parseExpr();
        expect(Tok::Semi, "';'");
        return a;
      }
      auto s = std::make_unique<ExprStmt>();
      s->loc.line = peek().line;
      s->e = parseExpr();
      expect(Tok::Semi, "';'");
      return s;
    } catch (const Loc&) {
      skipToSync();
      return nullptr;
    }
  }

  std::unique_ptr<Stmt> parseVarDecl() {
    auto d = std::make_unique<VarStmt>();
    d->loc.line = peek().line;
    d->type = parseType();
    d->name = expect(Tok::Ident, "variable name").text;
    if (accept(Tok::Assign)) d->init = parseExpr();
    expect(Tok::Semi, "';'");
    return d;
  }

  std::unique_ptr<Stmt> parseIf() {
    auto s = std::make_unique<IfStmt>();
    s->loc.line = peek().line;
    advance();                           // 'if'
    expect(Tok::LParen, "'('");
    s->cond = parseExpr();
    expect(Tok::RParen, "')'");
    s->thenS = parseDeclOrStmt();
    if (accept(Tok::ElseKw)) s->elseS = parseDeclOrStmt();
    return s;
  }

  std::unique_ptr<Stmt> parseWhile() {
    auto s = std::make_unique<WhileStmt>();
    s->loc.line = peek().line;
    advance();                           // 'while'
    expect(Tok::LParen, "'('");
    s->cond = parseExpr();
    expect(Tok::RParen, "')'");
    s->body = parseDeclOrStmt();
    return s;
  }

  std::unique_ptr<Stmt> parseReturn() {
    auto s = std::make_unique<ReturnStmt>();
    s->loc.line = peek().line;
    advance();                           // 'return'
    if (!check(Tok::Semi)) s->e = parseExpr();
    expect(Tok::Semi, "';'");
    return s;
  }

  std::unique_ptr<Stmt> parsePrint() {
    auto s = std::make_unique<PrintStmt>();
    s->loc.line = peek().line;
    advance();                           // 'print'
    s->e = parseExpr();
    expect(Tok::Semi, "';'");
    return s;
  }

  // ---------------- expressions: precedence climbing (Pratt, L6) ----------
  static int binaryPrec(Tok t) {
    switch (t) {
      case Tok::PipePipe: return 1;
      case Tok::AmpAmp:   return 2;
      case Tok::Lt: case Tok::Le: case Tok::Gt: case Tok::Ge:
      case Tok::EqEq: case Tok::NotEq: return 3;
      case Tok::Plus: case Tok::Minus: return 4;
      case Tok::Star: case Tok::Slash: case Tok::Percent: return 5;
      default: return 0;
    }
  }
  static BinaryExpr::Op mapOp(Tok t) {
    switch (t) {
      case Tok::Plus: return BinaryExpr::Add;   case Tok::Minus: return BinaryExpr::Sub;
      case Tok::Star: return BinaryExpr::Mul;   case Tok::Slash: return BinaryExpr::Div;
      case Tok::Percent: return BinaryExpr::Mod;
      case Tok::Lt: return BinaryExpr::Lt;      case Tok::Le: return BinaryExpr::Le;
      case Tok::Gt: return BinaryExpr::Gt;      case Tok::Ge: return BinaryExpr::Ge;
      case Tok::EqEq: return BinaryExpr::Eq;    case Tok::NotEq: return BinaryExpr::Ne;
      case Tok::AmpAmp: return BinaryExpr::And; default: return BinaryExpr::Or;
    }
  }

  std::unique_ptr<Expr> parseExpr(int minPrec = 0) {
    auto lhs = parseUnary();
    for (;;) {
      Tok t = peek().kind;
      int p = binaryPrec(t);
      if (p == 0 || p < minPrec) return lhs;   // left-associative: p < minPrec
      advance();
      auto rhs = parseExpr(p + 1);
      auto b = std::make_unique<BinaryExpr>(mapOp(t));
      b->loc = lhs->loc;
      b->lhs = std::move(lhs);
      b->rhs = std::move(rhs);
      lhs = std::move(b);
    }
  }

  std::unique_ptr<Expr> parseUnary() {
    if (check(Tok::Bang) || check(Tok::Minus)) {
      auto u = std::make_unique<UnaryExpr>(check(Tok::Bang) ? UnaryExpr::LNot
                                                            : UnaryExpr::Neg);
      u->loc.line = peek().line;
      advance();
      u->e = parseUnary();
      return u;
    }
    return parsePrimary();
  }

  std::unique_ptr<Expr> parsePrimary() {
    const Token& t = peek();
    switch (t.kind) {
      case Tok::Num: {
        advance();
        auto n = std::make_unique<NumExpr>(t.value);
        n->loc = t.loc;
        return n;
      }
      case Tok::TrueKw: case Tok::FalseKw: {
        bool v = (t.kind == Tok::TrueKw);
        advance();
        auto b = std::make_unique<BoolExpr>(v);
        b->loc = t.loc;
        return b;
      }
      case Tok::Ident: {
        advance();
        if (!check(Tok::LParen)) {
          auto v = std::make_unique<VarExpr>(t.text);
          v->loc = t.loc;
          return v;
        }
        auto c = std::make_unique<CallExpr>();
        c->loc = t.loc;
        c->callee = t.text;
        advance();                       // '('
        if (!check(Tok::RParen)) {
          do {
            c->args.push_back(parseExpr());
          } while (accept(Tok::Comma));
        }
        expect(Tok::RParen, "')'");
        return c;
      }
      case Tok::LParen: {
        advance();
        auto e = parseExpr();
        expect(Tok::RParen, "')'");
        return e;
      }
      default:
        error("unexpected token '" + t.text + "' in expression");
        throw Loc{};
    }
  }
};

}  // namespace minic
