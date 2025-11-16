"""
Includes class for bid, representing a bid in the marketplace.
"""

from pydantic import BaseModel
from configs import BIDS_JSON
import json

class Bid(BaseModel):
    bid_id: str
    buyer_id: str
    event_id: str
    num_tickets: int
    max_price: float
    price: float
    allowed_groups: list[str]
    sensitivity_to_price: str

    # add a function to load a bid from json using bid_id

    @classmethod
    def get_bid_by_id(cls, bid_id: str):
        # Implementation to load bid from JSON
        with open(BIDS_JSON, "r") as f:
            bids = json.load(f)
        bid_data = next((b for b in bids if b["bid_id"] == bid_id), None)
        if bid_data:
            return cls(**bid_data)
        else:
            raise ValueError(f"Bid with id {bid_id} not found")

    def get_bid_price(self) -> float:
        return self.price

    def get_bid_quantity(self) -> int:
        return self.num_tickets