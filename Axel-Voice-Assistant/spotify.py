import os, re, sys, json, spotipy, random, pyttsx3, traceback, time, subprocess, spacy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from json.decoder import JSONDecodeError
from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy import displacy
from spacy.attrs import POS
from difflib import SequenceMatcher
import speech_recognition as sr
import pyttsx3

def createSpotifyObject(): ###! CREATE SPOTIFY OBJECT !###

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
        spotifyObject = spotipy.Spotify(auth=token)
        devices = spotifyObject.devices()

        while len(devices['devices']) == 0:
            os.system('spotify')
            devices = spotifyObject.devices()
        ###? Try to open spotify if spotify is not opened ?###


        return spotifyObject

    except Exception as e:
        print(f"Error msg: {e}")
        input('Press enter to continue: ')
        return spotifyObject

nlp = spacy.load('en_core_web_sm')
client = createSpotifyObject()

###############################################################
###! This comment indicates what a function does !###
###? This comment explains what a step in the program does ?###
###* This comment is an emphisized comment *###
###TODO: This comment is a todo comment ###
###############################################################
def formatString(word): ###! REMOVE PUNCTUATION AND CAPITALIZATION FROM WORDS !###
    punctuation = ['!', '(', ')', ',', '[', ']', '{', '}', ';', ':', '\'', '\"', '\\', '<', '>', '.', '/', '?', '@', '#', '$', '%', '^', '&', '*', '~']
    for p in punctuation:
        word = word.replace(p,'')
    return word.lower()

def alterSpotifyState(speech, client): ###! CREATE ALTER SPOTIFY STATE !###
    try:
        task = ''
        ###? Go back ?###
        if any(phrase in speech for phrase in ['go back', 'previous track']):
            client.previous_track()
            return ("Playing previous track", speech, 'went back a track')
        
        if any(phrase in speech for phrase in ['skip track', 'skip this', 'play next', 'next track', 'skip song', 'skip track']):
            client.next_track()
            return ("Playing next track", speech, 'skipped to next track')


        if any(speech.endswith(phrase) for phrase in ['on shuffle', 'start shuffle', 'start shuffling', 'start shuffle']):
            client.shuffle(True)
            speech = speech.split()
            speech = speech[0:len(speech)-2]
            speech = ' '.join(speech)
            task = 'turned shuffle on'
        elif any(speech.endswith(phrase) for phrase in ['off shuffle', 'off shuffle', 'stop shuffling', 'stop shuffle']):
            client.shuffle(False)
            speech = speech.split()
            speech = speech[0:len(speech)-2]
            speech = ' '.join(speech)
            task = 'turned shuffle off'
        
        if any(speech.endswith(phrase) for phrase in ['on repeat', 'start repeat', 'start repeating']):
            client.repeat('track')
            speech = speech.split()
            speech = speech[0:len(speech)-2]
            speech = ' '.join(speech)
            task = 'repeating song'
        elif any(speech.endswith(phrase) for phrase in ['on loop', 'start loop', 'start looping']):
            client.repeat('context')
            speech = speech.split()
            speech = speech[0:len(speech)-2]
            speech = ' '.join(speech)
            task = 'looping context'
        elif any(speech.endswith(phrase) for phrase in ['off repeat', 'stop repeat', 'stop repeating', 'stop looping', 'stop loop']):
            client.repeat('off')
            speech = speech.split()
            speech = speech[0:len(speech)-2]
            speech = ' '.join(speech)
            task = 'turned off repeat'
        elif speech.startswith('repeat'):
            client.repeat('track')
            return('repeating song',speech,None)

        return ('', speech, task)

    except Exception as e:
        print(f"Error changing state of spotify: {e}")
        return ''

def addToQueue(speech, client, preprocessed=False): ###! ADD TO QUEUE !###
    try:
        found = preprocessed
        if not preprocessed:
            patterns = [r"^(add|put) (?P<song>.*) (by|from|in) (?P<suppName>.*) (to|in) queue$",
                        r"^(add|put) (?P<song>.*) (to|in) queue$"]
            for i, pattern in enumerate(patterns):
                m = re.match(pattern, speech)
                if m != None:
                    songName = m.group('song')
                    if i == 0: suppName = m.group('suppName')
                    else: suppName = ''
                    speech = f"{songName} {suppName}"
                    found = True
                    break 
        if found:
            searchResults = client.search(speech,1,0,"track")
            if searchResults['tracks']['items'] == []: 
                found = False
                searchResults = client.search(songName,10,0,"track")
                for result in searchResults['tracks']['items']:
                    for artist in result['artists']:
                        if suppName.lower() in artist['name'].lower() or SequenceMatcher(None, suppName, artist['name']).ratio() >= 0.8:
                            found = True
                            break
                    if found :
                        track = result['uri']
                        songName = result['name']
                        artistName = result['artists'][0]['name']
                        break
                    
                    album = result['album']
                    if album['album_type'] == 'single': continue
                    if suppName.lower() in album['name'].lower() or SequenceMatcher(None, suppName, album['name']).ratio() >= 0.8:
                        found = True
                    if found :
                        track = result['uri']
                        songName = result['name']
                        artistName = result['artists'][0]['name']
                        break
            else:
                track = searchResults['tracks']['items'][0]['uri']
                songName = searchResults['tracks']['items'][0]['name']
                artistName = searchResults['tracks']['items'][0]['artists'][0]['name']
            client.add_to_queue(track)
            return f"added {songName} by {artistName} to queue"
        
        return "Could not find song to add to queue"
    except Exception as e:
        return f"Error adding song to queue: {e}"
