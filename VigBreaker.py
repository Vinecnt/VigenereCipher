from sympy.ntheory import factorint
import numpy as np
import pandas as pd
from ic import *


not_processed_cipher_text = "TSMVM MPPCW CZUGX HPECP RFAUE IOBQW PPIMS \n" \
         "FXIPC TSQPK SZNUL OPACR DDPKT SLVFW ELTKR \n" \
         "GHIZS FNIDF ARMUE NOSKR GDIPH WSGVL EDMCM \n" \
         "SMWKP IYOJS TLVFA HPBJI RAQIW HLDGA IYOUX \n"
cipher_text = not_processed_cipher_text.replace("\n", "")
cipher_text = cipher_text.replace(" ", "")
cipher_text = cipher_text.lower()


def get_factors(num_int):
    ret_list = []
    sub_dict = factorint(num_int)
    for key in sub_dict.keys():
        ret_list = ret_list + [str(key)] * sub_dict[key]
    return ", ".join(ret_list)


# found this piece of code logic at
# https://cs.stackexchange.com/questions/79182/im-looking-for-an-algorithm-to-find-unknown-patterns-in-a-string
def show_repetitions(c_text):
    s = c_text
    min_len = 2
    min_cnt = 2
    d = {}
    for sub_len in range(min_len, int(len(s)/min_cnt)):
        for i in range(0, len(s)-sub_len):
            sub = s[i:i+sub_len]
            cnt = s.count(sub)
            if cnt >= min_cnt and sub not in d:
                start = i
                # find the substring in s start at i+1
                end = s.find(sub, i+1)
                d[sub] = [start, end, end-start, get_factors(end-start)]
    df = pd.DataFrame(d, index=['start', 'end', 'distance', 'factors'])
    print(df.T)


def break_n_parts(c_text, n):
    alphabet_list = [c_text[i::n] for i in range(0, n)]
    return alphabet_list


def get_letter_frequencies(alphabet_list):
    ret_list = []
    for x in alphabet_list:
        freq_list = [0]*26
        for letter in list(map(chr, range(97, 123))):
            freq_list[ord(letter)-97] = x.lower().count(letter)
        ret_list = ret_list + [freq_list]
    return ret_list


def show_freq(freq):
    char_freq = list("HMMMHMMHHMMMMHHMLHHHMLLLLL")
    df_freq = pd.DataFrame(freq + [char_freq], columns=list(map(chr, range(97, 123))))

    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    print(df_freq)


def replace_letter(alphabet_num, period, a_maps_to, c_text):
    map_distance = (ord(a_maps_to) - ord("a"))
    for x in range(alphabet_num, len(c_text), period):
        letter = chr((ord(c_text[x]) - 97 - map_distance + 26) % 26 + 97)
        c_text = c_text[:x] + letter.upper() + c_text[x+1:]
    return c_text


def readable_c_text(c_text):
    ret_list = [c_text[i:i+5]+" " for i in range(0, len(c_text), 5)]
    ret_str = ""
    for x in range(0, len(ret_list), 7):
        ret_str = ret_str + "".join(ret_list[x:x+7]) + "\n"
    print(ret_str)


# 1) get a period: show_repetitions(cipher_text) ~ period 5 or 11
# show_repetitions(cipher_text0
# 2) test IC:  get_IC(cipher_text) ~ 0.040 which is closer to 10 than 5
# get_IC(cipher_text)
# 3) Break message into n parts/ split into alphabets: choose period of 5; they do not suggest ic of 5
ab_list = break_n_parts(cipher_text, 5)
# for x in break_n_parts(cipher_text, 5):
#     get_IC(x)
# 4) frequency examination
frequencies = get_letter_frequencies(ab_list)
show_freq(frequencies)
# 5) Begin decryption
# Alphabet 0 looks like the normal alphabet
replaced_cipher = replace_letter(0, 5, "a", cipher_text)

# Alphabet 3 looks like c_text C maps to A
replaced_cipher = replace_letter(3, 5, "c", replaced_cipher)

# Alphabet 1 looks like c_text L maps to A (maybe) #matched the pattern
replaced_cipher = replace_letter(1, 5, "l", replaced_cipher)

# Alphabet 2 looks like c_text I maps to A (maybe) #abnormally high i
replaced_cipher = replace_letter(2, 5, "i", replaced_cipher)

# Alphabet 4 guess c_text
replaced_cipher = replace_letter(4, 5, "e", replaced_cipher)

readable_c_text(replaced_cipher)
print(replaced_cipher)