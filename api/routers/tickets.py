from fastapi import APIRouter
from api.models.ticket import Ticket
from api.services.ticket_service import list_tickets, create_ticket

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.get("/")
def get_tickets():
    return list_tickets()

@router.post("/create")
def create_ticket(ticket: Ticket):
    return create_ticket(ticket)