'''
def playSong(speech, client): ###! PLAY REUQESTED SONG !###
    try:
        if speech.startswith('play'): speech = speech[len('play'):].strip() ###* Get rid of 'play' *###


        ###? FIND artist-song PATTERNS ?###
        patterns = [
            r'^(.*) (by|from) (.*)$', ###* ex: up all night BY khalid *###
            r"^(.*)'s (.*)$" ###* ex: khalid's up all night *####
        ]

        found = False
        for pattern in patterns:
            m = re.match(pattern, speech)
            if m != None:
                found = True
                break
        
        if found:
            query = f"{m.group(2)} {m.group(1)}" ###* ex: up all night khalid *###
        ###? FIND artist-song PATTERNS ?###
        else:
            query = speech ###* No pattern found, just use the speech *###
        
    
        ###? PLAY SONG FROM QUERY ?###
        searchResults = client.search(query,1,0,"track")
        trackName = searchResults['tracks']['items'][0]['name']
        trackSelectionList = [searchResults['tracks']['items'][0]['uri']]

        trackSelectionList.append(searchResults['tracks']['items'][0]['uri'])
        ###? PLAY SONG FROM QUERY ?###

        return (trackSelectionList, None, None, f"Playing {query}")

    except Exception as e:
        return (None, None, None, f"Error playing song: {e}")

def playPlaylist(speech, client): ###! PLAY REQUESTED PLAYLIST !###
    try:
        if speech.startswith('play'): speech = speech[len('play'):].strip() ###* Get rid of 'play' *###
        found = False


    ###? Or find patterns starting with a certain song ?###
        patterns = [r"^(?P<artist>.*)'s (song|)(?P<song>.*) (on|in|from) (my|) (?P<playlist>.*) playlist$",
                    r"^(?P<song>.*) (by|from) (?P<artist>.*) (on|in|from) (my|) (?P<playlist>.*) playlist$",
                    r"^(?P<song>.*) (on|in|from) (my|) (?P<playlist>.*) playlist$",
                    r"^(my |)(?P<playlist>.*) playlist starting (with|from) (?P<song>.*) (by|from) (?P<artist>)$",
                    r"^(my |)(?P<playlist>.*) playlist starting (with|from) (?P<song>.*) (by|from) (?P<artist>)$"]
        
        for i, pattern in enumerate(patterns):
            m = re.match(pattern, speech)
            if m != None:
                try: artistName = m.group('artist') 
                except: artistName = ''
                playlistName = m.group('playlist')
                songName = m.group('song')
                found = True
                break
        
        if found:
            searchResults = client.search(playlistName,1,0,"playlist")
            playlist = searchResults['playlists']['items'][0]

            playlistTracks = client.playlist_items(playlist_id=playlist['id'],additional_types=['track'],limit=100)['items']
            i = 1
            while len(playlistTracks) / i >= 100:
                playlistTracks.extend(client.playlist_items(playlist_id=playlist['id'],additional_types=['track'],limit=100,offset=100*i)['items'])
                i+=1

            if any(songName in track['track']['name'].lower() for track in playlistTracks):
                queueQuery = f"{songName} {artistName}".strip()
            else:
                queueQuery = None

            return (None, searchResults['playlists']['items'][0]['uri'], queueQuery, f"Playing playlist {playlistName}")
    ###? Or find patterns starting with a certain song ?###


    ###? Find patterns my - playlist ?###
        patterns = [r'^(my |)playlist (P?<playlist>.*)$', ###* ex: play my playlist high energy *###
                    r'^(my |) (P?<playlist>.*) playlist$'] ###* ex: play my high energy *###
        
        for pattern in patterns:
            m = re.match(pattern, speech)
            if m != None:
                found = True
                break
        
        if found:
            query = m.group(1)
            searchResults = client.search(query,1,0,"playlist")
            return (None, searchResults['playlists']['items'][0]['uri'], None, f"Playing playlist {playlistName}")
    ###? Find patterns my - playlist ?###

        return (None, None, None, f"Could not play playlist")

       
    except Exception as e:
        return (None, None, None, f"Error playing playlist: {e}")

def playArtist(speech, client): ###! PLAY REQUESTED ARTIST !###
    if speech.startswith('play'): speech = speech[len('play'):].strip() ###* Get rid of 'play' *###
    found = False

    try:
    ###? Find patterns starting with a certain song ?###
        patterns = [r"^(?P<artist>.*[^'s])('s|) (songs|music) starting (with|from) (?P<song>.*)$",
                    r'^(.*) (by|from) (?P<artist>.*) starting (with|from) (?P<song>.*)$']
        
        for pattern in patterns:
            m = re.match(pattern, speech)
            if m != None:
                found = True
                artistName = m.group('artist')
                songName = m.group('song')
                break
        
        if found:
            try:
                searchResults = client.search(f"{songName} {artistName}",1,0,"track")
                artist = searchResults['tracks']['items'][0]['artists'][0]
                foundSong = True
            except:
                foundSong = False 
                searchResults = client.search(artistName,1,0,"artist")
                artist = searchResults['artists']['items'][0]

           
            if foundSong: 
                queue = f"{songName} {artistName}"
            else:
                queue = None
            
            return (None, artist['uri'], queue, f"Playing songs from {artist}")
            
    ###? Find patterns starting with a certain song ?###


    ###? Find just artist ?###
        patterns = [r"^(?P<artist>.*)('s|) (.*)$", ###* ex: play my playlist high energy *###
                    r'^(.*) (by|from) (?P<artist>.*)$'] ###* ex: play my high energy *###
        
        for pattern in patterns:
            m = re.match(pattern, speech)
            if m != None:
                found = True
                artistName = m.group('artist')
                break
        
        if found:
            artist = client.search(artistName,1,0,"artist")['artists']['items'][0]
            return (None, artist['uri'], None, f"Playing songs from {artist['name']}")
        else:
            return (None, None, None, "Could not find requested artist")
    ###? Find just artist ?###

    except Exception as e:
        return (None, None, None, f"Error playing artist: {e}")

def playAlbum(speech, client): ###! PLAY REQUESTED ALBUM !###
    if speech.startswith('play'): speech = speech[len('play'):].strip() ###* Get rid of 'play' *###
    found = False

    try:
        ###? Find album, artist, starting with certain song ?###
        patterns = [r'^(?P<album>.*) album by (?P<artist>.*) starting with (?P<song>.*)$', ###* LOCATION album by KHALID starting with AMERICAN TEEN *###
                    r'^(the |)album (?P<album>.*) by (?P<artist>.*) starting (with|from) (?P<song>.*)$', ###* album LOCATION by KHALID starting with AMERICAN TEEN *###
                    r'^(?P<album>.*) album starting with (?P<song>.*) (by|from) (?P<artist>.*)$', ###* LOCATION album starting with AMERICAN TEEN by KHALID *###
                    r'^(the |)album (?P<album>.*) starting (with|from) (?P<song>.*) (by|from) (?P<artist>.*)$', ###* album LOCATION starting with AMERICAN TEEN by KHALID *###
                    r"^(?P<artist>.*^['s])('s|) album (?P<album>.*) starting (with|from) (?P<song>.*)$", ###* KHALID's album LOCATION starting with AMERICAN TEEN *###
                    r"^(?P<artist>.*^['s])('s|) (?P<album>.*) album starting (with|from) (?P<song>.*)$", ###* KHALID's LOCATION album starting with AMERICAN TEEN *###
                    r"^(?P<song>.*) (by|from) (?P<artist>.*) in (the |)album (?P<album>.*)$", ###* AMERICAN TEEN by KHALID in album LOCATION *###
                    r"^(?P<song>.*) in (the |)album (?P<album>.*) (by|from) (?P<artist>.*)$", ###* SHOT DOWN in album AMERICAN TEEN by KHALID *###
                    r"^(?P<song>.*) in (the |)(?P<album>.*) album (by|from) (?P<artist>.*)$", ###* SHOT DOWN in AMERICAN TEEN album by KHALID *###
                    r"^(?P<artist>.*^['s])'s (?P<song>.*) in (the |)album (?P<album>.*)$", ###* KHALID's AMERICAN TEEN in album LOCATION *###
                    r"^(?P<song>.*) (by|from) (?P<artist>.*) in (the |)(?P<album>.*) album$", ###* AMERICAN TEEN by KHALID in LOCATION album *###
                    r"^(?P<artist>.*^['s])'s (?P<song>.*) in (the |) (?P<album>.*) album$"] ###* KHALID's AMERICAN TEEN in album LOCATION *###

        for i, pattern in enumerate(patterns):
            m = re.match(pattern, speech)
            if m != None:
                found = True
                songName = m.group('song')
                artistName = m.group('artist')
                albumName = m.group('album')
                break
        
        if found:
            searchResults = client.search(f"{albumName} {artistName}",1,0,"album")
            album = searchResults['albums']['items'][0]

            i = 1
            tracks = client.album_tracks(album['id'])['items']
            while len(tracks) / i >= 20:
                tracks.extend(client.album_tracks(album['id'], offset=20*i)['items'])
                i+=1
            
            foundSong = False
            for track in tracks:
                if track['name'].lower() == songName:
                        foundSong = True
                        break
            
            if foundSong:
                return (None, album['uri'], f"{songName} {artistName}", f"Playing album {albumName}")
            else:
                return (None, album['uri'], None, f"Playing album {albumName}")
        ###? Find patterns starting with a certain song ?###


        ###? Find patterns starting with a certian song ?###
        patterns = [r'^(?P<song>.*) in (the |)album (?P<album>.*)$',
                    r'^(?P<song>.*) in (the |)(?P<album>.*) album$',
                    r'^(the |)album (?P<album>.*) starting (with|from) (?P<song>.*)$',
                    r'^(the |)(?P<album>.*) album starting (with|from) (?P<song>.*)$']
        
        for i, pattern in enumerate(patterns):
            m = re.match(pattern, speech)
            if m != None:
                found = True
                albumName = m.group('album')
                songName = m.group('song')
                break
        
        if found:
            try:
                searchResults = client.search(f"{songName} {albumName}",1,0,"track")
                album = searchResults['tracks']['items'][0]['album']
                foundSong = True
            except: 
                searchResults = client.search(f"{songName} {albumName}",1,0,"album")
                album = searchResults['tracks']['items'][0]
                foundSong = False
            

            if foundSong:
                return (None, album['uri'], f"{songName} {albumName}", f"Playing album {albumName}")
            else:
                return (None, album['uri'], None, f"Playing album {albumName}")
            
        ###? Find patterns starting with a certain song ?###


        ###? Play album BY someone ?###
        patterns = [r'^(the |)album (?P<album>.*) (by|from) (?P<artist>.*)$',
                    r'^(the |)(?P<album>.*) album (by|from) (?P<artist>.*)$',
                    r"^(?P<artist>.*)('s|) (?P<album>.*) album",
                    r"^(?P<artist>.*)('s|) album (?P<album>.*)"]

        for i, pattern in enumerate(patterns):
            m = re.match(pattern,speech)
            if m != None:
                artistName = m.group('artist')
                albumName = m.group('album')

        if found:
            searchResults = client.search(f"{albumName} {artistName}",1,0,"album")
            album = searchResults['albums']['items'][0]
            return (None, album['uri'], None, f"Playing album {albumName}")
        ###? Play album BY someone ?###


        ###? PLAY album ?###
        patterns = [r'^(the |)album (?P<album>.*)$',
                    r'^(the |)(?P<album>.*) album$']
        
        for pattern in patterns:
            m = re.match(pattern, speech)
            if m != None:
                albumName = m.group('album')
                found = True
                break
        
        if found:
            searchResults = client.search(albumName,1,0,"album")
            album = searchResults['album']['items'][0]
            return (None, album['uri'], None, f"Playing album {albumName}")
        else:
            return (None, None, None, "Could not play album")
        ###? PLAY album ?###


    except Exception as e:
        (None, None, None, f"Error playing album {e}")
'''

