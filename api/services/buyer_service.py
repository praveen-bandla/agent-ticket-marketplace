def _clarification_question(missing_field):
    questions = {
        "event_name": "What artist or event are you looking for?",
        "venue": "Which venue or place do you prefer?",
        "num_tickets": "How many tickets do you need?",
        "ask_price": "What is your starting offer per ticket?",
        "max_price": "What is the most you're willing to pay per ticket?"
    }
    return questions[missing_field]
