import numpy
import json
import analysis as Model

num_iter = 100000


def run_samples():
    data = generate_decks()
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


def generate_decks():
    return []
