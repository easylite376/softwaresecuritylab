#!/usr/local/bin/python3
from time import sleep
import threading
import re
import urllib.error
import argparse,string
from urllib.request import urlopen
from urllib.error import HTTPError
from itertools import permutations
from permutations import create_str_bf 

URL = ""
RES=[]
THREADS=[]
slowdown_t = 0
SUBFOLDER = ['backup','data','config','docs']

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
            except urllib.error.URLError:
                break;
            except:
                sleep(1)
                raise
                print("Server overloaded. Please add slowdown higher than " + str(slowdown_t))

def searchFiles(filenameList):
    filenameListLength = len(filenameList)
    lastProgress = 0
    counter = 0
    print("Progress in %: ")
    while(filenameListLength > counter):
        while(threading.activeCount() < 300 and filenameListLength > counter):
            lastProgress = displayProgress(int(counter*100/filenameListLength),lastProgress)
            urlWithoutDir = "/".join([URL,filenameList[counter]])
            sleep(slowdown_t)
            try:
                THREADS.append(myThread(urlWithoutDir))
                THREADS[-1].start()
            except:
                sleep(1);
                THREADS[-1].start()
            for directory in SUBFOLDER:
                urlWithDir = "/".join([URL,directory,filenameList[counter]])
                try:
                    THREADS.append(myThread(urlWithDir))
                    THREADS[-1].start()
                except:
                    sleep(1);
                    THREADS[-1].start()
            counter += 1
        while (threading.activeCount()>100 and filenameListLength > counter):
            for t in THREADS:
                t.join(0.01)
                if not t.is_alive():
                    THREADS.remove(t);
    
    while (threading.activeCount()>1):
        for t in THREADS:
            t.join(0.1)
            if not t.is_alive():
                THREADS.remove(t);
    print()
    createReport()

def searchFile(filename):
    while (threading.activeCount()>500):
        for t in THREADS:
            t.join(0.01)
            if not t.is_alive():
                THREADS.remove(t);
    urlWithoutDir = "/".join([URL,filename])
    sleep(slowdown_t)
    try:
        THREADS.append(myThread(urlWithoutDir))
        THREADS[-1].start()
    except:
        sleep(1);
        THREADS[-1].start()
    for directory in SUBFOLDER:
        urlWithDir = "/".join([URL,directory,filename])
        try:
            THREADS.append(myThread(urlWithDir))
            THREADS[-1].start()
        except:
            sleep(1);
            THREADS[-1].start()

def isPresentOnServer(url):
    try:
        return urlopen(url).getcode() == 200
    except HTTPError:
        return False

def createReport():
    print("-------------------------------------------------")
    if (len(RES) != 0):
        print("The following urls are reachable on the webserver")
        print("-------------------------------------------------")
        for url in RES:
            print(url)
    else:
        print("Your webserver is save!")

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
parser.add_argument("-bflen",dest='bflen',help="Bruteforces length",type=int,default=3)
parser.add_argument("-t",dest="slowdown",help="slowdown factor in seconds, default=0.01",default=0.01,type=float)
args = parser.parse_args()
slowdown_t = args.slowdown
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

if re.match(regex, args.url) is None:
    print("Not a valid URL")
    parser.print_help()
    exit(1)
if (args.url[-1:] == "/"):
    URL = args.url[:-1]
else:
    URL = args.url
try:
    urlopen(URL).getcode();
except urllib.error.URLError:
    print("Baseurl returns Connection refused")
    parser.print_help()
    exit(1)
except:
    pass
if args.file:
    f = open(args.file,"r")
    filenameList = f.read().split()
    f.close()
    searchFiles(filenameList)
elif args.bruteforce:
    print("bruteforce turned on", args.bruteforce)
    print("length for Bruteforce is ", args.bflen)
    #filenameList = createAllPossibleStrings(2)
    # TODO Remove testfiles
    #filenameList.append("password.txt")
    #filenameList.append("config.txt")
    #print(len(filenameList))
    #searchFiles(args.url,filenameList)
    create_str_bf(searchFile,args.bflen) 
    while (threading.activeCount()>1):
        for t in THREADS:
            t.join(0.1)
            if not t.is_alive():
                THREADS.remove(t);
    createReport()
else:
    print("You have to use -i or -bruteforce");
    parser.print_help()
