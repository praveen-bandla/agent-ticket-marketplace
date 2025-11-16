"""
Defines data models used in the ticket marketplace API.

This module contains the Pydantic model representing a ticket listing.
It is used for input validation, serialization, and consistent data
handling across the service and routing layers.
"""

from pydantic import BaseModel


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
