"""
Defines data models used in the ticket marketplace API.

This module contains the Pydantic model representing a ticket listing.
It is used for input validation, serialization, and consistent data
handling across the service and routing layers.
"""

from pydantic import BaseModel
from configs import TICKETS_JSON
import json

class Ticket(BaseModel):
    ticket_id: str | None = None
    seller_id: str
    event_id: str
    group_id: str
    quantity: int
    price: float
    min_price: float
    date: str
    sensitivity: str
    immediate_sale: bool

    @classmethod
    def get_ticket_by_id(cls, ticket_id: str):
        # Implementation to load ticket from JSON
        with open(TICKETS_JSON, "r") as f:
            tickets = json.load(f)
        ticket_data = next((t for t in tickets if t["ticket_id"] == ticket_id), None)
        if ticket_data:
            return cls(**ticket_data)
        else:
            raise ValueError(f"Ticket with id {ticket_id} not found")

    def get_ticket_price(self) -> float:
        return self.price

    def get_ticket_quantity(self) -> float:
        return self.quantity
    
    def get_group_id(self) -> str:
        return self.group_id
