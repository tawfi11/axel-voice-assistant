import speech_recognition as sr
import pyttsx3, time, random, os, pyaudio
from parseApplication import parseApplication, callAxel
#from textblob import TextBlob
from universalMethods import Person, getFromTxt

def typeSpeak(user, greetings=[], engine=pyttsx3.init(), source=None, r=None): #let's you type instead of talking for faster usage
    speech = ""
    user.speak = False
    while True:
        #engine.say(greetings[random.randint(0,len(greetings) - 1)])
        #engine.runAndWait()
        speech = input(user.name + ": ")
        speech = speech.strip()
        if speech == '':
            user.speak = True
            break

        parseApplication(speech, source, r, engine,user)

    engine.say('Listening to your voice')
    engine.runAndWait()

def main():
    user = Person(getFromTxt('config.txt','Name'), getFromTxt('config.txt','Spotify-ID'),getFromTxt('config.txt','Spotify-Username'),
    getFromTxt('config.txt','Spotify-Secret'),getFromTxt('config.txt','Gmail-Address'),getFromTxt('config.txt','Gmail-Password'))

    greetings = ["Hello " + user.name + ", how may I assist you", "How may I be of service", "You called"]
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 185)
    engine.setProperty('voice', voices[0].id)
    engine.say("Warming-up voice")
    engine.runAndWait()
    engine.say("Initializing components")
    engine.runAndWait()
    #print("Hello World")
    r = sr.Recognizer()
    #print(sr.Microphone.list_microphone_names())
    mic = sr.Microphone(device_index=1)

    with mic as source:
        
        r.adjust_for_ambient_noise(source,duration = 5)
        r.threshold = 300
        engine.say('Hello, World')
        engine.runAndWait()
        #################################################################
        #typeSpeak(user, greetings, engine, source, r) #comment out when not testing - let's you type instead of talk for faster testing
        #################################################################
        while True:
            print('speak')
            try:
                audio = r.listen(source, phrase_time_limit=8,timeout=2)
                speech = r.recognize_google(audio, language ="en_US")
                print(speech)
            except:
                continue

            if callAxel(speech) and not callAxel(speech.split()[len(speech.split()) - 1]):
                speechSplit = speech.split()
                axel = ""
                for s in speechSplit:
                    if callAxel(s):
                        axel = s
                        break

                index = speech.index(axel)
                speech = speech[index+1+len(axel)::]
                engine.say('ok')
                engine.runAndWait()
                parseApplication(speech, source, r, engine,user)

            elif callAxel(speech) == True:
                taskCompleted = False
                engine.say(greetings[random.randint(0,len(greetings) - 1)])
                engine.runAndWait()
                while taskCompleted == False:
                    try:
                        audio = r.listen(source, timeout = 2, phrase_time_limit=7)
                        speech = r.recognize_google(audio, language='en-US')
                        print(speech)
                    except:
                        time.sleep(1)
                        try:
                            engine.say("I didn't catch that, please say it again")
                            engine.runAndWait()
                            audio = r.listen(source, timeout = 2, phrase_time_limit=7)
                            speech = r.recognize_google(audio)
                        except: 
                            time.sleep(1)
                            continue
                    if (speech.endswith('manual') or speech.endswith('type') or speech.endswith('typing') or (speech.endswith('mode') and (speech.find('type') != -1 or speech.find('typing') != -1))):
                        engine.say('Switching to typed mode')
                        engine.runAndWait()
                        typeSpeak(user.name, greetings, engine, source, r)
                        break
                    taskCompleted = parseApplication(speech, source, r, engine,user)


if __name__ == "__main__":
    main()