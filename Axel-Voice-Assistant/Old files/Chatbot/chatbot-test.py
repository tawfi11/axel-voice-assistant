from random import randint
from chatterbot.chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_first_response
from chatterbot.comparisons import SentimentComparison
import logging, keyboard
import speech_recognition as sr
from difflib import SequenceMatcher
import PySimpleGUI as sg

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
    file = 'Learning/user.txt'
    user.name = getFromTxt(file,'Name')
    user.mood = getFromTxt(file,'Mood')
    user.favorites = getFromTxt(file,'Favorites')
    return user

def talkToBot(bot=None,speech='',response=''):
    memoryRead = open('Learning/memory.txt','r')
    lines = memoryRead.readlines()
    i = 0
    j = 0
    ratios = []
    possibleResponses = []
    if response == '':
        for l in lines:
            if i % 2 == 0:
                l = l.replace('\n','')
                if SequenceMatcher(None,l.lower(),speech.lower()).ratio() > 0.9 and i < len(lines) - 1:
                    possibleResponse = lines[i+1]
                    possibleResponses.append(possibleResponse.replace('\n',''))
                    ratios.append(SequenceMatcher(None,l.lower(),speech.lower()).ratio())
            i+=1
        
        if len(ratios) > 0:
            i = ratios.index(max(ratios))
            response = possibleResponses[i]

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
    memoryWrite = open('Learning/memory.txt','w')

    for l in lines:
        l = l.replace('\n','')
        memoryWrite.writelines(l + '\n')

    memoryWrite.close()
    return response        

logging.basicConfig(level=logging.INFO)
bot = ChatBot(
    name='Axel',
    read_only=True,
    logic_adapters=[
            {
                "import_path": "chatterbot.logic.BestMatch",
                "statement_comparison_function": SentimentComparison
            },
        ],
    response_selection_method=get_first_response)

user = initializePerson()
response = ''
sg.theme('SandyBeach')
layout = [
        [sg.Text('User:', size=(15,1)),sg.InputText()],
        [sg.Text('Axel:' + response, size=(100,1))],
        [sg.Button('Enter', key='13', bind_return_key=True)]
    ]
window = sg.Window('Axel', layout, return_keyboard_events=True)

while True:
    event, value = window.read()
    if event == 'Control_L:17':
        response = talkToBot(bot,speech=value[0])

    window.close()
    layout1 = [
        [sg.Text('User:', size=(15,1)),sg.InputText()],
        [sg.Text('Axel:' + response, size=(100,1))],
        [sg.Button('Enter')]
    ]
    window = sg.Window('Axel', layout1)
    
