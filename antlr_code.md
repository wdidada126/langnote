# antlr_code
https://www.antlr.org/api/

https://www.antlr.org/api/Java/index.html
## Java

```shell
        <antlr4.version>4.7.2</antlr4.version>
    
            <dependency>
                <groupId>org.antlr</groupId>
                <artifactId>antlr4-runtime</artifactId>
                <version>${antlr4.version}</version>
            </dependency>
```

### org.antlr.v4.runtime

| org.antlr.v4.runtime | 类型 |      |
| ------------------------------ | ---- | ---- |
|    ANTLRErrorListener              | interface |      |
|    ANTLRErrorStrategy              | interface |      |
| ANTLRFileStream |      |      |
| ANTLRInputStream | | |
| BailErrorStrategy | | |
| BaseErrorListener | | |
| BufferedTokenStream | | |
| CharStream | interface | |
| CharStreams | | |
| CodePointBuffer | | |
| CodePointCharStream | abstract | |
| CommonToken | | |
| CommonTokenFactory | | |
| CommonTokenStream | | |
| ConsoleErrorListener | | |
| DefaultErrorStrategy | | |
| DiagnosticErrorListener | | |
| FailedPredicateException | | |
| InputMismatchException | | |
| InterpreterRuleContext | | |
| IntStream | interface | |
| Lexer | abstract | |
| LexerInterpreter | | |
| LexerNoViableAltException | | |
| ListTokenSource | | |
| NoViableAltException | | |
| Parser | abstract | |
| ParserInterpreter | | |
| ParserRuleContext | | |
| ProxyErrorListener | | |
| RecognitionException | | |
| Recognizer | abstract | |
| RuleContext | | |
| RuleContextWithAltNum | | |
| RuntimeMetaData | | |
| Token | interface | |
| TokenFactory | interface | |
| TokenSource | interface | |
| TokenStream | interface | |
| TokenStreamRewriter | | |
| UnbufferedCharStream | | |
| UnbufferedTokenStream | | |
| Vocabulary | interface | |
| VocabularyImpl | | |
| WritableToken | interface |      |

RecognitionException子类 

ANTLRErrorListener接口实现类



Lexer抽象类 

Recognizer抽象类

Parser抽象类 ParserInterpreter
RuleContext 子类
TokenSource接口实现类



### org.antlr.v4.runtime.atn

| org.antlr.v4.runtime.atn | 类型 |      |
| ------------------------------ | ---- | ---- |
|    AbstractPredicateTransition              | abstract |      |
| ActionTransition |      |      |
| AmbiguityInfo | | |
| ArrayPredictionContext | | |
| ATN | | |
| ATNConfig | | |
| ATNConfigSet | | |
| ATNDeserializationOptions | | |
| ATNDeserializer | | |
| ATNSerializer | | |
| ATNSimulator | abstract | |
| ATNState | abstract | |
| ATNType | enum | |
| AtomTransition | | |
| BasicBlockStartState | | |
| BasicState | | |
| BlockEndState | | |
| BlockStartState | abstract | |
| CodePointTransitions | abstract | |
| ContextSensitivityInfo | | |
| DecisionEventInfo | | |
| DecisionInfo | | |
| DecisionState | abstract | |
| EmptyPredictionContext | | |
| EpsilonTransition | | |
| ErrorInfo | | |
| LexerAction | interface | |
| LexerActionExecutor | | |
| LexerActionType | enum | |
| LexerATNConfig | | |
| LexerATNSimulator | | |
| LexerChannelAction | | |
| LexerCustomAction | | |
| LexerIndexedCustomAction | | |
| LexerModeAction | | |
| LexerMoreAction | | |
| LexerPopModeAction | | |
| LexerPushModeAction | | |
| LexerSkipAction | | |
| LexerTypeAction | | |
| LL1Analyzer | | |
| LookaheadEventInfo | | |
| LoopEndState | | |
| NotSetTransition | | |
| OrderedATNConfigSet | | |
| ParseInfo | | |
| ParserATNSimulator | | |
| PlusBlockStartState | | |
| PlusLoopbackState | | |
| PrecedencePredicateTransition | | |
| PredicateEvalInfo |      |      |
| PredicateTransition | | |
| PredictionContext | abstract | |
| PredictionContextCache | | |
| PredictionMode | enum | |
| ProfilingATNSimulator | | |
| RangeTransition | | |
| RuleStartState | | |
| RuleStopState | | |
| RuleTransition | | |
| SemanticContext | abstract | |
| SetTransition | | |
| SingletonPredictionContext | | |
| StarBlockStartState | abstract | |
| StarLoopbackState | | |
| StarLoopEntryState | | |
| TokensStartState | | |
| Transition | abstract | |
| WildcardTransition | | |

