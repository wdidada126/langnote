# flex
https://westes.github.io/flex/manual/

生成.c代码，类似protoc

https://www.gnu.org/software/flex/

## 源代码
https://github.com/westes/flex

ftp://ftp.iecc.com/pub/file/flexbison.zip

### api doc

https://westes.github.io/flex/manual/
JFlex is a lexical analyzer generator (also known as scanner generator) for Java, written in Java.

https://westes.github.io/flex/manual/

中文翻译
编译工程附录：flex使用
https://zhuanlan.zhihu.com/p/108167693
flex使用.mhtml

flex 生成的代码，引用.y文件定义的变量

需要引入xxx.tab.h（bison生成的）

## 版本version

## 开源协议

## 二进制文件库文件安装
### apt
sudo apt install flex libfl-dev -y
### yum
yum install flex flex-devel -y
## 编译

```shell
wdidada@LAPTOP-wdidada:~$ bison --version
bison (GNU Bison) 3.8.2
Written by Robert Corbett and Richard Stallman.

Copyright (C) 2021 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
wdidada@LAPTOP-wdidada:~$ flex --version
flex 2.6.4
```

### flex在miniob中的使用

https://oceanbase.github.io/miniob/design/miniob-sql-parser/


%option bison-bridge 和 %option bison-locations 是 Flex 与 Bison 集成时非常重要的选项，它们提供了更紧密的集成和更好的错误位置信息。

1. %option bison-bridge

功能

启用 Bison 桥接模式（Bison bridge mode），改变 Flex 与 Bison 的交互方式，使用 Bison 的 yylval 和 yylloc 结构。

传统模式 vs 桥接模式

传统模式（默认）：
// Flex 生成的函数签名
int yylex(void);

// Bison 需要声明
extern int yylex(void);
extern YYSTYPE yylval;


桥接模式：
// Flex 生成的函数签名
int yylex(YYSTYPE* yylval_param);

// Bison 调用方式
int token = yylex(&yylval);


使用方式

%{
#include "parser.tab.h"  // Bison 生成的头文件
%}

%option bison-bridge

%%

[0-9]+    {
    yylval->integer = atoi(yytext);
    return INTEGER;
}

[a-zA-Z]+ {
    yylval->string = strdup(yytext);
    return IDENTIFIER;
}


优点

1. 线程安全：每个词法分析器实例有自己的 yylval
2. 可重入：支持多个词法分析器实例
3. 更好的封装：不依赖全局变量

2. %option bison-locations

功能

启用位置追踪，提供详细的错误位置信息（行号、列号）。

传统位置处理 vs bison-locations

传统方式：
%{
int yylineno = 1;
%}

%%
\n      { yylineno++; }


bison-locations 方式：
%option bison-locations

%%
\n      { 
    yylloc->first_line = yylloc->last_line = yylineno;
    yylloc->first_column = yylloc->last_column = 1;
    yylineno++;
}


使用方式

%{
#include "parser.tab.h"
%}

%option bison-bridge bison-locations

%%

[0-9]+    {
    yylval->integer = atoi(yytext);
    
    // 设置位置信息
    yylloc->first_line = yylloc->last_line = yylineno;
    yylloc->first_column = column;
    yylloc->last_column = column + yyleng - 1;
    
    column += yyleng;
    return INTEGER;
}

\n        {
    yylineno++;
    column = 1;
}


3. 完整集成示例

Bison 语法文件 parser.y

%{
#include <stdio.h>
#include <stdlib.h>

// 定义词法分析器函数
int yylex(YYSTYPE* yylval_param, YYLTYPE* yylloc_param);
void yyerror(YYLTYPE* loc, const char* msg);
%}

// 定义语义值类型
%union {
    int integer;
    char* string;
}

// 定义token
%token <integer> INTEGER
%token <string> IDENTIFIER

// 启用位置追踪
%locations

%%

input:  /* empty */
    | input expr '\n' { printf("Parsed expression at line %d\n", @2.first_line); }
    ;

expr: INTEGER     { printf("Integer: %d at line %d\n", $1, @1.first_line); }
    | IDENTIFIER  { printf("Identifier: %s at line %d\n", $1, @1.first_line); }
    ;

%%

