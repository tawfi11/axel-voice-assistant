import spacy
from textblob import TextBlob
import os,sys, pandas

nlp = spacy.load('en_core_web_sm')

def parseInput(query, spacyDict):
    doc = nlp(u"{}".format(query))
    doc = nlp(query)

    posList = ""
    depList = ""
    tagList = ""

    subj = ""
    verb = ""
    root = ""
    possessive = ""
    question = ""
    pobj = ""
    dobj = ""
    ###? Get token POS tag ?###
    #print(f"\nTEXT       POS        TAG        DEP")
    for i, token in enumerate(doc):
        if "subj" in token.dep_: subj = token.text
        if "VERB" in token.pos_: verb = token.text
        if "ROOT" in token.dep_: root = token.text
        if "PRP$" in token.tag_: possessive = token.text
        if "WP" in token.tag_: question = token.text
        if "dobj" in token.dep_: dobj = token.text
        if "pobj" in token.dep_: pobj = token.text
        print(f"{token.text:{10}} {token.pos_:{10}} {spacy.explain(token.pos_):{10}} {token.tag_:{10}} {spacy.explain(token.tag_):{10}} {token.dep_:{10}} {spacy.explain(token.dep_)}")
        posList += f"{token.pos_} " 
        depList += f"{token.dep_} "
        tagList += f"{token.tag_} "
        spacyDict['Text'].append(token.text)
        spacyDict['POS'].append(token.pos_)
        spacyDict['POS Explain'].append(spacy.explain(token.pos_))
        spacyDict['TAG'].append(token.tag_)
        spacyDict['TAG Explain'].append(spacy.explain(token.tag_))
        spacyDict['DEP'].append(token.dep_)
        spacyDict['DEP Explain'].append(spacy.explain(token.dep_))
                                        
        
    ###?###################?###
    posList.strip()
    depList.strip()
    tagList.strip()

    print('\n')
    for ent in doc.ents:
        print(f"{ent.text:{10}} {ent.label_:{10}}")

    if subj != "": print(f"Subject is: {subj}")
    if verb != "": print(f"Verb is: {verb}")
    if root != "": print(f"ROOT is: {root}")
    if possessive != "": print(f"Person referred to is: {possessive}")
    if question != "": print(f"Question is :{question}")
    if dobj != "": print(f"Direct object is: {dobj}")
    if pobj != "": print(f"prepositional object is: {pobj}")
    
    return spacyDict

spacyDict = {
        'Text': [],
        'POS' : [],
        'POS Explain' : [],
        'TAG' : [],
        'TAG Explain' : [],
        'DEP' : [],
        'DEP Explain' : []
    }

while True:
    query = input("Say something: ")
    
    if query.replace('\n','') == "":
         pandas.DataFrame(spacyDict).to_csv(os.path.abspath(os.path.dirname(sys.argv[0]) + "/word_spacy.csv"), mode='a')
    spacyDict = parseInput(str(query), spacyDict)