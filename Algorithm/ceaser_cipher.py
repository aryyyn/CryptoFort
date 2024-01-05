import random,time

def simpleEcnryption(NormalText):
    Encrypted_text = ""
    for i in range(len(NormalText)):
        ch = NormalText[i]
        Enc = (chr(ord(ch) + 9))
        Encrypted_text+=Enc
    return Encrypted_text
        

def SimpleDecription(Text):
    DecryptedText = ""
    for i in range(len(Text)):
        char = Text[i]
        Dec = (chr(ord(char) -9))
        DecryptedText+=Dec
    return DecryptedText

        
EncryptedText = simpleEcnryption("Password")
DecryptedText = SimpleDecription(EncryptedText)
print(EncryptedText)
print(DecryptedText)


