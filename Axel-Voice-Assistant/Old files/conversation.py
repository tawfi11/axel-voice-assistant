
def conversation(engine, source, r, speech):
    if speech.find('are you') != -1 or speech.find('it going') != -1 or speech.find('what\'s up') != -1 or speech.find('you doing') != -1:
        smallTalk(engine, source, r, speech)

def smallTalk(engine, source, r, speech):
    engine.say('I\'m doing well, thanks for asking. How has your day been?')
    engine.runAndWait()
    conversationOver = False

    responseDict = {
        "pain" : "I can't begin to imagine what you're going through.",
        "sad" : "I'm here to listen whenever you need me. No matter when or why",
        "cry" : "It's okay to cry. We don't have to talk, I'm happy just sitting here with you",
        "hard" : "I can only imagine how difficult it is. But, I know you can overcome it!",
        "lonely" : "You have a lot of friends, including myself",
        "stressful" : "I know it must be really hard for you. But stress is short term and usually the outcome far outweighs the work you took to get here. You can do this!",
        "ya know" : "I get it",
        "you know" : "Yeah, I get it"
    }
    
    engine.say('why don\'t you tell me about it. I\'d love to listen')
    engine.runAndWait()

    while conversationOver == False:
        try:
            audio = r.listen(source, phrase_time_limit = 7)
            speech = r.recognize_google(audio)
            speech = speech.lower()
        except:
            continue
      
        if speech.find('I\'m good') != -1 or speech.find('not today') != -1 or speech.find('bye') != -1 or speech.find('thanks') != -1 or speech.find('thank you') != -1: 
            engine.say('See you. I hope you have a fantastic day!')
            engine.runAndWait()
            conversationOver = True
        else:
            for key in responseDict:
                if speech.find(key) != -1:
                    engine.say(responseDict[key])
            engine.say("If you want to tell me more, I'm not going anywhere!")
            engine.runAndWait()
                    
