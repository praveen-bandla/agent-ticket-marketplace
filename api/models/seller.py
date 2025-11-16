"""
Data model for a seller in the ticket marketplace.
"""

from pydantic import BaseModel
from configs import SELLERS
import json


class Seller(BaseModel):
    seller_id: str
    seller_name: str

    @classmethod
    def get_seller_by_id(cls, seller_id: str) -> "Seller":
        with open(SELLERS, "r") as f:
            sellers = json.load(f)

        seller_data = next((s for s in sellers if s["seller_id"] == seller_id), None)

        return cls(seller_id=seller_data["seller_id"], seller_name=seller_data["name"])
    