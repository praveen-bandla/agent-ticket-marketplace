import json
from typing import Optional
import uuid
from pathlib import Path

from api.models.event import Event


EVENT_PATH = Path(__file__).parents[1] / 'data' / 'events.json'
VENUE_PATH = Path(__file__).parents[1] / 'data' / 'venues.json'

def load_json(path: Path):
    data = {}
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def get_events():
    return load_json(EVENT_PATH)

def get_venues():
    return load_json(VENUE_PATH)

def get_event_by_id(id: str):
    with open(EVENT_PATH, "r") as f:
        events = json.load(f)

    for event in events:
        if event.get("event_id") == id:
            return event

    raise ValueError(f"Event with id {id} not found")