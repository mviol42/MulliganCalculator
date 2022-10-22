import random

import numpy
import json
import analysis as Model
import deck_generator

num_iter = 1000000


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


def find_optimal(data):
    max = 0
    max_key = ''
    for key in list(data.keys()):
        alpha, beta = float(data[key][0]), float(data[key][1])
        ratio = alpha / (beta + alpha)
        if ratio > max:
            max = ratio
            max_key = key
    return max_key

def run_samples():
    deck_location = './decks.json'
    # deck_generator.generate_decks(1000, deck_location)
    data = json.load(open(deck_location, 'r'))
    keys = list(data.keys())
    model = Model.train()

    for t in range(num_iter):
        max_sample = 0
        arm = ""
        random.shuffle(keys)
        for key in keys:
            alpha, beta = int(data[key][0]), int(data[key][1])
            s = numpy.random.beta(alpha, beta)
            if max_sample < s:
                arm = key
                max_sample = s

        sample_hand = get_sample_hand(arm)
        prediction = model.predict(numpy.array([sample_hand, ]), verbose=0)
        if prediction >= 0.5:
            data[arm][0] += 1
        else:
            data[arm][1] += 1

    print(find_optimal(data))
    with open(deck_location, "w") as outfile:
        json.dump(data, outfile)


if __name__ == "__main__":
    run_samples()
