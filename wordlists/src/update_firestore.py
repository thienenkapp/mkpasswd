#!/usr/bin/python3
from google.cloud import firestore
import helpers as mkpass
import os
import json
import yaml

#This script takes the existing wordlist maintained in an easy manner and uploads it to Google Firestore
#Example are here
#https://github.com/GoogleCloudPlatform/python-docs-samples/blob/d1ddeeff5f6fe3108ab0b2470d42db041ff07ebc/firestore/cloud-client/snippets.py#L71-L78

#Document format is
#country: value
#category: value
#subcategory: value
#nouns: array
#verbs: array
#adjectivs: array

#wordlist file format
#filename: country-category-subcategory.txt
#content: NOUNS: xxx \n VERBS xxx \n ADJECTIVS xxx \n

def ValidFileName(filename):
    #Parse filename
    filesplit = filename.replace('.','-').split('-')
    if (filesplit[filesplit.__len__()-1] != "txt") or (filesplit.__len__() <= 2):
        print ("Given filename ", filename, " can't be uploaded.")
        print ("Please follow the convention >country-category[-subcategory].txt")
        return False
    return True

def ValidWordlistJson(p_json):
    data = p_json

    # Validate the required keys
    required_keys = {"country", "category", "nouns"}
    if not required_keys.issubset(data.keys()):
        print("Missing required keys:", ", ".join(required_keys - data.keys()))
        return False

    # Validate the type of 'nouns' key
    if not isinstance(data["nouns"], list):
        print("Invalid type for 'nouns' key. Expected list.")
        return False

    # If all checks pass, return True
    return True

def SaveToFirestore(data):
    # Add a new doc in collection 'cities' with ID 'LA'
    documentname=data['country']+'-'+data['category'].replace(" ","_")
    if "subcategory" in data:
        documentname += "-"+data['subcategory'].replace(" ","_")
    db = firestore.Client()
    db.collection(u'mkpasswd-wordlists').document(documentname).set(data)
    print(f"Document {documentname} saved.")

def upload_wordfile_txt(filename):
    #filename = "de-buchstabiertafel-nato.txt"

    if not ValidFileName(filename):
        return None

    mkpass.wordsnoun=[]
    mkpass.wordsverb=[]
    mkpass.wordsadjective=[]

    #mkpass.ReadWordFile(mkpass.wordlistdir, filename)
    mkpass.ReadWordFile(filename)

    #Parse filename
    filesplit = filename.replace('.','-').split('-')

    data = {}
    data['country'] = filesplit[0]
    data['category'] = filesplit[1].replace('_',' ')
    if filesplit.__len__() > 3:
        data['subcategory'] = filesplit[2].replace('_',' ')
    if mkpass.wordsnoun.__len__()>0:
        data["nouns"] = mkpass.wordsnoun
    if mkpass.wordsverb.__len__()>0:
        data["verbs"] = mkpass.wordsverb
    if mkpass.wordsadjective.__len__()>0:
        data["adjectives"] = mkpass.wordsadjective

    if (ValidWordlistJson(data)):
        SaveToFirestore(data)
    else:
        print(f"Error saving file {filename} ")

def upload_wordfile_json(filename):
    #filename = "*.json"

    try:
        with open(filename, 'r') as f:
            data = json.loads(f.read())
    except:
        print("Error opening file")

    if (ValidWordlistJson(data)):
        SaveToFirestore(data)
    else:
        print(f"Error saving file {filename} ")

def upload_wordfile_yaml(filename):
    #filename = "*.yaml"

    try:
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
            # Convert to JSON object
            json_data = json.dumps(data)
    except:
        print("Error opening file")

    if (ValidWordlistJson(data)):
        SaveToFirestore(data)
    else:
        print(f"Error saving file {filename} ")

def upload_wordlists():
    os.chdir(mkpass.wordlistdir)
    wordfiles=os.listdir()
    wordfiles.sort()

    for wordfile in wordfiles:
        if wordfile.endswith(".txt"):
            upload_wordfile_txt(wordfile)

    for wordfile in wordfiles:
        if wordfile.endswith(".json"):
            upload_wordfile_json(wordfile)

    for wordfile in wordfiles:
        if wordfile.endswith(".yaml"):
            upload_wordfile_yaml(wordfile)

if __name__ == "__main__":
    upload_wordlists()
