def readFiles(i):
    f = open(f'Input  text files\Text{i}.txt', "r")
    text=f.read().lower()
    p= open(f'PatternFiles\Pattern{i}.txt', "r")
    patt=p.read().lower()
    return text, patt

def callfun(i):
    text,pattern=readFiles(i)
    outputFile = open(f'Outputs/patternmatch{i}.output', "w")

    if '?' in pattern:
        result= QuestionKmpMatch(text,pattern)
    elif '$' in pattern:
        result=EndKmpMatch(text,pattern)
    elif '^' in pattern:
        result= StartKmpMatch(text,pattern)
    else:
        result= kmpMatch(text,pattern)

    if result:
        outputFile.write(str(len(result)) + " Match(es) Found!\n")
        for line, idx in result:
            outputFile.write("Line " + str(line) +
                             ", Index " + str(idx) + "\n")
    else:
        outputFile.write("No Match Found!\n")


def kmpPreProccess(pattern):
    m=len(pattern)
    preArr=[0]*m
    k=0
    for i in range(1 ,m):
        while k>0 and pattern[k+1]!=pattern[i] :
            k=preArr[k]
        if pattern[k+1]==pattern[i]:
            k=k+1
        preArr[i]=k
    return preArr


def kmpMatch(text, pattern):
    n=len(text)
    m=len(pattern)
    i=0
    q=0
    linenumber=1
    charIndex=0
    preArr=kmpPreProccess(pattern)
    matchingPositions=[]

    while i<n:
        if text[i]=='\n':
            linenumber+=1
            charIndex= i+1

        if pattern[q]== text[i]:
            i+=1
            q+=1
            if q==m:
                matchingPositions.append([linenumber,i-(q+charIndex)])
                q=preArr[q-1]

        else:
            if q!=0:
                q=preArr[q-1]
            else:
                i+=1
    return matchingPositions

def StartKmpMatch(text, pattern):
    n=len(text)
    pattern=pattern.replace(pattern[0],"",1)
    m=len(pattern)
    i=0
    q=0
    linenumber=1
    charIndex=0
    preArr=kmpPreProccess(pattern)
    matchingPositions=[]
    beginingOfWord=False

    while i<n:
        if text[i]=='\n':
            linenumber+=1
            charIndex= i+1

        if i-charIndex==0 or text[i-1]==" ":
            beginingOfWord=True

        if beginingOfWord:
            if pattern[q]== text[i]:
                i+=1
                q+=1
                if q==m:
                    matchingPositions.append([linenumber,i-(q+charIndex)])
                    q=preArr[q-1]

            else:
                if q!=0:
                    q=preArr[q-1]
                else:
                    i+=1

        else:
            i+=1
    return matchingPositions

def EndKmpMatch(text, pattern):
    n=len(text)
    pattern=pattern.replace(pattern[0],"",1)
    m=len(pattern)
    i=0
    q=0
    linenumber=1
    charIndex=0
    preArr=kmpPreProccess(pattern)
    matchingPositions=[]
    endOfWord=False

    while i<n:
        if text[i]=='\n':
            linenumber+=1
            charIndex= i+1

        if i+m<n and (text[i+m]=="\n" or text[i+m]==" "):
            endOfWord=True

        if endOfWord:
            if pattern[q]== text[i]:
                i+=1
                q+=1
                if q==m:
                    matchingPositions.append([linenumber,i-(q+charIndex)])
                    q=preArr[q-1]

            else:
                if q!=0:
                    q=preArr[q-1]
                else:
                    i+=1

        else:
            i+=1
    return matchingPositions

def QuestionKmpMatch(text, pattern):
    ptr1 = ""
    ptr2 = ""
    for i in pattern:
        if i != '?':
            ptr1 += i
            ptr2 += i
        else:
            ptr2 = ptr2[:-1]

    matchingPositions = kmpMatch(text, ptr1)
    for i in kmpMatch(text, ptr2):
        if i not in matchingPositions:
            matchingPositions.append(i)

    sortedmatchingPositions = sorted(matchingPositions, key=lambda x: (x[0], x[1]))

    return sortedmatchingPositions

#main

n=int(input("Enter number of text cases : "))
for i in range (1,n+1):
    callfun(i)
