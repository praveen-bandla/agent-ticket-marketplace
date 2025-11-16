"""
Contains the class for resolving transactions between buyers and sellers.
"""

from typing import List, Tuple, Optional
from api.models.bid import Bid
from api.models.ticket import Ticket
from configs import BIDS_JSON, TICKETS_JSON, TRANSACTIONS_JSON
import json

class TransactionResolver:
    """
    Responsible for resolving transactions between buyers and sellers.
    """
    
    def __init__(self, agreements) -> None:
        self.agreements = agreements

    def _check_for_conflicts(self) -> bool:
        """
        Checks to see if one buyer or seller is involved in multiple agreements.
        """
        buyer_ids = set()
        seller_ids = set()

        for agreement in self.agreements:
            bid_id, ticket_id, price, quantity, conversation_history = agreement
            buyer_id = bid_id.split("-")[0]
            seller_id = ticket_id.split("-")[0]

            if buyer_id in buyer_ids or seller_id in seller_ids:
                return True  # Conflict found

            buyer_ids.add(buyer_id)
            seller_ids.add(seller_id)

        return False  # No conflicts found

    def create_transaction_object(self, agreement: Tuple[str, str, float, int, List[dict]]) -> dict:
        """
        Creates a transaction object from an agreement tuple.
        """
        bid_id, ticket_id, price, quantity, conversation_history = agreement
        buyer_id = Bid.get_bid_by_id(bid_id).buyer_id
        seller_id = Ticket.get_ticket_by_id(ticket_id).seller_id
        transaction = {
            "bid_id": bid_id,
            "ticket_id": ticket_id,
            "price": price,
            "quantity": quantity,
            "buyer_id": buyer_id,
            "seller_id": seller_id,
            "conversation_history": conversation_history
        }
        return transaction
    
    def save_transactions(self, transactions: List[dict]) -> None:
        """
        Saves the list of transaction objects to the transactions JSON file.
        """
        with open(TRANSACTIONS_JSON, "w") as f:
            json.dump(transactions, f, indent=4)

        return

    def remove_bids(self, bid_ids: List[str]) -> None:
        """
        Goes through bids.json to remove all bids by its ID.
        """
        with open(BIDS_JSON, "r") as f:
            all_bids = json.load(f)

        updated_bids = [bid for bid in all_bids if bid["bid_id"] not in bid_ids]

        with open(BIDS_JSON, "w") as f:
            json.dump(updated_bids, f, indent=4)

        return
    
    def remove_tickets(self, ticket_ids: List[str]) -> None:
        """
        Goes through tickets.json to remove all tickets by its ID.
        """
        with open(TICKETS_JSON, "r") as f:
            all_tickets = json.load(f)

        updated_tickets = [ticket for ticket in all_tickets if ticket["ticket_id"] not in ticket_ids]

        with open(TICKETS_JSON, "w") as f:
            json.dump(updated_tickets, f, indent=4)

        return
    
    def resolve_transactions(self) -> List[Tuple[str, str, float, int, List[dict]]]:
        """
        Resolves transactions by filtering out conflicting agreements.
        Returns a list of non-conflicting agreements.
        """
        if not self._check_for_conflicts():
            return self.agreements  # No conflicts, return all agreements

        sorted_agreements = sorted(self.agreements, key=lambda x: x[2], reverse=True)
        covered_tickets = set()
        covered_bids = set()
        resolvable_agreements = []

        for agreement in sorted_agreements:
            bid_id, ticket_id, price, quantity, conversation_history = agreement
            if bid_id in covered_bids or ticket_id in covered_tickets:
                continue  # Skip conflicting agreement
            covered_bids.add(bid_id)
            covered_tickets.add(ticket_id)
            resolvable_agreements.append(agreement)

        return resolvable_agreements
    
    def process_transactions(self) -> None:
        """
        Processes all agreements into transaction objects and updates bids/tickets data.
        Returns a list of transaction objects.
        """
        transactions_to_process = self.resolve_transactions()
        transaction_objects = []
        bid_ids_to_remove = []
        ticket_ids_to_remove = []

        for agreement in transactions_to_process:
            transaction = self.create_transaction_object(agreement)
            transaction_objects.append(transaction)
            bid_ids_to_remove.append(agreement[0])
            ticket_ids_to_remove.append(agreement[1])

        #self.remove_bids(bid_ids_to_remove)
        #self.remove_tickets(ticket_ids_to_remove)
        self.save_transactions(transaction_objects)
        return 
    

# test code

if __name__ == "__main__":
    from api.models.event import Event
    from api.core.market_negotiate import MarketNegotiator
    from api.core.sub_market import SubMarket
    import asyncio
    market_negotiator = MarketNegotiator()
    event = Event.get_event_by_id(event_id="event_001")
    submarket = SubMarket(event=event, group_id = "FLOOR_PREMIUM")
    results = asyncio.run(market_negotiator.negotiate_pairs_submarket(submarket))
    print(results)

    transaction_resolver = TransactionResolver(results)
    transaction_resolver.process_transactions()

    # market_negotiator = MarketNegotiator()
    # event = Event.get_event_by_id(event_id="event_001")
    # submarket = SubMarket(event=event, group_id = "FLOOR_PREMIUM")
    # results = asyncio.run(market_negotiator.negotiate_pairs_submarket(submarket))
    # print(results)

    # transaction_resolver = TransactionResolver(results)
