#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", dest="file" ,help="Wordlist")
parser.add_argument("-bruteforce",dest='bruteforce', action='store_true', help="Bruteforces the potential filenames")
args = parser.parse_args()
if args.file:
    print("i turned on",args.file)
if args.bruteforce:
    print("brutefoce turned on", args.bruteforce)
