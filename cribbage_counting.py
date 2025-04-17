def compute_cribbage_score(hand, starter_card=None):
    # Combine hand and starter card
    if starter_card is not None:
        total_hand = hand + [starter_card]
    else:
        total_hand = hand
    score = 0

    # Map card ranks to their values
    rank_values = {'A':1, '2':2, '3':3, '4':4, '5':5, 
                   '6':6, '7':7, '8':8, '9':9, '10':10,
                   'J':10, 'Q':10, 'K':10}
    face_values = {'A':1, '2':2, '3':3, '4':4, '5':5, 
                   '6':6, '7':7, '8':8, '9':9, '10':10,
                   'J':11, 'Q':12, 'K':13}
    
    values = [rank_values[card[0:-1].upper()] for card in total_hand]
    faces = [face_values[card[0:-1].upper()] for card in total_hand]
    suits = [card[-1].upper() for card in total_hand]
    ranks = [card[0:-1].upper() for card in total_hand]

    # Calculate fifteens
    from itertools import combinations
    for i in range(2,10):
        for combo in combinations(values, i):
            if sum(combo) == 15:
                score += 2

    # Calculate pairs
    from collections import Counter
    counts = Counter(ranks)
    for count in counts.values():
        if count == 2:
            score += 2
        elif count == 3:
            score += 6
        elif count == 4:
            score += 12

    # Calculate runs
    counts = Counter(faces)
    max_run_length = 0
    total_run_score = 0
    unique_faces = set(faces)
    for run_length in range(9, 2, -1):  # Check for runs from length 5 down to 3
        runs = []
        for combo in combinations(unique_faces, run_length):
            if max(combo) - min(combo) == run_length - 1:
                # Calculate multiplicity due to duplicate cards
                multiplicity = 1
                for face in combo:
                    multiplicity *= counts[face]
                runs.append((run_length, multiplicity))
        if runs:
            for run_length, multiplicity in runs:
                total_run_score += run_length * multiplicity
            score += total_run_score
            break  # Only count runs of the longest length

    # Calculate knobs
    if starter_card is not None:
        for card in hand:
            if card[0].upper() == 'J' and card[1] == starter_card[1]:
                score += 1
                break

    return score


# print(compute_cribbage_score(['2H', '3H', '4H', '5H'], '6H')) # 29