import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import pandas as pd
import tflearn
import tensorflow as tf
import random
import re
import json 
import pickle


def rearange_data(df):
    del df['Unnamed: 0']

    df = df.T

    df.columns = df.iloc[0]
    df = df.drop('Unnamed: 0.1')

    return df


df = pd.read_csv('Li-SOCl2/LS_LSH.csv')
df = rearange_data(df)


#s est une phrase, words sont tous les mots se trouvant dans les patterns
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)


def chat():
    print("You can start talking with the bot!\n"\
    "Type quit to quit the chat\n")
    while True:
        inp = input("You: ")
        if (inp.lower() == "quit"):
            break
        
        results = model.predict([bag_of_words(inp,words)])
        results_index = np.argmax(results)
        tag = labels[results_index]

        if (tag not in ["greeting", "goodbye", "name"]):
            pile_pattern = 'LSH? [0-9]*'
            pile_to_search = re.findall(pile_pattern, inp)

            #Une liste vide donne faux
            if not pile_to_search:
                print("You have to indicate a correct battery name")
            else:
                reponse = str(df.loc[pile_to_search, tag].to_numpy()[0])
                print("The " + tag.lower() + " of the "\
                + str(pile_to_search[0]) + " battery is " + reponse)
             
        else:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
                
            print(random.choice(responses))

        # if (tag == "Typical weight"):
        #     pile_pattern = 'LSH? [0-9]*'
        #     pile_to_search = re.findall(pile_pattern, inp)

        #     reponse = str(df.loc[pile_to_search, tag].to_numpy()[0])
        #     print("The weight of " + str(pile_to_search[0]) + ' is ' + reponse)


if __name__ == "__main__":
    stemmer = LancasterStemmer()

    with open("intents.json") as file:
        data = json.load(file)

    try:
        with open("data.pickle", "rb") as f:
            words, labels, training, output = pickle.load(f)
    except:
        words = []
        labels = []
        docs_x = []
        docs_y = []

        for intent in data["intents"]:
            for pattern in intent["patterns"]:
                wrds = nltk.word_tokenize(pattern)
                words.extend(wrds)
                docs_x.append(wrds)
                docs_y.append(intent["tag"])

            if intent["tag"] not in labels:
                labels.append(intent["tag"])

        words = [stemmer.stem(w.lower())
                for w in words if w != "?"]  # CONDITION PQ?
        words = sorted(list(set(words)))

        labels = sorted(labels)

        training = []
        output = []

        out_empty = [0 for _ in range(len(labels))]

        for x, doc in enumerate(docs_x):
            bag = []
            # On peut faire le stemming dans le premier for
            wrds = [stemmer.stem(w.lower()) for w in doc]

            #On check tous les mots qu'on a dans tous les patterns
            #Si le pattern qu'on traite mtn contient ce mot, alors
            #le bag of words decrivant ce pattern a 1 pour ce mot
            for w in words:
                if w in wrds:
                    bag.append(1)
                else:
                    bag.append(0)

            #Le label correspondant au bag qu'on a construit plus haut
            output_row = out_empty[:]
            output_row[labels.index(docs_y[x])] = 1

            training.append(bag)
            output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

    net=tflearn.input_data(shape=[None, len(training[0])])
    net=tflearn.fully_connected(net, 8)
    net=tflearn.fully_connected(net, 8)
    net=tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net=tflearn.regression(net)

    model=tflearn.DNN(net)

    # try:
    #     model.load("model.tflearn")
    # except:
    model.fit(training, output, n_epoch=500, batch_size=8, show_metric=True)
    model.save("model.tflearn")
    

    chat()