### org.antlr.v4.runtime.dfa

| org.antlr.v4.runtime.dfa | 类型 |      |
| ------------------------------ | ---- | ---- |
|    DFA              |  |      |
|       DFASerializer                         |      |      |
|           DFAState                     |      |      |
|           LexerDFASerializer                     |      |      |


### org.antlr.v4.runtime.misc

| org.antlr.v4.runtime.misc | 类型 |      |
| ------------------------------ | ---- | ---- |
|    AbstractEqualityComparator              | abstract |      |
| Array2DHashSet |      |      |
| DoubleKeyMap | | |
| EqualityComparator | interface | |
| FlexibleHashMap | | |
| IntegerList | | |
| IntegerStack | | |
| InterpreterDataReader | | |
| Interval | | |
| IntervalSet | | |
| IntSet | interface | |
| LogManager | | |
| MultiMap | | |
| MurmurHash | | |
| NotNull | @interface | |
| ObjectEqualityComparator |  | |
| OrderedHashSet |  | |
| Pair |  | |
| ParseCancellationException |  | |
| Predicate | interface | |
| TestRig | Deprecated | |
| Triple |  | |
| Utils |      |      |



### org.antlr.v4.runtime.tree

| org.antlr.v4.runtime.misc | 类型 |      |
| ------------------------------ | ---- | ---- |
|    AbstractParseTreeVisitor              | abstract |      |
| ErrorNode | interface |      |
| ErrorNodeImpl |      |      |
| IterativeParseTreeWalker | | |
| ParseTree | interface | |
| ParseTreeListener | interface | |
| ParseTreeProperty | | |
| ParseTreeVisitor | interface | |
| ParseTreeWalker | | |
| RuleNode | interface | |
| SyntaxTree | interface | |
| TerminalNode | interface | |
| TerminalNodeImpl |  | |
| Tree | interface | |
| Trees |  | |



### org.antlr.v4.runtime.tree.pattern

| org.antlr.v4.runtime.tree.pattern | 类型 |      |
| ------------------------------ | ---- | ---- |
|    Chunk              | abstract |      |
| ParseTreeMatch |      |      |
| ParseTreePattern |      |      |
| ParseTreePatternMatcher | | |
| RuleTagToken | | |
| TagChunk | | |
| TextChunk | | |
| TokenTagToken | | |
|  | | |
|  | | |



### org.antlr.v4.runtime.tree.xpath

| org.antlr.v4.runtime.tree.xpath | 类型 |      |
| ------------------------------ | ---- | ---- |
|    XPath              |  |      |
| XPathElement |      |      |
| XPathLexer |      |      |
| XPathLexerErrorListener | | |
| XPathRuleAnywhereElement | | |
| XPathRuleElement | | |
| XPathTokenAnywhereElement | | |
| XPathTokenElement | | |
| XPathWildcardAnywhereElement | | |
| XPathWildcardElement | | |



## c++

```yml
  - "antlr4-cppruntime/4.13.1"
  - "antlr4/4.13.1"
```



#include "antlr4-common.h"

