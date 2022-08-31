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

from tkinter import*
from gallery import photo_gallery

with open("intents.json") as file: #load json file into this pyhton file
    data = json.load(file)

try: #trying opening the trained pickle file first if data has already ran 
     #through than saving and running it every time
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    
    #vocabualary - reads intent.json and stores all the words in list
    words = []  # storing each word from the json file
    labels = [] # storing "tags" from the json file
    docs_x = [] # storing patterns from the json
    docs_y = [] #storing what "tag" docs_x[n] is labelled as
    

    for intent in data["intents"]:  #loop to store relevant placeholder in the variable
        for pattern in intent["patterns"]:    #stemming of each word
            wrds = nltk.word_tokenize(pattern)#tokenize by returning a list
            words.extend(wrds)                #addition of all tokenized words in words
            docs_x.append(wrds)               #storing the current pattern
            docs_y.append(intent["tag"])      #storing the tag of the current pattern

        if intent["tag"] not in labels:       #appending labels to store all tags in the intent file
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]#stemming wording covering them to variables
    words = sorted(list(set(words)))                            #remove duplicates

    labels = sorted(labels)

    training = []   #ilsts to store 0 and 1's for One Hot Encoding
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        #creating an empty bag for OneHot Encoding
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]
        
        for w in words:      #loop for One HOt Encoding
            if w in wrds:
                bag.append(1)# if the word is in the sorted stemmed words then append bags by 1
            else:
                bag.append(0)# if the word id no, then append by 0.

        output_row = out_empty[:]  #creating a copy of out_empty
        output_row[labels.index(docs_y[x])] = 1 
        
        training.append(bag)       #bags of words for tarining
        output.append(output_row)  #output (the response array for Moa)


    training = numpy.array(training) #switching to numpy arrays
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

ops.reset_default_graph() #getting rid of the previous setting 

net = tflearn.input_data(shape=[None, len(training[0])]) # define the input shape
net = tflearn.fully_connected(net, 8) #8 neurons for the first input layer
net = tflearn.fully_connected(net, 8) #8 neurons  fir the second input layer
net = tflearn.fully_connected(net, len(output[0]), activation="softmax") #output layer with the result of higest probability with softmax enabled.
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model3.tflearn") # once the load saved trying loading the file directly than just training all over again.

except: 

    #training the model with e= 2500 which provides the accuracy of 99%.
    #model was also tested at n_epoch = 1000, 2000 .find the saved models in the file folder 
    model.fit(training, output, n_epoch=2500, batch_size=8, show_metric=True)
    model.save("model3.tflearn")  
"""
model.fit(training, output, n_epoch=2500, batch_size=8, show_metric=True)
model.save("model3.tflearn")  
"""

def bag_of_words(s, words): #coverting the user input into Bag-of-words
    bag = [0 for _ in range(len(words))] #creating an empty bag

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:  #if the current word exitings in the json file please append it to the bag.
                bag[i] = 1
            
    return numpy.array(bag) #return the bag of words as a numpy array





  

def get_inputs(): # for the feedback form
    #user input to record the log
    name = input(" Please enter your Name: ")
    d =  {} 
    d ["Flower"]= input("Please enter the flower's name:  ")
    d['comment'] = input('Please enter your feedback or information:  ')
    d['links'] = input("Please enter the source of information or a link:  ")
    return(name,d)

def get_inputs2(): # for the report-form
    #user input to record the log
    name = input(" Please enter your Name: ")
    d =  {} 
    d ["msg"]= input("Please describle the problem: ")
    return(name,d)


