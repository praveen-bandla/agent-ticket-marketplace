from pydantic import BaseModel

class Ticket(BaseModel):
    ticket_id: str
    seller_id: str
    event_id: str
    group_id: str
    quantity: int
    ask_price: float
    min_price: float
    date: str
    sensitivity: str
    immediate_sale: bool
