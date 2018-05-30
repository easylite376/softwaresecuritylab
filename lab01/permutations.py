import string

def create_str_bf(cb,n):
    alphabet = list(string.ascii_lowercase)
    combinationList = list()
    extensions = [".cf",".txt",".conf",".bak",".conf.bak",".sql",".data"]
    for i in range(1,n+1):
        create_str_fixedlen(cb,i)        

def create_filename(cb,string):
    extensions = [".cf",".txt",".conf",".bak",".conf.bak",".sql",".data"]
    for i in extensions:
        cb(string+i)

def create_str_fixedlen(cb,n):
    alphabet = list(string.ascii_lowercase)
    filename = list(alphabet[0]*n)
    flag=False
    iI=0
    aI=0
    while (iI>-1):
        create_filename(cb,''.join(filename))
        iI=n-1
        while (iI>=0):
            aI=alphabet.index(filename[iI])
            if (aI>=len(alphabet)-1):
                if (iI >0):
                    filename[iI]=alphabet[0]
                iI-=1
            else:
                filename[iI]=alphabet[aI+1]
                break
