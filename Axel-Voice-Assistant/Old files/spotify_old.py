import os, sys, json, spotipy, webbrowser, random, pyttsx3, traceback, time
import spotipy.util as util
from json.decoder import JSONDecodeError
from difflib import SequenceMatcher
import googletrans
from googletrans import Translator
#from textblob import TextBlob

def keywordcheck(keywords, speech):
    for word in keywords:
        if word in speech:
            return True
    return False

def getFromTxt(file='config.txt',keyline='',delimiters=[':','\n',' ']):
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

def isEnglish(string):
    string = string.lower()
    words = [' ','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm','n','o','p','q','r','s','t','u','v','w','x','y','z',',','.','!']
    for word in words:
        string = string.replace(word,'')
    if string == '':
        return True
    else:
        return False

def playSong(song, spotifyObject, deviceID, artist=None):
    trackSelectionList = []
    engine = pyttsx3.init()
    if artist==None:
        artist = song
        query = song
    else:
        query = song + artist
    try:
        searchResults = spotifyObject.search(query,1,0,"track")
        trackName = searchResults['tracks']['items'][0]['name']
        if SequenceMatcher(None,song,trackName).ratio() > 0.6:
            trackSelectionList.append(searchResults['tracks']['items'][0]['uri'])
            spotifyObject.start_playback(device_id=deviceID, context_uri=None,uris=trackSelectionList)
            spotifyObject.repeat('context',deviceID)
            done = True
            engine.say('playing ' + song + ' on spotify')
            engine.runAndWait()
        else:
            commonWordDelimiter = ['songs', 'tracks', 'music']
            for word in commonWordDelimiter:
                if artist.find(word) != -1:
                    artist = artist.replace(word, '')
            done = playArtist(artist,spotifyObject,deviceID)
            engine.say('Playing songs from ' + artist + ' on spotify')
            engine.runAndWait()
        return done
    except:
        return False

def playArtist(query, spotifyObject, deviceID, song='any'):
    try:
        trackSelectionList = []
        searchResults = spotifyObject.search(query, 1, 0, 'artist')
        artist = searchResults['artists']['items'][0]
        artistID = artist['id']
        
        trackURIs = []
        trackName = []
        z = 0
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']
        for item in albumResults:
            print("ALBUM: " + item['name'])
            albumID = item['id']

            # Extract track data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']
            trackSelectionList = []
            for item in trackResults:
                print(str(z) + ": " + item['name'])
                trackURIs.append(item['uri'])
                trackName.append(item['name'].lower())
                trackSelectionList.append(item['uri'])
                z+=1
        MaxTracks = z
        #translator = Translator()
        i = 0
        
        song = input("which song would you like to play?").lower()
        if 'random' in song or 'any' in song:
                spotifyObject.start_playback(deviceID,context_uri=searchResults['artists']['items'][0]['uri'])
                spotifyObject.shuffle(True,deviceID)
                return True
        else:
            for name in trackName:
                try:
                    if not isEnglish(name):
                        name = translator.translate(name).text
                        time.sleep(1)
                except Exception:
                    print('error')
                name = name.replace(" ", "").lower()
                song = song.replace(" ", "").lower()
                if (name in song) or (song in name):
                    trackSelectionList.insert(0,trackURIs[i])
                    spotifyObject.start_playback(deviceID, None, trackSelectionList)
                    return True
                i+=1
            print('could not find song')
    except:
        return False

def GetKey(val, dictA):
    val = val.lower()
    for key, value in dictA.items():
        value = value.lower()
        if val in value or value in val:
            return key
    return "key doesn't exist"

def playPlaylist(query, spotifyObject, deviceID):
    try:
        searchResults = spotifyObject.search(query,1,0,"playlist")
        spotifyObject.start_playback(deviceID,context_uri=searchResults['playlists']['items'][0]['uri'])
        spotifyObject.shuffle(True,deviceID)
        return True
    except:
        return False

def playAlbum(query,spotifyObject,deviceID):

    searchResults = spotifyObject.search(query, 1, 0, 'album')
    song = 'any'
    try:
        album = searchResults['albums']['items'][0]
        
    
        if 'any' in song or 'random' in song:
            spotifyObject.start_playback(deviceID,context_uri=album['uri'])
            spotifyObject.shuffle(True,deviceID)
    except:
        return False
    
def decode(speech, spotifyObject, deviceID, engine, source, r):
    commonWordDelimiters = ["play ", " on spotify", 'open spotify']
    
    testSpeech = speech
    for delimiter in commonWordDelimiters:
        testSpeech = testSpeech.replace(delimiter, "")
    
    checkPresets(testSpeech,spotifyObject,deviceID,engine, source, r)
    
