from fastapi import APIRouter
from api.models.ticket import Ticket

router = APIRouter(prefix="/buyer", tags=["buyer"])


# @router.post("/search")
# def search_ticket(ticket: Ticket):
#     return create_ticket(ticket)
