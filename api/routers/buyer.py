import json
from typing import List
import uuid
from fastapi import APIRouter
from api.core.market_negotiate import negotiate
from api.core.sub_market import SubMarket
from api.models.buyer import BuyerQuery
from api.models.event import Event
from api.services.buyer_service import append_bid, write_search_results
from api.services.event_service import get_event_by_id, get_events, get_venues
from api.services.openrouter_client import call_openrouter
from api.services.ticket_service import list_tickets

router = APIRouter(prefix="/buyer", tags=["buyer"])

@router.post("/intent")
async def get_buyer_intent(payload: BuyerQuery):
    """
    Takes buyer request inatural language from buyer and returns extracted intent.
    Uses OpenRouter LLM to parse fields + detect missing parameters.
    """
    system_prompt = """
    Extract these fields from the given buyer request. Check if these fields are provided. The buyer doesn't need to mention them explicitely and it's your job to understand the text.
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

    clarifying_questions if not provided already:
    "What artist or event are you looking for?",
    "Which venue or place do you prefer?",
    "How many tickets do you need?",
    "What is your starting offer per ticket?",
    "What is the most you're willing to pay per ticket?"

    Generate a single question that sounds natural to request values for any required missing fields.

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
        "question": "Question for list of missing items",
        "results": {
            "event_id": "...",
            "num_tickets": ...,
            "max_price": ...,
            "price": ...,
            "allowed_groups": [...],
            "sensitivity_to_price": "..."
        }
    }

    Rules:
    - If unsure about a field, leave it null.
    - Do NOT guess.
    - Do NOT ask questions here. The backend handles follow-up.
    - Only respond in the given JSON format.
    """

    if isinstance(payload.query, List) and len(payload.query) > 0:
        messages = payload.query
    else:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Events data: {json.dumps(get_events())}"},
            {"role": "system", "content": f"Venues data: {json.dumps(get_venues())}"},
            {"role": "user", "content": f"Buyer request: {payload.query}. Please extract the information"}
        ]

    response = call_openrouter(messages).replace('```json', '').replace('```', '')
    missing = json.loads(response)["missing"]
    if len(missing) > 0:
        messages.append({"role": "assistant", "content": response})
        return messages
    else:
        # filter
        bid = json.loads(response)["results"]
        bid["bid_id"] = str(uuid.uuid4())
        bid["buyer_id"] = str(uuid.uuid4())
        append_bid(bid)
        event = get_event_by_id(bid["event_id"])
        messages.pop(0)
        messages.append({"role": "user", "content": f"Bid parameters: {str(bid)}. Now the task has changed where you need to filter the tickets and return in the same list of JSON objects."})
        messages.append({"role": "system", "content": f"Tickets data: {json.dumps(list_tickets())}"})
        messages.append({"role": "system", "content": f"Find the list of tickets that match the criteria provided by the user. List the top 5 based on price and seat's group_id. The seat groups are prioritized base on this relationship: {event["reference_values"]}"})
        messages.append({"role": "assistant", "content": "I'll now filter the available tickets and prove output in clean JSON format..."})
        response = call_openrouter(messages).replace('```json', '').replace('```', '')
        tickets = json.loads(response)
        search_results = [{"bid_id": bid["bid_id"], "ticket_id": t["ticket_id"]} for t in tickets]
        write_search_results(search_results)
        messages.append({"role": "assistant", "content": response})
        return messages




from fastapi import WebSocket, WebSocketDisconnect

