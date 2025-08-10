from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("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"))

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Apa ibu kota Indonesia?"}]
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")