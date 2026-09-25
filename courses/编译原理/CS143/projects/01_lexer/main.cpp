// ============================================================================
// MiniC stage 01 — LEXER driver. Course mapping: notes/L03, notes/L04.
// Build: ./build.sh (g++) or build.bat (cl) from THIS directory.
// Usage: ./minic01 [source.minic]        (default: ../samples/hello.minic)
// ============================================================================
#include <fstream>
#include <iostream>
#include <sstream>

#include "../common/lexer.h"

int main(int argc, char** argv) {
  std::string path = (argc > 1) ? argv[1] : "../samples/hello.minic";
  std::ifstream in(path);
  if (!in) {
    std::cerr << "cannot open " << path << "\n";
    return 2;
  }
  std::stringstream buf;
  buf << in.rdbuf();

  try {
    minic::Lexer lexer(buf.str());
    std::vector<minic::Token> toks = lexer.tokenize();
    std::cout << "=== tokens: " << toks.size() << " ===\n";
    for (const auto& t : toks) {
      std::cout << t.line << ":" << t.col << "  " << minic::tokName(t.kind);
      if (t.kind == minic::Tok::Ident || t.kind == minic::Tok::Num)
        std::cout << "  lexeme='" << t.text << "'";
      if (t.kind == minic::Tok::Num)
        std::cout << "  value=" << t.value;
      std::cout << "\n";
    }
    std::cout << "=== done ===\n";
  } catch (const minic::LexerError& e) {
    std::cerr << "lexical error: " << e.what() << "\n";
    return 1;
  }
  return 0;
}