#include "ANTLRErrorListener.h"
#include "ANTLRErrorStrategy.h"
#include "ANTLRFileStream.h"
#include "ANTLRInputStream.h"
#include "BailErrorStrategy.h"
#include "BaseErrorListener.h"
#include "BufferedTokenStream.h"
#include "CharStream.h"
#include "CommonToken.h"
#include "CommonTokenFactory.h"
#include "CommonTokenStream.h"
#include "ConsoleErrorListener.h"
#include "DefaultErrorStrategy.h"
#include "DiagnosticErrorListener.h"
#include "Exceptions.h"
#include "FailedPredicateException.h"
#include "InputMismatchException.h"
#include "IntStream.h"
#include "InterpreterRuleContext.h"
#include "Lexer.h"
#include "LexerInterpreter.h"
#include "LexerNoViableAltException.h"
#include "ListTokenSource.h"
#include "NoViableAltException.h"
#include "Parser.h"
#include "ParserInterpreter.h"
#include "ParserRuleContext.h"
#include "ProxyErrorListener.h"
#include "RecognitionException.h"
#include "Recognizer.h"
#include "RuleContext.h"
#include "RuleContextWithAltNum.h"
#include "RuntimeMetaData.h"
#include "Token.h"
#include "TokenFactory.h"
#include "TokenSource.h"
#include "TokenStream.h"
#include "TokenStreamRewriter.h"
#include "UnbufferedCharStream.h"
#include "UnbufferedTokenStream.h"
#include "Version.h"
#include "Vocabulary.h"
#include "Vocabulary.h"
#include "WritableToken.h"
#include "atn/ATN.h"
#include "atn/ATNConfig.h"
#include "atn/ATNConfigSet.h"
#include "atn/ATNDeserializationOptions.h"
#include "atn/ATNDeserializer.h"
#include "atn/ATNSimulator.h"
#include "atn/ATNState.h"
#include "atn/ATNType.h"
#include "atn/ActionTransition.h"
#include "atn/AmbiguityInfo.h"
#include "atn/ArrayPredictionContext.h"
#include "atn/AtomTransition.h"
#include "atn/BasicBlockStartState.h"
#include "atn/BasicState.h"
#include "atn/BlockEndState.h"
#include "atn/BlockStartState.h"
#include "atn/ContextSensitivityInfo.h"
#include "atn/DecisionEventInfo.h"
#include "atn/DecisionInfo.h"
#include "atn/DecisionState.h"
#include "atn/EpsilonTransition.h"
#include "atn/ErrorInfo.h"
#include "atn/LL1Analyzer.h"
#include "atn/LexerATNConfig.h"
#include "atn/LexerATNSimulator.h"
#include "atn/LexerAction.h"
#include "atn/LexerActionExecutor.h"
#include "atn/LexerActionType.h"
#include "atn/LexerChannelAction.h"
#include "atn/LexerCustomAction.h"
#include "atn/LexerIndexedCustomAction.h"
#include "atn/LexerModeAction.h"
#include "atn/LexerMoreAction.h"
#include "atn/LexerPopModeAction.h"
#include "atn/LexerPushModeAction.h"
#include "atn/LexerSkipAction.h"
#include "atn/LexerTypeAction.h"
#include "atn/LookaheadEventInfo.h"
#include "atn/LoopEndState.h"
#include "atn/NotSetTransition.h"
#include "atn/OrderedATNConfigSet.h"
#include "atn/ParseInfo.h"
#include "atn/ParserATNSimulator.h"
#include "atn/ParserATNSimulatorOptions.h"
#include "atn/PlusBlockStartState.h"
#include "atn/PlusLoopbackState.h"
#include "atn/PrecedencePredicateTransition.h"
#include "atn/PredicateEvalInfo.h"
#include "atn/PredicateTransition.h"
#include "atn/PredictionContext.h"
#include "atn/PredictionContextCache.h"
#include "atn/PredictionContextMergeCache.h"
#include "atn/PredictionContextMergeCacheOptions.h"
#include "atn/PredictionMode.h"
#include "atn/ProfilingATNSimulator.h"
#include "atn/RangeTransition.h"
#include "atn/RuleStartState.h"
#include "atn/RuleStopState.h"
#include "atn/RuleTransition.h"
#include "atn/SemanticContext.h"
#include "atn/SerializedATNView.h"
#include "atn/SetTransition.h"
#include "atn/SingletonPredictionContext.h"
#include "atn/StarBlockStartState.h"
#include "atn/StarLoopEntryState.h"
#include "atn/StarLoopbackState.h"
#include "atn/TokensStartState.h"
#include "atn/Transition.h"
#include "atn/WildcardTransition.h"
#include "dfa/DFA.h"
#include "dfa/DFASerializer.h"
#include "dfa/DFAState.h"
#include "dfa/LexerDFASerializer.h"
#include "misc/InterpreterDataReader.h"
#include "misc/Interval.h"
#include "misc/IntervalSet.h"
#include "misc/MurmurHash.h"
#include "misc/Predicate.h"
#include "support/Any.h"
#include "support/Arrays.h"
#include "support/BitSet.h"
#include "support/Casts.h"
#include "support/CPPUtils.h"
#include "tree/AbstractParseTreeVisitor.h"
#include "tree/ErrorNode.h"
#include "tree/ErrorNodeImpl.h"
#include "tree/ParseTree.h"
#include "tree/ParseTreeListener.h"
#include "tree/ParseTreeProperty.h"
#include "tree/ParseTreeVisitor.h"
#include "tree/ParseTreeWalker.h"
#include "tree/TerminalNode.h"
#include "tree/TerminalNodeImpl.h"
#include "tree/Trees.h"
#include "tree/pattern/Chunk.h"
#include "tree/pattern/ParseTreeMatch.h"
#include "tree/pattern/ParseTreePattern.h"
#include "tree/pattern/ParseTreePatternMatcher.h"
#include "tree/pattern/RuleTagToken.h"
#include "tree/pattern/TagChunk.h"
#include "tree/pattern/TextChunk.h"
#include "tree/pattern/TokenTagToken.h"
#include "tree/xpath/XPath.h"
#include "tree/xpath/XPathElement.h"
#include "tree/xpath/XPathLexer.h"
#include "tree/xpath/XPathLexerErrorListener.h"
#include "tree/xpath/XPathRuleAnywhereElement.h"
#include "tree/xpath/XPathRuleElement.h"
#include "tree/xpath/XPathTokenAnywhereElement.h"
#include "tree/xpath/XPathTokenElement.h"
#include "tree/xpath/XPathWildcardAnywhereElement.h"
#include "tree/xpath/XPathWildcardElement.h"
#include "internal/Synchronization.h"