def checkPresets(testSpeech,spotifyObject,deviceID,engine, source, r):
    
    try:
        if testSpeech == '' or testSpeech == ' ' or ((testSpeech.startswith('continue') and (testSpeech[9::].startswith('playing') or testSpeech[9::].startswith('playback'))) or (testSpeech.startswith('resume') and (testSpeech[7::].startswith('playback') or testSpeech[7::].startswith('playing')))):
            spotifyObject.start_playback(deviceID)
            return

        if testSpeech.find('on shuffle') != -1:
            spotifyObject.shuffle(True,deviceID)
            return

        if (testSpeech.find('next')!=-1 or testSpeech.find('skip')!=-1) and (testSpeech.find('song') != -1 or testSpeech.find('track') != -1):
            spotifyObject.next_track(deviceID)
            return
        
        if testSpeech.find('previous track') != -1 or testSpeech.find('last track') != -1:
            spotifyObject.previous_track(deviceID)
            return
        
        if testSpeech.find('on repeat') != -1:
            spotifyObject.repeat('context', deviceID)
            return

        if testSpeech.startswith('pause') and (testSpeech.endswith('song') or testSpeech.endswith('music')):
            spotifyObject.pause_playback(deviceID)
            return

        if testSpeech.find('my favourite') != -1 or testSpeech.find('my top') != -1 or testSpeech.find('my most listened') != -1:
            if testSpeech.find('artist') != -1:
                artist = spotifyObject.current_user_top_artists(limit=1)
                spotifyObject.start_playback(deviceID, context_uri=artist['items'][0]['uri'])
            elif testSpeech.find('track') != -1 or testSpeech.find('song') != -1:
                track = spotifyObject.current_user_top_tracks()
                trackList = []
                for t in track['items']:
                    trackList.append(t['uri'])
                spotifyObject.start_playback(deviceID,uris=trackList)
            return

        if keywordcheck(['songs similar','songs like this','similar songs','like the one playing'], testSpeech):
            playback = spotifyObject.currently_playing()
            genres = spotifyObject.artist(playback['item']['artists'][0]['id'])['genres']
            artists = []
            artists.append(playback['item']['artists'][0]['id'])
            tracks = []
            tracks.append(playback['item']['id'])
            track = spotifyObject.recommendations(seed_artists=artists, seed_tracks=tracks, seed_genres=genres)
            tracklist = []
            for t in track['tracks']:
                tracklist.append(t['uri'])
            spotifyObject.start_playback(deviceID,uris=tracklist)
            return

        if testSpeech.endswith('queue') or testSpeech.endswith('2q') or testSpeech.endswith('myq') or testSpeech.endswith('my queue'):
            if testSpeech.endswith('to my queue'):
                testSpeech = testSpeech[0:len(testSpeech)-12:]
            elif testSpeech.endswith('queue'):
                testSpeech = testSpeech[0:len(testSpeech)-9:] #to Queue or my Queue or on Queue
            elif testSpeech.endswith('2q'):
                testSpeech = testSpeech[0:len(testSpeech) - 3:]
            elif testSpeech.endswith('to myq'):
                testSpeech = testSpeech[0:len(testSpeech) - 7:]

            if testSpeech.startswith('put'):
                testSpeech = testSpeech[4::]
            elif testSpeech.startswith('add'):
                testSpeech = testSpeech[4::]
            elif testSpeech.startswith('at'):
                testSpeech = testSpeech[3::]

            if testSpeech.find('by') != -1:
                i = testSpeech.index(' by')
                song = testSpeech[0:i:]
                artist = testSpeech[i+3::]
                query = song + artist
            else:
                query = testSpeech

            searchResults = spotifyObject.search(query,1,0,"track")
            track = searchResults['tracks']['items'][0]['uri']
            spotifyObject.add_to_queue(track,deviceID)
            engine.say('Adding ' + testSpeech + ' to queue on spotify')
            engine.runAndWait() 
            return
        
        if testSpeech.find('add') != -1 and testSpeech.find('playlist') != -1:
            engine.say('add currently playing song to which playlist?')
            engine.runAndWait()
            audio = r.listen(source, timeout = 2, phrase_time_limit=7)
            speech = r.recognize_google(audio, language='en-US')
            delimiters = ['add to ', 'my ']
            
            for d in delimiters:
                if speech.startswith(d):
                    speech = speech.replace(d,'')
                
            searchResults = spotifyObject.search(speech,1,0,"playlist")
            playlist = searchResults['playlists']['items'][0]['id']
            track = []
            track.append(spotifyObject.currently_playing()['item']['uri'])
            spotifyObject.playlist_add_items(playlist,track)
            engine.say('adding ' + spotifyObject.currently_playing()['item']['name'] + ' to ' + searchResults['playlists']['items'][0]['name'])
            engine.runAndWait()
            return

    except:
        engine.say('error playing on spotify')
        engine.runAndWait()
        return
    
    play(testSpeech, spotifyObject, deviceID,engine)

