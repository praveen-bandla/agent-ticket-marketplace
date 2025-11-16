"""
Includes class for buyer negotiators in the marketplace.
"""

from api.models.buyer import Buyer
from api.models.bid import Bid
from api.models.ticket import Ticket
from typing import List
from api.core.sub_market import SubMarket
from configs import MAX_ROUNDS, PROMPTS_DIR
import os
import re
from api.services.openrouter_client import call_openrouter_with_prompt

class BuyerNegotiator:
    """
    Represents a buyer agent in the marketplace.
    """

    def __init__(self, bid: Bid, SubMarket: SubMarket) -> None:
        self.bid = bid
        self.Buyer = Buyer.get_buyer_by_id(bid.buyer_id)

        # Track negotiation state
        self.conversation_history: List[dict] = []
        self.current_offer = None
        self.num_rounds = 1
        self.max_rounds = MAX_ROUNDS
        self.submarket = SubMarket
        self.resolved = False

    def construct_prompt(self) -> str:
        """
        Constructs the prompt for the buyer negotiator from template.
        """
        # Load template
        template_path = os.path.join(PROMPTS_DIR, "buyer_negotiation.txt")
        with open(template_path, "r") as f:
            template = f.read()
        
        # Format with values
        prompt = template.format(
            num_tickets=self.bid.num_tickets,
            bid_price=self.bid.price,
            max_price=self.bid.max_price,
            allowed_groups=', '.join(self.bid.allowed_groups) if self.bid.allowed_groups else 'All Groups',
            reference_values=self.submarket.get_reference_values(),
            sensitivity_to_price=self.bid.sensitivity_to_price,
            conversation_history=self.conversation_history,
            max_rounds=self.max_rounds
        )
        
        return prompt
    
    def _offer_accepted(self, message: str) -> bool:
        """
        Checks if the buyer accepted the seller's offer.
        """
        return "ACCEPT" in message.upper()
    
    def is_resolved(self) -> bool:
        """
        Checks if the negotiation has been resolved.
        """
        return self.resolved
    
    def get_conversation_history(self) -> List[dict]:
        """
        Returns the shared conversation history.
        """
        return self.conversation_history

    
    def _extract_price_from_message(self, message: str) -> float:
        """
        Extracts the price from the seller's message.
        """
        # Implementation to parse the message and extract price (regex. find the number in the message)
        match = re.search(r'\d+', message)
        if match:
            return float(match.group())
        return None
    
    def process_seller_response(self, message: str) -> str:
        """
        Processes the seller's message and decides on next action.
        """
        if self._offer_accepted(message):
            self.resolved = True
        
        else:
            seller_price = self._extract_price_from_message(message)
            if seller_price is None:
                raise ValueError("Could not extract price from seller's message.")
            # change self.current_offer to seller price
            self.current_offer = seller_price
            self.conversation_history.append(f'Round {self.num_rounds} - Seller: {message}')
            self.num_rounds += 1

        return None
    
    def negotiate(self) -> str:
        """
        Decides on the next action based on current offer and bid constraints.
        """
        prompt = self.construct_prompt()
        model_response = call_openrouter_with_prompt(prompt)

        if self._offer_accepted(model_response):
            self.resolved = True
            return model_response
        
        else:
            offered_price = self._extract_price_from_message(model_response)
            if offered_price is None:
                raise ValueError("Could not extract price from buyer's message.")
            self.current_offer = offered_price
            self.conversation_history.append(f'Round {self.num_rounds} - Buyer: {model_response}')
            self.num_rounds += 1
        return model_response

       