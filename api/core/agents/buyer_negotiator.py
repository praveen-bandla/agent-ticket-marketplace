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
import logging
# from api.services.openrouter_client import call_openrouter_with_prompt
from api.services.gpt_service import call_gpt

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
        
        # Setup logger with bid context
        self.logger = logging.getLogger(f"{__name__}.{bid.bid_id}")
        if not self.logger.handlers:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger.info(f"BuyerNegotiator initialized for bid_id={bid.bid_id}, buyer_id={bid.buyer_id}")

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
        price = self._extract_price_from_message(message)
        if price == self.current_offer:
            return True
        return False
    
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
    
    def process_seller_response(self, message: str) -> str:
        """
        Processes the seller's message and decides on next action.
        """
        self.logger.info(f"Buyer processing seller response for bid_id={self.bid.bid_id}: {message[:100]}...")
        
        if self._offer_accepted(message):
            self.resolved = True
            self.logger.info(f"Buyer found ACCEPTED offer in seller message for bid_id={self.bid.bid_id}")
        
        else:
            seller_price = self._extract_price_from_message(message)
            if seller_price == -1:
                self.logger.error(f"Could not extract price from seller's message for bid_id={self.bid.bid_id}: {message}")
                raise ValueError("Could not extract price from seller's message.")
            
            # change self.current_offer to seller price
            elif seller_price == self.current_offer:
                self.resolved = True
                self.logger.info(f"Buyer found matching offer for bid_id={self.bid.bid_id}, price=${seller_price}")
            else:
                self.current_offer = seller_price
                self.conversation_history.append(f'Round {self.num_rounds} - Seller: {message}')
                self.num_rounds += 1
                self.logger.info(f"Buyer received new offer for bid_id={self.bid.bid_id}, round={self.num_rounds-1}, price=${seller_price}")

        return None
    
    def negotiate(self) -> str:
        """
        Decides on the next action based on current offer and bid constraints.
        """
        self.logger.info(f"Buyer starting negotiation round {self.num_rounds} for bid_id={self.bid.bid_id}")
        
        prompt = self.construct_prompt()
        self.logger.debug(f"Buyer prompt constructed for bid_id={self.bid.bid_id}, round={self.num_rounds}")
        
        model_response = call_gpt(prompt)
        self.logger.info(f"Buyer received LLM response for bid_id={self.bid.bid_id}: {model_response[:100]}...")

        if self._offer_accepted(model_response):
            self.resolved = True
            self.logger.info(f"Buyer ACCEPTED offer for bid_id={self.bid.bid_id}, final_price={self.current_offer}")
            return model_response
        
        else:
            offered_price = self._extract_price_from_message(model_response)
            if offered_price == -1:
                self.logger.error(f"Could not extract price from buyer's message for bid_id={self.bid.bid_id}: {model_response}")
                raise ValueError("Could not extract price from buyer's message.")
            
            self.current_offer = offered_price
            self.conversation_history.append(f'Round {self.num_rounds} - Buyer: {model_response}')
            self.logger.info(f"Buyer made offer for bid_id={self.bid.bid_id}, round={self.num_rounds}, price=${offered_price}")
        
        return model_response

       