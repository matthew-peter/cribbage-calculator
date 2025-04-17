from flask import Flask, request, render_template
import os
from cribbage_counting import compute_cribbage_score

app = Flask(__name__)
app.secret_key = "1234"

@app.route("/", methods=["GET", "POST"])
def home():
    # Handle both GET and POST at the main route
    # Define all cards in a deck
    suits = ['♠', '♥', '♦', '♣']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    deck = [(rank, suit) for rank in ranks for suit in suits]
    
    hand_score = None
    selected_cards = []
    starter_card_id = None
    error_message = None
    
    if request.method == "POST":
        # Get selected cards from form
        selected_cards = request.form.getlist("cards")
        starter_card_id = request.form.get("starter_card")
        
        # Make starter optional - only check for at least one hand card
        if len(selected_cards) < 1 or (starter_card_id and starter_card_id in selected_cards and len(selected_cards) < 2):
            error_message = "Please select at least 1 card"
        else:
            # Format cards for the compute_cribbage_score function
            # Extract hand cards (all selected cards except the starter)
            hand_cards = []
            for card in selected_cards:
                if card != starter_card_id:  # Skip the starter card
                    rank, suit = card.split('-')
                    suit_letter = {'♠': 'S', '♥': 'H', '♦': 'D', '♣': 'C'}[suit]
                    hand_cards.append(f"{rank}{suit_letter}")
            
            # Format the starter card if it exists
            starter = None
            if (starter_card_id != 'None') and (starter_card_id != ''):
                rank, suit = starter_card_id.split('-')
                suit_letter = {'♠': 'S', '♥': 'H', '♦': 'D', '♣': 'C'}[suit]
                starter = f"{rank}{suit_letter}"
            
            # Calculate score using the imported function, with optional starter
            hand_score = compute_cribbage_score(hand_cards, starter) if starter else compute_cribbage_score(hand_cards)
    
    return render_template("home.html", 
                          hand_score=hand_score, 
                          selected_cards=selected_cards,
                          starterCardId=starter_card_id,
                          error_message=error_message)

# Keep this route for compatibility - redirects to main route
@app.route("/home", methods=["GET", "POST"])
def cribbage():
    return home()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)