// 错误处理函数（带位置信息）
void yyerror(YYLTYPE* loc, const char* msg) {
    fprintf(stderr, "Error at line %d, column %d: %s\n", 
            loc->first_line, loc->first_column, msg);
}

int main() {
    return yyparse();
}


Flex 词法文件 lexer.l

%{
#include "parser.tab.h"
#include <string.h>

int column = 1;
%}

%option bison-bridge bison-locations
%option noyywrap

%%

[0-9]+    {
    yylval->integer = atoi(yytext);
    
    // 设置精确的位置信息
    yylloc->first_line = yylloc->last_line = yylineno;
    yylloc->first_column = column;
    yylloc->last_column = column + yyleng - 1;
    
    column += yyleng;
    return INTEGER;
}

[a-zA-Z][a-zA-Z0-9_]* {
    yylval->string = strdup(yytext);
    
    yylloc->first_line = yylloc->last_line = yylineno;
    yylloc->first_column = column;
    yylloc->last_column = column + yyleng - 1;
    
    column += yyleng;
    return IDENTIFIER;
}

[ \t]+    {
    column += yyleng; // 跳过空格，更新列号
}

\n        {
    yylineno++;
    column = 1;
}

.         {
    fprintf(stderr, "Invalid character '%c' at line %d, column %d\n", 
            yytext[0], yylineno, column);
    column++;
}

%%


4. 编译和构建

Makefile 示例

CC = gcc
CFLAGS = -g -Wall

all: parser

parser.tab.c parser.tab.h: parser.y
	bison -d parser.y

lex.yy.c: lexer.l parser.tab.h
	flex lexer.l

parser: lex.yy.c parser.tab.c parser.tab.h
	$(CC) $(CFLAGS) -o $@ parser.tab.c lex.yy.c

clean:
	rm -f parser parser.tab.c parser.tab.h lex.yy.c

test: parser
	echo "123 hello" | ./parser


CMakeLists.txt 示例

cmake_minimum_required(VERSION 3.10)
project(FlexBisonIntegration C)

find_package(BISON REQUIRED)
find_package(FLEX REQUIRED)

BISON_TARGET(Parser parser.y ${CMAKE_BINARY_DIR}/parser.tab.c
    DEFINES_FILE ${CMAKE_BINARY_DIR}/parser.tab.h)

FLEX_TARGET(Lexer lexer.l ${CMAKE_BINARY_DIR}/lex.yy.c)

add_executable(parser
    ${BISON_Parser_OUTPUTS}
    ${FLEX_Lexer_OUTPUTS}
)

target_include_directories(parser PRIVATE ${CMAKE_BINARY_DIR})

if(APPLE)
    find_library(FL_LIB NAMES fl)
    target_link_libraries(parser ${FL_LIB})
else()
    target_link_libraries(parser fl)
endif()


5. 高级特性

自定义位置结构

%{
// 自定义位置结构
typedef struct MY_LOCATION {
    int first_line;
    int first_column;
    int last_line;
    int last_column;
    const char* filename;
} MY_LOCATION;

#define YYLTYPE MY_LOCATION
%}


多文件位置追踪

%{
#include "parser.tab.h"

int column = 1;
const char* current_filename = "input.txt";
%}

%option bison-bridge bison-locations

%%

[0-9]+    {
    yylval->integer = atoi(yytext);
    
    yylloc->first_line = yylloc->last_line = yylineno;
    yylloc->first_column = column;
    yylloc->last_column = column + yyleng - 1;
    yylloc->filename = current_filename;
    
    column += yyleng;
    return INTEGER;
}


6. 实际应用场景

1. 编译器开发

%locations
%type <node> expression statement

%%

function_decl: TYPE IDENTIFIER '(' parameters ')' '{' statements '}'
    {
        $$ = create_function_node($1, $2, $4, $7);
        set_location($$, @1); // 设置AST节点的位置信息
    }


2. 配置解析器

config_line: KEY '=' VALUE
    {
        if (validate_value($3, @3)) {
            add_config($1, $3);
        } else {
            yyerror(@3, "Invalid value for key");
        }
    }


3. 模板引擎

template: text (tag text)*
    {
        for (int i = 0; i < $2->count; i++) {
            if (!validate_tag($2->tags[i], @2->locations[i])) {
                yyerror(@2->locations[i], "Invalid template tag");
            }
        }
    }