antlr4



| 命名空间 antlr                | 头文件      | 类型 |      |
| ----------------------------- | ----------- | ---- | ---- |
| ANTLRErrorListener            |             |      |      |
| ANTLRErrorStrategy            |             |      |      |
| ANTLRFileStream               |             |      |      |
| ANTLRInputStream              |             |      |      |
| BailErrorStrategy             |             |      |      |
| BaseErrorListener             |             |      |      |
| BufferedTokenStream           |             |      |      |
| CharStream                    |             |      |      |
| CommonToken                   |             |      |      |
| CommonTokenFactory            |             |      |      |
| CommonTokenStream             |             |      |      |
| ConsoleErrorListener          |             |      |      |
| DefaultErrorStrategy          |             |      |      |
| DiagnosticErrorListener       |             |      |      |
| RuntimeException              | Exception.h |      |      |
| IllegalStateException         | Exception.h |      |      |
| IllegalArgumentException      | Exception.h |      |      |
| NullPointerException          | Exception.h |      |      |
| IndexOutOfBoundsException     | Exception.h |      |      |
| UnsupportedOperationException | Exception.h |      |      |
| EmptyStackException           | Exception.h |      |      |
| IOException                   | Exception.h |      |      |
| CancellationException         | Exception.h |      |      |
| ParseCancellationException    | Exception.h |      |      |
| FailedPredicateException      |             |      |      |
| InputMismatchException        |             |      |      |
| InterpreterRuleContext        |             |      |      |
| IntStream                     |             |      |      |
| Lexer                         |             |      |      |
| LexerInterpreter              |             |      |      |
| LexerNoViableAltException     |             |      |      |
| ListTokenSource               |             |      |      |
| NoViableAltException          |             |      |      |
| Parser                        |             |      |      |
| ParserInterpreter             |             |      |      |
| ParserRuleContext             |             |      |      |
| ProxyErrorListener            |             |      |      |
| RecognitionException          |             |      |      |
| Recognizer                    |             |      |      |
| RuleContext                   |             |      |      |
| RuleContextWithAltNum         |             |      |      |
| RuntimeMetaData               |             |      |      |
| Token                         |             |      |      |
| TokenFactory                  |             |      |      |
| TokenSource                   |             |      |      |
| TokenStreamRewriter           |             |      |      |
| UnbufferedCharStream          |             |      |      |
| UnbufferedTokenStream         |             |      |      |
| WritableToken                 |             |      |      |





