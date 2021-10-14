import random
from chatterbot.chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_first_response
from chatterbot.comparisons import SynsetDistance, LevenshteinDistance
import os
import logging, pyttsx3, random
import speech_recognition as sr
from difflib import SequenceMatcher
from chatterbot.conversation import Statement

#Synset Distance = distance of synonyms between strings
#Sentiment Analysis = Analyzes whether a sequence is more +ve-sounding or -ve-sounding, depending on NLP analysis and word choice!
#Levenshetein Distance = The minimum number of single-character edits (insertons, deletions, substitutions) to change one string into another string

class Person():
    def __init__(self,name=None,mood=None,favorites=None):
        self.name = name
        self.mood = mood #happy, sad, neutral
        self.favorites = favorites

def getFromTxt(file='config.txt',keyline='',delimiters=[':','\n']):
    myFile = open(file,'r')
    for line in myFile:
        if line.startswith(keyline):
            length = len(keyline)
            outputline = line[length::]
            for delimiter in delimiters:
                outputline = outputline.replace(delimiter,'')
            return outputline
    return ''

def initializePerson():
    user = Person()
    dirname = os.path.dirname(__file__)
    file = os.path.join(dirname,'user.txt')
    user.name = getFromTxt(file,'Name')
    user.mood = getFromTxt(file,'Mood')
    user.favorites = getFromTxt(file,'Favorites')
    return user

def Rant():
    responses = ['Right', 'I see', 'I understand', 'Please go on', 'Tell me more']
    speech = ['placeholder', 'speech', 'for', 'now', 'lmao', 'a', 'ewtwe', 'werwerew', 'werewrewfwtwer']
    while len(speech) < 6:
        speech = input('Nusair: ')
        response = responses[random.int(0,len(responses) - 1)]
        print('Axel: ' + response)
        talkToBot(speech=speech,response=response)
        speech = speech.split(' ')

def trainBot(bot):
    dirname = os.path.dirname(__file__)
    conversationsFile = os.path.join(dirname,'conversations.txt')
    corpusTrainer = ChatterBotCorpusTrainer(bot)
    corpusTrainer.train('chatterbot.corpus.english')
    trainer = ListTrainer(bot)
    file = open(conversationsFile, 'r')
    lines = file.readlines()
    conversationList = []
    conversation = []
    i = 0
    
    for line in lines:
        line = line.replace('\n', '')
        lines[i] = lines[i].replace('\n','')
        if line == '':
            trainer.train(conversation)
            conversation.clear()
        elif line not in conversationList:
            conversation.append(line)
        conversationList.append(line)
        i+=1
    file.close()

    
def writeFromToFile(fileSrc,fileDest, mode='w', limit=-1):
    memory = open(fileSrc, 'r')
    memoryLongTerm = open(fileDest,'r')
    memoryLongContents = memoryLongTerm.readlines()
    
    memoryLongTerm.close()
    memoryLongTerm = open(fileDest, mode)
    limit = int(limit)
    tocopy = memory.readlines()
    if limit < 0:
        limit = len(tocopy)

    elif limit < len(tocopy):
        startIndex = len(tocopy) - limit
        tocopy = tocopy[startIndex::]
    
    k = 1
    for line in tocopy:
        if k == 0:
            k+=1
        else:
            if line in memoryLongContents and k != 0:
                i = memoryLongContents.index(line)
                j = tocopy.index(line)
                if i + 1 >= len(memoryLongContents) or j + 1 >= len(tocopy):
                    memoryLongTerm.write(line)
                elif tocopy[j+1] not in memoryLongContents[i+1]:
                    memoryLongTerm.write(line)
                else:
                    k = 0
            else:
                memoryLongTerm.write(line)

        
   
    memory.close()
    memoryLongTerm.close()

