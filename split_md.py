import os
from pathlib import Path

def split_markdown(markdown_file, output_folder, max_chars_per_file=1000):
    # 确保输出文件夹存在
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # 读取Markdown文件内容
    with open(markdown_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 分割内容到段落
    paragraphs = content.split('\n\n')
    current_chars = 0
    current_index = 1
    current_file_content = []

    for paragraph in paragraphs:
        # 检查当前段落是否会使文件超过字符限制
        if current_chars + len(paragraph) > max_chars_per_file:
            # 保存当前文件并开始新文件
            output_file = os.path.join(output_folder, f'paragraphs_{current_index}.md')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(current_file_content))
            current_index += 1
            current_file_content = [paragraph]  # 开始新文件的内容
            current_chars = len(paragraph)
        else:
            current_file_content.append(paragraph)
            current_chars += len(paragraph)

    # 保存最后一个文件
    if current_file_content:
        output_file = os.path.join(output_folder, f'paragraphs_{current_index}.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(current_file_content))

# 文件列表
markdown_files = [
    'D:\\AIGC\\auto-tags\\work.md',
    'D:\\AIGC\\auto-tags\\belief.md'
]

# 输出文件夹路径
output_folder = 'D:\\AIGC\\auto-tags\\split_md'

# 拆分每个Markdown文件
for markdown_file in markdown_files:
    split_markdown(markdown_file, output_folder)