### antlr4::atn

| antlr4::atn               | 头文件 | 类型 |      |
| ------------------------- | ------ | ---- | ---- |
| ActionTransition          |        |      |      |
| AmbiguityInfo             |        |      |      |
| ArrayPredictionContext    |        |      |      |
| ATN                       |        |      |      |
| ATNConfig                 |        |      |      |
| ATNConfigSet              |        |      |      |
| ATNDeserializationOptions |        |      |      |
|                           |        |      |      |
|                           |        |      |      |
|                           |        |      |      |
|                           |        |      |      |
|                           |        |      |      |





### antlr4::dfa

| antlr4::dfa | 头文件       | 类型 |      |
| ----------- | ------------ | ---- | ---- |
| Vocabulary  | Vocabulary.h |      |      |
|             |              |      |      |
|             |              |      |      |


## Antlr Tool

## org.antlr.v4

|      | 类型 |      |
| ---- | ---- | ---- |
| Tool |      |      |
|      |      |      |
|      |      |      |



### org.antlr.v4.analysis

|                              | 类型 |      |
| ---------------------------- | ---- | ---- |
| AnalysisPipeline             |      |      |
| LeftRecursionDetector        |      |      |
| LeftRecursiveRuleAltInfo     |      |      |
| LeftRecursiveRuleAnalyzer    |      |      |
| LeftRecursiveRuleTransformer |      |      |
|                              |      |      |



### org.antlr.v4.automata

|                    | 类型      |      |
| ------------------ | --------- | ---- |
| ATNFactory         | interface |      |
| ATNOptimizer       |           |      |
| ATNPrinter         |           |      |
| ATNVisitor         |           |      |
| LexerATNFactory    |           |      |
| ParserATNFactory   |           |      |
| TailEpsilonRemover |           |      |
|                    |           |      |

### org.antlr.v4.codegen

|                           | 类型      |      |
| ------------------------- | --------- | ---- |
| ActionTranslator          |           |      |
| BlankOutputModelFactory   |           |      |
| CodeGenerator             |           |      |
| CodeGeneratorExtension    |           |      |
| CodeGenPipeline           |           |      |
| DefaultOutputModelFactory | abstract  |      |
| LexerFactory              |           |      |
| OutputModelController     |           |      |
| OutputModelFactory        | interface |      |
| OutputModelWalker         |           |      |
| ParserFactory             |           |      |
| SourceGenTriggers         |           |      |
| Target                    | abstract  |      |
| UnicodeEscapes            | abstract  |      |
|                           |           |      |
|                           |           |      |


