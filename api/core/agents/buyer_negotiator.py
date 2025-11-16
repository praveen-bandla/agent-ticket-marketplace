"""
Includes class for buyer negotiators in the marketplace.
"""

from api.models.buyer import Buyer
from api.models.bid import Bid
from api.models.ticket import Ticket
from typing import List
from api.core.sub_market import SubMarket
from configs import MAX_ROUNDS

class BuyerNegotiator:
    """
    Represents a buyer agent in the marketplace.
    """

    def __init__(self, bid: Bid, SubMarket: SubMarket) -> None:
        self.bid = bid
        self.Buyer = Buyer.get_buyer_by_id(bid.buyer_id)

        # Track negotiation state
        self.conversation_history: List[dict] = []
        self.final_offer = None
        self.num_rounds = 0
        self.max_rounds = MAX_ROUNDS
        self.submarket = SubMarket


    