def talkToBot(bot=None,speech='',response=''):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'memory.txt')
    memoryRead = open(filename,'r')
    lines = memoryRead.readlines()
    i = 0
    j = 0
    ratios = []
    possibleResponses = []
    if response == '':
        for l in lines:
            l = l.replace('\n','')
            if l == '':
                j+=1
                continue
            if i % 2 == 0:
                fileStatement = Statement(l.lower())
                speechStatement = Statement(speech.lower())
                synset = LevenshteinDistance()
                print(synset.compare(statement=fileStatement,other_statement=speechStatement))
                if synset.compare(statement=fileStatement,other_statement=speechStatement) > 0.9 and i < len(lines) - 1:
                    possibleResponse = lines[j+1]
                    possibleResponses.append(possibleResponse.replace('\n',''))
                    ratios.append(synset.compare(statement=fileStatement,other_statement=speechStatement))
            i+=1 #Keeps track of if we're even or odd
            j+=1 #Keeps track of place in the list
        
        if len(ratios) > 0:
            i = ratios.index(max(ratios))
            response = possibleResponses[i]

            maxRatioStatements = []
            maxVal = max(ratios)
            i = 0

            for r in ratios:
                if r >= maxVal:
                    maxRatioStatements.append(possibleResponses[i])
                i+=1

            response = maxRatioStatements[random.randint(0,len(maxRatioStatements) - 1)]

    if response == '':
        response = bot.get_response(speech)
        response = response.text

    lines.append(speech)
    lines.append(response)
    lines.append('\n')
    

    if len(lines) > 300 and len(lines) % 2 == 0:
        lines.pop(0)
        lines.pop(0)

    memoryRead.close()
    memoryWrite = open(filename,'w')

    for l in lines:
        l = l.replace('\n','')
        memoryWrite.writelines(l + '\n')

    memoryWrite.close()
    return response        

dirname = os.path.dirname(__file__)
memoryFile = os.path.join(dirname, 'memory.txt')
longTermMemoryFile = os.path.join(dirname, 'memoryLongTerm.txt')
conversationsFile = os.path.join(dirname,'conversations.txt')

logging.basicConfig(level=logging.INFO)
bot = ChatBot(
    name='Axel',
    #read_only=True,
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///' + dirname + '/db.sqlite3',
    logic_adapters=[
            {
                "import_path": "chatterbot.logic.BestMatch",
                "statement_comparison_function": LevenshteinDistance
            },
        ],
    response_selection_method=get_first_response)
user = initializePerson()

while True:
    #try:
        print('1:Train with data\n2:Forget\n3:Train with talking')
        print('4:Commit to long term memory\n5:Transfer long term memory to short term')
        print('6:Transfer file contents to another file\n7:Transfer memory to training data\n8:Transfer long term memory to training data')
        try:
            choice = int(input('What do you want to do: '))
        except:
            choice = int(input("Choose an integer: "))
    
        if choice == 1:
            trainBot(bot)
        elif choice == 2:
            bot.storage.drop()
            print('erased Axel\'s memory')
        elif choice ==4:
            writeFromToFile(memoryFile,longTermMemoryFile,'a')
        elif choice == 5:
            limit = int(input('What is the limit (choose positive even number): '))
            while limit % 2 != 0 and not limit > 0:
                limit = int(input('Limit must be positive even number: '))
            writeFromToFile(longTermMemoryFile,memoryFile,mode='w',limit=limit)
        elif choice == 6:
            src = os.path.join(dirname, input('What is the src file name: '))
            dest = os.path.join(dirname, input('What is the dest file name: '))
            mode = input('What is the mode (a for append, w for write): ')
            while mode != 'a' and mode != 'w':
                mode = input('Mode must be a (append) or w (write): ')
            limit = int(input('How many terms would you like to copy (Type a negative number for all): '))
            writeFromToFile(src,dest,mode,limit)
        elif choice == 7:
            src = memoryFile
            dest = conversationsFile
            mode = 'a'
            writeFromToFile(src,dest,mode)
        elif choice ==8:
            src = longTermMemoryFile
            dest = conversationsFile
            mode = 'a'
            writeFromToFile(src,dest,mode)
        else:
            speech = 'lmao'
            response = ''
            oldResponse = ''
            while True:
                oldResponse = response
                speech = input("Nusair: ")
                #try:
                if speech == 'bye' or speech == 'see ya' or speech=='':
                    break
                
                inputStatement = Statement(speech,oldResponse)
                response = bot.get_response(inputStatement).text
                #response = talkToBot(bot,speech)
                print('Axel: ' + response)
                '''
                if response.endswith('Tell me about it'):
                    Rant()
                    user.mood = 'sad' 
                '''
                #except:
                  #  continue
            
    #except:
        print('Input a number')
        


'''
while True:
    question = input('Type something: ')
    if question == 'x':
        bot.storage.drop()
        break
    response = bot.get_response(question)
    print(response)
'''



