#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
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

LISTMODELS_URL = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"

def load_diff():
    try:
        content = open("diff.txt", "r", encoding="utf-8").read()
        print("🧾 diff.txt 内容预览:\n", content[:500])  # 最多打印前 500 字符
        return content
    except FileNotFoundError:
        print("⚠️ Warning: diff.txt not found — 跳过审核（默认通过）")
        return ""

def ensure_model_available():
    try:
        resp = requests.get(LISTMODELS_URL)
        resp.raise_for_status()
        obj = resp.json()
        if "models" in obj:
            names = [m["name"].split("/")[-1] for m in obj["models"]]
            if MODEL_ID not in names:
                print(f"❌ Error: 模型 {MODEL_ID} 不在 ListModels 返回列表中。")
                print("✅ 可用模型包括：", ", ".join(names[:10]), "...")
                sys.exit(1)
        else:
            print("⚠️ 无 models 字段，ListModels 返回异常内容。")
    except Exception as e:
        print("❌ 调用 ListModels 接口失败：", e)
        print("📝 响应内容：", resp.text if 'resp' in locals() else "")
        sys.exit(1)

def review_code(diff_text: str) -> str:
    prompt = f"""
你是一位高级代码审查员。请评估以下 Git diff 中的代码变更，并指出是否包含 **致命错误**（如：安全漏洞、数据丢失、无限循环、SQL 注入、权限问题等）。

如果发现致命错误，请按以下格式回复：
```
FATAL: 存在致命错误
原因: xxxxx
建议: xxxxx
```

如果仅有轻微问题或均可接受，请回复：
```
OK: 无致命错误
建议: xxxxx
```

以下是代码差异：
```diff
{diff_text}
```
"""
    body = {
        "model": MODEL_ID,
        "contents": [
            {"role": "user", "parts": [{"text": prompt.strip()}]}
        ],
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
        print("❌ 未在响应中找到 candidates 字段，内容：", data)
        sys.exit(1)

    candidate = data["candidates"][0]
    parts = candidate.get("content", {}).get("parts", [])
    if not parts:
        print("❌ 响应结构异常，parts 列表为空")
        sys.exit(1)

    return parts[0].get("text", "")

def main():
    diff_txt = load_diff()
    result = review_code(diff_txt)
    print("\n📝 Gemini Review Result:")
    print(result)
    if "FATAL" in result.splitlines()[0]:
        print("❌ 检测到致命错误，终止流程。")
        sys.exit(1)
    else:
        print("✅ 无致命错误，允许推送。")

if __name__ == "__main__":
    main()
