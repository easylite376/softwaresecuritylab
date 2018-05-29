#!/usr/local/bin/python3
from time import sleep
import threading
import argparse,string
from urllib.request import urlopen
from urllib.error import HTTPError
from itertools import permutations

RES=[]
slowdown_t = 0
SUBFOLDER = ['backup']

class myThread (threading.Thread):
    def __init__(self,  url):
        threading.Thread.__init__(self)
        self.url=url
    def run(self):
        while(True):
            try:
                if (urlopen(self.url).getcode() == 200):
                    RES.append(self.url);
                break;
            except HTTPError:
                break;
            except:
                sleep(1)
                raise

def searchFiles(url,filenameList):
    availUrls = list()
    filenameListLength = len(filenameList)
    lastProgress = 0
    counter = 0
    threads=[]
    print("Progress in %: ")
    if (url[-1:] == "/"):
        url = url[:-1]
    while(filenameListLength > counter):
        while(threading.activeCount() < 300 and filenameListLength > counter):
            lastProgress = displayProgress(int(counter*100/filenameListLength),lastProgress)
            urlWithoutDir = "/".join([url,filenameList[counter]])
            sleep(slowdown_t)
            try:
                threads.append(myThread(urlWithoutDir))
                threads[-1].start()
            except:
                sleep(1);
                threads[-1].start()
            for directory in SUBFOLDER:
                urlWithDir = "/".join([url,directory,filenameList[counter]])
            try:
                threads.append(myThread(urlWithDir))
                threads[-1].start()
            except:
                sleep(1);
                threads[-1].start()
            counter += 1
        while (threading.activeCount()>100 and filenameListLength > counter):
            for t in threads:
                t.join(0.01)
                if not t.is_alive():
                    threads.remove(t);
    
    while (threading.activeCount()>1):
        for t in threads:
            t.join(0.1)
            if not t.is_alive():
                threads.remove(t);
    print()
    createReport(availUrls)

def isPresentOnServer(url):
    try:
        return urlopen(url).getcode() == 200
    except HTTPError:
        return False

def createReport(reachableUrls):
    print("-------------------------------------------------")
    if (len(RES) != 0):
        print("The following urls are reachable on the webserver")
        print("-------------------------------------------------")
        for url in RES:
            print(url)
    else:
        print("Your webserver is save!")

def createAllPossibleStrings(combinationLength):
    alphabet = list(string.ascii_lowercase)
    combinationList = list()
    extensions = [".cf",".txt",".conf",".bak",".conf.bak",".sql",".data"]
    for combinationTuple in permutations(alphabet,combinationLength):
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
parser.add_argument("-t",dest="slowdown",help="slowdown factor in seconds, default=0.01",default=0.01,type=float)
args = parser.parse_args()
if args.file:
    print("i turned on",args.file)
    f = open("test.txt","r")
    filenameList = f.read().split()
    f.close()
if args.bruteforce:
    print("bruteforce turned on", args.bruteforce)
    filenameList = createAllPossibleStrings(4)
    # TODO Remove testfiles
    filenameList.append("password.txt")
    filenameList.append("config.txt")
    print(len(filenameList))
slowdown_t = args.slowdown
if args.file or args.bruteforce:
    searchFiles(args.url,filenameList)
