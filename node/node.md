# node

vscode调试Node.js指南
node --inspect

node.js和typescript什么关系呢？
js的语言部分（包括语法以及基础类型和函数），叫做ecmascript，下称es
让机器识别，翻译，并运行es的，叫es引擎，例如v8，gecko
v8是其中一款爆款引擎
引擎是由更贴近机器语言的语言实现的，例如cpp和rust等（因为性能好）
为es和es引擎提供运行以及相关api的所在环境，我们叫做宿主
比如浏览器就是es的宿主之一，它包含一个es的引擎，利用es引擎运行es并且为es提供bom/dom等api。
宿主提供的api大部分也不是由es实现的，同理而是由c++/c等其他更偏向硬件的语言实现的。
简单来说 语言是有基础语法api以及宿主提供的api组成
就是说javascript = es + bom/dom（浏览器提供的api）
同理 actionscript = es + flash提供的api
nodejs也是其中一个宿主，它提供一系列操作计算机以及相关软硬件的api，常用于服务器和前端相关构建服务
也就是 nodejs = es + node api
严格来说，js应该是指在浏览器宿主（们）运行的es，那么nodejs严格来说不叫nodejs，应该叫nodees。但由于我们的习惯的原因，所以一般将js等价为es
当然，除此之外，还有甚至操作硬件的宿主，感兴趣的可以去研究一下
由于es的迭代更新，所以会存在es2015，es2016，es2017等版本
比如ie9这个宿主，不支持es2016
为了解决这个问题，我们需要一个从高版本转换到低版本的工具
这个就是babel。它是一个工具，通过babel转换之后，我们也可以在低版本浏览器使用新版本的es
同理，nodejs也存在版本差异的问题，也可以通过babel去进行处理
注意的是，babel只会处理（由于es引擎版本不一样导致的）es的兼容问题，由于宿主版本差异存在的宿主api的差异，是需要自行想办法处理的
比如ie9没有blob和file api，是没法通过babel解决的，虽然它们属于js的范畴，但是不属于es的部分
而typescript，下称ts，是什么？ts既是一个工具，也是一种语言
作为语言，它是es的超集，它完全兼容es，也就是可以在.ts上写es的语法。其次，它提供了一套在es基础上实现类型检测的语法
作为工具，它提供了类似babel的转换兼容语法的功能，其次它为它的类型检测语法提供了相关检测工具
由于js是一个动态语言。类型检测的作用是能让你在开发阶段能通过静态类型的声明达到及早发现代码中存在的问题。让ide更准确给你提供开发提示指引。间接为js引擎上提供更准确的优化判断（比如v8的turbofan对bytecode转换为machine code的过程）
简单来说，你可以通过ts（语法），经过ts（工具）检测类型错误以及转换为合适版本的es，然后在不同的宿主（nodejs，浏览器）里边运行，这就是ts和nodejs之间的关系

npm设置国内账户
https://cloud.tencent.com/developer/article/1372949

js库，提供了js访问系统资源的能力

npm root -g
C:\Users\chengwu2\AppData\Roaming\npm\node_modules
npm root -g
D:\devtools\node\node_global\node_modules


npm config set prefix "D:\devtools\node\node_global"
npm config set cache "D:\devtools\node\node_cache"

https://www.jianshu.com/p/dadd0d5354d6

nodejs新建项目

mkdir -p testnodeproject
cd/d testnodeproject
npm init -y
npm install -y

node src/main.js

ts
tsc命令行

tsc xxx.ts
产生xxx.js

http://nodejs.cn/api/async_hooks.html

node 环境变量
