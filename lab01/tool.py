#!/usr/bin/python3

import argparse,urllib

SUBFOLDER = ['backup']

def searchFiles(url,filenameList):
    for filename in filenameList:
        #requestUrl("/".join([url,filename])
        for dir in SUBFOLDER:
            seq = "/".join([url,dir,filename])
            #requestUrl(seq)
            print(seq)

#def requestUrl(url):


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
