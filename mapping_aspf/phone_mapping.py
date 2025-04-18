import pathlib, tqdm, pickle, re
import pandas as pd, numpy as np

from helper.functions import read_phoible, process_phoneset, angular_similarity, find_closest, pf_adjacent
from helper.lists import full_phone_list, invalid_tokens

def phone_mapping(source_lang, target_lang, common_path, phoible):
    output = dict()
    
    # extract phonesets and frequency dictionaries
    source_phoneset, source_freq_dict = process_phoneset(common_path / source_lang / 'train.txt')
    target_phoneset, target_freq_dict = process_phoneset(common_path / target_lang / 'train.txt')

    for phone in target_phoneset:
        if phone in source_phoneset: # if exists in source language
            output[phone] = phone # no mapping needed
        else:
            closest_phones = find_closest(phone, source_phoneset, phoible)
            if len(closest_phones[1]) == 1: # if there are no ties
                output[phone] = closest_phones[1][0] # map to that only candidate
            else: # if there are ties
                pf_target = pf_adjacent(common_path, phone, target_lang) # get frequencies of all phones occuring before and after <phone> in <target_lang>
                candidate_score_dict = dict()
                
                for tie_candidate in closest_phones[1]:
                    pf_candidate = pf_adjacent(common_path, tie_candidate, source_lang)  # get frequencies of all phones occurring before and after <tie_candidate> in <source_lang>
                    aspf_front = angular_similarity(pf_target[0], pf_candidate[0])
                    aspf_back = angular_similarity(pf_target[1], pf_candidate[1])
                    aspf_avg = (aspf_front + aspf_back) / 2
                    candidate_score_dict[tie_candidate] = aspf_avg

                choice = max(candidate_score_dict, key=candidate_score_dict.get)
                output[phone] = choice
                    
    return output
    
if __name__ == '__main__':
    
    # read phoible 
    phoible = read_phoible("../assets/phoible-segments-features.tsv")
    
    # common path for metadata files
    common_path = pathlib.Path("./train_data")
    
    # define languages
    source_lang = 'en' # English
    target_lang = 'bg' # Bulgarian
    
    mapping_result = phone_mapping(source_lang, target_lang, common_path, phoible)
    print(mapping_result['o']) # 'ʉ' from candidates ['ɒ', 'ʉ', 'ʊ']