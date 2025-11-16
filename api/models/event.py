"""
Class managing for an event.
"""

from pydantic import BaseModel
from pyparsing import Optional
from api.models.venue import Venue
import json
from configs import EVENTS_JSON


class Event(BaseModel):
    event_id: str
    name: str
    date: str
    venue: Venue

    @classmethod
    def get_event_by_id(cls, event_id: str) -> "Event":
        with open(EVENTS_JSON, "r") as f:
            events = json.load(f)

        event_data = next((e for e in events if e["event_id"] == event_id), None)
        # Load venue
        venue = Venue.from_venue_id(event_data["venue_id"])  # Assumes Venue has similar method
        
        return cls(
            event_id=event_data["event_id"],
            name=event_data["name"],
            date=event_data["date"],
            venue=venue
        )