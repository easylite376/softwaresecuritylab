#!/usr/local/bin/python3

import argparse,string
from urllib.request import urlopen
from urllib.error import HTTPError
from itertools import combinations

SUBFOLDER = ['backup']

def searchFiles(url,filenameList):
    availUrls = list()
    filenameListLength = len(filenameList)
    lastProgress = 0
    counter = 0
    print("Progress in %: ")
    if (url[-1:] == "/"):
        url = url[:-1]
    for filename in filenameList:
        counter += 1
        lastProgress = displayProgress(int(counter*100/filenameListLength),lastProgress)
        urlWithoutDir = "/".join([url,filename])
        if (isPresentOnServer(urlWithoutDir)):
            availUrls.append(urlWithoutDir)
        for directory in SUBFOLDER:
            urlWithDir = "/".join([url,directory,filename])
            if (isPresentOnServer(urlWithDir)):
                availUrls.append(urlWithDir)
    print()
    createReport(availUrls)

def isPresentOnServer(url):
    try:
        return urlopen(url).getcode() == 200
    except HTTPError:
        return False

def createReport(reachableUrls):
    print("-------------------------------------------------")
    if (len(reachableUrls) != 0):
        print("The following urls are reachable on the webserver")
        print("-------------------------------------------------")
        for url in reachableUrls:
            print(url)
    else:
        print("Your webserver is save!")

def createAllPossibleStrings(combinationLength):
    alphabet = list(string.ascii_lowercase)
    combinationList = list()
    extensions = [".cf",".txt",".conf",".bak",".conf.bak",".sql",".data"]
    for combinationTuple in combinations(alphabet,combinationLength):
        for extension in extensions:
            combinationList.append("".join(str(tupleElement) for tupleElement in combinationTuple) + extension)    
    return combinationList

def displayProgress(actualProgress,lastProgress):
    if actualProgress != lastProgress:
        lastProgress = actualProgress
        print(str(lastProgress) + " ",end="",flush=True)
    return lastProgress

parser = argparse.ArgumentParser()
parser.add_argument("url",help="Url you want to test")
parser.add_argument("-i", dest="file" ,help="Wordlist")
parser.add_argument("-bruteforce",dest='bruteforce', action='store_true',
                    help="Bruteforces the potential filenames")
args = parser.parse_args()
if args.file:
    print("i turned on",args.file)
    f = open("test.txt","r")
    filenameList = f.read().split()
    f.close()
if args.bruteforce:
    print("bruteforce turned on", args.bruteforce)
    filenameList = createAllPossibleStrings(2)
    # TODO Remove testfiles
    filenameList.append("password.txt")
    filenameList.append("config.txt")
if args.file or args.bruteforce:
    searchFiles(args.url,filenameList)