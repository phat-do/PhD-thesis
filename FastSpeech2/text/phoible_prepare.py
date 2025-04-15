import pandas as pd
import torch, pickle
import pickle

# load PHOIBLE into a dataframe https://github.com/phoible/dev/blob/master/raw-data/FEATURES/phoible-segments-features.tsv
phoible_df = pd.read_csv("./phoible-segments-features.tsv", sep='\t')

# turn into more calculable format
phoible = dict()
for index, row in phoible_df.iterrows():
    vector_lst = row[1:] # 1st column is just the segment label
    phoible[row.segment] = torch.tensor([1.0 if i == '+' else 0.0 for i in vector_lst.values]) # both "0" (n/a) and "-" (no) can be considered "0"

phoible['sil'] = torch.zeros((37)) # to handle the silence token from MFA (note: can also do it another way: to have its own 38th value "is_silence")
phoible['spn'] = torch.zeros((37)) # "unknown" token from MFA

# dump into pickle file to use later
with open('phoible_dict.pkl', 'wb') as writefile:
	pickle.dump(phoible, writefile)
      
# note: depending on your data's annotation convention, there may be some weird symbols that are not in PHOIBLE. just use a dictionary to filter them out, e.g., 't͡': 't' (# remove tie bar)