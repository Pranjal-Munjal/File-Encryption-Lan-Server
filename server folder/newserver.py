import socket
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import os
import netifaces as ni

def encrypt(key, filename):
	chunksize = 64*1024
	outputFile = filename+".enc"
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = Random.new().read(16)

	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, 'rb') as infile:
		with open(outputFile, 'wb') as outfile:
			outfile.write(filesize.encode('utf-8'))
			outfile.write(IV)
			
			while True:
				chunk = infile.read(chunksize)
				
				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += b' ' * (16 - (len(chunk) % 16))

				outfile.write(encryptor.encrypt(chunk))


def decrypt(key, filename):
	chunksize = 64*1024
	outputFile = filename[:-4]
	
	with open(filename, 'rb') as infile:
		filesize = int(infile.read(16))
		IV = infile.read(16)

		decryptor = AES.new(key, AES.MODE_CBC, IV)

		with open(outputFile, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))
			outfile.truncate(filesize)


def getKey(password):
	hasher = SHA256.new(password.encode('utf-8'))
	return hasher.digest()
ni.ifaddresses("wlan0")
hostip = ni.ifaddresses("wlan0")[ni.AF_INET][0]["addr"]

serverpass = input("Enter the password of the server to start the server : ")

#estamblishing connection
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = 8888
s.bind((hostip,port))
s.listen(1) #only 1 client at a time
while(True):
    print("the IP address of the server is : " + hostip)
    print("Waiting for new incoming connection ... ")
    conn, addr = s.accept()
    print(addr, "is trying to connect to the server")
    #authentication test
    username_ENC = conn.recv(1024)
    password_ENC = conn.recv(1024)
    username = username_ENC.decode()
    password = password_ENC.decode()
    loggedin = "False"
    user_pass = username + " " + password
    decrypt(getKey(serverpass), "usernames_passwords.txt.enc")
    os.remove("usernames_passwords.txt.enc")
    with open ("usernames_passwords.txt", "r") as f:
        for line in f:
            head, sep, tail = line.partition("$")
            if(head == user_pass):
                print(addr, " has logged into the server\n")
                loggedin = "True"
    encrypt(getKey(serverpass), "usernames_passwords.txt")
    os.remove("usernames_passwords.txt")
    conn.send(loggedin.encode())
    if(loggedin == "True"):
        print("Authentication successful connecting to ",addr)
        while(True):
            #communicating with client
            option_ENC = conn.recv(1024)
            option = option_ENC.decode()
            if(option == '1'):
                print("sending mode")
                fl = conn.recv(1024)
                filename = fl.decode()
                file = open("/root/Desktop/EncFileServer/EncFileServer/DATA/" + filename , 'rb')
                file_data = file.read(1024)
                conn.send(file_data)
                print("Data has been transmitted successfully")
                file.close()
            elif(option == '2'):
                print("recieving mode")
                fl = conn.recv(1024)
                filename = fl.decode()
                file = open("/root/Desktop/EncFileServer/EncFileServer/DATA/" + filename, 'wb')
                file_data = conn.recv(1024)
                file.write(file_data)
                file.close()
                print("File has been received successfully.")
            elif(option == '3'):
                files = os.listdir("/root/Desktop/EncFileServer/EncFileServer/DATA")
                filestr = '\n'.join(files)
                conn.send(filestr.encode())
            elif(option == '4'):
                print("terminating connection with", addr)
                break
    elif(loggedin == False):
        print("request denied because of wring username and password")
        break
