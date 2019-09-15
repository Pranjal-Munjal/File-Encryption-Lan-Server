from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import os

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

while(True):
    print("\n --------------------------------------------------------------------------- \n")
    print("Welcome to Secure Server client settings menu")
    print("please select an option from the following")
    print("1. to add a new user")
    print("2. to view saved files passwords")
    print("3. to delete this user's saved passwords")
    print("4. to quit")
    option = input("you choice : ")
    if(option == "1"):
        print("enter your new password associated with you username on the server")
        password = input("password : ")
        with open ("filespasswords.txt", "a+") as f:
            print("file created")
        encrypt(getKey(password), "filespasswords.txt")
        os.remove("filespasswords.txt")
    elif(option == "2"):
        print("enter your new password associated with you username on the server")
        password = input("password : ")
        decrypt(getKey(password), "filespasswords.txt.enc")
        os.remove("filespasswords.txt.enc")
        print("usernames and passwords file is decrypted\n")
        with open("filespasswords.txt", "r") as f:
            for line in f:
                print(line,end='')
        encrypt(getKey(password), "filespasswords.txt")
        os.remove("filespasswords.txt")
    elif(option == "3"):
        print("enter your new password associated with you username on the server")
        password = input("password : ")
        decrypt(getKey(password), "filespasswords.txt.enc")
        os.remove("filespasswords.txt.enc")
        os.remove("filespasswords.txt")
    elif(option == "4"):
        break