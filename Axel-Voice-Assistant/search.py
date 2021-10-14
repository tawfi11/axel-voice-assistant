import wolframalpha, wikipedia, regex
from googlefuncs import searchUp
from wiki import wiki
  
# App id obtained by the above steps 
app_id = '5L5652-WYTL8LHAE9'
  
# Instance of wolf ram alpha  
# client class 
client = wolframalpha.Client(app_id) 
  
# Stores the response from  
# wolf ram alpha 
#res = client.query(question) 
  
# Includes only text from the response
#try:
 #   answer = next(res.results).text
#except:
 #   answer = 'no answer'
def resolveListOrDict(variable):
  if isinstance(variable, list):
    return variable[0]['plaintext']
  else:
    return variable['plaintext']

def wolfram(engine,speech = ''):
    try:
        wolfram = client.query(speech)
        if wolfram['@success'] != 'false':
            pod1 = wolfram['pod'][1]
            if (('definition' in pod1['@title'].lower()) or ('result' in  pod1['@title'].lower()) or (pod1.get('@primary','false') == 'true')):
                # extracting result from pod1
                result = resolveListOrDict(pod1['subpod'])
                if result != '(data not available)':
                    print('got answer from wolfram')
                    return result
    
        #wiki(engine,speech)
        return 'no answer'
    except:
        return 'no answer'
def removeString(string):
    string = regex.subf(r"\((?:[^()]++|(?R))*+\)", "", string)
    print(string)
    return string

def search(engine, speech):
    #engine.say('Finding answer for ' + speech)
    #engine.runAndWait()

    answer = wolfram(engine, speech)

    if(answer == 'no answer'):
        engine.say('Searching for answer on Google')
        engine.runAndWait()
        searchUp(speech, engine)
        return
    elif(answer == 'null'):
        return

    engine.say(answer)
    engine.runAndWait()
    print(answer)
