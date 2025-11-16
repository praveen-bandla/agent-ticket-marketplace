"""
Includes classes for buyer negotiators in the marketplace.
"""

from models.buyer import Buyer
from models.bid import Bid
from typing import List
from api.core.sub_market import SubMarket
from configs import MAX_ROUNDS

class BuyerNegotiator:
    """
    Represents a buyer agent in the marketplace.
    """

    def __init__(self, buyer: Buyer, bid: Bid, SubMarket: SubMarket) -> None:
        self.buyer = buyer
        self.bid = bid

        # Track negotiation state
        self.conversation_history: List[dict] = []
        self.final_offer = None
        self.num_rounds = 0
        self.max_rounds = MAX_ROUNDS

        self.submarket = SubMarket


