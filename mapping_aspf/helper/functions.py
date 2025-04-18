import math, operator, collections, re
import numpy as np, pandas as pd
from .lists import invalid_tokens, full_phone_list

def read_phoible(path):
    phoible_df = pd.read_csv(path, sep='\t', skiprows=2)
    phoible = dict()
    for index, row in phoible_df.iterrows():
        vector = np.array(row[1:]) # skipping segment label
        phoible[row.segment] = vector
    return phoible

def angular_similarity(vector_a, vector_b):
    cosine_similarity = np.inner(vector_a, vector_b) / (np.linalg.norm(vector_a) * np.linalg.norm(vector_b))
    cosine_similarity = 0 if math.isnan(cosine_similarity) else cosine_similarity

    angular_similarity = 1 - (2 * np.arccos(cosine_similarity) / np.pi)

    return angular_similarity

def process_phoneset(path_to_train_data):
    temp_set = set()
    freq_dict, freq_dict_count = dict(), dict()
    for phone in full_phone_list:
        freq_dict_count[phone] = 0
    
    with open(path_to_train_data, 'r', encoding='utf-8') as readfile:
        for readline in readfile.readlines():
            wavfile, speaker, annotation, text = readline.split("|")
            annotation = annotation.strip(r"{}")
            for phone in annotation.split(" "):
                if phone not in invalid_tokens:
                    temp_set.add(phone)
                    if phone not in freq_dict_count:
                        freq_dict_count[phone] = 0
                    else:
                        freq_dict_count[phone] += 1

    phoneset = sorted(list(temp_set))

    for phone, count in freq_dict_count.items():
        freq_dict[phone] = count / sum(freq_dict_count.values())

    return phoneset, freq_dict

def find_closest(phone, source_phoneset, database):
    compare_vector = database[phone]
    candidate_scores = dict()

    for candidate in source_phoneset:
        candidate_vector = database[candidate] if candidate != 'ɜ˞' else database['ə˞'] # special case
        candidate_score = np.sum(compare_vector == candidate_vector) # sums of True = similarity score (out of 37)
        if candidate_score not in candidate_scores.keys():
            candidate_scores[candidate_score] = [candidate]
        else:
            candidate_scores[candidate_score].append(candidate)
    
    candidate_scores = sorted(candidate_scores.items(), key=operator.itemgetter(0), reverse=True)
    candidate_scores = collections.OrderedDict(candidate_scores)
    result = candidate_scores.popitem(last=False)
    
    return result

def pf_adjacent(common_path, phone, language): # returns a tuple of padded phone frequencies of adjacent positions of a phone in a language

    #find all occurrences
    with open(common_path / language / 'train.txt', 'r', encoding='utf-8') as readfile:
        content = readfile.read() # read train.txt file
        content = re.sub(r'.*\|\{', '', content) # remove all, leave only the phone annotations
        content = re.sub(r'\}\|.*', '', content)
        occurrences_pre = re.findall(r'(?:^|\s)([\S]+) ' + phone + r'(?:$|\s)', content)
        occurrences_post = re.findall(r'(?:^|\s)' + phone + r' ([\S]+)(?:$|\s)', content)

    front_freq_dict_count, back_freq_dict_count = dict(), dict() # initialize dicts to store counts
    front_freq_dict, back_freq_dict = dict(), dict() # dicts to store the frequencies

    for phone in full_phone_list: # populate the empty dicts
        if phone not in invalid_tokens:        
            front_freq_dict_count[phone] = 0
            back_freq_dict_count[phone] = 0

    for phone in occurrences_pre: # count the occurrences of each phone
        if phone not in invalid_tokens:
            front_freq_dict_count[phone] += 1
    
    for phone in occurrences_post:
        if phone not in invalid_tokens:
            back_freq_dict_count[phone] += 1

    for k, v in front_freq_dict_count.items():
        front_freq_dict[k] = v / sum(front_freq_dict_count.values())

    for k, v in back_freq_dict_count.items():
        back_freq_dict[k] = v / sum(back_freq_dict_count.values())

    return np.array(list(front_freq_dict.values())), np.array(list(back_freq_dict.values()))
