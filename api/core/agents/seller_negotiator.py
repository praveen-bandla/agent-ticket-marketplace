"""
Includes class for seller negotiators in the marketplace.
"""

from api.models.seller import Seller
from api.models.ticket import Ticket
from typing import List
from api.core.sub_market import SubMarket
from configs import MAX_ROUNDS, PROMPTS_DIR
# from api.services.openrouter_client import call_openrouter_with_prompt
from api.services.gpt_service import call_gpt
import os
import re
import logging

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
        
        # Setup logger with ticket context
        self.logger = logging.getLogger(f"{__name__}.{ticket.ticket_id}")
        if not self.logger.handlers:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger.info(f"SellerNegotiator initialized for ticket_id={ticket.ticket_id}, seller_id={ticket.seller_id}")


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
    
    def _extract_price_from_message(self, message: str) -> float:
        """
        Extract the last numeric amount from the message and return it as int.
        Supports thousands separators and optional decimals. Returns -1 if none found.
        """
        pattern = re.compile(r'(?P<num>-?(?:\d{1,3}(?:,\d{3})*|\d+)(?:\.\d{1,2})?)')
        last = None
        for m in pattern.finditer(message):
            last = m
        if not last:
            return -1

        num_str = last.group('num').replace(',', '')
        try:
            # Cast via float to handle decimals; int() truncates toward zero.
            return float(num_str)
        except ValueError:
            return -1
    
    def process_buyer_response(self, message: str) -> str:
        """
        Processes the buyer's message and decides on next action.
        """
        self.logger.info(f"Seller processing buyer response for ticket_id={self.ticket.ticket_id}: {message[:100]}...")
        
        if self._offer_accepted(message):
            self.resolved = True
            self.logger.info(f"Seller found ACCEPTED offer in buyer message for ticket_id={self.ticket.ticket_id}")
            
        else:
            buyer_price = self._extract_price_from_message(message)
            if buyer_price == -1:
                self.logger.error(f"Could not extract price from buyer's message for ticket_id={self.ticket.ticket_id}: {message}")
                raise ValueError("Could not extract price from buyer's message.")
            elif buyer_price == self.current_offer:
                self.resolved = True
                self.logger.info(f"Seller found matching offer for ticket_id={self.ticket.ticket_id}, price=${buyer_price}")
            else:
                # change self.current_offer to buyer price
                self.current_offer = buyer_price
                self.conversation_history.append(f'Round {self.num_rounds} - Buyer: {message}')
                self.num_rounds += 1
                self.logger.info(f"Seller received new offer for ticket_id={self.ticket.ticket_id}, round={self.num_rounds-1}, price=${buyer_price}")
    
    def negotiate(self) -> str:
        """
        Conducts the negotiation process.
        """
        self.logger.info(f"Seller starting negotiation round {self.num_rounds} for ticket_id={self.ticket.ticket_id}")
        
        prompt = self.construct_prompt()
        self.logger.debug(f"Seller prompt constructed for ticket_id={self.ticket.ticket_id}, round={self.num_rounds}")
        
        model_response = call_gpt(prompt)
        self.logger.info(f"Seller received LLM response for ticket_id={self.ticket.ticket_id}: {model_response[:100]}...")

        if self._offer_accepted(model_response):
            self.resolved = True
            self.logger.info(f"Seller ACCEPTED offer for ticket_id={self.ticket.ticket_id}, final_price={self.current_offer}")
            return model_response
        
        else:
            offered_price = self._extract_price_from_message(model_response)
            if offered_price == -1:
                self.logger.error(f"Could not extract price from seller's message for ticket_id={self.ticket.ticket_id}: {model_response}")
                raise ValueError("Could not extract price from seller's message.")
            
            self.current_offer = offered_price
            self.conversation_history.append(f'Round {self.num_rounds} - Seller: {model_response}')
            self.logger.info(f"Seller made offer for ticket_id={self.ticket.ticket_id}, round={self.num_rounds}, price=${offered_price}")
        
        return model_response