def helpsection(): # for the help-menu
    out={}
    #welcome statement and the help menu
    print("Moa: ********Welcome to the Help Department******** \n Please type the following number of interest to learn more about it. \n -How does the search for works?? : Press 1 \n -To learn above the avaiable data in Moa: Press 2\n -Others: Press 3"  )
    inp = input("You: ") #if the user input from is the following options
    #then print the simultaneous answer
    if inp.lower() == "1": 
        print("Moa is chatbot which shares information about Flowers. \n There are 3 major types of searches which can be performed in Moa. \n - Search about a particular Flower \n - Search for a list of all of Flower beginning with an Alphabet \n - And Pictorial Search. ")
        inp = input("You: ")
        
    elif inp.lower() == "2":
        print("The informational database of Moa is fully fed. \nCurrently The Database for Moa consists: The Alphabetical list of Flower from the range A to D. \nThe informational data for a particular Flower search is for: Rose, Sunflower and Lily. \nPictoral Search data for a flower is the same wel:Rose, sunflower, Lily. \n \n Moa will soon will be ready will more Flowers. THANK YOU!! ")
        inp = input("You: ")
        
    elif inp.lower() =="3":
        print("Would you like to Report a problem a issue with Moa??")
        inp = input("You: ")
        
        exit = input('Moa:  Would you like to Report a problem?  (y/n)? ')
        if exit.lower() == 'n':
            print("Thank you !!!!!")
            
        else:
            name, d = get_inputs2()
            out[name] = d
            print(" \nThank you, The team will get back to you shortly.")
        
    with open('f.json','a') as f:
        json.dump(out, f, indent=2) 
        
def feedback(): #for the user to give the feedback to moa'system
    out={}
    print("Moa: Would you like to give us any extra funfact about flowers that we can add to the library :)?? (yes/no)")
  
    inp = input("You: ")
    if inp.lower() == "yes":
        exit = input('MOa: Do you want to give use an information about a flower??  (y/n)? ')
        if exit.lower() == 'n':
            a= input("Moa: Please rate your experience on the scale of 1-5 :) \n")
            print("Thank you !!!!!")
            
        else:
            name, d = get_inputs()
            out[name] = d
    else: 
        print("MOa: ByeBye")
        
        

    with open('r.json','a') as f:       #to dump python format user-input a json file
        json.dump(out, f, indent=2)
        #print(pd.read_json('r.json',lines= True))
        #break
    
def chat(): #the main chat function which runs the Moa and calls out all the functionalities
    print("\n \n \n*********************************************************")
    print("Moa : Welcome to the World of Flowers :) \n 1) To find the list of flowers type the alphabetical letter (e.g. Letter A) \n 2) To search about a specific flower type their name (e.g. Rose) \n 3) To Write a feedback please type Quit and select the Feedback option. \n 4) To view photo-gallery, Please type: photo \n 5) To view feedbacks and sources shared by other users,\n Please type: feedback \n 6) For Help-Menu, Please type: help \n \n  Start talking with the bot (type quit to stop)!")
    out = {}
    while True:
        inp = input("You: ")
        
        if inp.lower() == "photo":
            print("Moa:what flower's picture would you like to see?")
            photo_gallery()
            inp = input("You: ")
        
        elif inp.lower()== "help":
            helpsection()
            inp = input("You: ")
            
        elif inp.lower()== "feedback":
            print("Moa:***************Apologizes***************** \nThis feature is under construction at the moment, Kindly come back later to operate it :)")
            inp = input("You: ")
            #the displaying feedback feature was giving errors hence it just prints the message
            #with open('r.json','a') as f:
                #json.dump(out, f, indent=2)
            #print(pd.read_json('r.json',lines= True))
                
        elif inp.lower() == "quit":
           
            feedback()
            print("\n       Thank you, BYE!!   ")
            break
            

       
           
        #turning the input from the user into bag of words
        results = model.predict([bag_of_words(inp, words)])[0]
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        #print(results)
        
        if results[results_index] > 0.7: # Threshold is set 0.7 = 70% probability at the minimum
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
    
            print("Moa:",random.choice(responses)) #chose a random response from the 'response' inside the json file
        
        else:
            print("I didnt get that, try again please?") #or return this statement
    

chat()