@router.websocket("/intent/ws")
async def ws_buyer_intent(websocket: WebSocket):
    system_prompt = """
    Extract these fields from the given buyer request. Check if these fields are provided. The buyer doesn't need to mention them explicitely and it's your job to understand the text.
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

    clarifying_questions if not provided already:
    "What artist or event are you looking for?",
    "Which venue or place do you prefer?",
    "How many tickets do you need?",
    "What is your starting offer per ticket?",
    "What is the most you're willing to pay per ticket?"

    Generate a single question that sounds natural to request values for any required missing fields.

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
        "question": "Question for list of missing items",
        "results": {
            "event_id": "event_001"
            "num_tickets": ...,
            "max_price": ...,
            "price": ...,
            "allowed_groups": [...],
            "sensitivity_to_price": "..."
        }
    }

    Rules:
    - If unsure about a field, leave it null.
    - Do NOT guess.
    - Do NOT ask questions here. The backend handles follow-up.
    - Only respond in the given JSON format.
    - Don't show reasoning
    """
    await websocket.accept()
    print("WS accepted")
    try:
        payload_raw = await websocket.receive_text()
        payload = BuyerQuery(**json.loads(payload_raw))

        print("Payload:", payload)

        # Build messages EXACTLY as before
        if isinstance(payload.query, list) and len(payload.query) > 1:
            payload.query.insert(0, {"role": "system", "content": system_prompt})
            messages = payload.query
        else:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "system", "content": f"Events data: {json.dumps(get_events())}"},
                {"role": "system", "content": f"Venues data: {json.dumps(get_venues())}"},
                {"role": "user", "content": f"Buyer request: {payload.query}. Please extract the information"}
            ]

        # 1) Send intermediate status
        await websocket.send_text(json.dumps({
            "phase": "parsing",
            "messages": messages
        }))

        print("Calling OpenRouter...")

        # 2) First LLM call
        response = call_openrouter(messages).replace("```json", "").replace("```", "")

        print("LLM response:", response[:1024])

        missing = safe_json_loads(response)["missing"]
        print(missing)
        print(messages)
        if len(missing) > 0:
            messages.append({"role": "assistant", "content": safe_json_loads(response)})
            await websocket.send_text(json.dumps({
                "phase": "extraction",
                "messages": messages
            }))
            return

        bid = safe_json_loads(response)["results"]
        bid["bid_id"] = str(uuid.uuid4())
        bid["buyer_id"] = str(uuid.uuid4())
        bid["event_id"] = 'event_001'
        append_bid(bid)

        # 3) Filtering tickets
        messages.pop(0)
        messages.append({"role": "assistant", "content": str(bid)})
        await websocket.send_text(json.dumps({
            "phase": "filtering",
            "messages": messages
        }))

        event = get_event_by_id(bid["event_id"])

        messages.append({"role": "user", "content": f"Bid parameters: {str(bid)}. Now the task has changed where you need to filter the tickets and return in the same list of tickets JSON objects."})

        messages.append({"role": "system", "content": f"Tickets data: {json.dumps(list_tickets())}"})
        messages.append({"role": "system", "content": f"Seat priority: Find the list of tickets that match the criteria provided by the user. List the top 5 based on price and seat's group_id. The seat groups are prioritized base on this relationship: {event['reference_values']}"})
        messages.append({"role": "system", "content": f"Rules: - Only respond in the given JSON format. - Don't show reasoning"})
        messages.append({"role": "assistant", "content": "I'll now filter the available tickets and prove output in clean JSON format..."})
        messages.append({"role": "assistant", "content": "Filtering tickets..."})

        response = call_openrouter(messages).replace("```json", "").replace("```", "")
        tickets = safe_json_loads(response)

        search_results = [{"bid_id": bid["bid_id"], "ticket_id": t["ticket_id"]} for t in tickets]
        write_search_results(search_results)

        await websocket.send_text(json.dumps({
            "phase": "final_tickets",
            "tickets": tickets
        }))

        await websocket.send_text(json.dumps({
            "phase": "final_transaction_start",
            "best_order": {
                "status": "In progress",
                "message": "Negotiating..."
            }
        }))

        try:
            results = await negotiate()
        except:
            pass

        await websocket.send_text(json.dumps({
            "phase": "final_transaction",
            "best_order": {
                "status": "failed",
                "message": "failed to reach a deal."
            }
        }))

        # if not results[0]:
        #     await websocket.send_text(json.dumps({
        #         "phase": "final_transaction",
        #         "best_order": {
        #             "status": "failed",
        #             "message": "failed to reach a deal."
        #         }
        #     }))
        # else:
        #     
        #     await websocket.send_text(json.dumps({
        #         "phase": "final_transaction",
        #         "best_order": {
        #             "status": "failed",
        #             "message": {
        #                 "ticket_id": results[0]["ticket_id"],
        #                 "price": str(results[0]["price"])
        #             }
        #         }}
        #     }))

        await websocket.close()

    except WebSocketDisconnect:
        print("Client disconnected")


import json  # if allowed, or write a simple fixer

def safe_json_loads(s: str):
    try:
        return json.loads(s)
    except:
        # attempt to extract a JSON object from text
        import re
        match = re.search(r"\{.*\}", s, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                pass
        print(s)
        raise ValueError("Model returned invalid JSON")
