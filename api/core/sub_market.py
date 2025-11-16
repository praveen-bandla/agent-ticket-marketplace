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

    def get_num_tickets(self) -> int:
        """
        Returns the number of tickets in this submarket.
        """
        return len(self.tickets)

    def get_num_bids(self) -> int:
        """
        Returns the number of bids in this submarket.
        """
        return len(self.bids)


# test

# if __name__ == "__main__":
#     # # add path to PYTHONPATH and run this file to test
#     # import os
#     # import sys
#     # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
#     import api.models.event as event

#     submarket = SubMarket(event=event.Event.from_event_id("001"), group_id="FLOOR_PREMIUM")
#     print(f"Number of tickets in submarket: {submarket.get_num_tickets()}")
#     print(f"Number of bids in submarket: {submarket.get_num_bids()}")
#     print("Tickets:")
#     for ticket in submarket.tickets:
#         print(ticket)
#     print("Bids:")
#     for bid in submarket.bids:
#         print(bid)