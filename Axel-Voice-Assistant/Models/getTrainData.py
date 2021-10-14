import pandas as pd
import os, sys, time
from RandomWordGenerator import RandomWord
import random, json

#############################
#This script takes a skeleton of phrases, adds random words, and creates a ton of datasets to train a model
#############################
with open(os.path.join(os.path.dirname(sys.argv[0]),'config.json')) as jsonFile:
    jsonConfigFile = json.load(jsonFile)
    csvPath = os.path.join(os.path.dirname(sys.argv[0]),r'Train_Data\{}'.format(jsonConfigFile['CSV TRAIN DATA'].strip()))
    inputPath = os.path.join(os.path.dirname(sys.argv[0]),r'Train_Data\{}'.format(jsonConfigFile['STATE TRAIN DATA'].strip()))

NumberOfData = 150

phraseDict = {}
inputPhrases = []
inputState = []
r = RandomWord(constant_word_size=False)
with open(inputPath,'r') as inFile:
    for line in inFile.readlines():
        line = line.replace('\n','')
        if line == '' or line.startswith('#'): continue

        line = line.split(',')
        phraseDict[line[0]] = line[1]
    
    for key in phraseDict.keys():
        state = phraseDict[key]
        for rangeNum in range(NumberOfData):
            phraseIn = key

            digit = 0
            while any(char.isdigit() for char in phraseIn):
                rw = ''
                randomInt = random.randint(1,5)
                for rand in range(randomInt):
                    rw = f"{rw}{r.generate()} "
                
                phraseIn = phraseIn.replace(str(digit), rw.strip())
                digit+=1
            inputPhrases.append(phraseIn)
            inputState.append(state)



if len(inputPhrases) > 0 and len(inputState) > 0:
    with open(csvPath, 'w') as csv:
        csv.write(f"Phrases,State")
        csv.write('\n')
        for i, p in enumerate(inputPhrases):
            print(f'Wrote {i+1} to csv',end='\r')
            csv.write(f"{p},{inputState[i]}")
            csv.write('\n')