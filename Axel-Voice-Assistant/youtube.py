from random import randint
import pyttsx3
import speech_recognition as sr
from googlesearch import search
import webbrowser
import random

def giveSomeMotivation(engine):
    choice = randint(1,12)
    chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
    query = 'lmao'
    webbrowser.open("https://www.youtube.com/watch?v=Tq1r6FiBfrE&list=PLARpUvpFxzhbLTR9QN5bBcXTin3vUvlPO&index=" + str(choice))
    engine.say('Hopefully this gives you motivation')
    engine.runAndWait()
    return

def cheerUp(engine):
    choice = randint(1, 49)
    chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
    query = 'lmao'
    webbrowser.open("https://www.youtube.com/watch?v=w_DbjO7n6FM&list=PLARpUvpFxzhYK-SdOwNQcFAKULK22Jcme&index=" + str(choice))
    engine.say('Hopefully this will cheer you up')
    engine.runAndWait()
    return

def relaxing(engine):
    choice = randint(1, 59)
    chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
    query = 'lmao'
    webbrowser.open("https://www.youtube.com/watch?v=3FzJHsri8Zw&list=PLARpUvpFxzhb4pR48bDsYWLu9iXA1dCik&index=" + str(choice))
    engine.say('Dont get distracted!')
    engine.runAndWait()
    return

def grind(engine):
    choice = randint(1, 5)
    chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
    query = 'lmao'
    webbrowser.open("https://www.youtube.com/watch?v=T7XbwTos5vI&list=PLARpUvpFxzhYQ05rUF_Tc8h9o0heEIkAF&index=" + str(choice))
    engine.say('Get that bread!')
    engine.runAndWait()
    return