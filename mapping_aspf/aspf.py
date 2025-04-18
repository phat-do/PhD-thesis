import re, pathlib, math
import numpy as np

from helper.functions import read_phoible, process_phoneset, angular_similarity, find_closest, pf_adjacent
from helper.lists import full_phone_list, invalid_tokens

def aspf(source_lang, target_lang, common_path):
    
    # extract phonesets and frequency dictionaries
    source_phoneset, source_freq_dict = process_phoneset(common_path / source_lang / 'train.txt')
    target_phoneset, target_freq_dict = process_phoneset(common_path / target_lang / 'train.txt')
    
    source_values, target_values = np.array(list(source_freq_dict.values())), np.array(list(target_freq_dict.values()))
    
    return angular_similarity(source_values, target_values)
    
if __name__ == '__main__':
    
    # common path for metadata files
    common_path = pathlib.Path("./train_data")
    
    # define languages
    source_lang = 'en' # English
    target_lang = 'bg' # Bulgarian
    
    print(aspf(source_lang, target_lang, common_path))