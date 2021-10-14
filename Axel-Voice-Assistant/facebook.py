import fbchat
from getpass import getpass
import re, pickle

fbchat._util.USER_AGENTS    = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"]
fbchat._state.FB_DTSG_REGEX = re.compile(r'"name":"fb_dtsg","value":"(.*?)"')
agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
user = 'nusair11@gmail.com' #nusair11@gmail.com
password = 'Rameen1!'#'LWS4GXYMYQ' #App Password
def login():
    
    session = []
    client = fbchat.Client(user,password, max_tries=1, session_cookies=session)
    friends = client.searchForUsers('Jahin Zaman')
    print(friends)
    session = client.getSession()
    print("Was successful")

    with open('somefile.txt', 'wb') as f:
        pickle.dump(session, f)

def cookies():
    with open('somefile.txt', 'rb') as f:
        session = pickle.load(f)
    
    client = fbchat.Client(user, password, max_tries=1,session_cookies=session)
    #friends = [client.searchForUsers('Jahin Zaman'), client.searchForUsers('Angelina Ta'), client.searchForGroups('Woop De Scoop'), client.searchForGroups('Pirates of the Hudson\'s Bay')]
    friends = client.searchForUsers('Hafsa Choudhary')
    #print(friends[1][0])
    print(friends[0])
    print("Sign in was ezpz")
    msg = fbchat.Message('Hey Hafsa')
    #msg = fbchat.Message('Yoyo sidenote, this is a message I had axel send :) also fuck Linedin, it\'s so weird why do random dudes with \'entrepreuneur\' in their bio keep sliding into my DMs. Is this how girls feel on any social media lmao, has a dude hit on you on LinkedIn? Love, Axel')
    len = 4
    i = 0
    client.send(msg, friends[0].uid, friends[0].type)
    '''
    while i < len:
        client.send(msg,friends[i][0].uid, friends[i][0].type)
        i+=1
    '''
cookies()