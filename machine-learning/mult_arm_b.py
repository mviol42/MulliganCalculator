import numpy
import json
import analysis as Model
from data import deck_generator

num_iter = 100000


def run_samples():
    data = deck_generator.generate_decks()
    model = Model.train()
    for t in range(num_iter):
        max_sample = 0
        arm = data[0]
        for deck in data:
            alpha, beta = deck[0], deck[1]
            s = numpy.random.beta(alpha, beta)
            if max_sample < s:
                arm = deck
                max_sample = s

        prediction = model.predict(arm)
        if prediction >= 0.5:
            data[arm][0] += 1
        else:
            data[arm][1] += 1
