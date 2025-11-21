# 知乎



redis集群





[redis 集群](https://www.zhihu.com/question/21419897/answer/89771396)


知乎收藏夹 一键导出到markdown文档
要将知乎收藏夹导出为Markdown文档，可以使用以下步骤：

1. 打开知乎网页并登录到你的帐户。
2. 导航到你的收藏夹页面，找到你想导出的收藏夹。
3. 打开浏览器的开发者工具。在大多数浏览器中，可以通过按下F12键或右键点击页面并选择"检查"或"开发者工具"来打开开发者工具。
4. 在开发者工具中，切换到"网络"选项卡。
5. 在知乎页面上滚动收藏夹，直到所有收藏项都加载完毕。
6. 在开发者工具的"网络"选项卡中，找到一个名为"activities"的请求。这是用于加载收藏夹内容的请求。
7. 右键点击该请求，然后选择"复制"，再选择"复制响应"。
8. 打开一个文本编辑器，例如Notepad++或Sublime Text。
9. 将复制的响应粘贴到文本编辑器中，并将文件保存为`.json`文件，例如`collection.json`。
10. 使用一个适当的脚本或工具来将JSON文件转换为Markdown格式。你可以编写自己的脚本或使用现有的工具。以下是一个简单的Python脚本示例，用于将收藏夹JSON转换为Markdown：

```python
import json

def convert_to_markdown(collection):
    markdown = ""
    for item in collection["data"]:
        title = item["title"]
        url = item["url"]
        markdown += f"- [{title}]({url})\n"

    return markdown

# 读取JSON文件
with open("collection.json", "r", encoding="utf-8") as file:
    json_data = file.read()

# 解析JSON数据
collection_data = json.loads(json_data)

# 转换为Markdown格式
markdown_output = convert_to_markdown(collection_data)

# 将Markdown保存到文件
with open("collection.md", "w", encoding="utf-8") as file:
    file.write(markdown_output)
```

在上面的示例中，你需要将`collection.json`替换为你保存的JSON文件的路径。脚本将生成一个名为`collection.md`的Markdown文件，其中包含收藏夹中的所有项的链接。

请注意，这只是一个简单的示例脚本，你可能需要根据你的JSON结构进行适当的调整和处理。

使用上述步骤和示例脚本，你应该能够将知乎收藏夹导出为Markdown文档。