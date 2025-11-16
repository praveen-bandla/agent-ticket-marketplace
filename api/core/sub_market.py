"""
Class for keeping track of a submarket context.
"""

from api.models.ticket import Ticket
from api.models.bid import Bid
from typing import List
from api.models.event import Event
from configs import TICKETS_JSON, BIDS_JSON
import json
import numpy as np

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

        ticket_prices = {}
        bid_prices = {}
        group_ids = self.event.get_group_ids()
        for gid in group_ids:
            ticket_prices[gid] = [
                ticket.get_ticket_price()
                for ticket in self.tickets
                if ticket.get_group_id() == gid
                for _ in range(ticket.quantity)
            ]
            bid_prices[gid] = [
                bid.get_bid_price()
                for bid in self.bids
                if gid in bid.allowed_groups or len(bid.allowed_groups) == 0
                for _ in range(bid.get_bid_quantity())
            ]
        
        lines = []
        for gid in group_ids:
            tickets = ticket_prices.get(gid)
            bids = bid_prices.get(gid)
            num_tick, num_bids = len(tickets), len(bids)
            avg_tick = sum(tickets) / num_tick if num_tick > 0 else "N/A"
            avg_bid = sum(bids) / num_bids if num_bids > 0 else "N/A"
            median_tick = np.median(tickets) if num_tick > 0 else "N/A"
            median_bid = np.median(bids) if num_bids > 0 else "N/A"
            lines.append(f"Group ID: {gid} -> num_tickets: {num_tick} avg_ticket_price: {avg_tick} median_ticket_price: {median_tick} num_bids: {num_bids} avg_bid_price: {avg_bid} median_bid_price: {median_bid}")

            summary = "\n".join(lines)

        return summary
    
    def get_reference_values(self) -> dict[str, float]:
        """
        Retrieves the reference values for this submarket's event.
        """
        return self.event.get_reference_values()

# test

if __name__ == "__main__":
    from api.models.event import Event

    submarket = SubMarket(event=Event.get_event_by_id("event_001"), group_id="FLOOR_PREMIUM")
    print("Tickets:")
    for ticket in submarket.tickets:
        print(ticket)
    print("Bids:")
    for bid in submarket.bids:
        print(bid)

    print(submarket._summarize_market())