#Joshua Hernandez

# This function inverts the bytes
def invert_bytes(data: bytes) -> bytes:
    return bytes(b ^ 0xFF for b in data)
     
# Encryption code            
def Encrypt():
    #link (https://stackoverflow.com/questions/18815820/how-to-convert-string-to-binary)
    rawCrypt = str(input("Type in code to encrypt: ")).encode('ascii')
    encrypted = invert_bytes(rawCrypt)
    # Write to a file
    with open("crypt.bin", "wb") as file:
        file.write(encrypted)
    print(f"Encryption written to crypt.txt {encrypted}\n")
    
# Decryption code    
def Decrypt():
    x = bytes
    #Opens file and reads
    with open("crypt.bin", "rb") as file:
        x = file.read()
    y = invert_bytes(x)
    rawCrypt = y.decode('ascii')
    print(f"The Decrypted code is {rawCrypt}\n")

#Menu options switch
menu_options = {
    1: Encrypt,
    2: Decrypt,
    3: exit
}    
    
#selecting an option
while True:
    #menu
    print("Menu\n1) Encrypt\n2) Decrypt\n3) Exit\n")
    try:
        #inner function
        def InvalidOption():
            print("You have inputed an invalid option!")
        #get user input and go through switch statement
        userInput = int(input("Input an integer to select an option: "))
        menu_options.get(userInput, InvalidOption)()
    #Error Checking    
    except ValueError as e:
        print(e)
            
