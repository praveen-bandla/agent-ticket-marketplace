"""
Wrapper for calling OpenRouter LLM models.
Handles headers, routing, rate limits, and errors.
"""

import os

import requests
import json
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"



def call_openrouter(messages, model="google/gemma-3-27b-it:free") -> str:
    response = requests.post(
        url = OPENROUTER_URL,
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}"
        },
        data=json.dumps({
            "model": model,
            "messages": messages
        })
    )
    # if there is no response.json()['choices], print the response text for debugging
    if 'choices' not in response.json():
        print("Error response from OpenRouter:", response.text)
        raise ValueError("Invalid response from OpenRouter API")
    return response.json()['choices'][0]['message']['content']

def call_openrouter_with_prompt(prompt, model="google/gemma-3-27b-it:free"):
    messages = [{
        "role": "user",
        "content": prompt
    }]
    return call_openrouter(messages, model=model)