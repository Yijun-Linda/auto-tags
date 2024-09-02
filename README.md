# auto-tags
Auto tag paragraphs

## Split markdown to meet the limition of long context
我有3000多行记录的文字段，想让大语言模型去分类。我恐怕上下文窗口不够用的，并且内容长了出错的概率也会很大，所以要拆分。我不知道md文件是否直接可以导出以多个段落的总字数接近1000字来分割成小md文件，让 AI 帮你写一个大md文件拆分成小md文件的程序，被保存到一个单独的md文件中，文件名会根据段落在Markdown文件中的顺序进行编号

我命名的脚本文件为 split_md.py

文件名为 work.md 文件的路径在 D:\AIGC\auto-tags\work.md。

文件名为 belief.md 文件的路径在 D:\AIGC\auto-tags\belief.md。

Then run split_md.py

## Prompt

我现在手里有一份md文字文件，里面大概有3000多行文字，我想用ai来给每一行打标签，请帮我生成：
- 5条标签，要详细，大约1段文字
- 完整的标签分类，大约10条
- 一条Prompt来根据输入的标签编号和标签返回对应的标签分类，返回JSON格式。
- 输入示例：[{"id": "123", "description": "XXXXX"}, {"id": "345", "description": "YYYY" }]
  返回示例：{"123", "cat1", "345": "cat2"}

### test in Gemini

8. 写程序调用 LLM 的 API 

教我如何调用 API 的事情，借助 LLM 帮忙，帮你写代码，这部分代码主要逻辑：

a) 每次读取一个小CSV文件
b) 解析CSV文件内容，得到文字的列表
c) 调用 LLM 的 API，输入前面调试好的 Prompt，输入CSV中的文字列表，按照Prompt设定好的输入格式输入
d) 解析 API 返回的结果，得到文字段和标签分类之间的对应关系
e) 保存为新的 CSV 文件，在原来的基础上给每个问字段加上标签分类
f) 直到生成所有新的带有分类的CSV文件

小CSV文件的命名规则是paragraphs_1，一直到paragraphs_36

调试好的 Prompt
你是一位经验丰富的归纳标签的工程师，你的任务是根据输入的标签编号和标签，将其分类到合适的标签类别。你的分类标准如下：

1. Writing 101
2. Life 101
3. Health 101
4. Business 101
5. Work 101
6. Networking 101
7. Mental 101

Prompt 示例
以下是用于根据输入的标签编号和描述返回对应标签分类的 Prompt：

```json
{
  "prompt": "根据输入的标签编号和描述，返回对应的标签分类，格式为 JSON。输入示例：[{'id': '123', 'description': 'Mental 101'}, {'id': '345', 'description': 'Business 101'}]，返回示例：{'123': 'Mental 101', '345': 'Business 101'}"
}

JSON 返回示例
```json
Copy
{
  "123": "Dating 101",
  "345": "Business 101"
}

以下是输入
```json
{
  "prompt": "根据输入的标签编号和标签描述，返回对应的标签分类。",
  "input": [
    {
      "id": "001",
      "description": "讨论了如何dating的内容。"
    },
    {
      "id": "002",
      "description": "分析了如何在职场摆脱学生思维。"
    }
  ],
  "output": {
    "001": "Dating 101",
    "002": "Work 101"
  }
}

## 写程序调用 LLM 的 API 

requirement：安装requests库，这个库将用于处理API调用

我用的是百度的千帆大模型