def getTrackURI(query, nlp, client): ###! FINDS TRACK URIS GIVEN A QUERY FOR A SONG !###
    doc = nlp(u"{}".format(query))


    ###? Get token POS tag ?###
    for token in doc:
        print(f"{token.text:{10}} {token.pos_:{10}} {token.tag_:{10}} {spacy.explain(token.tag_)}")        
    ###?###################?###
    

    ###? Check if the exact song is a match ?###
    '''for search in client.search(query, type='track',limit=1)['tracks']['items']:
        if search['name'].lower() == query.lower():
            songName = search['name']
            artistName = search['artists'][0]['name']
            trackURI = search['uri']
            print(f"Playing {songName} by {artistName}")
            return [trackURI]'''
    ###?#####################################?###
    
    
    print('\n')

    ###? Create a list of requests AXEL will make to find the song ?###
    querySplit = query.split()
    requestList = []
    requestList.append(query)
    punctuationCount = 0
     ##* This part of the code finds requests based on artist, song *## 
    for i, token in enumerate(doc):
        i -= punctuationCount
        if token.text.lower() in ['.', ',', '!']:
            punctuationCount += 1
            continue
        if token.pos_ == 'ADP' and token.tag_ == 'IN' and token.text.lower() in ['by', 'from']:
            querySplit[i] = 'ADP'
            requestList.append(' '.join(querySplit))
            querySplit[i] = token.text
        elif token.text.lower() == "'s": ###TODO: Properly update the query split ###
            querySplit[i-1] = querySplit[i-1].replace("'s", '')
            querySplit.insert(i, 'POS')
            requestList.append(' '.join(querySplit))
            querySplit[i] = token.text
     ##*##############################################################*##

    ##* This part of the code eliminates unnecceasry parts of text based on a personalized list, these are last as we don't want to eliminate necessary info
    unecessaryWordsList = ['for me', 'for me', 'me']
    unecessaryWordsPos = ['begin', 'end', 'begin']
    
    for request in requestList.copy():
        for i, unecessary in enumerate(unecessaryWordsList):
            pattern = ''
            if unecessaryWordsPos[i] == 'end':
                pattern = r"^(.*) {}$".format(unecessary)
            else:
                pattern = r"^{} (.*)$".format(unecessary)
            
            if pattern != '': m = re.match(pattern, r"{}".format(request))
            if m != None:
                request = m.group(1)
        requestList.append(request)
     ##*##############################################################*##
    
    ###?#####################################?###


    ###? Find track ?###
    patterns = [
        r"^(?P<song>.*) ADP (?P<artist>.*)$",
        r"^(?P<artist>.*) POS (?P<song>.*)$",
        r"^(?P<song>.*)"]

    for request in requestList:
        for i, pattern in enumerate(patterns):
            m = re.match(pattern, r"{}".format(request))
            if m == None: continue

            if i < 2: artistName = m.group('artist')
            else: artistName = ''
            songName = m.group('song')
            try:
                trackSearchList = client.search(f"{songName} {artistName}",type='track',limit=1)['tracks']['items']
                if len(trackSearchList) > 0:
                    search = trackSearchList[0]
                    songName = formatString(songName)
                    foundName = formatString(search['name'].lower())
                    if songName in foundName or SequenceMatcher(None, songName, foundName).ratio() >= 0.8:
                        return search
            except Exception as e:
                print(e)
                return None
    
    return None
    ###?#####################################?###

