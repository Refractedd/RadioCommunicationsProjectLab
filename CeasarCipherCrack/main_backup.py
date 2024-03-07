#
# Adapted from Robert Eisele https://www.xarg.org/2010/05/cracking-a-caesar-cipher/
#
import time

from icecream import ic
import numpy as np
from scipy.spatial.distance import cdist

ic.disable()

msg = "Caesar's Cipher couldn't prevent his homies stabbing him."
msg2 = "alot longer text is more likely"
msg3 = "UNDECIPHERABLE CODEWORD"
word = 'hello'
w2 = 'goodbye'
w3 = 'Caeser Cipher'
together = 'hello goodbye Caesar Cipher'


def caesar(string, key):
    key = int(key)
    if key > 26:
        key = key % 26
    elif key < 0:
        key = 26 + key
    encrypt = ''
    for j in range(len(string)):
        c = ord(string[j])
        if 97 <= c < 123:
            encrypt += chr((c + key + 7) % 26 + 97)  # lowecase
        elif 65 <= c < 91:
            encrypt += chr((c + key + 13) % 26 + 65)  # uppercase
        else:
            encrypt += string[j]
    return encrypt


def crack_cipher(string):
    maxi = 0
    weight = np.array([6.51, 1.89, 3.06, 5.08, 17.4,
                       1.66, 3.01, 4.76, 7.55, 0.27,
                       1.21, 3.44, 2.53, 9.78, 2.51,
                       0.29, 0.02, 7.00, 7.27, 6.15,
                       4.35, 0.67, 1.89, 0.03, 0.04, 1.13])

    c = np.zeros(26)
    s = np.zeros(26)

    for i in range(len(string)):
        x = (ord(string[i]) | 32) - 97
        if 0 <= x < 26: c[x] += 1

    for off in range(26):
        for i in range(26):
            s[off] += 0.01 * c[i] * weight[(i + off) % 26]
            if maxi < s[off]: maxi = s[off]

    ind = int(np.where(s == maxi)[0])
    dKey = (26 - ind) % 26

    return dKey, caesar(string, ind)

key = np.random.randint(0, 26)
ic(key)
cipher1 = caesar(word, key)
cipher2 = caesar(w2, key)
cipher3 = caesar(w2, key)
cipher4 = caesar(together, key)
ic(cipher1)
ic(crack_cipher(cipher1))
ic(crack_cipher(cipher2))
ic(crack_cipher(cipher3))
ic(crack_cipher(cipher4))
Message = ''
Key = ''
CipheredMsg = ''
DecipheredMsg = ''

while True:
    print(f"Message: {Message}")
    print(f"Key : {Key}")
    print(f"CipheredMessage : {CipheredMsg}")
    print(f"DecipheredMessage : {DecipheredMsg}\n")
    print("1. Cipher a new input Message.")
    print("2. Enter New Key.")
    print("3. Crack Current Ciphered Message.")

    option = int(input("Choose an option: "))

    if option == 1:
        Message = input("Enter your message: ")
        Key = int(input("Enter your key: "))
        if Key > 26: print(f"Key effectively = {Key % 26}\n")
        CipheredMsg = caesar(Message, Key)
        print(f"Cipher: {CipheredMsg}\n")
    elif option == 2:
        Key = input("Enter your key: ")
        CipheredMsg = caesar(Message, Key)
    elif option == 3:
        if CipheredMsg != '':
            Key, DecipheredMsg = crack_cipher(CipheredMsg)
            print(f"Your message was: {DecipheredMsg}")
            print(f"Encrypting using the Key: {Key}\n")
        else:
            print("First enter a message using option 1.\n")








#R1 = np.vstack((c, s)).T
    #R2 = np.vstack((s, weight)).T
    #ic(R1, R2)
    #dist = cdist(R1, R2).argmax()
    #ic((26 - dist) % 26)
    #ic(dist)

# Look for single letter like a and i to instantly decipher
# 5 and 1/2 sec breaths