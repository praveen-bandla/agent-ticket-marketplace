"""
Contains the class for negotiations between buyers and sellers.
"""

from api.models.bid import Bid
from api.core.sub_market import SubMarket
from api.models.ticket import Ticket
from typing import List, Optional, Tuple
from api.core.agents.buyer_negotiator import BuyerNegotiator
from api.core.agents.seller_negotiator import SellerNegotiator
from configs import MAX_ROUNDS


class Negotiation:
    """
    Represents a negotiation between a buyer and a seller.
    """

    def __init__(
        self,
        buyer_negotiator: BuyerNegotiator,
        seller_negotiator: SellerNegotiator,
        submarket: SubMarket
    ) -> None:
        self.buyer_negotiator = buyer_negotiator
        self.seller_negotiator = seller_negotiator
        self.submarket = submarket
        self.is_resolved = False
        self.agreement: Optional[Tuple[float, int]] = None  # (price, quantity)
        self.rounds = 1
        self.max_rounds = MAX_ROUNDS
        self.shared_conversation_history: List[dict] = []
        self.quantity = min(
            self.buyer_negotiator.bid.get_bid_quantity(),
            self.seller_negotiator.ticket.get_ticket_quantity()
        )

    def resolve(self) -> Optional[Tuple[float, int]]:
        """
        Conducts the negotiation until an agreement is reached or max rounds exceeded.
        Returns the agreement (price, quantity) if successful, else None.
        """

        seller_price = self.seller_negotiator.ticket.get_ticket_price()
        buyer_price = self.buyer_negotiator.bid.get_bid_price()

        if buyer_price >= seller_price:
            agreed_price = seller_price
            agreed_quantity = min(
                self.buyer_negotiator.bid.get_bid_quantity(),
                self.seller_negotiator.ticket.get_ticket_quantity()
            )
            self.agreement = (agreed_price, agreed_quantity)
            self.is_resolved = True
            return self.agreement
        
        else:
            pass
        
    def simulate_negotiation(self):
        """
        Simulates an entire negotiation process between buyer and seller.
        """
        while not self.is_resolved and self.rounds <= self.max_rounds:
            
            if self.buyer_negotiator.is_resolved():
                self.is_resolved = True
                self.agreement = (self.buyer_negotiator.current_offer, self.quantity)
                return self.agreement

            
            if self.seller_negotiator.is_resolved():
                self.is_resolved = True
                self.agreement = (self.seller_negotiator.current_offer, self.quantity)
                return self.agreement
            
            buyer_response = self.buyer_negotiator.negotiate()
            seller_response = self.seller_negotiator.negotiate()
            self.buyer_negotiator.process_seller_response(seller_response)
            self.seller_negotiator.process_buyer_response(buyer_response)

            self.rounds += 1

        self.shared_conversation_history = self.buyer_negotiator.get_conversation_history()

        return None

# test

if __name__ == "__main__":
    bid = Bid.get_bid_by_id("bid_001")
    ticket = Ticket.get_ticket_by_id("ticket_001")

    from api.models.event import Event
    event = Event.get_event_by_id("event_001")

    submarket = SubMarket(event, group_id="group_001")

    buyer_negotiator = BuyerNegotiator(bid, submarket)
    seller_negotiator = SellerNegotiator(ticket, submarket)

    negotiation = Negotiation(buyer_negotiator, seller_negotiator, submarket)
    result = negotiation.simulate_negotiation()
    for line in negotiation.shared_conversation_history:
        print(line)
    print("Negotiation Result:", result)
    