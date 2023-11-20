filename = "data new.txt"
inputFile = open(filename, "r")
file=input("Enter the file name:")

fileInput = inputFile.readlines()
f=open("data new.txt","r")
for x in f:
    print (x)


for line in inputFile.readlines():

    lname, hours, wage =line.split()
    hours = int(hours)
    wage = float(wage)
    totalPay = hours * wage
    print('%-15s%-10d%-10.2f'% (name, hours, total))

    f.close()





