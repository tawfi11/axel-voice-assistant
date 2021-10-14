from chatterbot.chatterbot import ChatBot
from chatterbot.response_selection import get_first_response
from chatterbot.comparisons import SynsetDistance
from chatterbot.comparisons import LevenshteinDistance
from difflib import SequenceMatcher
import os, random
from chatterbot.conversation import Statement

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Learning/memoryToSend.txt')
user = os.path.join(dirname,'Learning/user.txt')

def talkToBot(bot=None,speech='',response='', secret=False):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'Learning/memoryToSend.txt')
    memoryRead = open(filename, 'r')
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
    if secret == False:
        memoryWrite = open(filename,'w')

        for l in lines:
            l = l.replace('\n','')
            memoryWrite.writelines(l + '\n')

        memoryWrite.close()
    return response       

bot = ChatBot(
    name='Axel',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///' + dirname+ '/db.sqlite3',
    logic_adapters=[
            {
                "import_path": "chatterbot.logic.BestMatch",
                "statement_comparison_function": LevenshteinDistance
            },
        ],
    response_selection_method=get_first_response)

response = ''
file = open(user)
line = file.readline()
if line.startswith('Name:'):
    name = line[5::]
    name = name.replace('\n','')
else:
    name = 'User'
file.close()
secret = False
while True:
    speech = input(name+ ": ")
    if speech.find('secret') != -1 and secret==False:
        secret = True
        print('Axel: Your secret is safe with me. I won\'t remember what you said until you type \'end secret\'')
        continue
    if speech.lower() == 'end secret' and secret==True:
        secret = False
        print('Axel: Ended secret, I will now start remembering what you said again')
        continue
    print('Axel: ' + talkToBot(bot,speech,secret=secret))
