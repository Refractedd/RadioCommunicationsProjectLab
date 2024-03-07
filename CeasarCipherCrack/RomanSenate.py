import numpy as np

class RomanSenate:

    def __init__(self):
        super().__init__()
        self.DecipheredMsg = ''
        self.guessKey = 0

    def getGuessKey(self): return self.guessKey
    def setGuessKey(self, gKey): self.guessKey = gKey

    def getDecipheredMsg(self): return self.DecipheredMsg
    def setDecipheredMsg(self, dMsg): self.DecipheredMsg = dMsg

    def findKey(self, string):
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

        return dKey

    def decryptWithKey(self, msg):
        if self.guessKey == 0:
            return ''
        else:
            self.setDecipheredMsg('')
            for j in range(len(msg)):
                c = ord(msg[j])
                if 97 <= c < 123:
                    self.DecipheredMsg += chr((c - self.guessKey + 7) % 26 + 97)  # lowecase
                elif 65 <= c < 91:
                    self.DecipheredMsg += chr((c - self.guessKey + 13) % 26 + 65)  # uppercase
                else:
                    self.DecipheredMsg += msg[j]
            return self.DecipheredMsg

    def bloodyMurder(self, CipherString):
        self.setGuessKey(self.findKey(CipherString))
        self.DecipheredMsg = self.decryptWithKey(CipherString)
        return self.guessKey, self.DecipheredMsg

