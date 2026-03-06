# Bevy

https://bevyengine.org/

Rust库 数据驱动
游戏库

aes


openssl

https://github.com/bevyengine/bevy

Bevy 是 Rust 社区目前最活跃、最受欢迎的数据驱动游戏引擎（基于 ECS），代码仓库地址超级简单：

官方主仓库（核心代码 + 示例 + 文档）：  
https://github.com/bevyengine/bevy

- 这是 Bevy 的唯一核心仓库（monorepo 风格），包含：
  - 引擎源码（bevy/src/）
  - 大量示例（examples/ 目录超级丰富，从 2D/3D 到 UI、物理、音频、资产加载等）
  - Cargo.toml（workspace 配置，类似 Axum 那种）
  - 文档、CHANGELOG 等

直接 clone 就能开始玩：

```bash
git clone https://github.com/bevyengine/bevy.git
cd bevy
cargo run --example breakout  # 经典打砖块示例
# 或者 cargo run --example 3d_scene 等其他示例
```

其他常用地址（中文用户常看）：

- 官方网站：https://bevy.org （有 Quick Start、Roadmap、Showcase）
- API 文档（docs.rs）：https://docs.rs/bevy/latest/bevy/
- Bevy Cheat Book（超级好用的非官方中文/英文参考书）：https://bevy-cheatbook.github.io/ （有中文版翻译）
- Bevy Assets（社区资产）：https://bevyengine.org/assets/
- Discord（最活跃社区）：https://discord.gg/bevy

如果你想快速上手，推荐先跑官方示例：

1. clone 上面仓库
2. `cargo run --example hello_world` （最简单入门）
3. 再试 `cargo run --example 2d_scene` 或 `cargo run --example ui`

Bevy 的开发节奏很快（目前 0.14/0.15 左右版本在迭代，2026 年可能更高），仓库 star 已经 4.4w+，Rust 游戏引擎里绝对第一梯队。

想看 Cargo.toml 结构、具体示例代码、或对比 Axum 的 workspace 风格，也可以继续问～