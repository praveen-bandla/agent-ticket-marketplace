"""
Contains the class for negotiations between buyers and sellers.
"""

from api.models.bid import Bid
from api.core.sub_market import SubMarket
from api.models.ticket import Ticket
from typing import List, Optional, Tuple
from api.core.agents.buyer_negotiator import BuyerNegotiator
from api.core.agents.seller_negotiator import SellerNegotiator


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
        self.rounds = 0

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
    result = negotiation.resolve()
    if result:
        print(f"Agreement reached: Price ${result[0]}, Quantity {result[1]}")
    else:
        print("No agreement reached.")

    