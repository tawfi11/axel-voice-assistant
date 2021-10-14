import pyttsx3, os, smtplib,ssl,base64,time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import speech_recognition as sr
from googlesearch import search
import webbrowser
from universalMethods import getFromTxt,getContact

def parseGoogleSearch(speech, source, engine, r, user):
    try:
        speech = speech.lower().strip().replace(' on google', '')
        if speech.endswith(' for me'):
            speech = speech.strip(' for me')

        commonWords = ['search up ', 'look up ']
        for c in commonWords: #see if it starts with search/look up
            if speech.startswith(c):
                speech = speech.replace(c,'').strip()
                if speech.lower() == 'something':
                    googleSearch(source,engine,r,user)
                else:
                    searchUp(speech,engine)
                return
        
        commonWords = ['search ', 'look '] #sees if search [...] up
        for c in commonWords:
            if speech.startswith(c):      
                speech = speech.replace(c,'').strip()
                break
        
        if speech.endswith('up') and speech.strip() != 'up':
            speech = speech[0:len(speech)-3:].strip()

        if speech.lower() == 'something':
            googleSearch(source,engine,r,user)
            return

        searchUp(speech,engine)
            
    except Exception as e:
        print(str(e))
        engine.say('Error message: ' + str(e))
        engine.runAndWait()


def googleSearch(source, engine, r,user):
    try:
        engine.say('What would you like to search on Google?')
        engine.runAndWait()


        if user.speak:
            try:
                audio = r.listen(source, timeout = 5, phrase_time_limit=7)
                query = r.recognize_google(audio, language='en-US')
            except:
                try:
                    engine.say('I didnt catch that, can you repeat that')
                    engine.runAndWait()
                    audio = r.listen(source, timeout = 5, phrase_time_limit=7)
                    query = r.recognize_google(audio,language='en_US')
                except:
                    engine.say('Unfortunately, I couldnt understand you')
                    engine.runAndWait()
                    return
        else:
            query = input('Search query: ')

        chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
        for url in search(query, tld="co.in", num=1, stop = 1, pause = 2):
            webbrowser.open("https://google.com/search?q=%s" % query)

        engine.say('Here are the results for ' + query)
        engine.runAndWait()
        return
    
    except Exception as e:
        engine.say('Error message: %s' % e.message)
        engine.runAndWait()

def searchUp(speech, engine):
    commonDelimiter = ["a", "the"]
    if(speech.startswith('search up') == True):
        query = speech[10: : ]
        
        for common in commonDelimiter:
            if(query.startswith(common) == True):
                query = query[len(common) + 1 : :]

    else: query = speech
    print(query)
    chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
    webbrowser.open("https://google.com/search?q=%s" % query)

    engine.say('Here are the results for ' + speech)
    engine.runAndWait()
    return

def openGmail(engine, speech):
    chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
    query = 'lmao'
    webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
    engine.say('Opening your google account')
    engine.runAndWait()
    return

def parseGmail(engine, speech,user,r,source):
    try:
        if speech.lower().startswith('send'):
            engine.say('Preparing to send email from file')
            engine.runAndWait()
            prepareToSendemail(user,engine,r,source)
        else:
            openGmail(engine,speech)
    except Exception as e:
        print(e)