def playSong(searchString='', nlp=None, client=None): ###! FORMATS A SONG SEARCH QUERY !###
    if searchString == '': searchString = input('song to play: ')
    searchString = searchString.lower()
    if searchString.split()[0] == 'play': searchString = searchString[len('play'):].strip()
    
    try:
        search = getTrackURI(searchString,nlp,client)
        if search != None:
            artistName = search['artists'][0]['name']
            songName = search['name']
            trackURI = search['uri']
            client.start_playback(uris=[trackURI])
            return f'Playing {songName} by {artistName}'
        else:
            return "Could not find song requested"
    except Exception as e:
        return f"Error finding song {e}"

def playPlaylist(searchString='', nlp=None, client=None): ###! PLAYS PLAYLIST !###
    if searchString == '': searchString = input('playlist to play: ')
    if searchString.split()[0].lower() == 'play': searchString = searchString[len('play'):].strip()
    doc = nlp(u"{}".format(searchString))


    ###? Get token POS tag ?###
    for token in doc:
        print(f"{token.text:{10}} {token.pos_:{10}} {token.tag_:{10}} {spacy.explain(token.tag_)}")        
    ###?###################?###
    print('\n')


    ###?See if it should start with a song ?###
    songInQueue = None
    if 'starting with' in searchString or 'in' in searchString or 'on' in searchString:
        patterns = [r"^(?P<song>.*) (in|on) (?P<hold1>.*)playlist(?P<hold2>.*)$",
                    r"^(?P<hold1>.*)playlist(?P<hold2>.*) starting with (?P<song>.*)$"]
        
        for pattern in patterns:
            m = re.match(pattern, r"{}".format(searchString))
            if m != None: 
                songInQueue = m.group('song')
                searchStringHold = f"{m.group('hold1')}playlist{m.group('hold2')}"
                break
                
        if songInQueue != None:
            doc2 = nlp(u"{}".format(songInQueue))
            queueList = []
            queueList.append(songInQueue)
            querySplit = songInQueue.split()
            ##* This part of the code finds requests based on artist, song *## 
            for i, token in enumerate(doc2):
                if token.pos_ == 'ADP' and token.tag_ == 'IN' and token.text.lower() in ['by', 'from']:
                    querySplit[i] = 'ADP'
                    queueList.append(' '.join(querySplit))
                    querySplit[i] = token.text
                elif token.text.lower() == "'s": ###TODO: Properly update the query split ###
                    querySplit[i-1] = querySplit[i-1].replace("'s", '')
                    querySplit.insert(i, 'POS')
                    queueList.append(' '.join(querySplit))
                    querySplit[i] = token.text
            ##*##############################################################*##

            ##* This part of the code eliminates unnecceasry parts of text based on a personalized list, these are last as we don't want to eliminate necessary info
            unecessaryWordsList = ['for me', 'for me', 'me']
            unecessaryWordsPos = ['begin', 'end', 'begin']
            
            for request in queueList.copy():
                for i, unecessary in enumerate(unecessaryWordsList):
                    pattern = ''
                    if unecessaryWordsPos[i] == 'end':
                        pattern = r"^(.*) {}$".format(unecessary)
                    else:
                        pattern = r"^{} (.*)$".format(unecessary)
                    
                    if pattern != '': m = re.match(pattern, r"{}".format(request))
                    if m != None:
                        request = m.group(1)
                queueList.append(request)
            ##*##############################################################*##

            searchString = searchStringHold
    ###?######################################?###

    doc = nlp(u"{}".format(searchString))
    ###? Find possesive word ?###
    posessiveWord = ''
    searchQuery = searchString.split()
    requestList = []
    #requestList.insert(0,searchString)
    for i, token in enumerate(doc):
        if token.pos_ == 'PRON' and token.tag_ == 'PRP$' and token.text == 'my':
            posessiveWord = token.text
            searchQuery.pop(i)
            requestList.insert(0,' '.join(searchQuery))
            break

        if token.pos_ == 'PART' and token.tag_ == 'POS' and token.text == "'s":
            posessiveWord = doc[i-1].text
            searchQuery.pop(i-1)
            requestList.insert(0,' '.join(searchQuery))
            break

        if token.pos_ == 'ADP' and token.tag_ == 'IN' and token.text in ['by', 'from']:
            posessiveWord = doc[i+1].text
            #searchQuery = searchQuery[0:i]
            searchQuery.pop(i)
            searchQuery.pop(i)
            requestList.insert(0,' '.join(searchQuery))
            break
    ###?#####################?###


    ###? Extract common words that add nothing to the playlist name ?###
    unecessaryWords = ['the', 'me', 'me the', 'for me']
    unecessaryWordsPos = ['begin', 'begin', 'begin', 'end']
    for request in requestList.copy():
        for i, unecessary in enumerate(unecessaryWords):
            pattern = ''
            if unecessaryWordsPos[i] == 'end':
                pattern = r"^(.*) {}$".format(unecessary)
            else:
                pattern = r"^{} (.*)$".format(unecessary)
            
            if pattern != '': m = re.match(pattern, r"{}".format(request))
            if m != None:
                request = m.group(1)
        requestList.insert(0,request)
    ###?#########################################################?###
    requestList.append(searchString)

    ###? Find + play playlist dependent on possessive person ?###
    
    '''for playlistSearchResult in client.search(playlistName,limit=50,type='playlist')['playlists']['items']:
        if re.sub(r'w[^\w\s]','',posessiveWord) in re.sub(r'w[^\w\s]','',playlistSearchResult['owner']['display_name'].lower()):
            client.start_playback(context_uri=playlistSearchResult['uri'])
            client.shuffle(True)
            client.repeat('context')
            return True'''
    ###?####################################################?###

    patterns = [
        r"^(?P<playlist>.*) playlist(.*)$",
        r"^(.*)playlist (?P<playlist>.*)$"]

    for i, request in enumerate(requestList):
        for i, pattern in enumerate(patterns):
            m = re.match(pattern, r"{}".format(request))
            if m == None: continue

            playlistName = m.group('playlist')
            try:
                #if posessiveWord == "my": posessiveWord = client.current_user()['display_name']
                posessiveWord = posessiveWord.lower()
                playlistSearchResult = client.search(playlistName,type='playlist',limit=50)['playlists']['items']
                if len(playlistSearchResult) > 0:
                    for playlist in playlistSearchResult:
                        playlistName = formatString(playlistName)
                        foundName = formatString(playlist['name'].lower())
                        posessiveWord = formatString(posessiveWord)
                        foundCreator = formatString(playlist['owner']['display_name'].lower())

                        if (playlistName in foundName or SequenceMatcher(None, playlistName, foundName).ratio() >= 0.8) and (posessiveWord == '' or posessiveWord == 'my' or (posessiveWord in foundCreator or SequenceMatcher(None, posessiveWord, foundCreator).ratio() >= 0.8)):

                            if songInQueue != None:
                                foundQueue = False
                                i=0
                                playlist_items = []
                                while len(client.playlist_items(playlist['id'],offset=i*100)['items']) > 0:
                                    for item in client.playlist_items(playlist['id'],offset=i*100)['items']:
                                        playlist_items.append(item)
                                    i+=1

                                for track in playlist_items:
                                    trackName = formatString(track['track']['name'])
                                    trackArtists = []
                                    for artist in track['track']['artists']:
                                        trackArtists.append(formatString(artist['name']))

                                    queuePatterns = [
                                        r"^(?P<song>.*) ADP (?P<artist>.*)$",
                                        r"^(?P<artist>.*) POS (?P<song>.*)$",
                                        r"^(?P<song>.*)"]

                                    for queue in queueList:
                                        for i, queuePattern in enumerate(queuePatterns):
                                            m = re.match(queuePattern, r"{}".format(queue))
                                            if m == None: continue

                                            if i < 2: artistName = formatString(m.group('artist'))
                                            else: artistName = ''
                                            songName = formatString(m.group('song'))

                                            if (songName in trackName or SequenceMatcher(None, songName, trackName).ratio() > 0.8) and (i < 2 or any(artistName in trackArtist for trackArtist in trackArtists) or any(SequenceMatcher(None, artistName, trackArtist).ratio() > 0.8 for trackArtist in trackArtists)):
                                                songInQueue = track['track']
                                                foundQueue = True
                                                break
                                        if foundQueue: break
                                    if foundQueue: break

                            if songInQueue != None: 
                                if not foundQueue: continue
                            
                            client.start_playback(context_uri=playlist['uri'])
                            if songInQueue != None:
                                print(f"starting with {songInQueue['name']} by {songInQueue['artists'][0]['name']}")
                                client.add_to_queue(songInQueue['uri'])
                                client.next_track()
                                return f"Playing playlist {playlist['name']} by {playlist['owner']['display_name']} starting with {songInQueue['name']} by {songInQueue['artists'][0]['name']}"
                            return f"Playing playlist {playlist['name']} by {playlist['owner']['display_name']}"

                            


                return "Could not find playlist"
            except Exception as e:
                print(e)
                return f"Error finding playlist: {e}"

    return False

