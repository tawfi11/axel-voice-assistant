import re, spotipy, sys, os
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from json.decoder import JSONDecodeError


###? Initialize application information ?###
clientID = '4d69a1fdddec4723a77d7060d535185d'
clientSecret = '61be34f6da764189a27e1471f4b16c96'
user = 'Nusair Islam'
redirect_uri = 'https://www.google.ca/'
scope = 'user-read-private user-read-playback-state user-modify-playback-state user-top-read playlist-modify-public playlist-modify-private playlist-read-collaborative'
###? Initialize application information ?###


###? Find/create cache for faster login ?###
cacheFolder = os.path.join(os.path.dirname(sys.argv[0]),'cache')
if os.path.exists(cacheFolder) == False:
    os.mkdir(cacheFolder)

cacheFile = os.path.join(cacheFolder,f"spotifyCache.cache-{user}")
###? Find/create cache for faster login ?###

#cacheHandler = spotipy.cache_handler.CacheFileHandler(cacheFile,user)
#auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope, cache_handler=cacheHandler,show_dialog=True,client_id=clientID,client_secret=clientSecret,redirect_uri=redirect_uri)

try:
    ###? Try to get login token from cache, if not, prompt user for login and save cache ?###
    try:
        token = util.prompt_for_user_token(user, scope, clientID, clientSecret, redirect_uri, cacheFile)
    except (AttributeError, JSONDecodeError):
        os.remove(cacheFile)
        token = util.prompt_for_user_token(user,scope,clientID,clientSecret,redirect_uri, cacheFile)
    ###? Try to get login token from cache, if not, prompt user for login and save cache ?###


    ###? Try to open spotify if spotify is not opened ?###
    client = spotipy.Spotify(auth=token)
    devices = client.devices()

    while len(devices['devices']) == 0:
        os.system('spotify')
        devices = client.devices()
    ###? Try to open spotify if spotify is not opened ?###

except Exception as e:
    print(f"Error msg: {e}")
    input('Press enter to continue: ')


class spotifyQuery:
    def __init__(self):
        self.name = ''
        self.owner = '' #Owner of this object type
        self.type = '' #Either album, song, playlist, artist
        self.action = '' ###! p = play, q = add to queue, n = skip to next track, s = state change !###
        self.returnMsg = '' #What the return message will be

def createSpotifyQuery(query, predefinedAction=''):
    spotifyQ = spotifyQuery()

    if predefinedAction == '':
        verb = query.split()[0].strip()
        verbsList = [
            ['play'],
            ['add'],
            ['skip'],
            ['turn', 'repeat', 'put']
        ]
        codeList = ['p', 'q', 'n', 's']
        for i, verbList in enumerate(verbsList):
            if any(verb == verbToCompare for verbToCompare in verbList):
                verb = codeList[i]
                break
        
    else: verb = predefinedAction
    
    spotifyQ.action = verb

    verbs = ','.join(verb)

    for v in verbs:

        ###? Get the type of request we're dealing with ?###
        for spotifyType in ['album', 'playlist', 'artist']:
            if spotifyType in query:
                spotifyQ.type = spotifyType
                break
        ###? Get the type of request we're dealing with ?###'


        if v == 'n':
            client.next_track()
            spotifyQ.returnMsg = "Okay, skipping track"
        elif v == 's':
            if any(phrase in query for phrase in ['off', 'stop']):
                on = False
            else: on = True

            if 'shuffle' in query or 'shuffling' in query:
                client.shuffle(on)
                if on: on = 'on'
                else: on = 'off'
                spotifyQ.returnMsg = f"Okay, turning {on} shuffle"
            elif 'repeat' or 'repeating':
                if not on: 
                    client.repeat('off')
                    spotifyQ.returnMsg = f"Okay, turning off repeat"
                elif spotifyQ.type != '':
                    client.repeat('context')
                    spotifyQ.returnMsg = f"Okay, looping this {spotifyQ.type}"
                else: 
                    client.repeat('track')
                    spotifyQ.returnMsg = f"Okay, turning on repeat"

        elif v == 'q' or v == 'p':
            if v == 'p': query = query.split()[1:len(query.split())]
            else:
                query.replace('to queue', '')
                query = query.split()[1:len(query.split())]
            
            query = ' '.join(query)

            ###? Check posessive words to get actual spotifyQ data?###
            posessiveDict = [
                r"^(?P<owner>.*)'s (?P<name>.*)$",
                r"^(?P<name>.*) by (?P<owner>.*)$",
                r"^(.*)my (?P<name>.*)"
            ]
            for i, pattern in enumerate(posessiveDict):
                m = re.match(pattern, query)
                if m != None:
                    if i < 2:
                        spotifyQ.owner = m.group('owner').strip()
                        spotifyQ.name = m.group('name').strip()
                    else:
                        spotifyQ.name = m.group('name').strip()
                        spotifyQ.owner = 'Nusair Islam'
                    break
            ###? Check posessive words to get actual spotifyQ data?###

            if v == 'q':
                searchResults = client.search(f"{spotifyQ.name} {spotifyQ.owner}",1,0,"track")
                track = searchResults['tracks']['items'][0]['uri']
                client.add_to_queue(track)
            else:
                if spotifyQ.type == '': 
                    spotifyQ.type = 'track'
                    searchResults = client.search(f"{spotifyQ.name} {spotifyQ.owner}", type ='track')['tracks']['items'][0]
                    spotifyQ.name = searchResults['name']
                    spotifyQ.owner = searchResults['artists'][0]['name']
                    client.start_playback(uris=[searchResults['uri']])
                    client.repeat('context')
                    spotifyQ.returnMsg = f"Okay, playing {spotifyQ.name} by {spotifyQ.owner}"
                else:
                    searchResults = client.search(f"{spotifyQ.name} {spotifyQ.owner}", type=spotifyQ.type)
        

    spotifyQ.name = spotifyQ.name.replace(spotifyQ.type, '').strip()
    return spotifyQ


query = r"{}".format(input('what would you like to do: '))


###? Multiple actions ?###
multipleRequestsDict = {
    r"^(?P<first>.*) starting with (?P<second>.*)$" : ['', 'qn'], #Reversed because of how this will be implemented (play media THEN add to queue and skip)
    r"^(?P<first>.*) then (?P<second>.*)" : ['',''],
}

requests = []
predefinedActions = []
for pattern in multipleRequestsDict.keys():
    m = re.match(pattern, query)
    if m != None:
        requests = [m.group('first'), m.group('second')]
        predefinedActions = multipleRequestsDict[pattern]
        break
    else: 
        requests = [query]
        predefinedActions = ['']
###? Multiple actions ?###


for i, request in enumerate(requests):
    spotifyQ = createSpotifyQuery(request, predefinedActions[i])
    print(spotifyQ)