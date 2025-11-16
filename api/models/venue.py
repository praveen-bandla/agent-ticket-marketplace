"""
Represents a venue where events take place.
"""

from pydantic import BaseModel
import json
from configs import VENUES_JSON

class Venue(BaseModel):
    venue_id: str
    name: str
    city: str
    seating_groups: list[str]
    valuation_map: list[str]


    @classmethod
    def from_venue_id(cls, venue_id: str) -> "Venue":

        with open("api/data/venues.json", "r") as f:
            venues = json.load(f)

        venue_data = next((v for v in venues if v["venue_id"] == venue_id), None)
        
        return cls(
            venue_id=venue_data["venue_id"],
            name=venue_data["name"],
            city=venue_data["city"],
            seating_groups=[group["group_id"] for group in venue_data["seating_groups"]],
            valuation_map=venue_data["valuation_map"]
        )