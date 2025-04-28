from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from ollama import Client
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# OpenAI
def call_llm(prompt: str, model: str = "gpt-4o-mini") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=2048,
    )
    # print(response.choices[0].message.content)
    return json.loads(response.choices[0].message.content)


clientllama = Client(host="http://localhost:11434")


import re


# ollama
def call_llama3(prompt: str, model: str = "EEVE-Korean-10.8B") -> dict:
    response = clientllama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.5},
    )
    content = response["message"]["content"]

    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        json_content = match.group()
        return json.loads(json_content)
    else:
        raise ValueError("JSON 구조를 찾지 못했습니다. 받은 응답:", content)
