// ============================================================================
// MiniC stage 03 — SEMANTIC ANALYSIS driver (symbol table + static type check).
// Course mapping: notes/L10 (PA3 equivalent for MiniC).
// The checking logic itself lives in ../common/checker.h (the stage's "new
// material"); this driver only wires lexer/parser/checker and reports.
// Build: ./build.sh or build.bat. Usage: ./minic03 [file.minic]
// ============================================================================
#include <fstream>
#include <iostream>
#include <sstream>

#include "../common/lexer.h"
#include "../common/ast.h"
#include "../common/parser.h"
#include "../common/checker.h"

using namespace minic;

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
    for (const auto& m : parser.errors()) std::cout << "  " << m << "\n";
    std::cout << "note: semantic analysis needs a syntactically valid AST\n";
    return 1;
  }

  Checker checker;
  bool ok = checker.checkProgram(*prog);
  std::cout << "=== semantic check: " << (ok ? "PASS" : "FAIL") << " ===\n";
  for (const auto& w : checker.warnings()) std::cout << "  " << w << "\n";
  if (!ok) {
    std::cout << "=== type errors (" << checker.errors().size() << ") ===\n";
    for (const auto& e : checker.errors()) std::cout << "  " << e << "\n";
  } else {
    // Show the synthesized "attribute" of every function's body statements
    // is enough: print the signature table, the checker's real product.
    std::cout << "  program is well-typed; " << prog->funcs.size()
              << " function(s) accepted\n";
  }
  return ok ? 0 : 1;
}
