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
        self.shared_conversation_history: List[dict] = []
        self.final_offer = None
        self.num_rounds = 0
        self.max_rounds = MAX_ROUNDS
        self.submarket = SubMarket

    def construct_initial_prompt(self) -> str:
        """
        Constructs the initial prompt for the buyer negotiator.
        """
        prompt = (
            f"You are an expert and friendly ticket buyer negotiator buying re-sale tickets. Your task is to negotiate a price with a seller negotiator (also an AI agent) to purchase tickets for an event.\n\n"
            f"For the buyer you are representing, you have the following bid details:\n"
            f"- Number of Tickets: {self.bid.num_tickets}\n"
            f"- Maximum Price: ${self.bid.max_price}\n"
            f"- Allowed Groups: {', '.join(self.bid.allowed_groups) if self.bid.allowed_groups else 'All Groups'}\n\n"

            f"The allowed groups correspond to the ticket groups that the buyer is willing to purchase from. If the list is empty, the buyer is open to tickets from any group.\n\n"
            f"Reference the following seat values for the event:\n"
            f"{self.submarket.get_reference_values()}\n"
            f"Use these values to decide on your negotiation strategy and offers.\n\n"
            "Further, you have this HIDDEN information about the buyer that you will use to make strategic negotiation but not reveal to the seller:"
            f" - Price Sensitivity: {self.bid.sensitivity_to_price}\n"
            f" - Maximum Price Willing to Pay: ${self.bid.max_price}\n\n"
        )
        return prompt

    