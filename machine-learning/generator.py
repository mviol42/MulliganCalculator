import json
import sys

from config import card_types, decks_location


def get_base_deck():
    base_deck = []
    min_deck_size = 0
    for card_type in card_types.keys():
        num = card_types[card_type]['min_number']
        base_deck.append(num)
        min_deck_size += num

    return base_deck, min_deck_size


def main():
    # entry point for generate decks program
    # For each card type, we have some min number of cards in that card type.
    # We also have the range
    # For example, for lands has min of 30 and range of 10, so
    # it should move between 30 and 40 (30 + 10) cards in the deck
    # first, generate a base deck which represents the min number of cards together in a deck
    base_deck, min_deck_size = get_base_deck()
    set_of_decks = set()

    def generate_decks(curr_deck_so_far, types, which_type, max_in_deck):
        cards_in_deck = sum(curr_deck_so_far)
        if tuple(curr_deck_so_far) in set_of_decks or cards_in_deck > max_in_deck:
            return

        if cards_in_deck == max_in_deck:
            set_of_decks.add(tuple(curr_deck_so_far))

        if cards_in_deck < max_in_deck and which_type < len(types):
            for i in range(card_types[types[which_type]]['range']):
                # this makes a new instance of the array,
                # meaning the future recursive calls won't touch this same array
                tmp = curr_deck_so_far[:]
                curr_deck_so_far[which_type] = card_types[types[which_type]]['min_number'] + i
                generate_decks(curr_deck_so_far,
                               types,
                               which_type + 1,
                               max_in_deck)
                curr_deck_so_far = tmp

    # then, starting with this base deck and min size, use recursion to build out various decks
    # this technique is very memory intensive and would likely be better as a for-loop or similar
    # perhaps a DP angle
    generate_decks(curr_deck_so_far=base_deck,
                   types=list(card_types),
                   which_type=0,
                   max_in_deck=100)

    output_decks = {}
    for deck in set_of_decks:
        deck_sting = ",".join(str(num_type) for num_type in list(deck))
        output_decks[deck_sting] = tuple([1, 1])

    with open(decks_location, "w") as outfile:
        json.dump(output_decks, outfile)


if __name__ == "__main__":
    main()
