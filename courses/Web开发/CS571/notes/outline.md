# CS571 逐周要点（骨架）

## W01 React 基础
- JSX 即函数调用；组件是返回 UI 的函数。
- props 只读；组合优于配置。
- 开发环境：Vite/CRA 迁移史与 starter 结构。

## W02 状态与事件
- useState 与不可变更新陷阱（对象/数组拷贝）。
- 状态提升与单一数据源。
- 列表 key 与受控表单组件。

## W03 副作用与数据获取
- useEffect 依赖数组语义与清理函数。
- 异步加载：loading/error/竞态处理。
- "派生状态在渲染期计算"原则。

## W04 组件进阶
- useRef 与"不触发渲染的可变值"。
- 自定义 Hook 抽取复用逻辑。
- children/渲染属性/组件即参数等组合模式。

## W05 表单与路由
- 表单验证策略与错误呈现。
- React Router：Route/NavLink/params/loader 概念。
- URL 即状态：深链与刷新可恢复。

## W06 状态管理进阶
- Context：跨层传递与其重渲染代价。
- useReducer 管理复杂状态迁移。
- 何时需要外部状态库的判断树。

## W07 样式与组件库
- CSS 方案谱系：module/styled/Tailwind。
- Material Design 与 MUI 组件体系。
- NativeWind：Web 样式思路进入 RN。

## W08 测试与调试
- 以用户视角写 RTL 测试；查询优先级。
- mock 网络与 fixture 管理。
- React DevTools Profiler 与重渲染定位。

## W09 React Native 入门
- Expo 工程结构、OTA 更新与真机调试。
- 核心组件映射：View/Text/Image/FlatList。
- React Navigation：stack/tab/drawer 与深链。

## W10 原生能力与动画
- 设备 API：相机/相册/定位/推送（FCM）。
- 动画：Animated vs Reanimated/Gesture Handler。
- 性能：JSI/Fabric 新架构概念与列表优化。

## W11 后端与对话式 UI
- 与 REST/GraphQL/Firestore 对接的数据层。
- 认证（Firebase Auth）与本地存储策略。
- Dialogflow：意图/实体/Fulfillment 接入聊天 UI。

## W12 UX 与展示
- 可用性原则：可视反馈/一致性/容错。
- 设计系统与主题化；移动端手势与导航惯例。
- Final 路演与性能/稳定性清单复盘。
