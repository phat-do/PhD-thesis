""" from https://github.com/keithito/tacotron """
import re

from text import cleaners
from text.symbols import symbols

# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}

# Regular expression matching text enclosed in curly braces:
_curly_re = re.compile(r"(.*?)\{(.+?)\}(.*)")

with open('text/phoible_dict.pkl', 'rb') as readfile: # comes from phoible_prepare.py
	phoible_dict = pickle.load(readfile)

def phoible_filter(text):
    dic = {
        # remove tie bar
        't͡': 't',
        'd͡': 'd',

         # looks the same but actually different
        'ç': 'ç', 
        'ã': 'ã', 
        'ũ': 'ũ', 
        'ĩː': 'ĩː', 
        'õ': 'õ', 
        'ẽː':'ẽː', 
        'ẽ':'ẽ', 
        'g': 'ɡ', 
        
        # separate rhotic diacritic
        'ɝ': 'ə˞',
        'ɜ˞': 'ə˞',
        'ɚ': 'ə˞',

        # others
        'tɕʲ':'tɕ',
        'd͡ʒʱ':'dʒ',
        'dʒ̤':'d̤ʒ̤',
        'dʒʱ':'dʒ',
        'd͡ʒ̤':'d̤ʒ̤',
        'ɽ̥':'ɽ',
        'ʂʲː':'ʂ',
        'eʱ': 'eʰ',
        'ɫ̩': 'ɫ',
        'ɫː': 'ɫ',

        # too rare
        'ɕːʲ': 'ɕː',
        'd̪ᵊ':'d̪',
        'ˈɾ':'ɾ',
        }
    
    for k, v in dic.items():
        text = re.sub(k, v, text)
    
    return text

def text_to_sequence(text, cleaner_names):
    
    text = text.strip("{}")
    text = phoible_filter(text)
    
    sequence = torch.zeros((37)).unsqueeze(0) # initialize with the right dimention
    
    for phone in text.split(" "):
        temp = phoible_dict[phone].unsqueeze(0)
        sequence = torch.cat((sequence, temp), 0)

    sequence = sequence[1:, :] # get rid of first index: all zeros

    return sequence

def sequence_to_text(sequence):
    """Converts a sequence of IDs back to a string"""
    result = ""
    for symbol_id in sequence:
        if symbol_id in _id_to_symbol:
            s = _id_to_symbol[symbol_id]
            # Enclose ARPAbet back in curly braces:
            if len(s) > 1 and s[0] == "@":
                s = "{%s}" % s[1:]
            result += s
    return result.replace("}{", " ")


def _clean_text(text, cleaner_names):
    for name in cleaner_names:
        cleaner = getattr(cleaners, name)
        if not cleaner:
            raise Exception("Unknown cleaner: %s" % name)
        text = cleaner(text)
    return text


def _symbols_to_sequence(symbols):
    missing=[s for s in symbols if not _should_keep_symbol(s)]
    if missing:
        print('MISSING!: ', missing)
    return [_symbol_to_id[s] for s in symbols if _should_keep_symbol(s)]


def _arpabet_to_sequence(text):
    return _symbols_to_sequence(["@" + s for s in text.split()])


def _should_keep_symbol(s):
    return s in _symbol_to_id and s != "_" and s != "~"
