import os
import requests
import sys

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY

def load_diff():
    with open("diff.txt", "r", encoding="utf-8") as f:
        return f.read()

def review_code(diff_text):
    prompt = f"""
你是一位高级代码审查员。请评估以下 Git diff 中的代码变更，并指出其中是否存在 **致命错误**（包括：安全问题、数据丢失、死循环、SQL注入、权限问题等）。

如果存在，请返回以下格式：
```
FATAL: 存在致命错误
原因: xxx
建议: xxx
```

如果只是轻微问题，请返回：
```
OK: 无致命错误
建议: xxx
```

以下是代码差异：
```diff
{diff_text}
```
"""
    response = requests.post(
        GEMINI_URL,
        headers={"Content-Type": "application/json"},
        json={
            "contents": [{"parts": [{"text": prompt}]}]
        }
    )

    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def main():
    diff = load_diff()
    result = review_code(diff)

    print("Gemini Review Result:\n", result)

    if "FATAL" in result:
        print("❌ 检测到致命错误，终止推送。")
        sys.exit(1)
    else:
        print("✅ 没有检测到致命错误，允许推送。")

if __name__ == "__main__":
    main()
