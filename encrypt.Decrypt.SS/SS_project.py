from binascii import hexlify , unhexlify
from scipy.interpolate import lagrange
import numpy as np
from numpy.polynomial.polynomial import Polynomial
import base64
from cryptography.fernet import Fernet
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#create password
k = os.urandom(5)
password = hexlify(k)
key = ''
threshold = 3

#Encryption Function
def enc():
    datafile = open('c.png', 'rb')
    data = datafile.read()
    u = Fernet(GenerateEncryptionKey(password))
    x = u.encrypt(data)
    cipher = open('encdata.txt' , 'wb')
    cipher.write(x)
    datafile.close()
    cipher.close()

#Decryption Function
def dec():
    cipherfile = open('encdata.txt', 'rb')
    cipher = cipherfile.read()
    rkey =  reconstruct()
    u = Fernet(rkey)
    x = u.decrypt(cipher)
    data = open('Newc.png' , 'wb')
    data.write(x)
    print("     - DONE !!! ")
    cipherfile.close()
    data.close()

#Reconstruct password from shares function
def reconstruct ():
    global threshold
    #get X & Y vlues
    intryx = []
    intryy = []
    for q in range(threshold):
        v = int(input('Share Numper - '))
        intryx.append(v)
        k = int(input('Share value - '))
        intryy.append(k)

    #reconstruct
    x = np.array(intryx)
    y = np.array(intryy)
    p = lagrange(x,y)
    p = Polynomial(p).coef
    f = int(p[-1])
    j = hex(f)
    rpassword = bytes(j[2:],'utf-8')
    return GenerateEncryptionKey(rpassword)

#create encryption key from password
def GenerateEncryptionKey (s):
    global key
    salt = b'\x9e\x8d\xdf\x0f\x9bb\xc6\xda&ya\xd3uK\x9a\xfd'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode((kdf.derive(s)))
    return key


print("password :",int(password.decode(),16))

#create a Secret
secret = int(password.decode(),16)

#create shares & threshold
nshares = int(input("Numper of Shares : "))
threshold = int(input("thershold : "))
while threshold > nshares:
    print('Threshold Cant be greater than Number of Shares !!! ')
    nshares = int(input("Numper of Shares : "))
    threshold = int(input("thershold : "))


shares = {}
for i in range(nshares):
    index = i+1
    share = secret + (166*index) + (94*(pow(index,2)))
    shares.update({index:share})

#printing Shares
for k,v in shares.items():
    print(k,v)

i = 0
while i < 1:
    print('Do You Want To :')
    print('     1. Encrypt File')
    print('     2. Decrypt File')
    print('     3. Close The Program')
    choice = input('- ')
    if choice == '1':
        enc()
    elif choice == '2':
        dec()
    elif choice == '3':
        print('Thank You & come back soon ')
        i = 2
