#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import re
import requests

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("❌ Error: missing GEMINI_API_KEY environment variable")
    sys.exit(1)

MODEL_ID = "gemini-2.5-pro"
GENERATE_URL = (
    f"https://generativelanguage.googleapis.com/v1/models/{MODEL_ID}:generateContent"
    f"?key={API_KEY}"
)

def load_diff():
    try:
        content = open("diff.txt", "r", encoding="utf-8").read()
        print("🧾 diff.txt 内容预览:\n", content[:500])
        return content
    except FileNotFoundError:
        print("⚠️ Warning: diff.txt not found — 跳过审核（默认通过）")
        return ""

def review_code(diff_text: str) -> str:
    prompt = f"""
你是一个专业的 AI 代码审查助手，请对以下 Git diff 进行分析并使用 **Markdown 格式** 输出结构化审查结果。

请包含三部分（必须使用如下标题）：

---

### 📌 代码变更摘要
简要说明本次 diff 中代码的新增、修改或删除内容。

### 🛡 审查结论（结构化）
- 如果发现致命错误，请输出：
  ```
  FATAL: 存在致命错误
  原因: xxx
  建议: xxx
  ```
- 如果没有致命错误，请输出：
  ```
  OK: 无致命错误
  建议: xxx
  ```

### 💡 分文件建议列表（可定位）
请使用如下结构化格式，按文件分组：

- 文件: src/example.cpp
  - 行号: 42
    - 问题: 使用未初始化变量
    - 建议: 将变量初始化为默认值以避免 UB

---

以下是 Git diff 内容：
```diff
{diff_text}
```
"""

    body = {
        "model": MODEL_ID,
        "contents": [{"role": "user", "parts": [{"text": prompt.strip()}]}],
        "generationConfig": {
            "candidateCount": 1,
            "temperature": 0.2,
        }
    }

    for attempt in range(3):
        resp = requests.post(GENERATE_URL, json=body)
        if resp.status_code == 500:
            print(f"⚠️ 第 {attempt+1} 次尝试失败，重试中...")
            time.sleep(2)
            continue
        break
    try:
        resp.raise_for_status()
    except Exception:
        print("❌ 调用 GenerateContent 接口失败：", resp.status_code, resp.text)
        sys.exit(1)

    data = resp.json()
    print("🔍 Gemini Raw Response:\n", json.dumps(data, indent=2, ensure_ascii=False))

    if "candidates" not in data or not data["candidates"]:
        print("❌ 未在响应中找到 candidates 字段")
        sys.exit(1)

    content = data["candidates"][0].get("content", {})
    parts = content.get("parts", [])
    if not parts:
        print("❌ 响应结构异常，parts 为空")
        sys.exit(1)

    return parts[0].get("text", "")

import re

def extract_inline_comments_force_all(text: str):
    import re

    comments = []
    current_file = None
    current_line = None
    current_problem = None
    current_suggestion = None

    lines = text.splitlines()
    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("- 文件:"):
            current_file = re.sub(r"- 文件:\s*`?(.*?)`?$", r"\1", line).strip()

        elif line.startswith("- 行号:"):
            try:
                current_line = int(line.split(":", 1)[1].strip())
            except:
                continue

        elif line.startswith("- 问题:"):
            current_problem = line.split(":", 1)[1].strip()

        elif line.startswith("- 建议:"):
            current_suggestion = line.split(":", 1)[1].strip()

        if current_file and current_line and current_problem and current_suggestion:
            comments.append({
                "file": current_file,
                "line": current_line,
                "body": f"> ⚠️ **{current_problem}**\n> 💡 **建议**：{current_suggestion}"
            })
            current_line = None
            current_problem = None
            current_suggestion = None  # ⬅️ 注意：不重置文件名，允许多条出现在同一文件

    return comments

def main():
    diff = load_diff()
    if not diff.strip():
        print("📭 diff.txt is empty. Skipping review.")
        result = "OK: 无致命错误\n建议: 没有检测到任何变更，跳过审查。"
    else:
        result = review_code(diff)

    print("📝 Gemini Review Result:\n", result)

    with open("review_output.txt", "w", encoding="utf-8") as f:
        f.write(result)

    inline_comments = extract_inline_comments(result)
    with open("inline_comments.json", "w", encoding="utf-8") as f:
        json.dump(inline_comments, f, indent=2, ensure_ascii=False)
        print("✅ 解析出可定位评论数量:", len(inline_comments))

    if result.strip().startswith("FATAL"):
        print("❌ 检测到致命错误，终止流程。")
        sys.exit(1)
    else:
        print("✅ 无致命错误，允许推送。")

if __name__ == "__main__":
    main()
