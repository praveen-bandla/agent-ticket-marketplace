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

    Respond ONLY in JSON with:
    {
        "extracted": {
            "event_name": "...",
            "num_tickets": ...,
            "max_price": ...,
            "seat_type": "...",
            "sensitivity": "...",
            "certainty": "..."
        },
        "missing": ["venue", "price"]
    }

    Rules:
    - If unsure about a field, leave it null.
    - Do NOT guess.
    - Do NOT ask questions here. The backend handles follow-up.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": payload.query}
    ]

    response = 'test'#call_openrouter(messages)
    return [{"role": "user", "content": payload.query}, {"role": "system", "content": response}]