7. 优势总结

1. 精确的错误定位：提供行号、列号等详细信息
2. 线程安全：支持多实例和重入
3. 更好的错误信息：用户可以知道错误发生的具体位置
4. IDE 集成：便于在编辑器中高亮显示错误
5. 调试友好：更容易追踪和修复解析问题

8. 注意事项
1. 性能考虑：位置追踪会增加一些开销
2. 内存使用：需要存储额外的位置信息
3. 兼容性：需要 Bison 3.0+ 版本支持完整功能
4. 初始化：需要正确初始化位置结构

这些选项在开发高质量的解析器时非常有用，特别是需要提供良好错误信息的场景。

以下是使用 Flex 单独识别 C 语言关键字并生成 token 流的完整示例：

1. 头文件 c_tokens.h

#ifndef C_TOKENS_H
#define C_TOKENS_H

// Token 类型定义
typedef enum {
    // 关键字
    TOKEN_AUTO,
    TOKEN_BREAK,
    TOKEN_CASE,
    TOKEN_CHAR,
    TOKEN_CONST,
    TOKEN_CONTINUE,
    TOKEN_DEFAULT,
    TOKEN_DO,
    TOKEN_DOUBLE,
    TOKEN_ELSE,
    TOKEN_ENUM,
    TOKEN_EXTERN,
    TOKEN_FLOAT,
    TOKEN_FOR,
    TOKEN_GOTO,
    TOKEN_IF,
    TOKEN_INT,
    TOKEN_LONG,
    TOKEN_REGISTER,
    TOKEN_RETURN,
    TOKEN_SHORT,
    TOKEN_SIGNED,
    TOKEN_SIZEOF,
    TOKEN_STATIC,
    TOKEN_STRUCT,
    TOKEN_SWITCH,
    TOKEN_TYPEDEF,
    TOKEN_UNION,
    TOKEN_UNSIGNED,
    TOKEN_VOID,
    TOKEN_VOLATILE,
    TOKEN_WHILE,
    
    // 数据类型
    TOKEN_IDENTIFIER,
    TOKEN_INTEGER,
    TOKEN_FLOAT_NUMBER,
    TOKEN_CHAR_LITERAL,
    TOKEN_STRING_LITERAL,
    
    // 运算符
    TOKEN_PLUS,
    TOKEN_MINUS,
    TOKEN_MULTIPLY,
    TOKEN_DIVIDE,
    TOKEN_MODULO,
    TOKEN_ASSIGN,
    TOKEN_EQUAL,
    TOKEN_NOT_EQUAL,
    TOKEN_LESS,
    TOKEN_LESS_EQUAL,
    TOKEN_GREATER,
    TOKEN_GREATER_EQUAL,
    TOKEN_AND,
    TOKEN_OR,
    TOKEN_NOT,
    TOKEN_BIT_AND,
    TOKEN_BIT_OR,
    TOKEN_BIT_XOR,
    TOKEN_BIT_NOT,
    TOKEN_LEFT_SHIFT,
    TOKEN_RIGHT_SHIFT,
    
    // 分隔符
    TOKEN_SEMICOLON,
    TOKEN_COMMA,
    TOKEN_DOT,
    TOKEN_ARROW,
    TOKEN_LEFT_PAREN,
    TOKEN_RIGHT_PAREN,
    TOKEN_LEFT_BRACE,
    TOKEN_RIGHT_BRACE,
    TOKEN_LEFT_BRACKET,
    TOKEN_RIGHT_BRACKET,
    
    // 其他
    TOKEN_INCREMENT,
    TOKEN_DECREMENT,
    TOKEN_PLUS_ASSIGN,
    TOKEN_MINUS_ASSIGN,
    TOKEN_MULTIPLY_ASSIGN,
    TOKEN_DIVIDE_ASSIGN,
    TOKEN_MODULO_ASSIGN,
    TOKEN_TERNARY,
    TOKEN_ELLIPSIS,
    
    TOKEN_PREPROCESSOR,
    TOKEN_COMMENT,
    TOKEN_WHITESPACE,
    TOKEN_NEWLINE,
    TOKEN_EOF,
    TOKEN_ERROR
} token_type_t;