#### org.antlr.v4.codegen.model

|                           | 类型       |      |
| ------------------------- | ---------- | ---- |
| Action                    |            |      |
| AddToLabelList            |            |      |
| AltBlock                  |            |      |
| ArgAction                 |            |      |
| BaseListenerFile          |            |      |
| BaseVisitorFile           |            |      |
| CaptureNextToken          |            |      |
| CaptureNextTokenType      |            |      |
| Choice                    | abstract   |      |
| CodeBlockForAlt           |            |      |
| CodeBlockForOuterMostAlt  |            |      |
| dbg                       |            |      |
| DispatchMethod            |            |      |
| ElementFrequenciesVisitor |            |      |
| ExceptionClause           |            |      |
| InvokeRule                |            |      |
| LabeledOp                 | interface  |      |
| LeftRecursiveRuleFunction |            |      |
| Lexer                     |            |      |
| LexerFile                 |            |      |
| ListenerDispatchMethod    |            |      |
| ListenerFile              |            |      |
| LL1AltBlock               |            |      |
| LL1Choice                 | abstract   |      |
| LL1Loop                   |            |      |
| LL1OptionalBlock          |            |      |
| LL1OptionalBlockSingleAlt |            |      |
| LL1PlusBlockSingleAlt     |            |      |
| LL1StarBlockSingleAlt     |            |      |
| Loop                      |            |      |
| MatchNotSet               |            |      |
| MatchSet                  |            |      |
| MatchToken                |            |      |
| ModelElement              | @interface |      |
| OptionalBlock             |            |      |
| OutputFile                | abstract   |      |
| OutputModelObject         | abstract   |      |
| Parser                    |            |      |
| ParserFile                |            |      |
| PlusBlock                 |            |      |
| Recognizer                | abstract   |      |
| RuleActionFunction        |            |      |
| RuleElement               |            |      |
| RuleFunction              |            |      |
| RuleSempredFunction       |            |      |
| SemPred                   |            |      |
| SerializedATN             |            |      |
| SrcOp                     | abstract   |      |
| StarBlock                 |            |      |
| Sync                      |            |      |
| TestSetInline             |            |      |
| ThrowEarlyExitException   |            |      |
| ThrowNoViableAlt          |            |      |
| ThrowRecognitionException |            |      |
| VisitorDispatchMethod     |            |      |
| VisitorFile               |            |      |
| Wildcard                  |            |      |
|                           |            |      |
|                           |            |      |



OutputModelObject (org.antlr.v4.codegen.model)
    SrcOp (org.antlr.v4.codegen.model)
        RuleElement (org.antlr.v4.codegen.model)
            Choice (org.antlr.v4.codegen.model)
                AltBlock (org.antlr.v4.codegen.model)
                    OptionalBlock (org.antlr.v4.codegen.model)
                LL1Choice (org.antlr.v4.codegen.model)
                    LL1AltBlock (org.antlr.v4.codegen.model)
                        LL1OptionalBlock (org.antlr.v4.codegen.model)
                    LL1OptionalBlockSingleAlt (org.antlr.v4.codegen.model)
                LL1Loop (org.antlr.v4.codegen.model)
                    LL1StarBlockSingleAlt (org.antlr.v4.codegen.model)
                    LL1PlusBlockSingleAlt (org.antlr.v4.codegen.model)
                Loop (org.antlr.v4.codegen.model)
                    PlusBlock (org.antlr.v4.codegen.model)
                    StarBlock (org.antlr.v4.codegen.model)
            MatchToken (org.antlr.v4.codegen.model)
                MatchSet (org.antlr.v4.codegen.model)
                    MatchNotSet (org.antlr.v4.codegen.model)
                Wildcard (org.antlr.v4.codegen.model)
            Action (org.antlr.v4.codegen.model)
                ArgAction (org.antlr.v4.codegen.model)
                SemPred (org.antlr.v4.codegen.model)
            InvokeRule (org.antlr.v4.codegen.model)



