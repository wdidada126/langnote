# vite

Vite（发音 /vit/，意为“快速”）是由 Vue 作者尤雨溪开发的新一代前端构建工具，定位与 Webpack 类似（负责项目编译、打包、开发服务），但核心原理、速度和体验完全不同——主打极速开发，是目前 Vue/React 等现代项目的主流首选。

### 一、Vite 核心定位
- 开发服务器 + 生产构建工具（类似 webpack-dev-server + webpack）
- 开发模式：基于浏览器原生 ES Module (ESM)，不打包、按需编译
- 生产模式：底层用 Rollup 打包（比 Webpack 更擅长 ESM 与 Tree-shaking）
- 核心优势：冷启动极快、热更新（HMR）几乎瞬时、配置极简

### 二、Vite vs Webpack：核心原理差异（最关键）
#### 1. Webpack 思路（传统）
> 先全量打包 → 再运行
- 启动时递归分析所有依赖、生成完整依赖图
- 把所有 JS/CSS/图片等打包成 bundle(s)
- 项目越大，启动越慢、热更新越卡

#### 2. Vite 思路（现代）
> 先启动服务 → 浏览器请求时再按需编译
- 启动几乎瞬时（不管项目多大）
- 浏览器直接用原生 `import/export` 请求模块
- Vite 只编译当前用到的文件（.vue/.tsx/.less 等）
- 热更新只更新单个模块，不重建整个依赖图

### 三、核心对比（一眼看懂）
| 维度 | Vite | Webpack |
| :--- | :--- | :--- |
| 开发启动 | 秒级（与项目大小无关） | 慢（项目越大越慢） |
| 热更新 HMR | 极快（单模块更新） | 较慢（需重新打包） |
| 底层核心 | 开发：ESM + esbuild；生产：Rollup | 全量打包（自有模块系统） |
| 配置 | 极简（开箱即用） | 复杂（loader/plugin 多） |
| 生产打包 | Rollup（体积小、Tree-shaking 好） | 成熟、生态极强 |
| 适用场景 | 现代框架（Vue3/React/Svelte） | 全场景（含老旧项目、高度定制） |
| 生态 | 快速增长（主流插件齐全） | 极其成熟（几乎所有场景） |

### 四、Vite 主要特点
1. 极速冷启动
   - 用 esbuild（Go 编写） 预构建第三方依赖（比 JS 工具快 10–100 倍）
   - 源码直接走 ESM，不打包、按需编译
2. 开箱即用
   - 内置支持：TS/JSX、Sass/Less、CSS Modules、静态资源、代理等
   - 配置文件 `vite.config.js` 通常几行搞定
3. 极致 HMR
   - 修改代码后浏览器几乎瞬间更新，不刷新页面、不丢失状态
4. 生产优化
   - Rollup 打包、自动代码分割、懒加载、压缩、Tree-shaking
5. 框架无关
   - 官方支持：Vue、React、Preact、Svelte、Solid 等


### 五、简单使用（1 分钟上手）
```bash
# 创建项目
npm create vite@latest my-project
# 选择框架：Vue / React / Vanilla 等

cd my-project
npm install

# 开发（极速启动）
npm run dev

# 生产构建（Rollup 打包）
npm run build
```

### 六、总结
- Vite ≈ 更快、更简单的现代版 Webpack
- 开发体验碾压 Webpack（大型项目尤其明显）
- 生产构建稳定可靠（Rollup 加持）
- 现在新项目（尤其 Vue3/React）优先选 Vite；老旧/高度定制项目仍可用 Webpack

要不要我给你一份 Vite 常用配置清单（包含代理、路径别名、环境变量、多页面、兼容旧浏览器），你直接复制到 `vite.config.js` 就能用？