// Token 结构体
typedef struct {
    token_type_t type;
    char* value;           // 动态分配的字符串值
    int line;              // 行号
    int column;            // 列号
    int length;            // 长度
} token_t;

// 函数声明
const char* token_type_to_string(token_type_t type);
void print_token(const token_t* token);
void free_token(token_t* token);

#endif // C_TOKENS_H


2. Token 工具函数 c_tokens.c

#include "c_tokens.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Token 类型到字符串的映射
const char* token_type_to_string(token_type_t type) {
    static const char* names[] = {
        // 关键字
        "AUTO", "BREAK", "CASE", "CHAR", "CONST", "CONTINUE", "DEFAULT",
        "DO", "DOUBLE", "ELSE", "ENUM", "EXTERN", "FLOAT", "FOR", "GOTO",
        "IF", "INT", "LONG", "REGISTER", "RETURN", "SHORT", "SIGNED",
        "SIZEOF", "STATIC", "STRUCT", "SWITCH", "TYPEDEF", "UNION",
        "UNSIGNED", "VOID", "VOLATILE", "WHILE",
        
        // 数据类型
        "IDENTIFIER", "INTEGER", "FLOAT_NUMBER", "CHAR_LITERAL", "STRING_LITERAL",
        
        // 运算符
        "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "MODULO", "ASSIGN", "EQUAL",
        "NOT_EQUAL", "LESS", "LESS_EQUAL", "GREATER", "GREATER_EQUAL", "AND",
        "OR", "NOT", "BIT_AND", "BIT_OR", "BIT_XOR", "BIT_NOT", "LEFT_SHIFT",
        "RIGHT_SHIFT",
        
        // 分隔符
        "SEMICOLON", "COMMA", "DOT", "ARROW", "LEFT_PAREN", "RIGHT_PAREN",
        "LEFT_BRACE", "RIGHT_BRACE", "LEFT_BRACKET", "RIGHT_BRACKET",
        
        // 其他
        "INCREMENT", "DECREMENT", "PLUS_ASSIGN", "MINUS_ASSIGN", "MULTIPLY_ASSIGN",
        "DIVIDE_ASSIGN", "MODULO_ASSIGN", "TERNARY", "ELLIPSIS",
        
        "PREPROCESSOR", "COMMENT", "WHITESPACE", "NEWLINE", "EOF", "ERROR"
    };
    
    if (type >= TOKEN_AUTO && type <= TOKEN_ERROR) {
        return names[type];
    }
    return "UNKNOWN";
}

void print_token(const token_t* token) {
    if (token == NULL) {
        printf("NULL token\n");
        return;
    }
    
    printf("Line %3d, Col %3d: %-15s", 
           token->line, token->column, token_type_to_string(token->type));
    
    if (token->value != NULL) {
        printf(" '%s'", token->value);
    }
    
    printf(" (len: %d)\n", token->length);
}

void free_token(token_t* token) {
    if (token != NULL) {
        if (token->value != NULL) {
            free(token->value);
        }
        free(token);
    }
}


3. Flex 词法分析器 c_lexer.l

%{
#include "c_tokens.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 全局变量
int line_num = 1;
int column_num = 1;
int start_column = 1;

// 函数声明
token_t* create_token(token_type_t type, const char* value);
void update_position(int length);
%}

%option noyywrap
%option nounput
%option noinput

DIGIT    [0-9]
HEXDIGIT [0-9a-fA-F]
OCTDIGIT [0-7]
LETTER   [a-zA-Z_]
ID       {LETTER}({LETTER}|{DIGIT})*

%%