def prepareToSendemail(user,engine,r,source,inFile=True):
    toNames = []
    toEmails = []
    subject = ''
    salutation = ''
    body = ''
    closing = ''
    if inFile:
        toNames = getFromTxt('email.txt','Names').split(',')
        toEmails = getFromTxt('email.txt', 'To').split(',')
        if len(toNames) != len(toEmails):
            engine.say('Incorrect number of addresses and names. Fix this and try again')
            engine.runAndWait()
            return

        subject = getFromTxt('email.txt', 'Subject')
        salutation = getFromTxt('email.txt', 'Salutation')
        closing = getFromTxt('email.txt','Closing')
        body = ''

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'Axel Usage Files/email.txt')
        myFile = open(filename,'r')
        bodyWrite = False
        for line in myFile:
            if bodyWrite:
                body += line
            elif line == 'Body:\n' and not bodyWrite:
                bodyWrite = True

    if subject == '' or subject == ' ': #if no subject
        engine.say('The subject field is empty. What would you like your subject to be?')
        engine.runAndWait()

        if user.speak:
            audio = r.listen(source,timeout=2)
            subject = r.recognize_google(audio, language ="en_US")
            if (subject.endswith('manual') or subject.endswith('type') or subject.endswith('typing') or (subject.endswith('mode') and (subject.find('type') != -1 or subject.find('typing') != -1))):
                engine.say('Switching to typed mode')
                engine.say('Okay, I will use what you type as the subject')
                engine.runAndWait()
                subject = input(user.name + ': ')
        else:
            subject = input(user.name + ": ")
        
        if subject.lower().startswith('nevermind') or subject == '':
            engine.say('Okay, I won\'t send the email')
            engine.runAndWait()
            return
    
    if len(toEmails) == 1 and toEmails[0] == '': #if no emails to send to
        toEmails = []
        toNames = []
        engine.say('To emails field is empty')
        engine.runAndWait()
        if user.speak:
            engine.say('Seperate multiple contacts by saying and. Which contacts would you like to send the email to?')
            engine.runAndWait()
            audio = r.listen(source,timeout=2)
            contactNames = r.recognize_google(audio,language='en_US')

            if (contactNames.endswith('manual') or contactNames.endswith('type') or contactNames.endswith('typing') or (contactNames.endswith('mode') and (contactNames.find('type') != -1 or contactNames.find('typing') != -1))):
                engine.say('Switching to typed mode')
                engine.say('Okay, seperate multiple contacts by commas. Which contacts would you like to send the email to?')
                engine.runAndWait()
                contactNames = input(user.name + ': ')
                contactNames = contactNames.split(',')
            else:
                contactNames = contactNames.split('and')
        else:
            engine.say('Seperate multiple contacts by commas. Which contacts would you like to send the email to?')
            engine.runAndWait()
            contactNames = input(user.name + ": ")
            contactNames = contactNames.split(',')

        for c in contactNames:
            c = c.strip()
            if c.lower().startswith('nevermind') or c == '':
                engine.say('Okay, I won\'t send the email')
                engine.runAndWait()
                return
            
            contact = getContact(c)
            contact[0] = contact[0].strip()
            contact[2] = contact[2].strip()
            if contact[0] == '':
                engine.say('Could not find contact ' + c + ". Skipping this contact")
                engine.runAndWait()
                continue

            elif contact[2] == '':
                engine.say('contact ' + contact[0] + ' does not have an email associated with their contact. Skipping contact')
                engine.runAndWait()
                continue
            toNames.append(contact[0].split()[0].strip())
            toEmails.append(contact[2])
        
        if len(toEmails) == 1 and toEmails[0] == '':
            engine.say('Could not find anybody to send email to. Will not send email')
            engine.runAndWait()
            return

    if salutation == '' or salutation == ' ': #if no salutation
        engine.say('The salutation field is empty. What would you like your salutation to be?')
        engine.runAndWait()

        if user.speak:
            audio = r.listen(source,timeout=2)
            subject = r.recognize_google(audio, language ="en_US")
            if (salutation.endswith('manual') or salutation.endswith('type') or salutation.endswith('typing') or (salutation.endswith('mode') and (salutation.find('type') != -1 or salutation.find('typing') != -1))):
                engine.say('Switching to typed mode')
                engine.say('Okay, I will use what you type as the subject')
                engine.runAndWait()
                salutation = input(user.name + ': ')
        else:
            salutation = input(user.name + ": ")
        
        if salutation.lower().startswith('nevermind') or salutation == '':
            engine.say('Okay, I won\'t send the email')
            engine.runAndWait()
            return

    if closing == '' or closing == ' ': #if no closing
        engine.say('The closing field is empty. What would you like your closing to be?')
        engine.runAndWait()

        if user.speak:
            audio = r.listen(source,timeout=2)
            subject = r.recognize_google(audio, language ="en_US")
            if (closing.endswith('manual') or closing.endswith('type') or closing.endswith('typing') or (closing.endswith('mode') and (closing.find('type') != -1 or closing.find('typing') != -1))):
                engine.say('Switching to typed mode')
                engine.say('Okay, I will use what you type as the subject')
                engine.runAndWait()
                closing = input(user.name + ': ')
        else:
            closing = input(user.name + ": ")
        
        if closing.lower().startswith('nevermind') or closing == '':
            engine.say('Okay, I won\'t send the email')
            engine.runAndWait()
            return

    if body == '' or body == ' ': #if body empty
        engine.say('Body field is empty. Not sending email')
        engine.runAndWait()
        return
    
    i = 0
    for t in toEmails:
        print(toNames[i] + "  -  " + t)
        i+=1
    
    engine.say('Would you like to send the email to ' + toNames[0] + ' and ' + str(len(toEmails) - 1) + ' others?')
    engine.runAndWait()
    if user.speak:
        engine.say('Say yes, or no')
        engine.runAndWait()
        audio = r.listen(source,timeout=2)
        send = r.recognize_google(audio, language ="en_US")
    else:
        engine.say('Type yes, or no')
        engine.runAndWait()
        send = input(user.name + ": ")

    if send.lower().startswith('ye'): 
        sendEmail(toNames,toEmails,subject,salutation,closing,body,user,engine)    
    else:
        engine.say('Okay. I will not send any emails')
        engine.runAndWait()

def sendEmail(toNames,toEmails,subject,salutation,closing,body,user,engine):
    username = user.gmailUser
    password = user.gmailPass
    name = getFromTxt('email.txt','Gmail-Signoff-Name')

    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
    server.ehlo()
    server.login(username, password)

    i = 0
    j = 0
    for addr in toEmails:
        addr.replace(' ','')
        if addr == '':
            i+=1
            continue

        while toNames[i].startswith(' '):
            toNames[i] = toNames[i][1::]

        while toNames[i].endswith(' '):
            toNames[i] = toNames[i][::len(toNames[i])-2]

        message = "%s %s, \n\n%s\n\n%s,\n\n%s" %(salutation, toNames[i],body,closing, name)

        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = addr
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))
        raw_string = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        try:
            server.sendmail(username, addr, msg.as_string())
            
            print('Email sent!')
            time.sleep(1)
            j+=1
        
        except Exception as e:
            print(e)
            engine.say("Error. Sent " + str(j) + " emails successfully")
            engine.runAndWait()
            server.close()
            return
        i+=1

    server.close()

    engine.say('Successfully sent ' + str(j) + ' emails')
    engine.runAndWait()

'''
def googleWebScrape():
    response = GoogleSearch().search('Pokemon')
    for result in response.results:
        print(result.title)
        print(result.getText())

googleWebScrape()
'''