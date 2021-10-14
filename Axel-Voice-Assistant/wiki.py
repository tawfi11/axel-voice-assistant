import wolframalpha, wikipedia, regex, urllib.parse
from googlefuncs import searchUp
  
# App id obtained by the above steps 
app_id = '5L5652-WYTL8LHAE9'
  
# Instance of wolf ram alpha  
# client class 
client = wolframalpha.Client(app_id) 

def wiki(engine, speech):
    #engine.say('Finding answer for ' + speech)
    #engine.runAndWait()
    commonWords = ["what's","what're","what","are", "is", "were"]
    for common in commonWords:
        if speech.startswith(common) == True:
            speech = speech[len(common) + 1: :]
    
    try:
        wiki_res = wikipedia.summary("u'" + speech, sentences = 2) #u' is used for parsing the wiki page
        x = removeString(wiki_res)
        wiki_res = x
        engine.say(wiki_res)
        print(wiki_res)
        engine.runAndWait()
        print(speech)
    except:
        engine.say('Searching for answer on Google')
        engine.runAndWait()
        searchUp(speech, engine)

def removeString(string):
    string = regex.subf(r"\((?:[^()]++|(?R))*+\)", "", string)
    return string
