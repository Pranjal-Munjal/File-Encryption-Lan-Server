import socket               

s = socket.socket()         # Create a socket object
host = '0.0.0.0'    #private ip address of machine running fedora
port = 5006                
s.bind((host, port))       

s.listen(5)                
c, addr = s.accept()       
print('Got connection from', addr)    
while True:
   c.send(raw_input("Server please type: "))
   print("From Client: ", c.recv(1024))

c.close()