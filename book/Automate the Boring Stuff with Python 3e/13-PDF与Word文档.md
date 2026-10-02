# 13 · PDF 与 Word 文档

> 一句话定位：`pypdf` 读/合并/切割 PDF，`python-docx` 生成 Word——文档自动化。
> 原书 pp. 英文 3e 第 13 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 13.1 | 读 PDF 文本 | `pypdf` |
| 13.2 | 合并/切割 | `PdfWriter` |
| 13.3 | 加密/解密 | 略 |
| 13.4 | 写 Word | `python-docx` |
| 13.5 | 读 Word | `Document` |

## 核心精讲

```
# 教学示意，不参与构建
from pypdf import PdfReader, PdfWriter
reader = PdfReader('a.pdf')
print(reader.pages[0].extract_text())        # 提取首页文本
writer = PdfWriter()
writer.add_page(reader.pages[0])
writer.write('first_page.pdf')

from docx import Document
doc = Document()
doc.add_heading('报告', level=1)
doc.add_paragraph('正文……')
doc.save('report.docx')
```

- **3e 用 `pypdf`**（原 `PyPDF2`/`PyPDF4` 已合并入 `pypdf`），统一 API。
- `PdfReader.pages` 是页列表；`extract_text()` 提取文本（复杂排版可能不准）。
- `python-docx` 创建/修改 `.docx`：标题、段落、表格、图片。

## 版本演进

- **3e 关键变化**：PDF 库从 `PyPDF2` 迁移到 `pypdf`（维护更活跃、API 统一）。
- `python-docx` 长期稳定；读旧 `.doc` 需先转 `.docx`。
- PDF 文本提取对扫描件无效，需 OCR（`pytesseract`）。

## 经典论文与原始文献

- pypdf 文档：https://pypdf.readthedocs.io/
- python-docx 文档：https://python-docx.readthedocs.io/

## 近年研究与工业界开源实践（2015–2026）

- `pdfplumber` 提供精准文本与表格提取（基于 `pdfminer`）。
- `docx2pdf`/`libreoffice --headless` 做格式转换。
- `PyMuPDF`(fitz) 在渲染/提取上高性能。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 2e 用 `PyPDF2` | 3e 统一 `pypdf`；`PyPDF2` 已弃用 |
| 认为 PDF 文本可完美提取 | 扫描件/复杂排版需 OCR/专用库 |
| `python-docx` 改样式难 | 用模板 + 替换占位符更稳 |
| 🔧 本书未提 `pdfplumber` | 表格提取优先 `pdfplumber` |

## 与其他章 / 其他书的联系

- 文件 I/O 见[第08章 读写文件](08-读写文件.md)。
- 批量文档处理常配合[第09章 组织文件](09-组织文件.md)。
