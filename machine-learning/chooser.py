import random

import numpy
import json
import analysis as Model
from config import decks_location
from tqdm import tqdm

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
    max_ratio = 0
    max_key = ''
    for key in list(data.keys()):
        alpha, beta = float(data[key][0]), float(data[key][1])
        ratio = alpha / (beta + alpha)
        if ratio > max_ratio:
            max_ratio = ratio
            max_key = key
    return max_key

def run_samples():
    data = json.load(open(decks_location, 'r'))
    keys = list(data.keys())
    model = Model.train()

    for t in tqdm(range(num_iter)):
        max_sample = 0
        arm = ""
        # shuffle the keys so we randomly pick the first 100
        # we do this since the threshold gets so high for MAB that it is basically impossible to surpass
        # so we'd only be looking at the first set of decks anyway
        random.shuffle(keys)
        for i in range(100):
            key = keys[i]
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

        # write every 25,000 so we can continually store data and our run won't be lost if it stops
        if t % 25000 == 0:
            with open(decks_location, "w") as outfile:
                json.dump(data, outfile)


if __name__ == "__main__":
    run_samples()
