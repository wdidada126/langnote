# BPO-AVASR：通过双焦点偏好优化增强音视频语音识别

> 来源：日常笔记 `2026/202603/20260313.md`（ASR 领域「多模态语音识别」方向第 2 条）
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | Enhancing Audiovisual Speech Recognition through Bifocal Preference Optimization |
| 作者 | Yihan Wu, Yichen Lu, Yifan Peng, Xihua Wang, Ruihua Song, Shinji Watanabe（共 6 人） |
| arXiv | 2412.19005v1 |
| 提交 / 更新 | 2024-12-26 / 2024-12-26 |
| 发表 | **AAAI 2025**（arXiv comment 标注 Accepted） |
| 链接 | https://arxiv.org/abs/2412.19005 |
| 官方代码 | 源笔记未列；arXiv 摘要亦未给出代码链接 |
| 主题 | 音视频语音识别（AV-ASR）/ 偏好优化 |

## 一句话结论

以往 AV-ASR 只是把**纯音频 ASR 模型**在音视频数据上微调、优化常规 ASR 目标，**忽视了视觉特征与真实视频中的常见错误**；BPO-AVASR 用**双焦点偏好优化**——从**输入侧**（扰动音频或视觉）与**输出侧**（改写转写文本）两个焦点构造偏好数据——显著提升真实视频场景的识别准确率，超越此前 SOTA。

## 核心要点

- **任务**：AV-ASR 借助视觉信号提升语音识别准确率。
- **难点**：在**无约束的真实世界场景**中尤为困难——**噪声声学环境**、**自发口语（spontaneous speech）**、以及**视觉信息使用的不确定性**。
- **既有做法的缺陷**：多数工作只是在音视频数据集上微调 audio-only ASR 模型，优化常规 ASR 目标，**既忽视视觉特征，也忽视无约束视频场景下的常见错误**。
- **偏好数据构造（两个焦点 / bifocal）**：
  1. **输入侧**：通过操纵 **audio 或 vision 输入**来模拟 AV-ASR 中出现的常见错误
  2. **输出侧**：通过**重写输出转写**来模拟错误
- **方法 BPO-AVASR**：Bifocal Preference Optimization，**同时利用 input-side 与 output-side 偏好**来改进 AV-ASR 模型。
- **效果**：大量实验表明在多个域上显著提升识别准确率，在**真实世界视频语音识别**上超越此前 SOTA。

## 代码仓库

| 仓库 | 说明 |
|------|------|
| 本文官方仓库 | 源笔记未列，arXiv 摘要亦未给出代码链接 |
| ESPnet | 作者含 Shinji Watanabe（CMU），其维护的 ESPnet 是 AV-ASR 相关实现最常用的落点 |

## 源笔记摘录

> 2. 多模态语音识别（AV-ASR）
> • 论文标题：BPO-AVASR (Bifocal Preference Optimization for Audiovisual Speech Recognition)
> • 核心内容：来自人大与CMU的研究，提出双焦点偏好优化方法，通过优化音视频输入和输出偏好，在真实视频场景下显著提升识别准确率。
> • 论文链接：https://arxiv.org/abs/2412.19005

## 勘误与提醒

- ✔ 源笔记的概括准确：「双焦点偏好优化」「优化音视频输入和输出偏好」「真实视频场景提升显著」都与论文吻合。
- ℹ️ 源笔记写「来自人大与 CMU 的研究」：作者列表中 **Yihan Wu、Yichen Lu、Ruihua Song**（中国人民大学）与 **Shinji Watanabe**（CMU）对应，判断成立 ✔。
- ℹ️ 源笔记未记发表会议；arXiv comment 确认为 **AAAI 2025**，此处已补齐。
- ℹ️ 源笔记未给代码仓库，本文也确实未公开明确官方实现，动手可从 ESPnet 的 AV-ASR 配方入手。

## BibTeX

```bibtex
@inproceedings{bpoavasr2025,
  title     = {Enhancing Audiovisual Speech Recognition through Bifocal Preference Optimization},
  author    = {Wu, Yihan and Lu, Yichen and Peng, Yifan and Wang, Xihua and Song, Ruihua and Watanabe, Shinji},
  booktitle = {AAAI 2025},
  year      = {2025},
  eprint    = {2412.19005},
  url       = {https://arxiv.org/abs/2412.19005}
}
```
