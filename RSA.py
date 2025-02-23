#Uses the Euclidean algorithm to find the greatest common divisor of a and b
def gcd(a,b):          
    if (b == 0):
        return abs(a)
    else:
        return gcd(b, a % b)
    
#Uses the extended Euclidean algorithm to find the greatest common divisor of and b
#as well as values x and y such that ax + by = gcd(a,b)
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1  
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1-(b//a)*x1
    y = x1
    return gcd, x, y

#Finds the modular inverse
def modular_inverse(e, nt):
    gcd,x,y = extended_gcd(e, nt)
    if gcd != 1:
        print("No modular inverse")
    else:
        return x % nt

#Gets a value for e from the user or generates one
def find_e(nt):
    valid = False
    while valid == False:
        inp = input("Would you like to choose the value for e? (y/n) ")
        if inp.lower() in ["y","n"]:
            valid = True
        else:
            print("Input must be 'y' or 'n'")
            
    if inp.lower() == "n":        
        for e in range(nt, 1, -1):    #Finds greatest integer e that is coprime with nt
            if gcd(nt, e) == 1:
                break
    else:
        valid = False
        while valid == False:
            try:
                e = int(input("Enter your value for e: "))
                if gcd(nt,e) == 1:
                    valid = True
                else:
                    print("Invalid value for e")
            except:
                print("e must be an integer value")
    return e

#Returns d as the modular inverse of e and the totient of n
def find_d(e,nt):
    return modular_inverse(e,nt)

#Returns the values necessary for encryption/decryption
def get_values():
    valid = False
    while valid == False:
        try:
            p = int(input("enter value for p\n"))
            q = int(input("enter value for q\n"))
            valid = True
        except:
            print("Value must be an integer")
    n = p*q
    nt = (p-1)*(q-1)
    e = find_e(nt)
    d = find_d(e, nt)
    
    return n,nt,e,d

#Takes in an input from the user, splits it and stores each character in an array
def split_message():
    array = []
    string = str(input("enter your message\n"))
    print("\n")
    for char in string:
        array.append(char)
    return array

#Loops for each character in the array, encrypts the integer representing it and appends it to an arry
def encrypt_message(array, e, n):
    eArray = []
    for char in array:
        eArray.append((ord(char)**e) % n)
    return eArray

#Loops for each integer in the array, decrypts it and appends the associated unicode to an array
def decrypt_message(array, d, n):
    dArray = []
    for char in array:
        dArray.append(chr((char**d) % n))
    return dArray

#Prints the charcters in the array
def print_message(prefix, array):
    message = ""
    for char in array:
        message += str(char)
    print(prefix,message)

#Loops for each character in the array and appends the integer representing it to another array
def integer_message(array):
    iArray = []
    for char in array:
        iArray.append(ord(char))
    return iArray

#Loops for each integer in the array and appends the unicode it represents to another array
def unicode_message(array):
    uArray = []
    for char in array:
        uArray.append(chr(char))
    return uArray

n,nt,e,d = get_values()

message = split_message()
print_message("Your message: ", message)

iMessage = integer_message(message)
print_message("Integer message: ", iMessage)


eMessage = encrypt_message(message,e,n)
print_message("Integer encrypted message: ",eMessage)

ueMessage = unicode_message(eMessage)
print_message("Encrypted message: ",ueMessage)
 
dMessage = decrypt_message(eMessage,d,n)
idMessage = integer_message(dMessage)

print_message("Integer decrypted message: ",idMessage)

print_message("Decrypted message: ",dMessage)