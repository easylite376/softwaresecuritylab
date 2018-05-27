#!/usr/local/bin/python3

import argparse
from urllib.request import urlopen
from urllib.error import HTTPError

SUBFOLDER = ['backup']

def searchFiles(url,filenameList):
    presentFiles = list()
    if (url[-1:] == "/"):
        url = url[:-1]
    for filename in filenameList:
        urlWithoutDir = "/".join([url,filename])
        if (isPresentOnServer(urlWithoutDir)):
            presentFiles.append(urlWithoutDir)
        for dir in SUBFOLDER:
            urlWithDir = "/".join([url,dir,filename])
            if (isPresentOnServer(urlWithDir)):
                presentFiles.append(urlWithDir)
    print(presentFiles)

def isPresentOnServer(url):
    try:
        return urlopen(url).getcode() == 200
    except HTTPError:
        return False

parser = argparse.ArgumentParser()
parser.add_argument("url",help="Url you want to test")
parser.add_argument("-i", dest="file" ,help="Wordlist")
parser.add_argument("-bruteforce",dest='bruteforce', action='store_true', help="Bruteforces the potential filenames")
args = parser.parse_args()
if args.file:
    print("i turned on",args.file)
    f = open("test.txt","r")
    filenameList = f.read().split()
    f.close()
if args.bruteforce:
    print("brutefoce turned on", args.bruteforce)

searchFiles(args.url,filenameList)

if args.url:
    print("url=",args.url)
