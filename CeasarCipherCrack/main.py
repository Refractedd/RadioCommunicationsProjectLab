#
# Adapted from Robert Eisele https://www.xarg.org/2010/05/cracking-a-caesar-cipher/
#
import numpy as np
from JuliusCaesar import JuliusCaesar
from RomanSenate import RomanSenate

exampleMsg = 'Julius Caesar was stabbed 23 times by his own Roman Senate'

Caesar = JuliusCaesar()
Senate = RomanSenate()
Caesar.setKey(np.random.randint(1, 26))
Caesar.CaesarCipher(exampleMsg, Caesar.Key)
Senate.bloodyMurder(Caesar.CipheredMsg)

print("Initial Example: \n"
      "Message = 'Julius Caesar was stabbed 23 times by his own Roman Senate'\n"
      f"Using random key : {Caesar.Key}\n"
      f"Ciphered Message : {Caesar.CipheredMsg}\n"
      f"Deciphered Message : {Senate.DecipheredMsg}\n"
      f"Guessed Key : {Senate.guessKey}")

Message = ''
Key = 0
GuessedKey = 0
CipheredMsg = ''
DecipheredMsg = ''

while True:
    print(f"\nMessage: {Message}")
    print(f"Key : {Key}")
    print(f"CipheredMessage : {CipheredMsg}")
    print(f"DecipheredMessage : {DecipheredMsg}")
    print(f"Guessed Key : {GuessedKey}\n")
    print("1. Cipher a new input Message.")
    print("2. Enter New Key.")
    print("3. Crack Current Ciphered Message.\n")

    option = input("Choose an option: ")
    if option == '1' or option == '2' or option == '3':
        option = int(option)

        if option == 1:
            Caesar.setMessage(input("Enter your message: "))
            Message = Caesar.Message

            Caesar.setKey(input("Enter your key: "))
            Key = Caesar.Key

            Caesar.CaesarCipher(Caesar.Message, Caesar.Key)
            CipheredMsg = Caesar.CipheredMsg

            print(f"Cipher: {CipheredMsg}\n")
        elif option == 2:
            Caesar.setKey(input("Enter your key: "))
            Key = Caesar.Key
            Caesar.CaesarCipher(Caesar.Message, Caesar.Key)
            CipheredMsg = Caesar.CipheredMsg
        elif option == 3:
            if CipheredMsg != '':
                GuessedKey, DecipheredMsg = Senate.bloodyMurder(CipheredMsg)
                print(f"Your message was: {Senate.DecipheredMsg}")
                print(f"Encrypting using the Key: {Senate.guessKey}\n")
            else:
                print("First enter a message using option 1.\n")
    else:
        print("Enter a valid option 1, 2, or 3.\n")