def playAlbum(speech='',client=None): ###! PLAY REQUESTED ALBUM !###
    if speech == '': speech = input('Request album: ')
    if speech.startswith('play'): speech = speech[len('play'):].strip() ###* Get rid of 'play' *###
    found = False

    try:
        requestList = []
        requestList.append(speech)
        ##* This part of the code eliminates unnecceasry parts of text based on a personalized list, these are last as we don't want to eliminate necessary info
        unecessaryWords = ['the', 'me', 'me the', 'for me']
        unecessaryWordsPos = ['begin', 'begin', 'begin', 'end']
        for request in requestList.copy():
            for i, unecessary in enumerate(unecessaryWords):
                pattern = ''
                if unecessaryWordsPos[i] == 'end':
                    pattern = r"^(.*) {}$".format(unecessary)
                else:
                    pattern = r"^{} (.*)$".format(unecessary)
                
                if pattern != '': m = re.match(pattern, r"{}".format(request))
                if m != None:
                    request = m.group(1)
            requestList.insert(0,request) 
     ##*##############################################################*##
        for speech in requestList:
            if found: break
            ###? Find album, artist, starting with certain song ?###
            patterns = [r'^(?P<album>.*) album by (?P<artist>.*) starting with (?P<song>.*)$', ###* LOCATION album by KHALID starting with AMERICAN TEEN *###
                        r'^(the |)album (?P<album>.*) by (?P<artist>.*) starting (with|from) (?P<song>.*)$', ###* album LOCATION by KHALID starting with AMERICAN TEEN *###
                        r'^(?P<album>.*) album starting with (?P<song>.*) (by|from) (?P<artist>.*)$', ###* LOCATION album starting with AMERICAN TEEN by KHALID *###
                        r'^(the |)album (?P<album>.*) starting (with|from) (?P<song>.*) (by|from) (?P<artist>.*)$', ###* album LOCATION starting with AMERICAN TEEN by KHALID *###
                        r"^(?P<artist>.*^['s])('s|) album (?P<album>.*) starting (with|from) (?P<song>.*)$", ###* KHALID's album LOCATION starting with AMERICAN TEEN *###
                        r"^(?P<artist>.*^['s])('s|) (?P<album>.*) album starting (with|from) (?P<song>.*)$", ###* KHALID's LOCATION album starting with AMERICAN TEEN *###
                        r"^(?P<song>.*) (by|from) (?P<artist>.*) in (the |)album (?P<album>.*)$", ###* AMERICAN TEEN by KHALID in album LOCATION *###
                        r"^(?P<song>.*) in (the |)album (?P<album>.*) (by|from) (?P<artist>.*)$", ###* SHOT DOWN in album AMERICAN TEEN by KHALID *###
                        r"^(?P<song>.*) in (the |)(?P<album>.*) album (by|from) (?P<artist>.*)$", ###* SHOT DOWN in AMERICAN TEEN album by KHALID *###
                        r"^(?P<artist>.*^['s])'s (?P<song>.*) in (the |)album (?P<album>.*)$", ###* KHALID's AMERICAN TEEN in album LOCATION *###
                        r"^(?P<song>.*) (by|from) (?P<artist>.*) in (the |)(?P<album>.*) album$", ###* AMERICAN TEEN by KHALID in LOCATION album *###
                        r"^(?P<artist>.*^['s])'s (?P<song>.*) in (the |) (?P<album>.*) album$"] ###* KHALID's AMERICAN TEEN in album LOCATION *###

            for i, pattern in enumerate(patterns):
                m = re.match(pattern, speech)
                if m != None:
                    found = True
                    songName = m.group('song')
                    artistName = m.group('artist')
                    albumName = m.group('album')
                    break
            
            if found:
                searchResults = client.search(f"{albumName} {artistName}",1,0,"album")
                album = searchResults['albums']['items'][0]
                albumName = album['name']
                artistName = album['artists'][0]['name']

                i = 1
                tracks = client.album_tracks(album['id'])['items']
                while len(tracks) / i >= 20:
                    tracks.extend(client.album_tracks(album['id'], offset=20*i)['items'])
                    i+=1
                
                foundSong = False
                for track in tracks:
                    if songName in track['name'].lower() or SequenceMatcher(None, songName, track['name'].lower()).ratio() > 0.8:
                            songName = track['name']
                            foundSong = True
                            break
                
                client.start_playback(context_uri=album['uri'])
                if foundSong:
                    client.add_to_queue(client.search(f"{songName} {artistName}", type='track')['tracks']['items'][0]['uri'])
                    client.next_track()
                    return f"Playing {songName} in album {albumName} by {artistName}"               
                else:
                    return f"Playing album {albumName} by {artistName}"
            ###? Find patterns starting with a certain song ?###


            ###? Find patterns starting with a certian song ?###
            patterns = [r'^(?P<song>.*) in (the |)album (?P<album>.*)$',
                        r'^(?P<song>.*) in (the |)(?P<album>.*) album$',
                        r'^(the |)album (?P<album>.*) starting (with|from) (?P<song>.*)$',
                        r'^(the |)(?P<album>.*) album starting (with|from) (?P<song>.*)$']
            
            for i, pattern in enumerate(patterns):
                m = re.match(pattern, speech)
                if m != None:
                    found = True
                    albumName = m.group('album')
                    songName = m.group('song')
                    break
            
            if found:
                try:
                    searchResults = client.search(f"{songName} {albumName}",1,0,"track")
                    album = searchResults['tracks']['items'][0]['album']
                    albumName = album['name']
                    artistName = album['artists'][0]['name']
                    songName = searchResults['tracks']['items'][0]['name']
                    foundSong = True
                except: 
                    searchResults = client.search(f"{songName} {albumName}",1,0,"album")
                    album = searchResults['tracks']['items'][0]
                    albumName = album['name']
                    artistName = album['artists'][0]['name']
                    foundSong = False
                
                client.start_playback(context_uri=album['uri'])
                if foundSong:
                    client.add_to_queue(client.search(f"{songName} {artistName}", type='track')['tracks']['items'][0]['uri'])
                    client.next_track()
                    return f"Playing {songName} in album {albumName} by {artistName}"
                else:
                    return f"Playing album {albumName} by {artistName}"
                
            ###? Find patterns starting with a certain song ?###


            ###? Play album BY someone ?###
            patterns = [r'^(the |)album (?P<album>.*) (by|from) (?P<artist>.*)$',
                        r'^(the |)(?P<album>.*) album (by|from) (?P<artist>.*)$',
                        r"^(?P<artist>.*)('s|) (?P<album>.*) album",
                        r"^(?P<artist>.*)('s|) album (?P<album>.*)"]

            for i, pattern in enumerate(patterns):
                m = re.match(pattern,speech)
                if m != None:
                    artistName = m.group('artist')
                    albumName = m.group('album')
                    found = True
                    break

            if found:
                searchResults = client.search(f"{albumName} {artistName}",1,0,"album")
                album = searchResults['albums']['items'][0]
                albumName = album['name']
                artistName = album['artists'][0]['name']

                client.start_playback(context_uri=album['uri'])
                return f"Playing album {albumName} by {artistName}"
            ###? Play album BY someone ?###


            ###? PLAY album ?###
            patterns = [r'^(the |)album (?P<album>.*)$',
                        r'^(the |)(?P<album>.*) album$']
            
            for pattern in patterns:
                m = re.match(pattern, speech)
                if m != None:
                    albumName = m.group('album')
                    found = True
                    break
        
            if found:
                searchResults = client.search(albumName,1,0,"album")
                album = searchResults['albums']['items'][0]
                albumName = album['name']
                artistName = album['artists'][0]['name']

                client.start_playback(context_uri=album['uri'])
                return f"Playing album {albumName} by {artistName}"
        ###? PLAY album ?###

        return 'Couldnt find album'

    except Exception as e:
        return f"Error playing album: {e}"

