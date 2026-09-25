// ============================================================================
// MiniC stage 05 — driver: compile the whole pipeline, then EXECUTE on the
// three-address virtual machine (and optionally dump the IR with -S).
// Build: ./build.sh or build.bat. Usage:
//   ./minic05 [-S] [file.minic]        (default: ../samples/hello.minic)
// ============================================================================
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

#include "../common/lexer.h"
#include "../common/ast.h"
#include "../common/parser.h"
#include "../common/checker.h"
#include "../04_ir/icode.h"
#include "interp.h"

using namespace minic;

int main(int argc, char** argv) {
  bool showIR = false;
  std::string path = "../samples/hello.minic";
  for (int i = 1; i < argc; ++i) {
    std::string a = argv[i];
    if (a == "-S") showIR = true;
    else path = a;
  }

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
    for (const auto& m : parser.errors()) std::cout << m << "\n";
    return 1;
  }
  Checker checker;
  if (!checker.checkProgram(*prog)) {
    for (const auto& e : checker.errors()) std::cout << e << "\n";
    return 1;
  }

  std::vector<IRFunc> ir;
  try {
    ir = IRGen().generate(*prog);
  } catch (const std::runtime_error& e) {
    std::cerr << e.what() << "\n";
    return 1;
  }
  if (showIR) dumpIR(std::cout, ir);

  try {
    std::cout << "=== program output ===\n";
    Machine vm(ir);
    long long rc = vm.run("main");
    std::cout << "=== main returned " << rc << " ===\n";
    (void)rc;                                  // rc is demo data, not exit status
    return 0;
  } catch (const std::runtime_error& e) {
    std::cerr << "runtime error: " << e.what() << "\n";
    return 1;
  }
}