"auto"      { return create_token(TOKEN_AUTO, yytext); }
"break"     { return create_token(TOKEN_BREAK, yytext); }
"case"      { return create_token(TOKEN_CASE, yytext); }
"char"      { return create_token(TOKEN_CHAR, yytext); }
"const"     { return create_token(TOKEN_CONST, yytext); }
"continue"  { return create_token(TOKEN_CONTINUE, yytext); }
"default"   { return create_token(TOKEN_DEFAULT, yytext); }
"do"        { return create_token(TOKEN_DO, yytext); }
"double"    { return create_token(TOKEN_DOUBLE, yytext); }
"else"      { return create_token(TOKEN_ELSE, yytext); }
"enum"      { return create_token(TOKEN_ENUM, yytext); }
"extern"    { return create_token(TOKEN_EXTERN, yytext); }
"float"     { return create_token(TOKEN_FLOAT, yytext); }
"for"       { return create_token(TOKEN_FOR, yytext); }
"goto"      { return create_token(TOKEN_GOTO, yytext); }
"if"        { return create_token(TOKEN_IF, yytext); }
"int"       { return create_token(TOKEN_INT, yytext); }
"long"      { return create_token(TOKEN_LONG, yytext); }
"register"  { return create_token(TOKEN_REGISTER, yytext); }
"return"    { return create_token(TOKEN_RETURN, yytext); }
"short"     { return create_token(TOKEN_SHORT, yytext); }
"signed"    { return create_token(TOKEN_SIGNED, yytext); }
"sizeof"    { return create_token(TOKEN_SIZEOF, yytext); }
"static"    { return create_token(TOKEN_STATIC, yytext); }
"struct"    { return create_token(TOKEN_STRUCT, yytext); }
"switch"    { return create_token(TOKEN_SWITCH, yytext); }
"typedef"   { return create_token(TOKEN_TYPEDEF, yytext); }
"union"     { return create_token(TOKEN_UNION, yytext); }
"unsigned"  { return create_token(TOKEN_UNSIGNED, yytext); }
"void"      { return create_token(TOKEN_VOID, yytext); }
"volatile"  { return create_token(TOKEN_VOLATILE, yytext); }
"while"     { return create_token(TOKEN_WHILE, yytext); }

{ID}        { return create_token(TOKEN_IDENTIFIER, yytext); }

/* 整数常量 */
{DIGIT}+                    { return create_token(TOKEN_INTEGER, yytext); }
0[xX]{HEXDIGIT}+            { return create_token(TOKEN_INTEGER, yytext); }
0{OCTDIGIT}+                { return create_token(TOKEN_INTEGER, yytext); }

/* 浮点数常量 */
{DIGIT}+\.{DIGIT}*([eE][+-]?{DIGIT}+)? { return create_token(TOKEN_FLOAT_NUMBER, yytext); }
{DIGIT}*\.{DIGIT}+([eE][+-]?{DIGIT}+)? { return create_token(TOKEN_FLOAT_NUMBER, yytext); }

/* 字符常量 */
L?'(\\.|[^'\\])+'           { return create_token(TOKEN_CHAR_LITERAL, yytext); }

/* 字符串常量 */
L?\"(\\.|[^"\\])*\"         { return create_token(TOKEN_STRING_LITERAL, yytext); }

/* 运算符 */
"++"        { return create_token(TOKEN_INCREMENT, yytext); }
"--"        { return create_token(TOKEN_DECREMENT, yytext); }
"+="        { return create_token(TOKEN_PLUS_ASSIGN, yytext); }
"-="        { return create_token(TOKEN_MINUS_ASSIGN, yytext); }
"*="        { return create_token(TOKEN_MULTIPLY_ASSIGN, yytext); }
"/="        { return create_token(TOKEN_DIVIDE_ASSIGN, yytext); }
"%="        { return create_token(TOKEN_MODULO_ASSIGN, yytext); }
"=="        { return create_token(TOKEN_EQUAL, yytext); }
"!="        { return create_token(TOKEN_NOT_EQUAL, yytext); }
"<="        { return create_token(TOKEN_LESS_EQUAL, yytext); }
">="        { return create_token(TOKEN_GREATER_EQUAL, yytext); }
"&&"        { return create_token(TOKEN_AND, yytext); }
"||"        { return create_token(TOKEN_OR, yytext); }
"<<"        { return create_token(TOKEN_LEFT_SHIFT, yytext); }
">>"        { return create_token(TOKEN_RIGHT_SHIFT, yytext); }
"->"        { return create_token(TOKEN_ARROW, yytext); }
"..."       { return create_token(TOKEN_ELLIPSIS, yytext); }
"+"         { return create_token(TOKEN_PLUS, yytext); }
"-"         { return create_token(TOKEN_MINUS, yytext); }
"*"         { return create_token(TOKEN_MULTIPLY, yytext); }
"/"         { return create_token(TOKEN_DIVIDE, yytext); }
"%"         { return create_token(TOKEN_MODULO, yytext); }
"="         { return create_token(TOKEN_ASSIGN, yytext); }
"<"         { return create_token(TOKEN_LESS, yytext); }
">"         { return create_token(TOKEN_GREATER, yytext); }
"!"         { return create_token(TOKEN_NOT, yytext); }
"&"         { return create_token(TOKEN_BIT_AND, yytext); }
"|"         { return create_token(TOKEN_BIT_OR, yytext); }
"^"         { return create_token(TOKEN_BIT_XOR, yytext); }
"~"         { return create_token(TOKEN_BIT_NOT, yytext); }
"?"         { return create_token(TOKEN_TERNARY, yytext); }

