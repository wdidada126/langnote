# JSX

是的，JSX（JavaScript XML） 是 JavaScript 的一种语法扩展，主要用于 React 和类似的 UI 库（如 Vue 3 的 setup + JSX 模式）。它允许你在 JavaScript 代码中直接编写类似 HTML 的标记结构，使 UI 组件的声明更直观。

JSX 的核心特点

1. 不是字符串，也不是 HTML

JSX 看起来像 HTML，但实际上是 JavaScript 的语法糖，最终会被编译成普通的 JavaScript 函数调用（如 React.createElement() 或 Vue 的 h()）。

示例：
const element = <h1>Hello, JSX!</h1>;

编译后（Babel 转换）：
const element = React.createElement("h1", null, "Hello, JSX!");


2. 可以在 JSX 中嵌入 JavaScript 表达式

用 { } 包裹 JavaScript 代码：
const name = "Alice";
const element = <p>Hello, {name}!</p>;


3. JSX 是表达式

JSX 可以赋值给变量、作为函数返回值，或用于条件判断：
function Greeting({ isLoggedIn }) {
  return isLoggedIn ? <p>Welcome back!</p> : <p>Please sign in.</p>;
}


4. 属性命名采用驼峰式（camelCase）

HTML 的 class 在 JSX 中是 className，tabindex 变成 tabIndex：
<div className="container" tabIndex="1"></div>


JSX 在 Vue 中的应用

Vue 默认推荐模板语法（.vue 文件中的 <template>），但也支持 JSX：
1. Vue 2 + JSX

需要安装 @vue/babel-preset-jsx：
export default {
  render() {
    return <button onClick={this.handleClick}>Click me</button>;
  },
  methods: {
    handleClick() {
      alert("Clicked!");
    },
  },
};


2. Vue 3 + JSX

使用 defineComponent 和 setup：
import { defineComponent } from "vue";

export default defineComponent({
  setup() {
    const count = ref(0);
    return () => (
      <button onClick={() => count.value++}>Count: {count.value}</button>
    );
  },
});


JSX vs Vue 模板语法

特性 JSX Vue 模板语法

灵活性 高（可任意组合 JavaScript） 中（受限于模板指令）

学习成本 较高（需熟悉 JSX 规则） 低（类似 HTML）

适用场景 复杂逻辑、动态组件 大多数 Vue 项目

编译后 转为 h() 函数调用 转为虚拟 DOM 渲染函数

为什么在 Vue 中使用 JSX？

1. 更灵活的 JavaScript 控制  
   适合需要复杂逻辑的组件（如动态渲染、高阶组件）。

2. 类型支持更好（TypeScript）  
   JSX 在 TypeScript 中的类型推断比模板更友好。

3. React 开发者更熟悉  
   如果团队有 React 背景，JSX 可以减少上下文切换成本。

总结

• JSX 是 JavaScript 的扩展语法，不是模板语言。

• React 默认使用 JSX，Vue 也支持（但更推荐模板语法）。

• JSX 适合复杂逻辑，模板语法适合大多数 Vue 场景。

• 在 Vue 中使用 JSX 需要配置 Babel（如 @vue/babel-preset-jsx）。

如果你在 Vue 中写 JSX，本质上是在用 JavaScript 的语法生成虚拟 DOM，而不是传统的字符串模板。