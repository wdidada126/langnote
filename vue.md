# vue

v-show 不显示
v-if   不加载

vue iview自定义Modal弹窗内容的使用

```js
JSON.stringify(row)
let params = JSON.parse(this.$route.query.params)
```

data()中定义的变量，在methods中使用，需要用


没有完全遵循MVVM模型

data:

`this` 指向 vm 实例

document.getEmementById();

v-bind 缩写
v-on 缩写

字符串操作
this.message.split('').reverse().join('')

v-bind:class

v-if
v-else
v-else-if

v-show
当 v-if 与 v-for 一起使用时，v-for 具有比 v-if 更高的优先级。

https://cn.vuejs.org/v2/guide/components-registration.html
如果你没有通过 import/require 使用一个模块系统，

v-modle

Vue-router

Vue http接口 根据url映射不同的网址

### 传参

跨页面传参 route
一个页面不同模块传参 props

this.$emit("update:filterVisible", false);
这里update是干啥的？

在 Vue.js 中，this.$emit("update:filterVisible", false) 是用来触发一个特定格式的自定义事件的语法。这里的 update: 前缀有特殊含义，它是 Vue 的 .sync 修饰符的配套用法。

具体解释：

1. .sync 修饰符的作用：
   • 在父组件中使用子组件时，如果希望实现父子组件间的双向绑定（但不想用 v-model），可以使用 .sync 修饰符
   • 例如：<child-component :filterVisible.sync="someValue"></child-component>

2. update: 前缀的含义：
   • 当子组件需要修改父组件传递的 prop 时，应该触发一个名为 update:propName 的事件
   • 这就是为什么你会看到 this.$emit("update:filterVisible", false) 这样的代码

3. 工作原理：
   <!-- 父组件模板 -->
   <mq-create-drawer :filterVisible.sync="filterVisible" />
   
   等价于：
   <mq-create-drawer 
     :filterVisible="filterVisible"
     @update:filterVisible="val => filterVisible = val"
   />
   

4. 在子组件中的对应操作：
   // 子组件中关闭 drawer 时
   this.$emit("update:filterVisible", false);
   这会通知父组件将 filterVisible 更新为 false

在您的代码中的具体应用：

1. 父组件 (main.vue)：
   <mq-create-drawer
     :filterVisible.sync="filterVisible"
     @callback="drawerCallback"
   />
   

2. 子组件 (mqCreateDrawer.vue)：
   methods: {
     handleCancel() {
       // 通知父组件更新 filterVisible 为 false
       this.$emit("update:filterVisible", false);
     },
     
     handleSubmit() {
       // 表单验证通过后
       this.$emit("update:filterVisible", false);
     }
   }
   

为什么这样设计？

这种模式比直接修改 prop 更符合 Vue 的单向数据流原则，因为它：
1. 明确表达了"子组件希望父组件更新某个值"的意图
2. 保持了数据修改的源头清晰可追踪
3. 是 Vue 官方推荐的处理 prop "双向绑定"的方式

对比常规事件：
方式 语法 适用场景
常规事件 this.$emit('event-name', value) 一般事件通信

.sync 模式 this.$emit('update:propName', value) 专门用于 prop 的"双向绑定"

注意事项：

1. 从 Vue 2.3.0+ 开始支持 .sync 修饰符
2. 在 Vue 3 中，v-model 可以替代大多数 .sync 的使用场景
3. 当需要"双向绑定"多个 prop 时，.sync 比多个 v-model 更简洁


问题：列表中描述列有2000个字符

在Ant Design Vue的表格组件中，ellipsis: true是一个用于控制表格单元格文本显示的属性，它的作用和含义如下：
作用
当设置为 true 时，如果单元格内容过长超出列宽，会显示为省略号（...）而不是换行或溢出。同时会自带 tooltip 提示，鼠标悬停时可以查看完整内容。

具体效果
1. 视觉表现：
   • 文本超出宽度时自动显示为省略号（如："这是一个很长的Topic名称..."）
   • 保持表格列宽固定，不会因为内容过长而撑开

2. 交互功能：
   • 鼠标悬停在省略号上时，会自动显示包含完整内容的 tooltip
   • 不需要额外编写tooltip代码

示例代码解析

const columns = [
  {
    title: "Topic名称",
    dataIndex: "MQ_DETAIL",  // 对应数据源的字段名
    key: "MQ_DETAIL",        // React需要的key
    width: 200,             // 固定列宽
    ellipsis: true          // 启用省略号效果
  },
  // 其他列...
]


对比有无ellipsis的效果
设置 内容超出时表现 鼠标悬停效果
ellipsis: true 显示为省略号 显示完整内容
ellipsis: false 或 不设置 可能换行或溢出 无特殊效果

实现原理

Ant Design 内部实际上是使用了以下CSS样式来实现这个效果：
white-space: nowrap;
overflow: hidden;
text-overflow: ellipsis;


何时使用
1. 当列宽固定且内容可能很长时
2. 需要保持表格布局整齐时
3. 需要节省空间但仍需提供完整信息查看功能时

注意事项
1. 必须配合width使用才能生效
2. 如果同时需要自动换行和tooltip，需要自定义render函数
3. 在移动端可能需要注意 tooltip 的触发方式

进阶用法

如果需要自定义tooltip内容或样式，可以使用customRender：
{
  title: "Topic名称",
  dataIndex: "MQ_DETAIL",
  key: "MQ_DETAIL",
  width: 200,
  customRender: text => ({
    children: <a-tooltip title={text}>{text}</a-tooltip>,
    props: {
      style: {
        whiteSpace: 'nowrap',
        overflow: 'hidden',
        textOverflow: 'ellipsis'
      }
    }
  })
}

