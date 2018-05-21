#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url",help="Url you want to test")
parser.add_argument("-i", dest="file" ,help="Wordlist")
parser.add_argument("-bruteforce",dest='bruteforce', action='store_true', help="Bruteforces the potential filenames")
args = parser.parse_args()
if args.file:
    print("i turned on",args.file)
    f = open("test.txt","r")
    for fileName in f.read().split():
        print(fileName)
    f.close()
if args.bruteforce:
    print("brutefoce turned on", args.bruteforce)

if args.url:
    print("url=",args.url)
