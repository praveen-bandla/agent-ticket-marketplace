import json
from typing import List
from fastapi import APIRouter
from api.models.buyer import BuyerQuery
from api.services.openrouter_client import call_openrouter

router = APIRouter(prefix="/buyer", tags=["buyer"])

@router.post("/intent")
async def get_buyer_intent(payload: BuyerQuery):
    """
    Takes natural language from buyer and returns extracted intent.
    Uses OpenRouter LLM to parse fields + detect missing parameters.
    """
    system_prompt = """
    You are an assistant that extracts ticket-purchase intent from natural language.
    Required fields:
    - event_name
    - venue
    - num_tickets
    - price
    - max_price

    Optional:
    - seat_type (default "any")
    - sensitivity (default "normal")
    - certainty (default "definitely")

    clarifying_questions = {
        "event_name": "What artist or event are you looking for?",
        "venue": "Which venue or place do you prefer?",
        "num_tickets": "How many tickets do you need?",
        "ask_price": "What is your starting offer per ticket?",
        "max_price": "What is the most you're willing to pay per ticket?"
    }

    Generate a single compund question that sounds natural in case of multiple missing fields.

    Respond ONLY in JSON format with:
    {
        "extracted": {
            "event_name": "...",
            "num_tickets": ...,
            "max_price": ...,
            "seat_type": "...",
            "sensitivity": "...",
            "certainty": "..."
        },
        "missing": ["venue", "price"],
        "question": "Question for list of missing items"
    }

    Rules:
    - If unsure about a field, leave it null.
    - Do NOT guess.
    - Do NOT ask questions here. The backend handles follow-up.
    """

    if isinstance(payload.query, List) and len(payload.query) > 0:
        messages = payload.query
    else:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": payload.query}
        ]

    response = call_openrouter(messages)
    missing = json.loads(response)["missing"]
    if (missing) > 0:
        messages.append({"role": "assistant", "content": response})
        return messages
    else:
        # filter
        return None
