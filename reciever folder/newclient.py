import socket
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import os

print("-----------------------------------------------------")
print("WELCOME TO SECURE SERVER")
print("Please enter...")
username = input("Username : ")
password = input("Password : ")
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = input("Please enter the IP address of the server : ")
port = 8888
s.connect((host,port))
print("Connecting to the server...")
s.send(username.encode())
s.send(password.encode())


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

result_ENC = s.recv(1024)
result = result_ENC.decode()
if(result == "True"):
    while(True):
        print("select option")
        print("1. to download the file from server")
        print("2. to upload the file to server")
        print("3. to list the files on the server")
        print("4. to quit")
        option = input("Your Choice : ")
        s.send(option.encode())
        if(option == '1'):
            filename = input("Please enter a filename for the incoming file : ")
            s.send(filename.encode())
            file = open(filename, 'wb')
            file_data = s.recv(1024)
            file.write(file_data)
            file.close()
            print("File has been received successfully.")
            print("attempting to decrypt")
            password2 = input("Password: ")
            decrypt(getKey(password2), filename)
            os.remove(filename)
            print("file is downloaded and decrypted sucessfully")
        elif(option == '2'):
            #encryption here
            filename = input("Please enter a filename for the outgoing file : ")
            password2 = input("Enter the Password to encrypt it with : ")
            encrypt(getKey(password2), filename)
            print("Encryption done, uploading to the server")
            truefilename = filename+".enc"
            s.send(truefilename.encode())
            file = open(truefilename , 'rb')
            file_data = file.read(1024)
            s.send(file_data)
            print("Data has been transmitted successfully")
            file.close()
            os.remove(filename)
            decrypt(getKey(password), "filespasswords.txt.enc")
            os.remove("filespasswords.txt.enc")
            with open ("filespasswords.txt", "a+") as f:
                f.write(filename + " " + password2)
            encrypt(getKey(password), "filespasswords.txt")
            os.remove("filespasswords.txt")
        elif(option == '3'):
            print("listing files :\n")
            encfile = s.recv(1024)
            files = encfile.decode()
            print(files)
        elif(option == '4'):
            print("exiting")
            break

else:
    print("incorrect username or password")