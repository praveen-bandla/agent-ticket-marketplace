"""
Includes class for seller negotiators in the marketplace.
"""

from api.models.seller import Seller
from api.models.ticket import Ticket
from typing import List
from api.core.sub_market import SubMarket
from configs import MAX_ROUNDS

class SellerNegotiator:
    """
    Represents a seller agent in the marketplace.
    """

    def __init__(self, ticket: Ticket, SubMarket: SubMarket) -> None:
        self.ticket = ticket
        self.seller = Seller.from_seller_id(ticket.seller_id)

        # Track negotiation state
        self.conversation_history: List[dict] = []
        self.final_offer = None
        self.num_rounds = 0
        self.max_rounds = MAX_ROUNDS
        self.submarket = SubMarket