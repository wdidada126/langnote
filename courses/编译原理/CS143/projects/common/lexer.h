#pragma once
// ============================================================================
// MiniC compiler core — stage L03/L04 material: the LEXER (hand-written DFA).
// Course mapping: CS143 L3 (regular languages / DFA) & L4 (FA implementation).
// Design notes:
//   * One token class per state-machine family; keywords are recognized by
//     running the IDENT automaton first and then consulting a keyword table
//     (guarantees maximal munch: "intx" is IDENT, never "int" + "x").
//   * Two-character operators use one-char lookahead (peek), the classic
//     "longest match with putback" technique from the Dragon book ch3.
//   * Nested block comments need a counter; strictly speaking unbounded
//     nesting is beyond regular languages (see notes/L03) — we accept the
//     counter as a pragmatic "automaton with one register" and stop there.
// ============================================================================
#include <cctype>
#include <cstdint>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace minic {

enum class Tok {
  IntKw, BoolKw, IfKw, ElseKw, WhileKw, ReturnKw, PrintKw, TrueKw, FalseKw,
  Ident, Num,
  Plus, Minus, Star, Slash, Percent,
  Lt, Le, Gt, Ge, EqEq, NotEq, AmpAmp, PipePipe, Bang, Assign,
  LParen, RParen, LBrace, RBrace, Semi, Comma,
  Eof
};

inline const char* tokName(Tok t) {
  switch (t) {
    case Tok::IntKw: return "int";         case Tok::BoolKw: return "bool";
    case Tok::IfKw: return "if";           case Tok::ElseKw: return "else";
    case Tok::WhileKw: return "while";     case Tok::ReturnKw: return "return";
    case Tok::PrintKw: return "print";     case Tok::TrueKw: return "true";
    case Tok::FalseKw: return "false";
    case Tok::Ident: return "IDENT";       case Tok::Num: return "NUM";
    case Tok::Plus: return "'+'";          case Tok::Minus: return "'-'";
    case Tok::Star: return "'*'";          case Tok::Slash: return "'/'";
    case Tok::Percent: return "'%'";
    case Tok::Lt: return "'<'";            case Tok::Le: return "'<='";
    case Tok::Gt: return "'>'";            case Tok::Ge: return "'>='";
    case Tok::EqEq: return "'=='";         case Tok::NotEq: return "'!='";
    case Tok::AmpAmp: return "'&&'";       case Tok::PipePipe: return "'||'";
    case Tok::Bang: return "'!'";          case Tok::Assign: return "'='";
    case Tok::LParen: return "'('";        case Tok::RParen: return "')'";
    case Tok::LBrace: return "'{'";        case Tok::RBrace: return "'}'";
    case Tok::Semi: return "';'";          case Tok::Comma: return "','";
    case Tok::Eof: return "<eof>";
  }
  return "?";
}

struct Token {
  Tok kind = Tok::Eof;
  std::string text;      // lexeme: identifier name / keyword / operator spelling
  long long value = 0;   // payload for NUM literals
  int line = 1;
  int col = 1;
};

class LexerError : public std::runtime_error {
 public:
  explicit LexerError(const std::string& msg) : std::runtime_error(msg) {}
};

class Lexer {
 public:
  explicit Lexer(std::string src) : src_(std::move(src)) {}

  // Tokenize the whole input; the result always ends with one Eof token.
  std::vector<Token> tokenize() {
    std::vector<Token> out;
    for (;;) {
      Token t = next();
      bool done = (t.kind == Tok::Eof);
      out.push_back(t);
      if (done) break;
    }
    return out;
  }

  Token next() {
    skipTrivia();
    int line = line_;
    int col = static_cast<int>(pos_ - lineStart_) + 1;
    if (eof()) return {Tok::Eof, "<eof>", 0, line, col};
    char c = src_[pos_];
    if (std::isalpha(static_cast<unsigned char>(c)) || c == '_')
      return readIdent(line, col);
    if (std::isdigit(static_cast<unsigned char>(c)))
      return readNumber(line, col);
    return readPunct(line, col);
  }

