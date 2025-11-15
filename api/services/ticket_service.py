import json
from pathlib import Path
from api.models.ticket import Ticket

DATA_PATH = Path(__file__).parents[1] / 'data' / 'tickets.json'

def list_tickets():
    tickets = {}
    with open(DATA_PATH, 'r') as f:
        tickets = json.load(f)
    return tickets

def create_ticket(ticket: Ticket):
    new_id = max([t['id'] for t in TICKETS], default=0) + 1
    ticket_dict = ticket.model_dump()
    ticket_dict['id'] = new_id
    TICKETS.append(ticket_dict)

    with open(DATA_PATH, 'w') as f:
        json.dump(TICKETS, f, indent=2)

    return ticket_dict
