from googlesearch import search
import webbrowser

def gotoWebsite(query, engine):
    commonWords = ["tell", "open", "show", "give", "take", "to", "my", "me", "the"]
    for common in commonWords:
        if query.startswith(common) == True:
            query = query[len(common) + 1: :]
    
    queryList = list(search(query, tld="com", num=1,stop=1))
    open = queryList[0]
    webbrowser.open(open)
    engine.say("opening" + query)
    engine.runAndWait()

