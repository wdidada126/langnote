// ============================================================================
// MiniC stage 04 — driver: source -> tokens -> AST -> (check) -> three-address IR.
// Course mapping: notes/L12, notes/L13 (PA4 equivalent: "AST -> IR").
// Build: ./build.sh or build.bat. Usage: ./minic04 [file.minic]
// ============================================================================
#include <fstream>
#include <iostream>
#include <sstream>

#include "../common/lexer.h"
#include "../common/ast.h"
#include "../common/parser.h"
#include "../common/checker.h"
#include "icode.h"

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
    return 1;
  }

  Checker checker;
  if (!checker.checkProgram(*prog)) {
    std::cout << "=== type errors (" << checker.errors().size() << ") ===\n";
    for (const auto& e : checker.errors()) std::cout << "  " << e << "\n";
    return 1;
  }
  for (const auto& w : checker.warnings()) std::cout << "  " << w << "\n";

  try {
    IRGen gen;
    std::vector<IRFunc> ir = gen.generate(*prog);
    std::cout << "=== three-address IR ===\n";
    dumpIR(std::cout, ir);
  } catch (const std::runtime_error& e) {
    std::cerr << "IRGen failure: " << e.what() << "\n";
    return 1;
  }
  return 0;
}
