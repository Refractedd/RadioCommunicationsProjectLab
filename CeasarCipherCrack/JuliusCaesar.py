class JuliusCaesar:

    def __init__(self):
        super().__init__()
        self.Message = ''
        self.Key = 0
        self.CipheredMsg = ''

    def getMessage(self): return self.Message

    def getCipheredMsg(self): return self.CipheredMsg

    def getKey(self): return self.Key

    def setMessage(self, msg): self.Message = msg

    def setKey(self, num): self.Key = int(num)

    def CaesarCipher(self, string, num):
        if num > 26:
            num = num % 26
        elif num < 0:
            num = 26 + num
        self.CipheredMsg = ''
        for j in range(len(string)):
            c = ord(string[j])
            if 97 <= c < 123:
                self.CipheredMsg += chr((c + num + 7) % 26 + 97)  # lowecase
            elif 65 <= c < 91:
                self.CipheredMsg += chr((c + num + 13) % 26 + 65)  # uppercase
            else:
                self.CipheredMsg += string[j]
        return self.CipheredMsg

