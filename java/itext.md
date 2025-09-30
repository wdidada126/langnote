# itext

在PDF表格中实现类似Excel的单元格合并功能，使用iText库可以轻松完成。下面为你详细介绍如何使用iText 5和iText 7两种版本来实现这一需求。
基础概念：单元格合并的两种方式
单元格合并主要通过设置单元格的列跨度和行跨度来实现：
横向合并（跨列）：使用 setColspan 方法，让一个单元格占据同一行中的多个列。
纵向合并（跨行）：使用 setRowspan 方法，让一个单元格占据同一列中的多个行。
使用iText 5实现合并
iText 5是较早的版本，其核心操作对象是 PdfPTable 和 PdfPCell。
代码示例：创建跨列和跨行的表格
```java
import com.itextpdf.text.Document;
import com.itextpdf.text.pdf.PdfPTable;
import com.itextpdf.text.pdf.PdfPCell;

// 创建一个3列的表格
PdfPTable table = new PdfPTable(3);

// 1. 创建一个跨3列的标题单元格（横向合并）
PdfPCell headerCell = new PdfPCell(new Paragraph("这是合并后的表头"));
headerCell.setColspan(3); // 关键代码：设置跨3列
table.addCell(headerCell);

// 2. 创建一个跨2行的单元格（纵向合并）
PdfPCell rowSpanCell = new PdfPCell(new Paragraph("跨两行"));
rowSpanCell.setRowspan(2); // 关键代码：设置跨2行
table.addCell(rowSpanCell);

// 添加其余单元格
table.addCell("第1行，第2列");
table.addCell("第1行，第3列");
// 注意：因为第二列的第一个单元格跨了2行，所以下一行这里会空出它的位置
table.addCell("第2行，第2列"); 
table.addCell("第2行，第3列");


使用 iText 7 实现合并

iText 7是较新的版本，API设计更为现代。其核心操作对象是 Table 和 Cell。

代码示例：创建跨列和跨行的表格

import com.itextpdf.layout.element.Table;
import com.itextpdf.layout.element.Cell;

// 定义一个3列的表格，并设置列宽
float[] columnWidths = {2f, 1f, 1f};
Table table = new Table(columnWidths);

// 1. 创建一个跨3列的标题单元格（横向合并）
Cell mergedHeader = new Cell(1, 3); // 关键代码：参数表示（跨1行，跨3列）
mergedHeader.add("这是合并后的表头");
table.addCell(mergedHeader);

// 2. 创建一个跨2行的单元格（纵向合并）
Cell rowSpanCell = new Cell(2, 1); // 关键代码：参数表示（跨2行，跨1列）
rowSpanCell.add("跨两行");
table.addCell(rowSpanCell);

// 添加其余单元格
table.addCell(new Cell().add("第1行，第2列"));
table.addCell(new Cell().add("第1行，第3列"));
table.addCell(new Cell().add("第2行，第2列"));
table.addCell(new Cell().add("第2行，第3列"));

```

在iText 7中，Cell 的构造函数 Cell(int rowspan, int colspan) 让合并操作更加直观。
注意事项与进阶技巧
表格宽度设置：在iText 5中，如果使用 setTotalWidth 方法设置了精确的表格宽度，通常需要调用 table.setLockedWidth(true) 来锁定宽度，防止布局自动调整。
内容居中显示：合并后的单元格内容默认可能不是居中显示。你可以使用以下方法实现居中：
iText 5: 对 PdfPCell 使用 setHorizontalAlignment(Element.ALIGN_CENTER)。
iText 7: 对 Cell 使用 setTextAlignment(TextAlignment.CENTER)。
边框与样式：可以为单元格设置边框、背景色等属性，使其更美观。
// iText 5 示例：设置单元格无边框和背景色
cell.setBorder(PdfPCell.NO_BORDER);
cell.setBackgroundColor(new BaseColor(0xDD, 0xDD, 0xDD));
表格嵌套：iText支持将一个完整的表格作为单元格添加到另一个表格中，用于创建复杂的布局。
希望这些详细的说明和代码示例能帮助你在PDF中实现所需的表格效果。如果你在具体操作中遇到问题，比如对样式调整有更细致的要求，可以随时提出。