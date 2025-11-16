"""
Includes class for seller negotiators in the marketplace.
"""

from api.models.seller import Seller
from api.models.ticket import Ticket
from typing import List
from api.core.sub_market import SubMarket
from configs import MAX_ROUNDS, PROMPTS_DIR
from api.services.openrouter_client import call_openrouter_with_prompt
import os
import re

class SellerNegotiator:
    """
    Represents a seller agent in the marketplace.
    """

    def __init__(self, ticket: Ticket, SubMarket: SubMarket) -> None:
        self.ticket = ticket
        self.seller = Seller.get_seller_by_id(self.ticket.seller_id)

        # Track negotiation state
        self.conversation_history: List[dict] = []
        self.current_offer = None
        self.num_rounds = 1
        self.max_rounds = MAX_ROUNDS
        self.submarket = SubMarket
        self.resolved = False


    def construct_prompt(self) -> str:
        """
        Constructs the prompt for the seller negotiator from template.
        """
        # Load template
        template_path = os.path.join(PROMPTS_DIR, "seller_negotiation.txt")
        with open(template_path, "r") as f:
            template = f.read()

        # Format with values
        prompt = template.format(
            num_tickets=self.ticket.quantity,
            list_price=self.ticket.price,
            min_price=self.ticket.min_price,
            ticket_group=self.ticket.group_id,
            sensitivity_to_price=self.ticket.sensitivity,
            conversation_history=self.conversation_history,
            reference_values=self.submarket.get_reference_values(),
            max_rounds=self.max_rounds
        )

        return prompt
    
    def _offer_accepted(self, message: str) -> bool:
        """
        Checks if the seller accepted the buyer's offer.
        """
        price = self._extract_price_from_message(message)
        if price == self.current_offer:
            return True
        return False
    
    def is_resolved(self) -> bool:
        """
        Checks if the negotiation has been resolved.
        """
        return self.resolved
    
    def _extract_price_from_message(self, message: str) -> float | None:
        """
        Extracts the offered price from the message.
        """
        match = re.search(r'(\d+(\.\d{1,2})?)', message)
        if match:
            return float(match.group())
        return -1
    
    def process_buyer_response(self, message: str) -> str:
        """
        Processes the buyer's message and decides on next action.
        """
        if self._offer_accepted(message):
                self.resolved = True
            
        else:
            buyer_price = self._extract_price_from_message(message)
            if buyer_price == -1:
                raise ValueError("Could not extract price from buyer's message.")
            # elif buyer_price == self.current_offer:
            #     self.resolved = True
            else:
                # change self.current_offer to buyer price
                self.current_offer = buyer_price
                self.conversation_history.append(f'Round {self.num_rounds} - Buyer: {message}')
                self.num_rounds += 1
    
    def negotiate(self) -> str:
        """
        Conducts the negotiation process.
        """
        prompt = self.construct_prompt()
        model_response = call_openrouter_with_prompt(prompt)

        if self._offer_accepted(model_response):
            self.resolved = True
            return model_response
        
        else:
            offered_price = self._extract_price_from_message(model_response)
            if offered_price == -1:
                raise ValueError("Could not extract price from seller's message.")
            self.current_offer = offered_price
            self.conversation_history.append(f'Round {self.num_rounds} - Seller: {model_response}')
        return model_response