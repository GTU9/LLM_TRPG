from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def clean_json(text: str) -> str:
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    text = text.strip()
    return text


def call_llm(prompt: str, model: str = "gpt-4o-mini") -> dict:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=2048,
    )
    content = response.choices[0].message.content
    content = clean_json(content)
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"[JSON 파싱 오류] {e}")
        print(f"[원본 응답]\n{content}")
        raise


# ollama (로컬 모델)
# from ollama import Client
# clientllama = Client(host="http://localhost:11434")
#
# def call_llama3(prompt: str, model: str = "EEVE-Korean-10.8B") -> dict:
#     response = clientllama.chat(
#         model=model,
#         messages=[{"role": "user", "content": prompt}],
#         options={"temperature": 0.5},
#     )
#     content = response["message"]["content"]
#     match = re.search(r"\{.*\}", content, re.DOTALL)
#     if match:
#         return json.loads(match.group())
#     else:
#         raise ValueError("JSON 구조를 찾지 못했습니다. 받은 응답:", content)
