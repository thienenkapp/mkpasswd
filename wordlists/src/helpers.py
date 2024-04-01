#!/usr/bin/python3
import os
import functools
import random
import math
import argparse

#Found the basic of the idea which is diceware:
#Here is nice FAQ
#https://theworld.com/~reinhold/dicewarefaq.html
#https://de.wikipedia.org/wiki/Diceware


#Print with no newline
printnonl=functools.partial(print,end="")

wordlistdir='./data'

wordfiles=[]
wordsnoun=[]
wordsverb=[]
wordsadjective=[]
wordsfill=['.','-','#','+','!',':',' ']
wordsnum=[0,1,2,3,4,5,6,7,8,0]
wordlistcategory=["all"]
numberwordfilesused=0

def usage():
    print("Make password")

def log(message,level):
    if level < 1:
        print(messeage)
    elif level < 2:
        print(message)

def ReadWordFile(sFile):
    #f = open(file_path+"/"+sFile,"r")
    f = open(sFile,"r")
    lines = f.readlines()
    f.close
    wordkind=''
    for line in lines:
        line=line.replace('\n','').replace('\r','')
        log(line,4)
        if (line=="NOUNS:"):
            wordkind="NOUN"
            continue
        elif (line=="VERBS:"):
            wordkind="VERB"
            continue
        elif (line=="ADJECTIVES:"):
            wordkind="ADJECTIVE"
            continue

        log(wordkind,4)

        if (wordkind!=""):
            if (line!="") or (line[1]!="#"):
                if (wordkind=="NOUN"):
                    log("Add word " + line + " to NOUN list",3)
                    wordsnoun.append(line)
                elif (wordkind=="VERB"):
                    log("Add word " + line + " to VERB list",3)
                    wordsverb.append(line)
                elif (wordkind=="ADJECTIVE"):
                    log("Add word " + line + " to ADJECTIV list",3)
                    wordsadjective.append(line)
                else:
                    log("ERROR",2)
            else:
                log("Skip line",4)
        else:
            log("Unknown wordkind",4)

def GeneratePassword():
    #
    # Target is to have at least three words, special characters and numbers
    # This pices must be shaked and the dictionary words slightly modified and we have something new
    # Let's start with fixed 3 words based on the word type NOUN, VERB and ADJECTIV
    # I will go with fixed order like
    #   - NOUN VERB ADJE
    #   - NOUN NOUN NOUN
    #   - NOUN VERB NOUN
    #
    pwords=[]
    rndgen=random.SystemRandom()

    #Get special character
    num=rndgen.randint(1,wordsfill.__len__())
    fill=wordsfill[num-1]

    if (wordsnoun.__len__()):
        num=rndgen.randint(1,wordsnoun.__len__())
        pwords.append(wordsnoun[num-1])


    if (wordsverb.__len__()):
        num=rndgen.randint(1,wordsverb.__len__())
        pwords.append(wordsverb[num-1])
    else:
        #Assumption is the NOUNS are always set
        num=rndgen.randint(1,wordsnoun.__len__())
        pwords.append(wordsnoun[num-1])

    if (wordsadjective.__len__()):
        num=rndgen.randint(1,wordsadjective.__len__())
        pwords.append(wordsadjective[num-1])
    else:
        #Assumption is the NOUNS are always set
        num=rndgen.randint(1,wordsnoun.__len__())
        pwords.append(wordsnoun[num-1])

    num=rndgen.randint(1,999)

    genPW=""
    for pword in pwords:
        genPW=genPW+pword+fill

    genPW=genPW+str(num)

    #print (genPW)
    return genPW


def CalculatePasswordEntropy(sPW):
    #https://generatepasswords.org/how-to-calculate-entropy/
    #https://www.pleacher.com/mp/mlessons/algebra/entropy.html
    L=sPW.__len__()
    #R=26_lowercase+26_uppercase+10_numbers+9_specialcahar
    R1=26+26+10+wordsfill.__len__()
    #R calculated based on number of words only
    R2 = wordsnoun.__len__() + wordsverb.__len__() + wordsadjective.__len__() #+999
    E1=math.log2(math.pow(R1,L))
    E2=math.log2(math.pow(R2,1))

    print(sPW + " E1: " + E1.__str__() + " E2: " + E2.__str__())
    return E1

if __name__ == "__main__":
    # A bit stupid to have two implementation of the password generation
    # Start this because of the initial missing CloudFunction and the knowledge about local cloud function testing
    parser = argparse.ArgumentParser(prog="helper",description='Uses existing wordfiles generate as password to test a file.')
    parser.add_argument('-l','--country', nargs='?', const='de', default='de', choices=['de', 'en'], required=False, help='Get wordlist of country (default: %(default)s)')
    parser.add_argument('-c','--category', nargs='*', default=['all'], required=False, help='Filter wordlists by category (default: %(default)s)')
    parser.add_argument('-n','--count', type=int, nargs='?', const='5', default=20, required=False, help='Number of passwords to generate (default: %(default)s)')
    args = parser.parse_args()

    print(args)
    log("Search for file in " + wordlistdir,9)

    os.chdir(wordlistdir)
    wordfiles=os.listdir()

    log("Found word list files:",9)
    log(wordfiles,3)

    wordlistcategory=args.category

    for wordfile in wordfiles:

        #Country filter
        CountryUseFile=False
        if wordfile.lower()[:2] == args.country.lower():
            CountryUseFile=True

        #Category filter
        CategoryUseFile=False
        for filter in wordlistcategory:
            if (filter.lower() == 'all'):
                CategoryUseFile=True
                continue
            elif wordfile.lower().find(filter.lower())>0:
                CategoryUseFile=True
                continue

        usefile=CountryUseFile and CategoryUseFile
        if (usefile):
            log("Search words in" + wordfile,9)
            ReadWordFile(wordlistdir, wordfile)
            numberwordfilesused+=1

    print("Done reading files")
    print("Statistics:")
    print("Category(ies): ", wordlistcategory)
    print("Files uses: " + numberwordfilesused.__str__())
    print("Nouns: " + wordsnoun.__len__().__str__())
    print("Verbs: " + wordsverb.__len__().__str__())
    print("Adjectivess: " + wordsadjective.__len__().__str__())

    if (numberwordfilesused>0):
        for i in range (0,args.count):
            s = GeneratePassword()
            e = CalculatePasswordEntropy(s)
    else:
        print("No word files found!")
