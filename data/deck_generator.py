import json
from math import trunc
import random as r

def generate_decks(num, out):
    # num is the number of hands for each number of lands
    # num = 100 means 100 hands of each number of lands

    lands = [31, 32, 33, 34, 35, 36, 37, 38, 39]
    decks ={}

    # [land, 0 cost mana, 1 cost mana, 1 threat, 2 threat, 3 threat, 4 threat,
    # 5 threat, interaction]
    
    #maximum and minimum number of one type of card in deck
    max_type = 15
    min_type = 5
    
    for land in lands:
        
        for i in range(num):
            
            deck = [i*min_type for i in range(1, 2) for _ in range(9)]
            deck[0] = land

            remaining = 100 - (land + (min_type * 8))

            while remaining  > 0:

                used_type = set()
                rand = r.random()
                type = trunc(rand * 8 + 1)

                if type not in used_type:
                    used_type.add(type)

                    cards = trunc(r.random() * max_type)
                    if cards > remaining: cards = remaining

                    deck[type] += cards
                    remaining = remaining - cards

            k = ",".join(str(x) for x in deck)
            decks[k] = tuple([1, 1])

    with open(out, "w") as outfile:
        json.dump(decks, outfile)


if __name__ == "__main__":
    generate_decks(1000, 'MulliganCalculator\data\decks.json')