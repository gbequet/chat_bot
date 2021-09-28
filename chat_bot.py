import pandas as pd
import numpy as np
import re
from collections import Counter
# from keras.preprocessing.text import Tokenizer

def rearange_data(df):
    del df['Unnamed: 0']

    df = df.T

    df.columns = df.iloc[0]
    df = df.drop('Unnamed: 0.1')

    return df


def most_frequent(list):
    occurence_count = Counter()
    for l in list:
        tmp = Counter(l)
        occurence_count = occurence_count + tmp
        
    return occurence_count.most_common(1)[0][0]


# Les piles commencent forcement par ca (à completer)
pile_prefix = ['LS', 'LSH']


if __name__ == "__main__":
    pile_pattern = 'LSH? [0-9]*'
    df = pd.read_csv('Li-SOCl2/LS_LSH.csv')

    df = rearange_data(df)

    attribute_names = list(df.columns)

    pile_names = []
    for i in range(len(df)):
        pile_names.append(df.iloc[i].name)

    print(pile_names)
    print(attribute_names)


    # question = "Cell size of LS 14250 ?"

    print('\n\n>>>> Bienvenue dans le chat bot des bg !')
    while True:
        question = input('>>>> ')
        word_list = question.split()

        res = []
        for w in word_list:
            if w != '?':
                r = re.compile('.*' + w)
                newlist = list(filter(r.match, attribute_names))
                if (len(newlist) != 0):
                    res.append(newlist)

        attr_to_search = most_frequent(res)

        pile_to_search = re.findall(pile_pattern, question)


        reponse = str(df.loc[pile_to_search, attr_to_search].to_numpy()[0])
        print(">>>> " + str(reponse))

    
    



