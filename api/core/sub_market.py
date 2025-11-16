"""
Class for keeping track of a submarket context.
"""

from api.models.ticket import Ticket
from api.models.bid import Bid
from typing import List
from api.models.event import Event
from configs import TICKETS_JSON, BIDS_JSON
import json

class SubMarket:
    """
    Represents a submarket within the larger marketplace.
    """
    def __init__(self, event: Event, group_id: str) -> None:
        self.event = event
        self.event_id = event.event_id
        self.group_id = group_id
        self.tickets = self._load_tickets()
        self.bids = self._load_bids()

    def _load_tickets(self) -> List[Ticket]:
        """
        Loads tickets from json that match this submarket's criteria.
        """
        with open(TICKETS_JSON, "r") as f:
            all_tickets = json.load(f)
        
        # Filter tickets matching this submarket (event_id and group_id)
        matching_tickets = [
            Ticket(**ticket_data)
            for ticket_data in all_tickets
            if ticket_data["event_id"] == self.event_id
            and ticket_data["group_id"] == self.group_id
        ]
        
        return matching_tickets
    
    def _load_bids(self) -> List[Bid]:
        """
        Loads bids from json that match this submarket's criteria.
        Bid matches if:
        - event_id matches
        - allowed_groups is empty (accepts all groups) OR group_id is in allowed_groups
        """
        with open(BIDS_JSON, "r") as f:
            all_bids = json.load(f)
        
        # Filter bids matching this submarket
        matching_bids = [
            Bid(**bid_data)
            for bid_data in all_bids
            if bid_data["event_id"] == self.event_id
            and (len(bid_data["allowed_groups"]) == 0 or self.group_id in bid_data["allowed_groups"])
        ]
        
        return matching_bids
    
    def _summarize_market(self) -> str:
        """
        Generates a summary of the submarket state.
        """
        ticket_prices = [
            ticket.get_ticket_price()
            for ticket in self.tickets
            for _ in range(ticket.quantity)
        ]

        bid_prices = [
            bid.get_bid_price()
            for bid in self.bids
            for _ in range(bid.get_bid_quantity())
        ]

        avg_ticket_price = sum(ticket_prices) / len(ticket_prices) if ticket_prices else 0
        avg_bid_price = sum(bid_prices) / len(bid_prices) if bid_prices else 0
        num_tickets = sum(ticket.quantity for ticket in self.tickets)
        num_bids = sum(bid.get_bid_quantity() for bid in self.bids)
        median_ticket_price = sorted(ticket_prices)[len(ticket_prices)//2] if ticket_prices else 0
        median_bid_price = sorted(bid_prices)[len(bid_prices)//2] if bid_prices else 0

        summary = (
            f"  Number of Tickets: {num_tickets}\n"
            f"  Number of Bids: {num_bids}\n"
            f"  Average Ticket Price: ${avg_ticket_price:.2f}\n"
            f"  Median Ticket Price: ${median_ticket_price:.2f}\n"
            f"  Average Bid Price: ${avg_bid_price:.2f}\n"
            f"  Median Bid Price: ${median_bid_price:.2f}\n"
        )

        return summary

# test

if __name__ == "__main__":
    import api.models.event as event

    submarket = SubMarket(event=event.Event.from_event_id("001"), group_id="FLOOR_PREMIUM")
    print("Tickets:")
    for ticket in submarket.tickets:
        print(ticket)
    print("Bids:")
    for bid in submarket.bids:
        print(bid)

    print(submarket._summarize_market())