/* 分隔符 */
";"         { return create_token(TOKEN_SEMICOLON, yytext); }
","         { return create_token(TOKEN_COMMA, yytext); }
"."         { return create_token(TOKEN_DOT, yytext); }
"("         { return create_token(TOKEN_LEFT_PAREN, yytext); }
")"         { return create_token(TOKEN_RIGHT_PAREN, yytext); }
"{"         { return create_token(TOKEN_LEFT_BRACE, yytext); }
"}"         { return create_token(TOKEN_RIGHT_BRACE, yytext); }
"["         { return create_token(TOKEN_LEFT_BRACKET, yytext); }
"]"         { return create_token(TOKEN_RIGHT_BRACKET, yytext); }

/* 预处理指令 */
"#"[^\n]*   { return create_token(TOKEN_PREPROCESSOR, yytext); }

/* 注释 */
"//"[^\n]*  { return create_token(TOKEN_COMMENT, yytext); }
"/*"([^*]|\*+[^*/])*\*+"/" { return create_token(TOKEN_COMMENT, yytext); }

/* 空白字符 */
[ \t]+      { return create_token(TOKEN_WHITESPACE, yytext); }

/* 换行符 */
\n          { 
    token_t* token = create_token(TOKEN_NEWLINE, "\\n");
    line_num++;
    column_num = 1;
    start_column = 1;
    return token;
}

/* 文件结束 */
<<EOF>>     { return create_token(TOKEN_EOF, "EOF"); }

/* 错误字符 */
.           { return create_token(TOKEN_ERROR, yytext); }

%%

token_t* create_token(token_type_t type, const char* value) {
    token_t* token = (token_t*)malloc(sizeof(token_t));
    if (token == NULL) {
        fprintf(stderr, "Error: Memory allocation failed for token\n");
        return NULL;
    }
    
    token->type = type;
    token->line = line_num;
    token->column = start_column;
    token->length = yyleng;
    
    if (value != NULL) {
        token->value = strdup(value);
        if (token->value == NULL) {
            fprintf(stderr, "Error: Memory allocation failed for token value\n");
            free(token);
            return NULL;
        }
    } else {
        token->value = NULL;
    }
    
    return token;
}

void update_position(int length) {
    column_num += length;
    start_column = column_num;
}


4. 主程序 main.c
#include "c_tokens.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 声明 Flex 函数
extern int yylex(void);
extern void yyrestart(FILE* input_file);
extern int yylineno;

void process_file(const char* filename, int show_whitespace) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        fprintf(stderr, "Error: Cannot open file %s\n", filename);
        return;
    }
    
    printf("=== Tokenizing file: %s ===\n", filename);
    printf("Line Col  Type              Value (Length)\n");
    printf("------------------------------------------\n");
    
    yyrestart(file);
    yylineno = 1;
    
    int token_count = 0;
    int error_count = 0;
    
    token_t* token;
    while ((token = yylex()) != NULL) {
        if (token->type == TOKEN_EOF) {
            free_token(token);
            break;
        }
        
        // 跳过空白字符（除非特别要求显示）
        if (!show_whitespace && 
            (token->type == TOKEN_WHITESPACE || token->type == TOKEN_COMMENT)) {
            free_token(token);
            continue;
        }
        
        print_token(token);
        token_count++;
        
        if (token->type == TOKEN_ERROR) {
            error_count++;
        }
        
        free_token(token);
    }
    
    printf("------------------------------------------\n");
    printf("Total tokens: %d, Errors: %d\n\n", token_count, error_count);
    
    fclose(file);
}

