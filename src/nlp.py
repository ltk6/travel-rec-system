import os, json
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path


base_path = Path(__file__).resolve().parent.parent
env_path = base_path

load_dotenv(dotenv_path=env_path / ".env")

api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    raise ValueError("Lỗi: Không tìm thấy GROQ_API_KEY. Kiểm tra lại file .env!")

client = Groq(api_key=api_key)

ALL_TAGS = [
    "mountain", "beach", "nature", "food",
    "culture", "quiet", "cool_weather"
]

def extract_tags(user_input: str):
    prompt = f"""
Trả về JSON array các tags phù hợp từ danh sách:
{ALL_TAGS}

Input: "{user_input}"
"""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = res.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "")
    return json.loads(raw)