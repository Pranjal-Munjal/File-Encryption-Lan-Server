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

print("\n --------------------------------------------------------------------------- \n")
print("Welcome to Encrypted LAN Server settings menu")
print("enter the password of the server")
filepassword = input("password : ")

while(True):
    print("\n please select an option from the following")
    print("1. to add a new user")
    print("2. to delete a user")
    print("3. to list all the users")
    print("4. to change server password")
    print("5. to encrypt an existing file")
    print("6. to decrypt an existing file")
    print("7. to quit\n\n")

    choice = input("enter you choice here : ")

    if(choice == "1"):
        decrypt(getKey(filepassword), "usernames_passwords.txt.enc")
        os.remove("usernames_passwords.txt.enc")
        print("usernames and passwords file is decrypted\n")
        newuser = input("enter new username : ")
        newpass = input("enter new password : ")
        newuserpass = "\n" + newuser +" " + newpass + "$"
        with open("usernames_passwords.txt", "a+") as f:
            f.write(newuserpass)
        encrypt(getKey(filepassword), "usernames_passwords.txt")
        os.remove("usernames_passwords.txt")


    elif(choice == "2"):
        decrypt(getKey(filepassword), "usernames_passwords.txt.enc")
        os.remove("usernames_passwords.txt.enc")
        print("usernames and passwords file is decrypted\n")
        deluser = input("enter the username and password of the user you want to delete : ")
        with open("usernames_passwords.txt", "r") as f:
            lines = f.readlines()
        with open("usernames_passwords.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != (deluser + "$"):
                    f.write(line)
        encrypt(getKey(filepassword), "usernames_passwords.txt")
        os.remove("usernames_passwords.txt")

    elif(choice == "3"):
        decrypt(getKey(filepassword), "usernames_passwords.txt.enc")
        os.remove("usernames_passwords.txt.enc")
        print("usernames and passwords file is decrypted\n")
        with open("usernames_passwords.txt", "r") as f:
            for line in f:
                print(line,end='')
        encrypt(getKey(filepassword), "usernames_passwords.txt")
        os.remove("usernames_passwords.txt")
    elif(choice == "4"):
        decrypt(getKey(filepassword), "usernames_passwords.txt.enc")
        os.remove("usernames_passwords.txt.enc")
        filepassword2 = input("enter new password for the server : ")
        filepassword1 = input("confirm new password : ")
        if(filepassword1 == filepassword2):
            encrypt(getKey(filepassword1), "usernames_passwords.txt")
            os.remove("usernames_passwords.txt")

    elif(choice == "5"):
        filename = input("File to encrypt: ")
        password = input("Password: ")
        encrypt(getKey(password), filename)
        print("Done.")
        os.remove(filename)
    elif(choice == "6"):
        filename = input("File to decrypt: ")  
        password = input("Password: ")
        decrypt(getKey(password), filename)
        print("Done.")
        os.remove(filename)
