from flask import Flask, request, render_template
import os
from cribbage_counting import compute_cribbage_score

app = Flask(__name__)
app.secret_key = "1234"

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/home", methods=["GET", "POST"])
def cribbage():
    # Define all cards in a deck
    suits = ['♠', '♥', '♦', '♣']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    deck = [(rank, suit) for rank in ranks for suit in suits]
    
    hand_score = None
    selected_cards = []
    error_message = None
    
    if request.method == "POST":
        # Get selected cards from form
        selected_cards = request.form.getlist("cards")
        
        if len(selected_cards) < 2:
            error_message = "Please select at least 2 cards (1 for hand and 1 starter card)"
        else:
            # Format cards for the compute_cribbage_score function
            # The function expects strings like "2H", "KS", etc.
            hand_cards = []
            for card in selected_cards[:-1]:  # All but the last card are the hand
                rank, suit = card.split('-')
                suit_letter = {'♠': 'S', '♥': 'H', '♦': 'D', '♣': 'C'}[suit]
                hand_cards.append(f"{rank}{suit_letter}")
            
            # The last card is the starter
            rank, suit = selected_cards[-1].split('-')
            suit_letter = {'♠': 'S', '♥': 'H', '♦': 'D', '♣': 'C'}[suit]
            starter_card = f"{rank}{suit_letter}"
            
            # Calculate score using the imported function
            hand_score = compute_cribbage_score(hand_cards, starter_card)
    
    return render_template("home.html", deck=deck, hand_score=hand_score, 
                           selected_cards=selected_cards, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)