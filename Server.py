import socket
from datetime import datetime
import json

def InsertData(name,phone):
    data = {}  
    data['phone'] = []

    try:
        f = open("phonebook.txt", "r")
        data= json.load(f)
        f.close()
    except:
        print("no data on phone book")

    data['phone'].append({  
    'name': name,
    'notelp': phone
    })
    with open('phonebook.txt', 'w') as outfile:  
        json.dump(data, outfile)
    return('success')

def FindData(name):
    data = {}  
    data['phone'] = []
    try:
        f = open("phonebook.txt", "r")
        data= json.load(f)
        f.close()
        result = [x for x in data['phone'] if x["name"]== name]
        #print(result)
        return result[0]
    except:
        return "no data on phone book"

def ServerProgram():
    # take the server name and port name
    host = socket.gethostname()
    port = 5001

    # create a socket at server side
    # using TCP / IP protocol
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket with server
    # and port number
    s.bind(('', port))

    # allow maximum 1 connection to
    # the socket
    s.listen(5)

    # wait till a client accept
    # connection
    c, addr = s.accept()
    print('Connection from : ',addr)
    while True:
        dataFromClient = c.recv(1024)
        typeMenu = dataFromClient.decode()
        print(typeMenu)
        if typeMenu == "1":
            dataFromClient = c.recv(1024)
            name = dataFromClient.decode()
            result = FindData(name)
            result = str.encode(json.dumps(result))
            c.send(result)
        elif typeMenu == "2":
            dataFromClient = c.recv(1024)
            name = dataFromClient.decode()
            dataFromClient = c.recv(1024)
            notelp = dataFromClient.decode()

            result = InsertData(name,notelp)
            c.send(result.encode())
        else:
            break
        # else : 
        #     result = InsertData(name,phone)
        #     result = menu(typeMenu,name)
        #     c.send('Adding Success'.encode())

        # disconnect the server

    c.close()

if __name__ == '__main__':
    ServerProgram()