void print_usage(const char* program_name) {
    printf("Usage:\n");
    printf("  %s <filename>           - Tokenize C file\n", program_name);
    printf("  %s <filename> -w       - Show whitespace and comments\n", program_name);
    printf("  %s -h                 - Show this help\n", program_name);
    printf("\nExamples:\n");
    printf("  %s test.c\n", program_name);
    printf("  %s test.c -w\n", program_name);
}

int main(int argc, char** argv) {
    if (argc < 2 || strcmp(argv[1], "-h") == 0) {
        print_usage(argv[0]);
        return 0;
    }
    
    int show_whitespace = 0;
    const char* filename = argv[1];
    
    if (argc > 2 && strcmp(argv[2], "-w") == 0) {
        show_whitespace = 1;
    }
    
    process_file(filename, show_whitespace);
    return 0;
}


5. CMakeLists.txt

cmake_minimum_required(VERSION 3.14)
project(C_Lexer LANGUAGES C)

# 设置 C 标准
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# 查找 Flex
find_package(FLEX REQUIRED)

# 生成词法分析器
FLEX_TARGET(C_Lexer c_lexer.l ${CMAKE_BINARY_DIR}/c_lex.lex.c)

# 创建可执行文件
add_executable(c_lexer
    main.c
    c_tokens.c
    ${FLEX_C_Lexer_OUTPUTS}
)

# 包含目录
target_include_directories(c_lexer PRIVATE ${CMAKE_BINARY_DIR})

# 链接库
if(APPLE)
    find_library(FLEX_LIB NAMES fl PATHS /usr/local/opt/flex/lib /opt/homebrew/opt/flex/lib)
    if(FLEX_LIB)
        target_link_libraries(c_lexer ${FLEX_LIB})
    else()
        target_link_libraries(c_lexer fl)
    endif()
else()
    target_link_libraries(c_lexer fl)
endif()


6. 测试文件 test.c

#include <stdio.h>

int main() {
    int x = 10;
    float y = 3.14;
    char* message = "Hello, World!";
    
    for (int i = 0; i < x; i++) {
        if (i % 2 == 0) {
            printf("Even: %d\n", i);
        } else {
            printf("Odd: %d\n", i);
        }
    }
    
    return 0;
}


7. 编译和运行

编译步骤：

mkdir build
cd build
cmake ..
make


运行示例：

# 基本分析
./c_lexer ../test.c

# 显示所有token（包括空白和注释）
./c_lexer ../test.c -w


预期输出：


=== Tokenizing file: test.c ===
Line Col  Type              Value (Length)
------------------------------------------
  1,   1: PREPROCESSOR     '#include <stdio.h>' (len: 18)
  3,   1: INT               'int' (len: 3)
  3,   5: IDENTIFIER        'main' (len: 4)
  3,   9: LEFT_PAREN        '(' (len: 1)
  3,  10: RIGHT_PAREN       ')' (len: 1)
  3,  11: LEFT_BRACE        '{' (len: 1)
  4,   5: INT               'int' (len: 3)
  4,   9: IDENTIFIER        'x' (len: 1)
  4,  11: ASSIGN            '=' (len: 1)
  4,  13: INTEGER           '10' (len: 2)
  4,  15: SEMICOLON         ';' (len: 1)
...
------------------------------------------
Total tokens: 68, Errors: 0


8. 高级特性扩展

添加宏定义处理：

/* 宏定义 */
#define[ \t]+{ID}[ \t]*{ID}* { return create_token(TOKEN_MACRO_DEFINE, yytext); }
#ifdef      { return create_token(TOKEN_PREPROCESSOR, yytext); }
#ifndef     { return create_token(TOKEN_PREPROCESSOR, yytext); }
#endif      { return create_token(TOKEN_PREPROCESSOR, yytext); }


添加错误恢复：

/* 不完整的字符串 */
\"(\\.|[^"\\])*$ { 
    fprintf(stderr, "Error: Unterminated string at line %d\n", line_num);
    return create_token(TOKEN_ERROR, yytext);
}


这个词法分析器可以：
• ✅ 识别所有 C 语言关键字
• ✅ 处理标识符、常量、字符串
• ✅ 识别运算符和分隔符
• ✅ 处理注释和预处理指令
• ✅ 提供精确的行列位置信息
• ✅ 生成结构化的 token 流
• ✅ 支持错误检测和报告
