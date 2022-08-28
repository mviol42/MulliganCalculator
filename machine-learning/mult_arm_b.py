import numpy
import json
import analysis as Model
import deck_generator

num_iter = 100000


def get_sample_hand(arm):
    card_amounts = arm.split(',')
    prob = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # standardize the weighting
    for i in range(len(card_amounts)):
        prob[i] = float(card_amounts[i]) / 100

    indices = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    results = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(7):
        results[numpy.random.choice(a=indices, p=prob)] += 1

    return results


def run_samples():
    deck_generator.generate_decks(1000, './decks.json')
    data = json.load(open('./decks.json', 'r'))
    model = Model.train()

    for t in range(num_iter):
        max_sample = 0
        arm = ""
        for deck in data:
            alpha, beta = int(deck[0]), int(deck[1])
            s = numpy.random.beta(alpha, beta)
            if max_sample < s:
                arm = deck
                max_sample = s

        sample_hand = get_sample_hand(arm)
        prediction = model.predict(sample_hand)
        if prediction >= 0.5:
            data[arm][0] += 1
        else:
            data[arm][1] += 1


if __name__ == "__main__":
    run_samples()
