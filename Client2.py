import socket
import json

def MenuType():
    print('1. Find a Phone Book')
    print('2. Add Phone Number to a Phone Book')
    print('3. Exit')

def client_program(data):
    result=[]
    # take the server name and port name
    host = 'local host'
    port = 2004

    # create a socket at client side
    # using TCP / IP protocol
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # connect it to server and port number on local computer.
    s.connect(('127.0.0.1', port))

    while data != "3":
        s.send(str.encode(data))
        if data == "1":
            data= input("Name : ")
            s.send(str.encode(data))
            msg = s.recv(1024)
            msg = msg.decode()
            result = json.loads(msg)
            try:
                name = result['name']
                phone = result['phonenumber']
                print('Name : ' , name)
                print('Phone Number : ', phone)
            except:
                print('Data Not Found')
        elif data == "2":  
            nama= input("Input Name : ")
            s.send(nama.encode())
            notelp= input("Input Phone No : ")
            s.send(notelp.encode())
            msg = s.recv(1024)        
            print('Status : ' + msg.decode()) 
        elif data == "3":
            break
        data= input("Choose Menu (1/2/3): ")
    s.close()

if __name__ == '__main__':
    MenuType()
    data= input("Choose Menu (1/2/3) : ")
    client_program(data)
