"""
Includes class for bid, representing a bid in the marketplace.
"""

from pydantic import BaseModel

class Bid(BaseModel):
    bid_id: str
    buyer_id: str
    event_id: str
    num_tickets: int
    max_price: float
    price: float
    allowed_groups: list[str]
    sensitivity_to_price: str