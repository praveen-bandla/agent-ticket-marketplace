"""
Contains the class to negotiate market transactions between buyers and sellers for all combinations of bids and tickets as listed in search results.
"""

from configs import SEARCH_RESULTS_JSON
import json
from api.core.sub_market import SubMarket
from api.core.negotiation import Negotiation
from api.models.event import Event
from typing import List, Tuple, Optional
from api.models.bid import Bid
from api.models.ticket import Ticket
from api.core.agents.buyer_negotiator import BuyerNegotiator
from api.core.agents.seller_negotiator import SellerNegotiator
import asyncio
import logging


class MarketNegotiator:
    """
    Responsible for negotiating transactions between buyers and sellers based on search results.
    """

    def __init__(self) -> None:
        self.pairs = self._retrieve_search_results()
        self.negotiation_results = []
        
        # Configure logging for negotiation tracking
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.logger.info("MarketNegotiator initialized with logger")

    def _retrieve_search_results(self) -> List[Tuple[str, str]]:
        """
        Loads search results from JSON file.
        Returns a list of (bid_id, ticket_id) tuples.
        """
        with open(SEARCH_RESULTS_JSON, "r") as f:
            results = json.load(f)
        
        return [(result["bid_id"], result["ticket_id"]) for result in results]
    
    def retrieve_search_resuls_submarket(self, submarket: SubMarket) -> List[Tuple[str, str]]:
        """
        Filters search results for a specific submarket.
        Returns a list of (bid_id, ticket_id) tuples relevant to the submarket.
        """
        filtered_pairs = []
        submarket_ticket_ids = [ticket.ticket_id for ticket in submarket.tickets]
        submarket_bid_ids = [bid.bid_id for bid in submarket.bids]
        for bid_id, ticket_id in self.pairs:
            if bid_id in submarket_bid_ids and ticket_id in submarket_ticket_ids:
                filtered_pairs.append((bid_id, ticket_id))
        return filtered_pairs
    
    async def _negotiate_single_pair(self, bid_id: str, ticket_id: str, submarket: SubMarket) -> Optional[Tuple[str, str, float, int, List[dict]]]:
        """
        Conducts a single negotiation between a bid and ticket.
        Returns agreement (bid_id, ticket_id, price, quantity, conversation_history) or None for failed negotiations.
        """
        self.logger.info(f"Starting negotiation for bid_id={bid_id}, ticket_id={ticket_id}")
        
        bid = next((b for b in submarket.bids if b.bid_id == bid_id), None)
        ticket = next((t for t in submarket.tickets if t.ticket_id == ticket_id), None)
        
        if bid and ticket:
            self.logger.info(f"Found valid bid and ticket for {bid_id}-{ticket_id}")
            buyer_negotiator = BuyerNegotiator(bid=bid, SubMarket=submarket)
            seller_negotiator = SellerNegotiator(ticket=ticket, SubMarket=submarket)
            
            negotiation = Negotiation(
                buyer_negotiator=buyer_negotiator,
                seller_negotiator=seller_negotiator,
                submarket=submarket
            )
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            agreement = await loop.run_in_executor(None, negotiation.simulate_negotiation)
            
            if agreement:
                self.logger.info(f"Negotiation SUCCESS for {bid_id}-{ticket_id}: price={agreement[2]}, quantity={agreement[3]}")
            else:
                self.logger.warning(f"Negotiation FAILED for {bid_id}-{ticket_id}: no agreement reached")
            
            return agreement
        else:
            self.logger.error(f"Invalid bid or ticket for {bid_id}-{ticket_id}: bid={bid is not None}, ticket={ticket is not None}")
            return None

    async def negotiate_pairs_submarket(self, submarket: SubMarket) -> List[Optional[Tuple[str, str, float, int, List[dict]]]]:
        """
        Conducts negotiations for all bid-ticket pairs in the specified submarket.
        Returns a list of agreements (bid_id, ticket_id, price, quantity, conversation_history) or None for failed negotiations.
        """
        filtered_pairs = self.retrieve_search_resuls_submarket(submarket)
        self.logger.info(f"Starting parallel negotiations for {len(filtered_pairs)} bid-ticket pairs")
        
        # Create tasks for all negotiations to run concurrently
        tasks = [
            self._negotiate_single_pair(bid_id, ticket_id, submarket)
            for bid_id, ticket_id in filtered_pairs
        ]
        
        # Run all negotiations in parallel
        agreements = await asyncio.gather(*tasks)
        
        successful_negotiations = [a for a in agreements if a is not None]
        self.logger.info(f"Completed negotiations: {len(successful_negotiations)}/{len(filtered_pairs)} successful")
        
        self.negotiation_results.extend(agreements)
        return agreements
        
    

if __name__ == "__main__":
    market_negotiator = MarketNegotiator()
    event = Event.get_event_by_id(event_id="event_001")
    submarket = SubMarket(event=event, group_id = "FLOOR_PREMIUM")
    results = asyncio.run(market_negotiator.negotiate_pairs_submarket(submarket))
    print(results)