import random,time

def simpleEcnryption(NormalText):
    Encrypted_text = ""
    for i in range(len(NormalText)):
        ch = NormalText[i]
        Enc = (chr(ord(ch) + 1))
        Encrypted_text+=Enc
    return Encrypted_text
        

def SimpleDecription(EncryptedText):
    DecryptedText = ""
    for i in range(len(EncryptedText)):
        char = EncryptedText[i]
        Dec = (chr(ord(char) -1))
        DecryptedText+=Dec
    return DecryptedText

        