def play(testSpeech, spotifyObject, deviceID, engine):
    done = False
    #test album
    try:
        if testSpeech.find('album') != -1:
            artist = ''
            if testSpeech.startswith('the '):
                testSpeech = testSpeech[4::]
            if testSpeech.find('by ') != -1:
                i = testSpeech.index(' by')
                artist = testSpeech[i+3::]
                testSpeech = testSpeech[0:i:]
            if testSpeech.startswith('album'):
                done = playAlbum(testSpeech[6::] + artist, spotifyObject, deviceID)
                engine.say('Playing album ' + testSpeech[6::] +  ' on spotify')
                engine.runAndWait()
            else:
                i = testSpeech.index(' album')
                done = playAlbum(testSpeech[0:i:] + artist, spotifyObject, deviceID)
                engine.say('Playing album ' + testSpeech[0:i:] + ' on spotify')
                engine.runAndWait()
            
        #test playlist
        elif testSpeech.find('playlist') != -1:
            if testSpeech.startswith('my'):
                testSpeech = testSpeech[3::]
            if testSpeech.startswith('playlist'):
                done = playPlaylist(testSpeech[9::], spotifyObject, deviceID)
                engine.say('Playing playlist ' + testSpeech[9::] + ' on spotify')
                engine.runAndWait()
            else:
                i = testSpeech.index(' playlist')
                done = playPlaylist(testSpeech[0:i:], spotifyObject, deviceID)
                engine.say('Playing playlist ' + testSpeech[0:i:] + ' on spotify')
                engine.runAndWait()

        #test artist - song
        elif testSpeech.find('artist') != -1:
            if testSpeech.find('artists') != -1:
                i = testSpeech.index('artists')
                testSpeech = testSpeech[i+8::]
            else:
                i = testSpeech.index('artist')
                testSpeech = testSpeech[i+7::]
            done = playArtist(testSpeech,spotifyObject,deviceID)
            engine.say('Playing songs from artist ' + testSpeech + ' on spotify')
            engine.runAndWait()
        #Play song
        else:
            if testSpeech.find('by') != -1:
                i = testSpeech.index(' by')
                song = testSpeech[0:i:]
                artist = testSpeech[i+3::]
                done = playSong(song, spotifyObject,deviceID,artist)
            else:
                done = playSong(testSpeech,spotifyObject,deviceID)
        
        
        if done == False:
            engine.say('Error playing on spotify')
            engine.runAndWait()
    except:
        engine.say('error playing on spotify')
        engine.runAndWait()

def runSpotify(engine, speech, source, r,user):

    os.system('Spotify')
    clientID = user.spotifyID
    #clientID = getFromTxt('config.txt','Spotify-ID')
    clientSecret = user.spotifyPass
    #clientSecret = getFromTxt('config.txt','Spotify-Secret')
    user = user.spotifyUser
    #user = getFromTxt('config.txt','Spotify-Username',[':','\n'])
    if clientID == '' or clientSecret == '' or user == '': #check if user inputted information
        engine.say('Information not found in config file')
        engine.runAndWait()
        return

    scope = 'user-read-private user-read-playback-state user-modify-playback-state user-top-read playlist-modify-public playlist-modify-private playlist-read-collaborative'
    try:
        try:
            token = util.prompt_for_user_token(user, scope, clientID, clientSecret, 'https://www.google.ca/')
        except (AttributeError, JSONDecodeError):
            os.remove(f".cache-{user}")
            token = util.prompt_for_user_token(user,scope,clientID,clientSecret,'https://www.google.ca/')
        spotifyObject = spotipy.Spotify(auth=token)
        devices = spotifyObject.devices()
        #print(json.dumps(devices, sort_keys=True, indent = 4))
    except:
        engine.say('Error signing into Spotify account')
        engine.runAndWait()
        return

    try:
        i = 0
        for device in devices['devices']:
            if device['is_active'] == True:
                break
            i+=1
        deviceID = devices['devices'][i]['id']
    except:
        time.sleep(5)
        try:
            deviceID = devices['devices'][0]['id']
        except:
            engine.say('Please have spotify running on a device and then call a command')
            engine.runAndWait()
            return
        

    decode(speech, spotifyObject, deviceID, engine, source, r)

'''
runSpotify(pyttsx3.init(),'put Halfway There on queue')
runSpotify(pyttsx3.init(),'play khalid songs')
runSpotify(pyttsx3.init(),'play moonlight in vermont by frank sinatra')
runSpotify(pyttsx3.init(),'play up all night')
'''

