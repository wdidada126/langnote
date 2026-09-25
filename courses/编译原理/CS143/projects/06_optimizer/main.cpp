// ============================================================================
// MiniC stage 06 — driver: compile, optimize, and DIFFERENTIAL-TEST the
// optimizer (run before/after on the stage-05 VM; outputs must match).
// Build: ./build.sh or build.bat. Usage: ./minic06 [file.minic]
// ============================================================================
#include <fstream>
#include <iostream>
#include <sstream>

#include "../common/lexer.h"
#include "../common/ast.h"
#include "../common/parser.h"
#include "../common/checker.h"
#include "../04_ir/icode.h"
#include "../05_backend/interp.h"
#include "opt.h"

using namespace minic;

static size_t countInstrs(const std::vector<IRFunc>& prog) {
  size_t n = 0;
  for (const auto& f : prog) n += f.code.size();
  return n;
}

static bool runTo(std::vector<IRFunc>& prog, std::string& outText,
                  std::string& errText) {
  try {
    std::stringstream sink;
    Machine vm(prog, sink);
    vm.run("main");
    outText = sink.str();
    return true;
  } catch (const std::exception& e) {
    errText = e.what();
    return false;
  }
}

int main(int argc, char** argv) {
  std::string path = (argc > 1) ? argv[1] : "../samples/dead.minic";
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

  std::vector<IRFunc> before = ir;
  std::cout << "=== IR BEFORE (" << countInstrs(before) << " instrs) ===\n";
  dumpIR(std::cout, before);

  std::string outA, errA, outB, errB;
  bool okA = runTo(before, outA, errA);

  Optimizer optimizer;
  bool changed = optimizer.optimize(ir);
  std::cout << "=== IR AFTER (" << countInstrs(ir) << " instrs, "
            << (changed ? "changed" : "unchanged") << ") ===\n";
  dumpIR(std::cout, ir);

  bool okB = runTo(ir, outB, errB);

  std::cout << "=== program output (before) ===\n" << outA;
  if (!okA) std::cout << "(runtime error: " << errA << ")\n";
  std::cout << "=== program output (after) ===\n" << outB;
  if (!okB) std::cout << "(runtime error: " << errB << ")\n";

  std::cout << "=== differential check ===\n";
  if (okA && okB && outA == outB) {
    std::cout << "PASS: optimizer preserved observable behavior\n";
    return 0;
  }
  std::cout << "FAIL: outputs diverge — the optimizer broke a semantics "
               "contract\n";
  return 1;
}
