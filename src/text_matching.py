import Levenshtein
import numpy as np
from itertools import permutations

def best_matches(mail_string, db, thresh=0.25):
    words = mail_string.replace('\n', ' ').replace("  ",' ').lower().split(" ")

    print(words)

    dist_matches = []
    ratio_matches = []
    best_match = 1000
    for full_name in db:
        split_name = full_name.lower().split(" ")
        # print('Split name:', split_name)
        scores = []
        for name in split_name:
            temp_score = 1000
            temp_best = tuple()
            for i, word in enumerate(words):
                dist = Levenshtein.distance(name, word) 
                # print('Distance: ', dist, name, word)
                if dist < temp_score:
                    #print(name, word,  dist)
                    temp_score = dist
                    temp_best = (temp_score, name, word)
            scores.append(temp_best)
        
        print(scores)
        tot = sum([val for val, name, word in scores])
        if tot < best_match:
            dist_matches.append((tot/len(full_name), full_name))

    sorted_dist_matches = sorted(dist_matches, key= lambda x: -x[0])
    #sorted_ratio_matches = sorted(ratio_matches, key= lambda x: x[0])

    # print(sorted_dist_matches[-3:])
    print(sorted_dist_matches)

    if sorted_dist_matches[-1][0] < thresh:
        return sorted_dist_matches[-1]
    else:
        return None, None


if __name__ == "__main__":
    # cam_out = "Roberto Wheeler is a banana slug, \n 487 Commonwealth Ave \n Boston, MA 02215, James"
    
    # database = {"Victor Pontis":"iperper@mit.edu", "Christopher Puchi": "iperper@mit.edu", "Enes Gotkas": "iperper@mit.edu", "Arash Kani":"iperper@mit.edu", "Diana Martin": "iperper@mit.edu", "Rob Wheeler": "iperper@mit.edu", "Jacob Jurewicz": "iperper@mit.edu" , "Mark Halsey": "iperper@mit.edu", "Lizi Yuan": "iperper@mit.edu"}

    # full_names = list(database.keys())

    # out = best_matches(cam_out, full_names, 0.30)
    
    # if not out:
    #     print("No Name Returned")
    # else:
    #     print(out[1])
    pass
    
