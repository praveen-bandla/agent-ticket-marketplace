from pydantic import BaseModel

class Ticket(BaseModel):
    id: int | None = None
    event: str
    date: str
    price: float
    seller: str
