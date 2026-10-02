# 第 13 章 处理 PDF 和 Word 文档（原书 pp.约321–约350）

> `pypdf` 读 PDF、`python-docx` 读写 Word。基线：原书 Python 3.8；本目录按 3.12+ 校验。

## 本章地图

| 小节 | 内容 | 结论 |
|---|---|---|
| 13.1 PDF 提取 | `pypdf` | 原书 PyPDF2 已改名 |
| 13.2 PDF 合并/加密 | 多文件拼接 | 注意权限 |
| 13.3 Word | `python-docx` | 段落/样式 |

## 核心精讲

教学示意，不参与构建（需 `pip install pypdf python-docx`）：

```python
from pypdf import PdfReader, PdfWriter
reader = PdfReader("a.pdf")
print(len(reader.pages), reader.pages[0].extract_text())

from docx import Document
doc = Document("b.docx")
for p in doc.paragraphs:
    print(p.text)
```

## 版本演进

- `PyPDF2` 已重命名为 `pypdf`（🔧 以官方为准）；原书模块名过期。
- `python-docx` 稳定。

## 经典论文与原始文献

- pypdf 文档：https://pypdf.readthedocs.io/ 规范文档。
- python-docx 文档：https://python-docx.readthedocs.io/ 规范文档。

## 近年研究与工业界开源实践（2015–2026）

- 复杂 PDF（表格/版式）用 `pdfplumber`/`camelot`；OCR 用 `pytesseract`。

## 常见误区与本书需修正之处

| 原书说法 | 问题 | 2026 正确写法 |
|---|---|---|
| import PyPDF2 | 已改名 | import pypdf |
| PDF 文本必准 | 扫描件无文本层 | 用 OCR |

## 与其他章 / 其他书的联系

- 文件基础见 [08-读写文件.md](08-读写文件.md)。
