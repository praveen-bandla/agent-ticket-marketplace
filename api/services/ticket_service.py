"""
Provides business logic for managing ticket listings.

This module handles loading and writing ticket data stored in a static
JSON file, along with operations for listing, creating, and deleting
tickets. It acts as the API's data layer in place of a database for
demo purposes.
"""

import json
import uuid
from pathlib import Path
from api.models.ticket import Ticket


DATA_PATH = Path(__file__).parents[1] / 'data' / 'tickets.json'

def load_json():
    tickets = {}
    with open(DATA_PATH, 'r') as f:
        tickets = json.load(f)
    return tickets

def list_tickets():
    return load_json()

def create_ticket(ticket: Ticket):
    tickets = load_json()
    new_id = str(uuid.uuid4())
    ticket_dict = ticket.model_dump()
    ticket_dict['ticket_id'] = new_id
    tickets.append(ticket_dict)

    with open(DATA_PATH, 'w') as f:
        json.dump(tickets, f, indent=2)

    return ticket_dict

def delete_ticket(id: str):
    tickets = load_json()
    updated_tickets = [t for t in tickets if t.get('ticket_id') != id]
    if len(updated_tickets) == len(tickets):
        return None
    with open(DATA_PATH, 'w') as f:
        json.dump(updated_tickets, f, indent=2)
    return True

def reduce_quantity(ticket_id: str, amount: int):
    tickets = load_json()
    updated_ticket = None

    for ticket in tickets:
        if ticket.get('ticket_id') == ticket_id:
            current_qty = ticket.get('quantity', 0)
            if amount <= 0 or amount > current_qty:
                return None

            ticket['quantity'] = current_qty - amount
            updated_ticket = ticket
            break

    if updated_ticket is None:
        return None

    with open(DATA_PATH, 'w') as f:
        json.dump(tickets, f, indent=2)

    return updated_ticket
