# Auto tag paragraphs

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

### test in Gemini or other LLM model

### 写程序调用 LLM 的 API 

在 GPT 4-o 里面问，教我如何调用 API 的事情，借助 LLM 帮忙，帮我写代码，

这部分代码主要逻辑：

a) 每次读取一个一份md文件

b) 解析md文件内容，得到文字的列表

c) 调用 LLM 的 API，输入前面调试好的 Prompt，输入md中的文字列表，按照 Prompt 设定好的输入格式输入

d) 解析 API 返回的结果，得到文字段和标签分类之间的对应关系

e) 保存为新的 md 文件，在原来的基础上给每个问字段加上标签分类

f) 直到生成所有新的带有分类的 md 文件

每一份分割后 md文件的命名规则是paragraphs_1，一直到paragraphs_67

调试 Prompt

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

{
  "123": "Dating 101",
  "345": "Business 101"
}

"以下是输入"
{
  "prompt": "根据输入的标签编号和标签描述，返回对应的标签分类。",
  "input": [
    {
      "id": "001",
      "description": "讨论了如何 Mental peace 的内容。"
    },
    {
      "id": "002",
      "description": "分析了如何在职场摆脱学生思维。"
    }
  ],
  "output": {
    "001": "Mental 101",
    "002": "Work 101"
  }
}
```

## 写程序调用 LLM 的 API 

我采用的是本地大模型部署

Docker Desktop，来提供部署本地容器化的大模型的环境
  - 拉取镜像
  - 运行容器
  - 配置必要的参数，如端口映射、存储路径

FastGPT、OneAPI

FastGPT 和 OneAPI 的 API 文档，了解如何进行身份验证、发送请求和处理响应。

在 Python 中可以使用 `requests` 库，配置 API 密钥或身份验证信息，发送请求并处理响应。



以下展示如何使用 `requests` 库调用一个 qwen 2:0.5b 的大模型 API：

```python
import requests

# API 地址
api_url = "http://localhost:8080/generate"

# 请求参数
data = {
    "prompt": "Hello, world!",
    "max_tokens": 50
}

# 发送请求
response = requests.post(api_url, json=data)

# 处理响应
if response.status_code == 200:
    result = response.json()
    generated_text = result["generated_text"]
    print(generated_text)
else:
    print(f"Error: {response.status_code}")
```