##### org.antlr.v4.codegen.model.chunk

|                            | 类型 |      |
| -------------------------- | ---- | ---- |
| ActionChunk                |      |      |
| ActionTemplate             |      |      |
| ActionText                 |      |      |
| ArgRef                     |      |      |
| LabelRef                   |      |      |
| ListLabelRef               |      |      |
| LocalRef                   |      |      |
| NonLocalAttrRef            |      |      |
| QRetValueRef               |      |      |
| RetValueRef                |      |      |
| RulePropertyRef            |      |      |
| RulePropertyRef_ctx        |      |      |
| RulePropertyRef_parser     |      |      |
| RulePropertyRef_start      |      |      |
| RulePropertyRef_stop       |      |      |
| RulePropertyRef_text       |      |      |
| SetAttr                    |      |      |
| SetNonLocalAttr            |      |      |
| ThisRulePropertyRef_ctx    |      |      |
| ThisRulePropertyRef_parser |      |      |
| ThisRulePropertyRef_start  |      |      |
| ThisRulePropertyRef_stop   |      |      |
| ThisRulePropertyRef_text   |      |      |
| TokenPropertyRef           |      |      |
| TokenPropertyRef_channel   |      |      |
| TokenPropertyRef_index     |      |      |
| TokenPropertyRef_int       |      |      |
| TokenPropertyRef_line      |      |      |
| TokenPropertyRef_pos       |      |      |
| TokenPropertyRef_text      |      |      |
| TokenPropertyRef_type      |      |      |
| TokenRef                   |      |      |
|                            |      |      |
|                            |      |      |



##### org.antlr.v4.codegen.model.decl

|                                   | 类型     |      |
| --------------------------------- | -------- | ---- |
| AltLabelStructDecl                |          |      |
| AttributeDecl                     |          |      |
| CodeBlock                         |          |      |
| ContextGetterDecl                 | abstract |      |
| ContextRuleGetterDecl             |          |      |
| ContextRuleListGetterDecl         |          |      |
| ContextRuleListIndexedGetterDecl  |          |      |
| ContextTokenGetterDecl            |          |      |
| ContextTokenListGetterDecl        |          |      |
| ContextTokenListIndexedGetterDecl |          |      |
| Decl                              |          |      |
| ElementListDecl                   |          |      |
| RuleContextDecl                   |          |      |
| RuleContextListDecl               |          |      |
| StructDecl                        |          |      |
| TokenDecl                         |          |      |
| TokenListDecl                     |          |      |
| TokenTypeDecl                     |          |      |


#### org.antlr.v4.codegen.target

|                  | 类型 |      |
| ---------------- | ---- | ---- |
| CppTarget        |      |      |
| CSharpTarget     |      |      |
| GoTarget         |      |      |
| JavaScriptTarget |      |      |
| JavaTarget       |      |      |
| Python2Target    |      |      |
| Python3Target    |      |      |
| SwiftTarget      |      |      |
|                  |      |      |
|                  |      |      |

### org.antlr.v4.gui

|                              | 类型      |      |
| ---------------------------- | --------- | ---- |
| BasicFontMetrics             | abstract  |      |
| GraphicsSupport              |           |      |
| JFileChooserConfirmOverwrite |           |      |
| PostScriptDocument           |           |      |
| SystemFontMetrics            |           |      |
| TestRig                      |           |      |
| TreeLayoutAdaptor            |           |      |
| TreePostScriptGenerator      |           |      |
| Trees                        |           |      |
| TreeTextProvider             | interface |      |
| TreeViewer                   |           |      |

### org.antlr.v4.misc

|                       | 类型     |      |
| --------------------- | -------- | ---- |
| CharSupport           |          |      |
| EscapeSequenceParsing | abstract |      |
| FrequencySet          |          |      |
| Graph                 |          |      |
| MutableInt            |          |      |
| OrderedHashMap        |          |      |
| Utils                 |          |      |
|                       |          |      |
|                       |          |      |

