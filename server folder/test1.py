import socket              

s = socket.socket()        
host = '146.196.34.6' 
port = 5001               

s.connect((host, port))
while True: 
    try:
        print("From Server: ", s.recv(1024)) 
        s.send(raw_input("Client please type: "))
    except:
        break
s.close()
