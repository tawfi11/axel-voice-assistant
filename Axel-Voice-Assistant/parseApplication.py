import time, random
from spotify import parseSpotify
from googlefuncs import parseGoogleSearch, parseGmail
from youtube import giveSomeMotivation, cheerUp, relaxing, grind
from wiki import wiki
from search import search
from openlink import gotoWebsite
from difflib import SequenceMatcher
import pandas as pd
#from pysparkModels import chooseState

def getKeyWordList(i): #Function get get the list of KeyWords in interest of looking less ugly
    arrayOfWords = [
        ['continue playing','resume playback','resume playing','continue playback','pause this song','pause song','pause the song',
        'pause the music','last track','next song', 'skip song','skip this song','album', 'playlist','spotify','skip track','skip this track','previous track', 
        'next track', 'on repeat', 'on shuffle', 'to queue', '2q', 'myq', 'my queue', 'songs similar', 'similar songs', 'songs like this', 'like the one playing'], #Spotify
        ['gmail', 'email','open','send'], #gmail/email
        ['search', 'look'] #search up on google
    ]
    try:
        return arrayOfWords[i]
    except:
        return []

def correctSpeechRecognizer(speech): #speech recognizer sometimes messes up words, so this fixes it
    incorrectWords = ['mister', 'milo', 'to Q', '2q']
    correctWords = ['Mr.', 'my low', 'to queue', 'to queue']
    i = 0
    for w in incorrectWords:
        if w in speech:
            speech = speech.replace(w,correctWords[i])
        i+=1
    return speech

def callAxel(speech): #determines if Axel is called
    speech = speech.lower().split(" ")
    keywords = ["ax", "ex"]
    i = 0
    for s in speech: #Checks if 'ax' or 'ex' appears next to each other in speech, otherwise Axel was not called
        if (s.find(keywords[0]) != -1) or (s.find(keywords[1]) != -1):
            break
        i+=1
    if i < len(speech): #Makes sure that ax/ex was not found at the end of speech (definitely not 'axel' or 'exel')
        word = speech[i]
        x = word.index('x')
        word = word[x+1 :x+3:]
        if word.startswith('l'): #If word is axl or exl
            return True
        elif word.startswith('a') or word.startswith('e') or word.startswith('i'): #if word is axal/exel, axel/exel, or axil/exil
            if word.endswith('l'):
                return True
    return False

def preset(speech, source, r, engine): #user-specific keyword action presets
    notPresetWords = ['spotify','gmail','email', 'on Google'] #words that mean the speech should NOT go thru presets
    for w in notPresetWords:
        if(w in speech):
            return False

    if speech.find('motivation') != -1:
        giveSomeMotivation(engine)
        return True
    elif speech.find('cheering up') != -1 or ((speech.find('i am') != -1 or speech.find("i'm") != -1) and speech.find('sad') != -1) or speech.find('under the weather') != -1:
        cheerUp(engine)
        return True
    elif speech.find('study') != -1:
        relaxing(engine)
        return True
    elif speech.find('grind') != -1 or speech.find('a long night') != -1 or speech.find('very high energy') != -1 or speech.find('a lot of energy') != -1:
        grind(engine)
        return True
    else:
        return False

def keywordcheck(keywords=['no','match'], speech="", count=1,mustHaveWords = []): #iterates through list of keywords and compares with speech, returns True if speech contains 'count' or more keywords
    i = 0
    foundKeyword = False
    for word in keywords:
        if word in speech:
            i += 1
            if i >= count:
                foundKeyword = True
    i = 0

    if len(mustHaveWords) < 1:
        return foundKeyword

    else:
        for word in mustHaveWords:
            if word not in speech:
                return False
        
        return foundKeyword

def parseApplication(speech, source, r, engine,user): #breaks down speech and analyzes it to determine what needs to be done
    commonWordDelimiters = ['can you ', 'please ', 'thanks ', 'thank you', ' for me'] #words that do not add anything to the command

    #remove common words that may confuse Axel and add nothing to command
    for delimiter in commonWordDelimiters:
        speech.replace(delimiter, "")

    #Axel sometimes gets words mixed up, this fixes common mix-ups
    speech = correctSpeechRecognizer(speech)

    speechLower = speech.lower() #so capitilization doesn't matter

    #Saying nevermind makes Axel do nothing
    if speechLower.startswith('nevermind'):
        engine.say('Okay then')
        engine.runAndWait()
        time.sleep(1)
        return True
    
    #state = stateChosen(createWordDic('Learning\phrase.csv'), speech)
    #print(state)

    #Check what to do based on a list of keyword
    if preset(speech,source,r,engine) == False: #Check if any user-defined keywords to trigger certain actions
        #Check spotify
        if "on spotify" in speechLower or "in spotify" in speechLower or speech.startswith('play') or any(phrase in speech for phrase in ['shuffle', 'shuffling', 'repeat', 'repeating']):
            speechLower = speechLower.replace(" on spotify", "")
            print(parseSpotify(speechLower, engine, source, r,user))
        
        #check gmail
        elif keywordcheck(getKeyWordList(1),speechLower,2):
            parseGmail(engine, speech,user,r,source)

        #search up on Google
        elif keywordcheck(getKeyWordList(2),speechLower,1,['on google']):
            parseGoogleSearch(speech,source,engine,r,user)
            

    finished = ['done','finished','as you requested']
    print('done')
    engine.say(finished[random.randint(0,len(finished) - 1)])
    engine.runAndWait()
    time.sleep(1)
    return True