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
import os


class Bot:
    def __init__(self):
        self.df = pd.read_csv('all_pile.csv')
        self.df = self.df.set_index('Unnamed: 0')

        self.stemmer = LancasterStemmer()

        with open("intents.json") as file:
            self.data = json.load(file)

        try:
            with open("data.pickle", "rb") as f:
                self.words, self.labels, self.training, self.output = pickle.load(f)
        except:
            self.words = []
            self.labels = []
            self.docs_x = []
            self.docs_y = []

            for intent in self.data["intents"]:
                for pattern in intent["patterns"]:
                    wrds = nltk.word_tokenize(pattern)
                    self.words.extend(wrds)
                    self.docs_x.append(wrds)
                    self.docs_y.append(intent["tag"])

                if intent["tag"] not in self.labels:
                    self.labels.append(intent["tag"])

            self.words = [self.stemmer.stem(w.lower())
                    for w in self.words if w != "?"]  # CONDITION PQ?
            self.words = sorted(list(set(self.words)))

            self.labels = sorted(self.labels)

            training = []
            output = []

            out_empty = [0 for _ in range(len(self.labels))]

            for x, doc in enumerate(self.docs_x):
                bag = []
                # On peut faire le stemming dans le premier for
                wrds = [self.stemmer.stem(w.lower()) for w in doc]

                #On check tous les mots qu'on a dans tous les patterns
                #Si le pattern qu'on traite mtn contient ce mot, alors
                #le bag of words decrivant ce pattern a 1 pour ce mot
                for w in self.words:
                    if w in wrds:
                        bag.append(1)
                    else:
                        bag.append(0)

                #Le label correspondant au bag qu'on a construit plus haut
                output_row = out_empty[:]
                output_row[self.labels.index(self.docs_y[x])] = 1

                self.training.append(bag)
                self.output.append(output_row)


        self.training = np.array(self.training)
        self.output = np.array(self.output)

        with open("data.pickle", "wb") as f:
            pickle.dump((self.words, self.labels, self.training, self.output), f)

        net = tflearn.input_data(shape=[None, len(self.training[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(self.output[0]), activation="softmax")
        net = tflearn.regression(net)
        
        self.model = tflearn.DNN(net)

        if os.path.exists("model.tflearn.meta"):
            self.model.load("model.tflearn")
        else:
            self.model.fit(self.training, self.output, n_epoch=500, batch_size=8, show_metric=True)
            self.model.save("model.tflearn")


    def treat_message(self, question):
        results = self.model.predict([self.bag_of_words(question)])
        results_index = np.argmax(results)
        tag = self.labels[results_index]

        if (tag not in ["greeting", "goodbye", "name"]):
            pile_pattern = 'LSH [0-9]{2}\-[0-9a-zA-Z]+|LSH? [0-9]{2}\s[A-Z][a-zA-Z]+|'\
                'LSH? [0-9a-zA-Z]*|'\
                'G [0-9]{2}/[0-9](?![0-9a-zA-Z])|'\
                'LO [0-9]{2} SXC?(?![0-9a-zA-Z])|LO [0-9]{2} SHX?(?![0-9a-zA-Z])|'\
                'M [0-9]{2} HR(?![0-9a-zA-Z])|M [0-9]{2}(?![0-9a-zA-Z])'
            pile_to_search = re.findall(pile_pattern, question)

            #Une liste vide donne faux
            if not pile_to_search:
                rep = "You have to indicate a correct battery name"
            else:
                try:
                    reponse = str(self.df.loc[pile_to_search, tag].to_numpy()[0])
                    rep = "The " + tag.lower() + " of the " + str(pile_to_search[0]) + " battery is " + reponse
                except:
                    rep = "You have to indicate a correct battery name"

        else:
            for tg in self.data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']

            rep = random.choice(responses)
        
        return rep


    # s est une phrase, words sont tous les mots se trouvant dans les patterns
    def bag_of_words(self, s):
        bag = [0 for _ in range(len(self.words))]

        s_words = nltk.word_tokenize(s)
        s_words = [self.stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i, w in enumerate(self.words):
                if w == se:
                    bag[i] = 1

        return np.array(bag)
