"""
Wrapper for calling OpenRouter LLM models.
Handles headers, routing, rate limits, and errors.
"""

import os

import requests
import json

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def call_openrouter(messages, model="google/gemma-3-27b-it:free"):
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
    return response.json()['choices'][0]['message']['content']
