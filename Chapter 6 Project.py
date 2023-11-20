def issorted (inputList):
    if len (inputList)<2:
        return True
    for i in range(len(inputList)-1):
        if inputList [i] > inputList[i+1]:
            return False
        return True

    def main():
        lyst=[]
        print(issorted(lyst))
        lyst=[1]
        lyst= list(range(10))
        print(issorted(lyst))
        lyst [9]=3