def playArtist(speech='', client=None): ###! PLAY ARTIST !###
    if speech == '': speech = input('Request artist: ')
    if speech.startswith('play'): speech = speech[len('play'):].strip() ###* Get rid of 'play' *###
    found = False

    try:
        requestList = []
        requestList.append(speech)
        ##* This part of the code eliminates unnecceasry parts of text based on a personalized list, these are last as we don't want to eliminate necessary info
        unecessaryWords = ['the', 'me', 'me the', 'for me']
        unecessaryWordsPos = ['begin', 'begin', 'begin', 'end']
        for request in requestList.copy():
            for i, unecessary in enumerate(unecessaryWords):
                pattern = ''
                if unecessaryWordsPos[i] == 'end':
                    pattern = r"^(.*) {}$".format(unecessary)
                else:
                    pattern = r"^{} (.*)$".format(unecessary)
                
                if pattern != '': m = re.match(pattern, r"{}".format(request))
                if m != None:
                    request = m.group(1)
            requestList.insert(0,request) 
     ##*##############################################################*##
        for speech in requestList:
        ###? Find patterns starting with a certain song ?###
            patterns = [r"^(?P<artist>.*[^'s])('s|) (songs|music) starting (with|from) (?P<song>.*)$",
                        r'^(.*) (by|from) (?P<artist>.*) starting (with|from) (?P<song>.*)$']
            
            for pattern in patterns:
                m = re.match(pattern, speech)
                if m != None:
                    found = True
                    artistName = m.group('artist')
                    songName = m.group('song')
                    break
            
            if found:
                try:
                    searchResults = client.search(f"{songName} {artistName}",1,0,"track")
                    artist = searchResults['tracks']['items'][0]['artists'][0]
                    foundSong = True
                    songName = searchResults['tracks']['items'][0]['name']
                except:
                    foundSong = False 
                    searchResults = client.search(artistName,1,0,"artist")
                    artist = searchResults['artists']['items'][0]

                artistName = artist['name']
                client.start_playback(context_uri=artist['uri'])
                if foundSong: 
                    songSearch = client.search(f"{songName} {artistName}", type='track')['tracks']['items'][0]
                    songName = songSearch['name']
                    client.add_to_queue(songSearch['uri'])
                    client.next_track()
                    return f"Playing songs by {artistName} starting with {songName}"
                else:
                   return f"Playing songs by {artistName}"
        ###? Find patterns starting with a certain song ?###


        ###? Find just artist ?###
            patterns = [r"^(?P<artist>.*)('s) (.*)$", ###* ex: play my playlist high energy *###
                        r'^(.*) (by|from) (?P<artist>.*)$'] ###* ex: play my high energy *###
            
            for pattern in patterns:
                m = re.match(pattern, speech)
                if m != None:
                    found = True
                    artistName = m.group('artist')
                    break
            
            if found:
                artist = client.search(artistName,1,0,"artist")['artists']['items'][0]
                artistName = artist['name']
                
                client.start_playback(context_uri=artist['uri'])
                return f"Playing songs by {artistName}"
        ###? Find just artist ?###
        return "Could not find artist"

    except Exception as e:
        return f"Error finding artist: {e}"

