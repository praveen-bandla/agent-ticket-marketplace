"""
Data model for a buyer in the ticket marketplace.
"""

from typing import Any, Dict, List, Union
from pydantic import BaseModel
from configs import BUYERS
import json

class Buyer(BaseModel):
    buyer_id: str
    buyer_name: str
    
    @classmethod
    def get_buyer_by_id(cls, buyer_id: str) -> "Buyer":
        with open(BUYERS, "r") as f:
            buyers = json.load(f)
        
        buyer_data = next((b for b in buyers if b["buyer_id"] == buyer_id), None)
        # TODO: Handle exception
        return cls(buyer_id=buyer_data["buyer_id"], buyer_name=buyer_data["name"]) # type: ignore
    

class BuyerQuery(BaseModel):
    query: Union[str, List[Dict[str, Any]]]

class BuyerIntent(BaseModel):
    event_name: str
    venue: str
    num_tickets: int
    price: float
    max_price: float
    seat_type: str = "any"
    sensitivity: str = "normal"
    certainty: str = "definitely"
