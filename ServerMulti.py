import socket
import os
from _thread import *
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
    'phonenumber': phone
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

ServerSideSocket = socket.socket()
host =  socket.gethostname()
port = 2004
ThreadCount = 0

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
ServerSideSocket.listen(5)

def multi_threaded_client(c):
    while True:
        # data = c.recv(2048)
        # response = 'Server message: ' + data.decode('utf-8')
        dataFromClient = c.recv(2048)
        typeMenu = dataFromClient.decode('utf-8')
        if typeMenu == "1":
            print('Finding Data')
            dataFromClient = c.recv(2048)
            name = dataFromClient.decode('utf-8')
            result = FindData(name)
            result = str.encode(json.dumps(result))
            c.send(result)
        elif typeMenu == "2":
            print('Inserting Data')
            dataFromClient = c.recv(2048)
            name = dataFromClient.decode('utf-8')
            dataFromClient = c.recv(2048)
            notelp = dataFromClient.decode('utf-8')
            result = InsertData(name,notelp)
            c.send(result.encode())
        if not dataFromClient:
            break
        # connection.sendall(str.encode(response))
    c.close()
while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    # print('Thread Number: ' + str(ThreadCount))
    
ServerSideSocket.close()