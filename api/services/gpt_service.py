from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY,
)

def call_gpt(messages, model="openai/gpt-5-nano"):
    completion = client.chat.completions.create(
      model=model,
      messages=[
        {
          "role": "user",
          "content": messages
        }
      ]
    )
    return completion.choices[0].message.content