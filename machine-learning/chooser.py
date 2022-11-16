import random

import numpy
import json
import analysis as Model
from config import decks_location, small_decks_location
from tqdm import tqdm
from collections import OrderedDict

num_iter = 1000000
keys_to_look_at = 500
itr_to_store_data = num_iter / 10


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


def find_success_ratio(key, data):
    success = float(data[key][0])
    fail = float(data[key][1])
    return success


def write_data(data):
    ordered_keys = sorted(data.keys(), key=lambda x: find_success_ratio(x, data), reverse=True)
    list_of_key_value_pairs = [(key, data[key]) for key in ordered_keys]
    ordered_to_write = OrderedDict(list_of_key_value_pairs)
    with open(decks_location, "w") as outfile:
        json.dump(ordered_to_write, outfile)


def write_small_subset_data(data):
    ordered_keys = sorted(data.keys(), key=lambda x: find_success_ratio(x, data), reverse=True)
    list_of_key_value_pairs = []
    for i in range(keys_to_look_at):
        list_of_key_value_pairs.append((ordered_keys[i], data[ordered_keys[i]]))
    ordered_to_write = OrderedDict(list_of_key_value_pairs)
    with open(small_decks_location, "w") as outfile:
        json.dump(ordered_to_write, outfile)


def run_samples():
    data = json.load(open(decks_location, 'r'))
    keys = list(data.keys())
    model = Model.train()

    for t in tqdm(range(num_iter)):
        max_sample = 0
        arm = ""
        # shuffle the keys so the first keys we view are random
        # we do this since the threshold gets so high for MAB that it is basically impossible to surpass
        # past ~100 keys
        random.shuffle(keys)
        for i in range(keys_to_look_at):
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

        # write every so often to we can continually store data so our run won't be lost if it stops
        if t % itr_to_store_data == 0:
            write_small_subset_data(data)

    write_data(data)


if __name__ == "__main__":
    run_samples()
