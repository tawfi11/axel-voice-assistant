import nltk, spacy, re, spotipy
import speech_recognition as sr
import spotipy.util as util
from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy import displacy
from spacy.attrs import POS
from difflib import SequenceMatcher

nlp = spacy.load('en_core_web_sm')
clientID = '4d69a1fdddec4723a77d7060d535185d'
clientSecret = '61be34f6da764189a27e1471f4b16c96'
user = 'Nusair Islam'
redirect_uri = 'https://www.google.ca/'
scope = 'user-read-private user-read-playback-state user-modify-playback-state user-top-read playlist-modify-public playlist-modify-private playlist-read-collaborative'
cacheFile = r"H:\User\Desktop\Voice-Assistant\Axel-Voice-Assistant\cache\spotifyCache.cache-Nusair Islam"
token = util.prompt_for_user_token(user, scope, clientID, clientSecret, redirect_uri, cacheFile)
client = spotipy.Spotify(auth=token)

def formatString(word): ###! REMOVE PUNCTUATION AND CAPITALIZATION FROM WORDS !###
    punctuation = ['!', '(', ')', ',', '[', ']', '{', '}', ';', ':', '\'', '\"', '\\', '<', '>', '.', '/', '?', '@', '#', '$', '%', '^', '&', '*', '~']
    for p in punctuation:
        word = word.replace(p,'')
    return word.lower()

def stringMatcher():
    a = input('string a: ')
    b = input('string b: ')
    print(SequenceMatcher(None,a,b).ratio())
    return

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration = 5)
        r.threshold = 300
        while True:
            print('speak')
            try:
                audio = r.listen(source, phrase_time_limit=5,timeout=2)
                speech = r.recognize_google(audio, language ="en_US")
                print(speech)
                doc = nlp(u"{}".format(speech))
                

                ###? Get token POS tag ?###
                with open(r'H:\User\Desktop\tokens.txt','a') as f:
                    for i, token in enumerate(doc):
                        if i == 0: continue
                        f.write(f"{token.text:{10}} {token.pos_:{10}} {token.tag_:{10}} {spacy.explain(token.tag_)}\n")
                    f.write('\n')
                    #playPlaylist(speech)
                ###?###################?###`

                playSong(speech)
            except:
                continue

def test():
    query = input('Type sentence: ')
    doc = nlp(u"{}".format(query))

    for token in doc:
        print(f"{token.text:{10}} {token.pos_:{10}} {token.tag_:{10}} {spacy.explain(token.tag_)}")

def getTrackURI(query): ###! FINDS TRACK URIS GIVEN A QUERY FOR A SONG !###
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

     ##* This part of the code finds requests based on artist, song *## 
    for i, token in enumerate(doc):
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
                        artistName = search['artists'][0]['name']
                        songName = search['name']
                        trackURI = search['uri']
                        print(f'Playing {songName} by {artistName}')
                        return [trackURI]
            except Exception as e:
                print(e)
    
    return None
    ###?#####################################?###

def playSong(searchString=''): ###! FORMATS A SONG SEARCH QUERY !###
    if searchString == '': searchString = input('song to play: ')
    searchString = searchString.lower()
    if searchString.split()[0] == 'play': searchString = searchString[len('play'):].strip()
    
    trackURI = getTrackURI(searchString)
    if trackURI != None:
        client.start_playback(uris=trackURI)
    else:
        print("Could not find song")

    print('\n\n')

def playPlaylist(searchString=''): ###! PLAYS PLAYLIST !###
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
    if 'starting with' in searchString or 'in' in searchString:
        patterns = [r"^(?P<song>.*) in (?P<hold1>.*)playlist(?P<hold2>.*)$",
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
                                for track in client.playlist_items(playlist['id'])['items']:
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
                            print(f"Playing playlist {playlist['name']} by {playlist['owner']['display_name']}")
                            client.start_playback(context_uri=playlist['uri'])
                            client.shuffle(True)
                            client.repeat('context')
                            if songInQueue != None:
                                print(f"starting with {songInQueue['name']} by {songInQueue['artists'][0]['name']}")
                                client.add_to_queue(songInQueue['uri'])
                                client.next_track()
                            

                            


                            return True
            except Exception as e:
                print(e)

    return False

def playAlbum(speech=''): ###! PLAY REQUESTED ALBUM !###
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
                    print(f"Playing {songName} in album {albumName} by {artistName}")
                    return True
                else:
                    print(f"Playing album {albumName} by {artistName}")
                    return True
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
                    print(f"Playing {songName} in album {albumName} by {artistName}")
                    return True
                else:
                    print(f"Playing album {albumName} by {artistName}")
                    return True
                
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
                albumName = album['name']
                artistName = album['artists'][0]['name']

                client.start_playback(context_uri=album['uri'])
                print(f"Playing album {albumName} by {artistName}")
                return True
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
                print(f"Playing album {albumName} by {artistName}")
                return True
        ###? PLAY album ?###

        print('Couldnt find album')
        return False

    except Exception as e:
        print(e)
        return False

def playArtist(speech=''): ###! PLAY ARTIST !###
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
                    print(f"Playing songs by {artistName} starting with {songName}")
                    return True
                else:
                    print(f"Playing songs by {artistName}")
                    return True                
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
                print(f"Playing songs by {artistName}")
                return True
        ###? Find just artist ?###
        return False

    except Exception as e:
        print(e)
        return False
    

choice = 'artist'
while True:
    if choice == 'song': playSong()
    elif choice == 'playlist': playPlaylist()
    elif choice == 'album': playAlbum()
    elif choice == 'artist': playArtist()
    elif choice == 'voice': listen()
    elif choice == 'vocab': test()
    elif choice == 'match': stringMatcher()