### org.antlr.v4.parse

|                         | 类型      |      |
| ----------------------- | --------- | ---- |
| ActionSplitter          |           |      |
| ActionSplitterListener  | interface |      |
| ANTLRLexer              |           |      |
| ANTLRParser             |           |      |
| ATNBuilder              |           |      |
| BlockSetTransformer     |           |      |
| GrammarASTAdaptor       |           |      |
| GrammarToken            |           |      |
| GrammarTreeVisitor      |           |      |
| LeftRecursiveRuleWalker |           |      |
| ResyncToEndOfRuleBlock  |           |      |
| ScopeParser             |           |      |
| TokenVocabParser        |           |      |
| ToolANTLRLexer          |           |      |
| ToolANTLRParser         |           |      |
| v3TreeGrammarException  |           |      |
| v4ParserException       |           |      |
|                         |           |      |

### org.antlr.v4.semantics

|                             | 类型 |      |
| --------------------------- | ---- | ---- |
| ActionSniffer               |      |      |
| AttributeChecks             |      |      |
| BasicSemanticChecks         |      |      |
| BlankActionSplitterListener |      |      |
| RuleCollector               |      |      |
| SemanticPipeline            |      |      |
| SymbolChecks                |      |      |
| SymbolCollector             |      |      |
| UseDefAnalyzer              |      |      |

### org.antlr.v4.tool

|                               | 类型      |      |
| ----------------------------- | --------- | ---- |
| Alternative                   |           |      |
| ANTLRMessage                  |           |      |
| ANTLRToolListener             | interface |      |
| Attribute                     |           |      |
| AttributeDict                 |           |      |
| AttributeResolver             | interface |      |
| BuildDependencyGenerator      |           |      |
| DefaultToolListener           |           |      |
| DOTGenerator                  |           |      |
| ErrorManager                  |           |      |
| ErrorSeverity                 | enum      |      |
| ErrorType                     | enum      |      |
| Grammar                       |           |      |
| GrammarInterpreterRuleContext |           |      |
| GrammarParserInterpreter      |           |      |
| GrammarSemanticsMessage       |           |      |
| GrammarSyntaxMessage          |           |      |
| GrammarTransformPipeline      |           |      |
| LabelElementPair              |           |      |
| LabelType                     | enum      |      |
| LeftRecursionCyclesMessage    |           |      |
| LeftRecursiveRule             |           |      |
| LexerGrammar                  |           |      |
| Rule                          |           |      |
| ToolMessage                   |           |      |
|                               |           |      |
|                               |           |      |

#### org.antlr.v4.tool.ast

|                       | 类型      |      |
| --------------------- | --------- | ---- |
| ActionAST             |           |      |
| AltAST                |           |      |
| BlockAST              |           |      |
| GrammarAST            |           |      |
| GrammarASTErrorNode   |           |      |
| GrammarASTVisitor     | interface |      |
| GrammarASTWithOptions |           |      |
| GrammarRootAST        |           |      |
| NotAST                |           |      |
| OptionalBlockAST      |           |      |
| PlusBlockAST          |           |      |
| PredAST               |           |      |
| QuantifierAST         | interface |      |
| RangeAST              |           |      |
| RuleAST               |           |      |
| RuleElementAST        |           |      |
| RuleRefAST            |           |      |
| SetAST                |           |      |
| StarBlockAST          |           |      |
| TerminalAST           |           |      |

#### org.antlr.v4.tool.templates

|      | 类型 |      |
| ---- | ---- | ---- |
|      |      |      |
|      |      |      |
|      |      |      |

### org.antlr.v4.unicode

|                               | 类型     |      |
| ----------------------------- | -------- | ---- |
| UnicodeDataTemplateController | abstract |      |
| UnicodeDataTemplateController | abstract |      |
|                               |          |      |
