# hermes_agent
📁 Your files (all in ~/.hermes/):

   Config:    ~/.hermes/config.yaml
   API Keys:  ~/.hermes/.env
   Data:      ~/.hermes/cron/, sessions/, logs/
   Code:      ~/.hermes/hermes-agent/

─────────────────────────────────────────────────────────

Commands:

   hermes              Start chatting
   hermes setup        Configure API keys & settings
   hermes config       View/edit configuration
   hermes config edit  Open config in editor
   hermes gateway install Install gateway service (messaging + cron)
   hermes update       Update to latest version


支持
Hermes Agent 明确支持 macOS 12.7（Monterey）。
 
一、官方要求
 
- 最低 macOS 版本：12.0 (Monterey) 及以上
- 你的版本 12.7：完全在兼容范围内
- 架构：同时支持 Intel 和 Apple Silicon
 
二、mac 12.7 安装要点
 
1. 必备工具bash
  
# 安装命令行工具（必须）
xcode-select --install
# 安装 Git
brew install git
 
2. 一键安装bash
  
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```[[__LINK_ICON]](https://github.com/ai-native-agentic/hermes-agent/blob/main/README.md?f_link_type=f_linkinlinenote&flow_extra=eyJpbmxpbmVfZGlzcGxheV9wb3NpdGlvbiI6MCwiZG9jX3Bvc2l0aW9uIjowLCJkb2NfaWQiOiJlMjdkNDUzNjEyOWI2YThkLWEzZjNhOTAzZDcyZjg5MGQifQ%3D%3D&inline_doc_id=e27d4536129b6a8d-a3f3a903d72f890d)

 
3. 加载环境bash
  
source ~/.zshrc  # 或 ~/.bashrc
```[[__LINK_ICON]](https://hermes-agent.ai/how-to/install-hermes-agent?f_link_type=f_linkinlinenote&flow_extra=eyJkb2NfcG9zaXRpb24iOjAsImRvY19pZCI6ImE5ZWI2YWFjYTJmNGUyZjQtNGY4NTUwNDE3OWFhNDA4NyIsImlubGluZV9kaXNwbGF5X3Bvc2l0aW9uIjowfQ%3D%3D&inline_doc_id=a9eb6aaca2f4e2f4-4f85504179aa4087)

 
 
三、已知注意事项（mac 12 专属）
 
- Python 3.11：脚本会自动安装，无需手动处理 
- 性能：本地跑大模型（Ollama）会比 Ventura/Sonoma 慢，但 API 模式完全流畅
- 钉钉网关：mac 12.7 上 正常运行，无兼容性问题
 
要不要我给你一份在 macOS 12.7 上安装 Hermes 并接入钉钉的完整步骤清单？

