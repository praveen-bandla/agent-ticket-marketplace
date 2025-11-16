"""
Defines the API routes related to ticket management.

This router exposes endpoints for listing, creating, and deleting
tickets. It communicates with the ticket service layer to execute
operations and returns structured responses to clients.
"""

from fastapi import APIRouter, HTTPException
from api.models.ticket import Ticket
from api.services.ticket_service import delete_ticket, list_tickets, create_ticket

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.get("/")
def get_tickets():
    return list_tickets()

@router.post("/create")
def post_ticket(ticket: Ticket):
    return create_ticket(ticket)

@router.delete("/{ticket_id}")
def remove_ticket(ticket_id: str):
    result = delete_ticket(ticket_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"status": "deleted", "ticket_id": ticket_id}