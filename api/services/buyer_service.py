import json
import os
import uuid
from pathlib import Path
from api.models.ticket import Ticket

BID_PATH = Path(__file__).parents[1] / 'data' / 'bids.json'
SEARCH_RESULTS_PATH = Path(__file__).parents[1] / 'data' / 'search_results.json'

def append_bid(new_bid):
    """
    Appends a new bid object to bids.json.
    
    Parameters:
        file_path (str): Path to bids.json
        new_bid (dict): The bid entry to append
    """

    # If file doesn't exist yet, initialize with an empty list
    if not os.path.exists(BID_PATH):
        with open(BID_PATH, "w") as f:
            json.dump([new_bid], f, indent=2)
        return

    # Load the existing bids
    with open(BID_PATH, "r") as f:
        try:
            bids = json.load(f)
        except json.JSONDecodeError:
            bids = []   # corrupted or empty file

    # Append new entry
    bids.append(new_bid)

    # Write updated list back
    with open(BID_PATH, "w") as f:
        json.dump(bids, f, indent=2)

def write_search_results(search_results):
    with open(SEARCH_RESULTS_PATH, "w") as f:
        json.dump(search_results, f, indent=2)