 private:
  static Tok kindFromIdent(const std::string& s) {
    static const std::unordered_map<std::string, Tok> kw = {
        {"int", Tok::IntKw},     {"bool", Tok::BoolKw},  {"if", Tok::IfKw},
        {"else", Tok::ElseKw},   {"while", Tok::WhileKw},{"return", Tok::ReturnKw},
        {"print", Tok::PrintKw}, {"true", Tok::TrueKw},  {"false", Tok::FalseKw},
    };
    auto it = kw.find(s);
    return it == kw.end() ? Tok::Ident : it->second;
  }

  bool eof() const { return pos_ >= src_.size(); }
  char cur() const { return src_[pos_]; }
  char peek(size_t k = 1) const {
    return pos_ + k < src_.size() ? src_[pos_ + k] : '\0';
  }
  void advance() {
    if (src_[pos_] == '\n') { ++line_; lineStart_ = pos_ + 1; }
    ++pos_;
  }

  void skipTrivia() {
    for (;;) {
      while (!eof() && std::isspace(static_cast<unsigned char>(cur()))) advance();
      if (!eof() && cur() == '/' && peek() == '/') {         // // line comment
        while (!eof() && cur() != '\n') advance();
        continue;
      }
      if (!eof() && cur() == '/' && peek() == '*') {         // /* nesting ok */
        advance(); advance();
        int depth = 1;
        while (!eof() && depth > 0) {
          if (cur() == '/' && peek() == '*') { advance(); advance(); ++depth; }
          else if (cur() == '*' && peek() == '/') { advance(); advance(); --depth; }
          else advance();
        }
        if (depth > 0)
          throw LexerError("line " + std::to_string(line_) + ": unterminated block comment");
        continue;
      }
      return;
    }
  }

  Token readIdent(int line, int col) {
    size_t start = pos_;
    while (!eof() && (std::isalnum(static_cast<unsigned char>(cur())) || cur() == '_'))
      advance();
    std::string name = src_.substr(start, pos_ - start);
    return {kindFromIdent(name), name, 0, line, col};
  }

  Token readNumber(int line, int col) {
    size_t start = pos_;
    long long v = 0;
    while (!eof() && std::isdigit(static_cast<unsigned char>(cur()))) {
      v = v * 10 + (src_[pos_] - '0');
      advance();
    }
    if (!eof() && cur() == '.' && std::isdigit(static_cast<unsigned char>(peek())))
      throw LexerError("line " + std::to_string(line) + ": floats are not part of MiniC");
    return {Tok::Num, src_.substr(start, pos_ - start), v, line, col};
  }

  Token readPunct(int line, int col) {
    char c = src_, n = peek();
    // Longest-match first: try all two-character operators, then one.
    if (c == '&' && n == '&') { advance(); advance(); return {Tok::AmpAmp, "&&", 0, line, col}; }
    if (c == '|' && n == '|') { advance(); advance(); return {Tok::PipePipe, "||", 0, line, col}; }
    if (c == '=' && n == '=') { advance(); advance(); return {Tok::EqEq, "==", 0, line, col}; }
    if (c == '!' && n == '=') { advance(); advance(); return {Tok::NotEq, "!=", 0, line, col}; }
    if (c == '<' && n == '=') { advance(); advance(); return {Tok::Le, "<=", 0, line, col}; }
    if (c == '>' && n == '=') { advance(); advance(); return {Tok::Ge, ">=", 0, line, col}; }
    Tok one = Tok::Eof;
    switch (c) {
      case '+': one = Tok::Plus; break;
      case '-': one = Tok::Minus; break;
      case '*': one = Tok::Star; break;
      case '/': one = Tok::Slash; break;
      case '%': one = Tok::Percent; break;
      case '<': one = Tok::Lt; break;
      case '>': one = Tok::Gt; break;
      case '!': one = Tok::Bang; break;
      case '=': one = Tok::Assign; break;
      case '(': one = Tok::LParen; break;
      case ')': one = Tok::RParen; break;
      case '{': one = Tok::LBrace; break;
      case '}': one = Tok::RBrace; break;
      case ';': one = Tok::Semi; break;
      case ',': one = Tok::Comma; break;
      default: {
        std::string what = "line ";
        what += std::to_string(line) + ", col " + std::to_string(col) +
                ": unexpected character '";
        what += c;
        what += "'";
        throw LexerError(what);
      }
    }
    advance();
    return {one, std::string(1, c), 0, line, col};
  }

  std::string src_;
  size_t pos_ = 0;
  int line_ = 1;
  size_t lineStart_ = 0;
};

}  // namespace minic
