import os

class Person:
    def __init__(self,name,spotifyID,spotifyUser,spotifyPass,gmailUser,gmailPass):
        self.name = name
        self.spotifyID = spotifyID
        self.spotifyUser = spotifyUser
        self.spotifyPass = spotifyPass
        self.gmailUser = gmailUser
        self.gmailPass = gmailPass
    speak = True

def getFromTxt(file='config.txt',keyline='',delimiters=[':','\n']):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'Axel Usage Files/'+file)
    myFile = open(filename,'r')
    for line in myFile:
        if line.startswith(keyline):
            length = len(keyline)
            outputline = line[length::]
            for delimiter in delimiters:
                outputline = outputline.replace(delimiter,'')
            myFile.close()
            return outputline
    myFile.close()
    return ''

def fixContactName(contactName): #If Axel misrecognizes someone's name, correct it here. Potentially use sequence matchers for a bit of error but more robust
    contactNameWrong = ['nusr','Shany', 'Jaheim', 'Jaheen','Jahnine']
    contactNameCorrect =['Nusair','Channy','Jahin','Jahin','Jahin']
    i = 0
    for wrong in contactNameWrong:
        if wrong.lower() in contactName.lower():
            contactName = contactNameCorrect[i]
            break
        i+=1
    
    return contactName

def getContact(contactName):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'Axel Usage Files/contacts.txt')
    myFile = open(filename,'r')
    contacts = []
    contactName = fixContactName(contactName)
    for line in myFile:
        if line.startswith('Name') or line == '\n' or line == ' ':
            continue
        
        line = line.strip()
        contacts = line.split(',')
        if contacts[0].lower().find(contactName.lower()) != -1:
            return contacts
    
    return ['','','']