def shuffle(speech, client): ###! TURN ON/OFF SHUFFLE !###
    try:
        positive = ['on', 'start']
        negative = ['off', 'stop']
        if any(neg in speech for neg in negative): 
            client.shuffle(False)
            return "Turned off shuffle"
        else: 
            client.shuffle(True)
            return "Turned on shuffle"
    except Exception as e:
        return f"Error changing shuffle: {e}"

def repeat(speech, client): ###! TURN ON/OFF REPEAT !###
    try:
        positive = ['on', 'start']
        negative = ['off', 'stop']
        songs = ['song', 'track', 'this']
        if any(neg in speech for neg in negative): 
            client.repeat('off')
            return "Turned off repeat"
        elif any(pos in speech for pos in positive) and any(song in speech for song in songs):
            client.repeat('track')
            return "Repeating this track"
        else: 
            client.repeat('context')
            return "Repeating this context"
    except Exception as e:
        return f"Error changing shuffle: {e}"

def parseSpotify(speech = "", engine=None, source=None, r=None,user=None): ###! MAIN SPOTIFY !###
    try:
        
        ###? STEP 1: Get spotify object ?###
        
        speech = speech.replace(' on spotify','').lower()
        if speech == '': return "No spotify command"
        ###? STEP 1: Get spotify object ?###


        ###? STEP 2: See if spotify should just be turned on ?###
        if speech.startswith('open') or speech.startswith('run'): return "Opened spotify"
        ###? STEP 2: See if spotify should just be turned on ?###


        ###? STEP 3: Check if there is a device playing, if not force the device opening spotify to play ?###
        devices = client.devices()
        activeDevice = any(device['is_active'] for device in devices['devices']) #Check devices
        #Check devices
        while activeDevice == False:
            client.transfer_playback(devices['devices'][0]['id'],True)
            time.sleep(2) ###* Give spotify some time to register the force startup *###
            devices = client.devices()
            activeDevice = any(device['is_active'] for device in devices['devices']) #Check devices
        ###? STEP 3: Check if there is a device playing, if not force the device opening spotify to play ?###


        ###? STEP 4: Get state and probability of state from spotify model ?###
        #0: Just open spotify
        #1: Play song
        #2: Play playlist
        #3: Play artist
        #4: Play album
        #5: Add to queue
        
        alterTask, speech, task = alterSpotifyState(speech, client) ###* Alter spotify state is possible *###

        #state, probability = chooseState(speech, 'Spotify')
        #print(f"\n\nState: {state}\nAccuracy: {probability}")

        if alterTask != '':
            return alterTask

        ###? STEP 4: Get state and probability of state from spotify model ?###

        returnMsg = ""
        ###? STEP 5: Do action based on query ?###
        if speech.startswith('play'):         
            if 'playlist' in speech: returnMsg = playPlaylist(speech,nlp,client)
            elif 'artist' in speech: returnMsg = playArtist(speech,client)
            elif 'album' in speech: returnMsg = playAlbum(speech,client)
            elif 'queue' in speech: returnMsg = addToQueue(speech, client, False)
            else: 
                returnMsg = playSong(speech,nlp,client)
                if returnMsg == 'Could not find song requested': returnMsg = playArtist(speech,client)
        elif speech.startswith('add') or speech.startswith('put'): returnMsg = addToQueue(speech,client) 
        else: returnMsg = task
        ###? STEP 5: Do action based on query ?###

        return f"{returnMsg}"
    
    except Exception as e: return f"Error encountered processing spotify request: {e}"
    
parseSpotify("add forever and more by role model to queue")