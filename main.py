import os
import json
import requests

from prompt import get_prompt

def read_md_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.readlines()

def call_llm_api(prompt, input_data):
    with open('config.json', 'r') as f:
        config = json.load(f)
    api_key = config["open_ai_api_key"]
    api_base = config["open_ai_api_base"]
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "prompt": prompt,
        "input": input_data
    }
    response = requests.post(api_base, headers=headers, json=data)
    print("Full API response:", response.json())
    return response.json()

def process_markdown_with_llm(file_path, prompt):
    lines = read_md_file(file_path)
    input_data = [{"id": str(i), "description": line.strip()} for i, line in enumerate(lines)]
    response = call_llm_api(prompt, input_data)
    new_content = ""
    for i, line in enumerate(lines):
        if str(i) in response:
            new_content += f"{response[str(i)]}: {line}\n"
        else:
            print(f"Key {str(i)} not found in response. Description: {line}")
            new_content += f"Unknown: {line}\n"
    tags_md_path = "tags_md"
    if not os.path.exists(tags_md_path):
        os.makedirs(tags_md_path)
    new_file_path = os.path.join(tags_md_path, os.path.basename(file_path))
    save_new_md_file(new_file_path, new_content)

def save_new_md_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    prompt_data = get_prompt()
    folder_path = "D:/AIGC/auto-tags/split_md"
    for i in range(1, 68):
        file_name = f"paragraphs_{i}.md"
        file_path = os.path.join(folder_path, file_name)
        process_markdown_with_llm(file_path, prompt_data["prompt"])

if __name__ == "__main__":
    main()