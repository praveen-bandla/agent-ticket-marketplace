"""
Data model for a buyer in the ticket marketplace.
"""

from pydantic import BaseModel
from configs import BUYERS
import json

class Buyer(BaseModel):
    buyer_id: str
    buyer_name: str
    
    @classmethod
    def from_buyer_id(cls, buyer_id: str) -> "Buyer":
        with open(BUYERS, "r") as f:
            buyers = json.load(f)
        
        buyer_data = next((b for b in buyers if b["buyer_id"] == buyer_id), None)

        return cls(buyer_id=buyer_data["buyer_id"], buyer_name=buyer_data["name"])