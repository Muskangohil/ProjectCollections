
#Note: this model is exact copy of the file moa_main.py but with 
#different chat()function as this py file will be working along side for
#for the GUI model file moa_gui.py
# look at the report for more details


import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle
from tensorflow.python.framework import ops
import pandas as pd


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

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]
        
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)


    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

ops.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model3.tflearn")

except: 


    model.fit(training, output, n_epoch=2500, batch_size=8, show_metric=True)
    model.save("model3.tflearn") 


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)




def feedback():
  
  print("What Flower is the fact about? ")
  ainp = input("You: ")
  
  for tg in data["intents"]:
      #if ainp ==tg['tag'] :
    inp= input("Please enter the fact:\n \n \n ")
      #print("thank you for your feedback :)")
    #for i in fd:
    #print("Enter user No-{}:".format(i+1))
    elm = inp
    fd.append(elm) #adding the element
    print(" the comment is entered", fd)
    break
"""
      else:
              
         print("yes done")
         break


"""
  
  #break    
      #if tg['tag'] == inp:
         # inp= input("Please enter the fact:\n \n \n ")  
          #if inp not in tg['responses']:
              #tg['responses'].apend(add)
             # break  

def get_inputs():
    #user input to record the log
    name = input(" Please enter your Name: ")
    d =  {} 
    d ["Flower"]= input("Please enter the flower's name: ")
    d['comment'] = input('Please enter your feedback or information: ')
    d['links'] = input("Please enter the source of information or a link ")
    return(name,d)
#print(pd.read_json('r.json')

bot_name = "Moa"  
 
def get_response(msg):
    
                
           
        #inp = nltk.word_tokenize(msg)
        results = model.predict([bag_of_words(msg, words)])[0]
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        #print(results)
        
        if results[results_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
    
            return (random.choice(responses))
        
        return "I didnt get that, try again please?"
    #with open('r.json','a') as f:
        #json.dump(out, f, indent=2)
    #print(pd.read_json('r.json'))

#chat()

