import numpy
import json
import analysis as Model

def run_samples():

    data = generate_decks()

    T = 100,000
    for t in range(T):
        
        max_sample = 0
        for deck in data:
            
            alpha, beta = deck[0], deck[1]
            s = numpy.random.beta(alpha, beta)
            if max_sample < s:
                
                arm = deck
                max_sample = s
            
        model = Model.train()
        if model.predict(arm):
            data[arm][0] += 1        
        else:
            data[arm][1] += 1


def generate_decks():
    
    
