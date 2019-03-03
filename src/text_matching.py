import Levenshtein
import numpy as np
from itertools import permutations

def best_matches(words, db):
    dist_matches = []
    ratio_matches = []
    best_match = 1000
    for full_name in db:
        split_name = full_name.lower().split(" ")
        scores = []
        for name in split_name:
            temp_score = 1000
            temp_best = tuple()
            for i, word in enumerate(words):
                dist = Levenshtein.distance(name, word)/len(name) 
                if dist < temp_score:
                    print(name, word,  dist)
                    temp_score = dist
                    temp_best= (temp_score, name, word)
            scores.append(temp_best)
        print(scores)
        tot = sum([val for val, name, word in scores])
        if tot < best_match:
            dist_matches.append((tot, full_name))

    sorted_dist_matches = sorted(dist_matches, key= lambda x: -x[0])
    #sorted_ratio_matches = sorted(ratio_matches, key= lambda x: x[0])
    return sorted_dist_matches[-3:]



if __name__ == "__main__":
    cam_out = "Hector Pontis is a banana slug, \n 487 Commonwealth Ave \n Boston, MA 02215, James"
    names = {"James", "Joyce", "Sara", "Blake", "Nic","Andre", "Nick", "Nicholas", "Andres", "Salamander", "Peacock", "Hector", "Pontis"}

    full_names = ["Hector Pontis", "James Joyce"]

    #lower_names = {name.lower() for name in names}

    cam_words = cam_out.replace('\n', '').replace("  ",' ').lower().split(" ")

    #print(cam_words)

    out = best_matches(cam_words, full_names)
    print(out)
    
