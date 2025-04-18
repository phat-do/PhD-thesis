import torch, pickle
import pandas as pd, numpy as np

if __name__ == '__main__':
    
    # load PHOIBLE into a dataframe
    phoible_df = pd.read_csv("../assets/phoible-segments-features.tsv", sep='\t', skiprows=2)
    phoible = dict()

    # turn into more calculable format
    for index, row in phoible_df.iterrows():
        vector_lst = row[1:]
        phoible[row.segment] = torch.tensor([1.0 if i == '+' else 0.0 for i in vector_lst.values])

    # special cases (alternatively, could have their own one-hot feature)
    phoible['sil'] = torch.zeros((37))
    phoible['spn'] = torch.zeros((37))

    # save as pickled dictionary for later use    
    with open('phoible_dict.pkl', 'wb') as writefile:
        pickle.dump(phoible, writefile)