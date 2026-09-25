// ============================================================================
// MiniC stage 02 — RECURSIVE DESCENT PARSER driver + AST pretty printer.
// Course mapping: notes/L05, notes/L06 (top-down parsing), notes/L08 (why
// CS143's official PA2 instead uses bison/LALR — see stage README).
// Build: ./build.sh or build.bat from THIS directory.
// Usage: ./minic02 [source.minic]   (default: ../samples/hello.minic)
// ============================================================================
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

#include "../common/lexer.h"
#include "../common/ast.h"
#include "../common/parser.h"

using namespace minic;

static void pad(int n) { std::cout << std::string(2 * n, ' '); }
static void dumpStmt(const Stmt& s, int ind);

// Recursive expression printer: one node per line, children indented.
static void dumpExprChild(const Expr* e, int ind) {
  if (!e) { pad(ind); std::cout << "<none>\n"; return; }
  pad(ind);
  switch (e->kind) {
    case Expr::ENum:
      std::cout << "num " << static_cast<const NumExpr*>(e)->v << "\n"; break;
    case Expr::EBool:
      std::cout << "bool " << (static_cast<const BoolExpr*>(e)->v ? "true" : "false") << "\n"; break;
    case Expr::EVar:
      std::cout << "var '" << static_cast<const VarExpr*>(e)->name << "'\n"; break;
    case Expr::EUnary:
      std::cout << (static_cast<const UnaryExpr*>(e)->op == UnaryExpr::Neg ? "unary '-'\n"
                                                                          : "unary '!'\n");
      dumpExprChild(static_cast<const UnaryExpr*>(e)->e.get(), ind + 1);
      break;
    case Expr::EBinary:
      std::cout << "binary '" << BinaryExpr::opName(static_cast<const BinaryExpr*>(e)->op) << "'\n";
      dumpExprChild(static_cast<const BinaryExpr*>(e)->lhs.get(), ind + 1);
      dumpExprChild(static_cast<const BinaryExpr*>(e)->rhs.get(), ind + 1);
      break;
    case Expr::ECall:
      std::cout << "call " << static_cast<const CallExpr*>(e)->callee
                << "(" << static_cast<const CallExpr*>(e)->args.size() << " args)\n";
      for (const auto& a : static_cast<const CallExpr*>(e)->args)
        dumpExprChild(a.get(), ind + 1);
      break;
  }
}

static void dumpBlock(const BlockStmt& b, int ind) {
  for (const auto& item : b.items) dumpStmt(*item, ind + 1);
}

static void dumpStmt(const Stmt& s, int ind) {
  pad(ind);
  switch (s.kind) {
    case Stmt::SExpr:
      std::cout << "expr-stmt\n";
      dumpExprChild(static_cast<const ExprStmt&>(s).e.get(), ind + 1);
      break;
    case Stmt::SAssign: {
      const auto& a = static_cast<const AssignStmt&>(s);
      std::cout << "assign " << a.name << " =\n";
      dumpExprChild(a.rhs.get(), ind + 1);
      break;
    }
    case Stmt::SVar: {
      const auto& d = static_cast<const VarStmt&>(s);
      std::cout << "decl " << tyName(d.type) << " " << d.name;
      if (!d.init) { std::cout << " (no init)\n"; break; }
      std::cout << " =\n";
      dumpExprChild(d.init.get(), ind + 1);
      break;
    }
    case Stmt::SPrint:
      std::cout << "print\n";
      dumpExprChild(static_cast<const PrintStmt&>(s).e.get(), ind + 1);
      break;
    case Stmt::SReturn: {
      const auto& r = static_cast<const ReturnStmt&>(s);
      std::cout << "return\n";
      dumpExprChild(r.e.get(), ind + 1);
      break;
    }
    case Stmt::SIf: {
      const auto& i = static_cast<const IfStmt&>(s);
      std::cout << "if\n";
      pad(ind + 1); std::cout << "cond\n"; dumpExprChild(i.cond.get(), ind + 1);
      pad(ind + 1); std::cout << "then\n"; dumpStmt(*i.thenS, ind + 2);
      if (i.elseS) { pad(ind + 1); std::cout << "else\n"; dumpStmt(*i.elseS, ind + 2); }
      break;
    }
    case Stmt::SWhile: {
      const auto& w = static_cast<const WhileStmt&>(s);
      std::cout << "while\n";
      pad(ind + 1); std::cout << "cond\n"; dumpExprChild(w.cond.get(), ind + 1);
      pad(ind + 1); std::cout << "body\n"; dumpStmt(*w.body, ind + 2);
      break;
    }
    case Stmt::SBlock:
      std::cout << "block\n";
      dumpBlock(static_cast<const BlockStmt&>(s), ind);
      break;
  }
}

int main(int argc, char** argv) {
  std::string path = (argc > 1) ? argv[1] : "../samples/hello.minic";
  std::ifstream in(path);
  if (!in) { std::cerr << "cannot open " << path << "\n"; return 2; }
  std::stringstream buf;
  buf << in.rdbuf();

  std::vector<Token> toks;
  try {
    toks = Lexer(buf.str()).tokenize();
  } catch (const LexerError& e) {
    std::cerr << "lexical error: " << e.what() << "\n";
    return 1;
  }

  Parser parser(toks);
  std::unique_ptr<Program> prog = parser.parseProgram();

  if (!parser.errors().empty()) {
    std::cout << "=== parse errors (" << parser.errors().size() << ") ===\n";
    for (const auto& msg : parser.errors()) std::cout << "  " << msg << "\n";
    std::cout << "note: this stage refuses to dump a partially-parsed tree\n";
    return 1;
  }

  std::cout << "=== AST ===\n";
  for (const auto& f : prog->funcs) {
    std::string ps;
    for (size_t i = 0; i < f->params.size(); ++i) {
      if (i) ps += ", ";
      ps += std::string(tyName(f->params[i].type)) + " " + f->params[i].name;
    }
    pad(0);
    std::cout << "func " << tyName(f->ret) << " " << f->name << "(" << ps << ")\n";
    dumpBlock(*f->body, 0);
  }
  if (prog->funcs.empty()) std::cout << "  <empty program>\n";
  return parser.errors().empty() ? 0 : 1;
}
